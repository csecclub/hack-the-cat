import discord
import os
import asyncio


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

        if message.content == 'FREE':
            self.start_here = True
            await message.author.send("You have successfully submitted 'FREE'!")
            await asyncio.sleep(.5)  # Wait for 1/2 seconds
            await message.author.send("If this was the real challenge the flag would be formated like this: ")
            await asyncio.sleep(.5)  # Wait for 1/2 seconds
            await message.author.send("csec{FREE} ฅ(^•ﻌ•^ฅ)")
            await asyncio.sleep(.5)  # Wait for 1/2 seconds
            await message.author.send("make sure to submit what is inside the {} (=^・^=)")
            await asyncio.sleep(.5)  # Wait for 1/2 seconds
            await message.author.send("When ready enter: {START HERE}")

        if message.content == "START HERE" and self.start_here:
            await self.send_ctf_challenges(message.author)
            self.start_here = False
            
    async def start_here(self, user, message):

        if message.content == 'START HERE':
            await self.send_ctf_challenges(user)
        

    async def send_ctf_challenges(self, user):
        # CTF challenges
        challenges = [
                {
                    'filename': 'csec_wireshark.pcap', 
                    'title' : "Wireshark 1"
                },
                {
                    'filename' : 'tcp.pcap',
                    'title' : 'Wireshark 2'
                },
            ]

        for challenge in challenges:
            file_path = os.path.join('ctf/', challenge['filename'])

            with open(file_path, 'rb') as file:
                embed = discord.Embed(title = challenge['title'],)
                await user.send(embed = embed)
                await asyncio.sleep(.5)  # Wait for 1/2 seconds
                await user.send(file = discord.File(file, filename = challenge['filename']))

                print(f'Sent {challenge["filename"]} to {user.name}')

intents = discord.Intents.default()

intents.typing = True
intents.presences = True  # Enable the Presence Intent
intents.members = True    # Enable the Server Members Intent
intents.message_content = True

intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
