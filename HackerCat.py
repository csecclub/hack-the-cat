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
        self.user_scores = {} # new dictionary to store all player's scores

    async def on_ready(self):
        print('Logged on as', self.user)

    async def display_all_scores(self, message):
        if not self.user_scores:
            await message.channel.send("No scores recorded yet.")
            return

        scores_list = sorted(self.user_scores.items(), key=lambda x: x[1], reverse=True)
        score_message = "**Current Scores:**\n"
        for user_id, score in scores_list:
            user = self.get_user(user_id)
            if user:
                score_message += f"{user.name}: {score} points\n"
        
        await message.channel.send(score_message)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        elif message.content.lower() == "!scores":
            await self.display_all_scores(message)

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

        elif message.content == 'admin':
            await self.display_all_scores(message)

         # Start ctf challenges
        elif message.content == "START HERE" and message.author not in self.users_in_challenges:
            await self.send_ctf_challenges(message.author)

         # Validate answers
        elif message.author in self.users_in_challenges:
            await self.validate_answer(message.author, message.content)

    async def send_ctf_challenges(self, user):
        points = 0
        challenges = [
            {
                'filename': 'csec_wireshark.pcap',
                'title': "Wireshark: TCP 1",
                'Question': "What's the hidden flag?(csec{xxxxx})",
            },
            {
                'filename': 'Meta.jpg',
                'title': 'META: Test your abilities to extract metadata.',
                'Question 1': 'When was the image created? Round down to the nearest minute [format: YYYY:MM:DD:MM:SS]',
                'Question 2': 'What are the dimensions of the image? (ex: 800x600)',
                'Question 3': 'What is the make of the camera that took the picture?',
                'Question 4': 'What is the make of the camera that took the picture?',
                'Question 5': 'What is the make of the camera that took the picture?',
            },
            {
                'filename': '',
                'title': 'Cryptography: Our analysts have obtained password dumps storing hacker passwords. After obtaining a few plaintext passwords, it appears that they are all simply encoded using different number bases.',
                'Question 1': 'Patrick: 0x73636f7270696f6e',
                'Question 2': 'Stevie: c2NyaWJibGU=',
                'Question 3': 'Nan: 01110011 01100101 01100011 01110101 01110010 01100101 01101100 01111001',
                'Question 4': 'Molly: 01100010 01000111 00111001 01110011 01100010 01000111 01101100 01110111 01100010 00110011 01000001 00111101',
            },
            {
                'filename': 'git_backup.zip',
                'title': 'Version control[git]:',
                'Question 1': 'What is the email address of the employee who was compromised?',
                'Question 2': "Each employee is assigned a flag. What is the flag that was compromised?",
                'Question 3': "Greg thinks that he may have had additional account credentials that were compromised. What's the name of the service provider for that other compromised account?",
                'Question 4': "What was the password on that compromised account?",
            },
            {
                'filename': 'auth.log',
                'title': 'Log Analysis: Analyze this ssh log file to answer the following questions.',
                'Question 1': 'What is the hostname of the ssh server that was compromised?',
                'Question 2': "What was the first IP address to attack the server?",
                'Question 3': "What was the second IP address to attack the server?",
                'Question 4': "What was the third IP address to attack the server?",
                'Question 5': "Which user was targeted in the attack?",
                'Question 6': "From which IP address was the attacker able to successfully log in?",
            },
        ]

        for challenge in challenges:
            # if theres not file, then don't send one, if there is, then do
            if challenge['filename'] != "":
                file_path = os.path.join('ctf/', challenge['filename'])
                with open(file_path, 'rb') as file:
                    embed = discord.Embed(title=challenge['title'])
                    await user.send(embed=embed)
                    await asyncio.sleep(0.5)  # Wait for 1/2 seconds

                    # if there's a blank file, don't send anything
                    await user.send(file=discord.File(file, filename=challenge['filename']))
                    print(f'Sent {challenge["filename"]} to {user.name}')
            else:
                embed = discord.Embed(title=challenge['title'])
                await user.send(embed=embed)
                await asyncio.sleep(0.5)  # Wait for 1/2 seconds
                
                

            questions = [q for q in challenge if q.startswith('Question')]
            for question_num, question in enumerate(questions, start=1):
                await user.send(f"**{question_num}. {challenge[question]}**")
                answer = await self.wait_for_answer(user)

                if self.is_answer_correct(challenge, question, answer.content):
                        # if user not in scores dictoinary add them
                        if user.id not in self.user_scores:
                            self.user_scores[user.id] = 0

                        self.user_scores[user.id] += 1  # Increment score for the user
                        await user.send(f"✅ Correct answer for question {question_num}! +1")
                        await user.send(f"Your score: {self.user_scores[user.id]}")

                while not self.is_answer_correct(challenge, question, answer.content):
                    await user.send(f"❌ Incorrect answer for question {question_num}. Please try again.")
                    answer = await self.wait_for_answer(user)
                    if self.is_answer_correct(challenge, question, answer.content):
                        await user.send(f"✅ Correct answer for question {question_num}!")

        await user.send(f'CTF Completed! come get your prize!')
        print(f'{user.name} Has completed all the CTFS')
                

    async def wait_for_answer(self, user):
        def check(message):
            return message.author == user and message.channel == user.dm_channel
        return await self.wait_for('message', check=check)

    def is_answer_correct(self, challenge, question, answer):
        
        if challenge['title'] == "Wireshark: TCP 1" and question == "Question":
            return answer == "csec{1N_2040_AI_wi11_D3BU6_our_C0de}"
        
        elif challenge['title'] == "META: Test your abilities to extract metadata.":
            if question == "Question 1":
                return answer == "2015:05:15:02:14"
            elif question == "Question 2":
                return answer == "1024x768"
            elif question == "Question 3":
                return answer == "Apple"
            elif question == "Question 4":
                return answer == "Apple iPhone 5"
            elif question == "Question 5":
                return answer == "1/640"
            
        elif challenge['title'] == "Cryptography: Our analysts have obtained password dumps storing hacker passwords. After obtaining a few plaintext passwords, it appears that they are all simply encoded using different number bases.":
            if question == "Question 1":
                return answer == "scorpion"
            elif question == "Question 2":
                return answer == "scribble"
            elif question == "Question 3":
                return answer == "securely"
            elif question == "Question 4":
                return answer == "lollipop"
            
        elif challenge['title'] == "Version control[git]:":
            if question == "Question 1":
                return answer == "gpeterson@mpd.hacknet.cityinthe.cloud"
            elif question == "Question 2":
                return answer == "-SKY-LRHX-4910"
            elif question == "Question 3":
                return answer == "Facebook" or answer == "FB" or answer == "facebook"
            elif question == "Question 4":
                return answer == "waffles85" 
        
        elif challenge['title'] == "Log Analysis: Analyze this ssh log file to answer the following questions.":
            if question == "Question 1":
                return answer == "myraptor"
            elif question == "Question 2":
                return answer == "169.139.243.218"
            elif question == "Question 3":
                return answer == "56.13.188.38"
            elif question == "Question 4":
                return answer == "30.167.206.91" 
            elif question == "Question 5":
                return answer == "harvey" 
            elif question == "Question 6":
                return answer == "30.167.206.91"

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