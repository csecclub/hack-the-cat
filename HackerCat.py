import discord
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_in_challenges = set()  # Set to track users in challenges

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # welcome message when typed FREE
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

         # Start ctf challenges
        elif message.content == "START HERE" and message.author not in self.users_in_challenges:
            await self.send_ctf_challenges(message.author)

         # Validate answers
        elif message.author in self.users_in_challenges:
            await self.validate_answer(message.author, message.content)

    async def send_ctf_challenges(self, user):
        challenges = [
            {
                'filename': 'csec_wireshark.pcap',
                'title': "Wireshark: TCP 1",
                'Question': "What's the hidden flag?(csec{xxxxx})",
            },
            {
                'filename': 'splitTCP.pcap',
                'title': 'Wireshark: TCP 2',
                'Question': 'Whats the hidden flag?(bayFLAG{xxxx})',
            },
            {
                'filename': 'DNS1.pcap',
                'title': 'Wireshark: DNS 1',
                'Question 1': 'What is the type of the DNS query requested?',
                'Question 2': "What domain was requested?",
                'Question 3': "How many items were in the response?",
                'Question 4': "What is the TTL for all of the DNS records?\n(note that this is the TTL for the DNS record, not the IP packet.)\n(also can answer using{# h}{# m}{# s})",
                'Question 5': "What is the IP address for the 'welcome' subdomain?",
            },
            {
                'filename': 'HTTP1.pcap',
                'title': 'Wireshark: HTTP 1',
                'Question 1': 'What Linux tool was used to execute a file download?',
                'Question 2': "What is the name of the web server software that handled the request?",
                'Question 3': "What IP address initiated request?",
                'Question 4': "What is the IP address of the server?",
                'Question 5': "What is the md5sum of the file downloaded?",
            },
        ]

        for challenge in challenges:
            file_path = os.path.join('ctf/', challenge['filename'])
            with open(file_path, 'rb') as file:
                embed = discord.Embed(title=challenge['title'])
                await user.send(embed=embed)
                await asyncio.sleep(0.5)  # Wait for 1/2 seconds
                await user.send(file=discord.File(file, filename=challenge['filename']))
                print(f'Sent {challenge["filename"]} to {user.name}')

            questions = [q for q in challenge if q.startswith('Question')]
            for question_num, question in enumerate(questions, start=1):
                await user.send(f"**{question_num}. {challenge[question]}**")
                answer = await self.wait_for_answer(user)
                if self.is_answer_correct(challenge, question, answer.content):
                        await user.send(f"✅ Correct answer for question {question_num}!")
                while not self.is_answer_correct(challenge, question, answer.content):
                    await user.send(f"❌ Incorrect answer for question {question_num}. Please try again.")
                    answer = await self.wait_for_answer(user)
                    if self.is_answer_correct(challenge, question, answer.content):
                        await user.send(f"✅ Correct answer for question {question_num}!")
                

    async def wait_for_answer(self, user):
        def check(message):
            return message.author == user and message.channel == user.dm_channel
        return await self.wait_for('message', check=check)

    def is_answer_correct(self, challenge, question, answer):
        if challenge['title'] == "Wireshark: TCP 1" and question == "Question":
            return answer == "csec{1N_2040_AI_wi11_D3BU6_our_C0de}"
        elif challenge['title'] == "Wireshark: TCP 2" and question == "Question":
            return answer == "bayFLAG{H4v3_y0u_c53ck3d_0uT_M0BI?}"
        elif challenge['title'] == "Wireshark: DNS 1":
            if question == "Question 1":
                return answer == "AXFR"
            elif question == "Question 2":
                return answer == "etas.com"
            elif question == "Question 3":
                return answer == "4"
            elif question == "Question 4":
                return answer == "1 h" or answer == "3600 s" or answer == "60 m"
            elif question == "Question 5":
                return answer == "1.1.1.1"
        elif challenge['title'] == "Wireshark: HTTP 1":
            if question == "Question 1":
                return answer == "wget"
            elif question == "Question 2":
                return answer == "nginx"
            elif question == "Question 3":
                return answer == "192.168.1.140"
            elif question == "Question 4":
                return answer == "174.143.213.184"
            elif question == "Question 5":
                return answer == "966007c476e0c200fba8b28b250a6379"
        else:
            return False

    

intents = discord.Intents.default()
intents.typing = True
intents.presences = True  # Enable the Presence Intent
intents.members = True    # Enable the Server Members Intent
intents.message_content = True

intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)