import discord
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()

intents.typing = True
intents.presences = True  # Enable the Presence Intent
intents.members = True    # Enable the Server Members Intent
intents.message_content = True

intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)

