import discord
import asyncio
import os
from datetime import datetime, time

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == 'channel_A':
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    await message.channel.send('Saving the image from {0.author.name}'.format(message))
                    await attachment.save(f'./images/{attachment.filename}')
                    channel_b = discord.utils.get(message.guild.channels, name='channel_B')
                    if channel_b:
                        with open(f'./images/{attachment.filename}', 'rb') as f:
                            picture = discord.File(f)
                            await channel_b.send(f'Picture from {message.author.name}', file=picture)
                            await message.delete()
        else:
            await message.channel.send('Please attach an image to this channel!')

async def open_channel_b():
    await client.wait_until_ready()
    guild = discord.utils.get(client.guilds, name='Your Guild Name')
    channel_b = discord.utils.get(guild.channels, name='channel_B')
    if channel_b:
        await channel_b.set_permissions(guild.default_role, read_messages=True)

schedule_day = 3  # Wednesday
async def run_schedule():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.now().time()
        if now.weekday() == schedule_day and now.hour == 0 and now.minute == 0:
            await open_channel_b()
            await asyncio.sleep(86400)  # 24 hours
        else:
            await asyncio.sleep(60)

client.loop.create_task(run_schedule())
client.run('YOUR_DISCORD_BOT_TOKEN')
