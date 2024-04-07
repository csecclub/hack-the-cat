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

        if message.content == 'SEND THE FLAGS':
            await self.send_ctf_challenges(message.author)
            
    async def send_ctf_challenges(self, user):
        # CTF challenges
        challenge_files = ['csec_wireshark.pcap', 'tcp.pcap']

        for file_name in challenge_files:
            file_path = os.path.join('ctf/', file_name)
            with open(file_path, 'rb') as file:
                await user.send(file=discord.File(file, filename=file_name))
                print(f'sent {file_name} to {user.name}')

intents = discord.Intents.default()

intents.typing = True
intents.presences = True  # Enable the Presence Intent
intents.members = True    # Enable the Server Members Intent
intents.message_content = True

intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)

