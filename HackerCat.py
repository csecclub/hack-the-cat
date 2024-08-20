import discord
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

# GLOBAL BOOLS
# idea is to create a bunch of bools, that are inverted, and once switched on cannot be answered again
# is there a better way to do this, perhaps but this is what i can think of at the moment
question1 = False
question2 = False
question3 = False
question4 = False
question5 = False
question6 = False
question7 = False
question8 = False
question9 = False
question10 = False
question11 = False
question12 = False
question13 = False
question14 = False
question15 = False
question16 = False
question17 = False
question18 = False
question19 = False

class MyClient(discord.Client):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_in_challenges = set()  # Set to track users in challenges
        self.user_scores = {} # new dictionary to store all player's scores

    async def on_ready(self):
        print('Logged on as', self.user)


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

        # admin command to display scores
        elif message.content == 'admin':
            await self.display_all_scores(message)

        # Start ctf challenges if users aren't in the challenge
        elif message.content == "START HERE" and message.author not in self.users_in_challenges:
            await self.send_ctf_challenges(message.author)

        # Validate answers if users are in the challenge
        elif message.author in self.users_in_challenges:
            await self.validate_answer(message.author, message.content)

    # sends message to user to display every players score
    async def display_all_scores(self, message):
        # if there are no scores return
        if not self.user_scores:
            await message.channel.send("No scores recorded yet.")
            return
        # else sort the scores
        scores_list = sorted(self.user_scores.items(), key=lambda x: x[1], reverse=True)
        score_message = "**Current Scores:**\n"
        # list each users point
        for user_id, score in scores_list:
            # get users id
            user = self.get_user(user_id)
            if user:
                # create score message and list their name and score
                score_message += f"{user.name}: {score} points\n"
        
        # send the score message
        await message.channel.send(score_message)


    # send's ctf challanges to the player
    async def send_ctf_challenges(self, user):
        # stores total score per user
        points = 0
        # stores all challenges
        challenges = [
            {
                'filename': 'csec_wireshark.pcap',
                'title': "Wireshark: TCP 1",
                'Question 1': "What's the hidden flag?(csec{xxxxx})",
            },
            {
                'filename': 'Meta.jpg',
                'title': 'META: Test your abilities to extract metadata.',
                'Question 2': 'When was the image created? Round down to the nearest minute [format: YYYY:MM:DD:MM:SS]',
                'Question 3': 'What are the dimensions of the image? (ex: 800x600)',
                'Question 4': 'What is the make of the camera that took the picture?',
                'Question 5': 'What is the make of the camera that took the picture?',
                'Question 6': 'What is the make of the camera that took the picture?',
            },
            {
                'filename': '',
                'title': 'Cryptography: Our analysts have obtained password dumps storing hacker passwords. After obtaining a few plaintext passwords, it appears that they are all simply encoded using different number bases.',
                'Question 7': 'Patrick: 0x73636f7270696f6e',
                'Question 8': 'Stevie: c2NyaWJibGU=',
                'Question 9': 'Nan: 01110011 01100101 01100011 01110101 01110010 01100101 01101100 01111001',
                'Question 10': 'Molly: 01100010 01000111 00111001 01110011 01100010 01000111 01101100 01110111 01100010 00110011 01000001 00111101',
            },
            {
                'filename': 'git_backup.zip',
                'title': 'Version control[git]:',
                'Question 11': 'What is the email address of the employee who was compromised?',
                'Question 12': "Each employee is assigned a flag. What is the flag that was compromised?",
                'Question 13': "Greg thinks that he may have had additional account credentials that were compromised. What's the name of the service provider for that other compromised account?",
                'Question 14': "What was the password on that compromised account?",
            },
            {
                'filename': 'auth.log',
                'title': 'Log Analysis: Analyze this ssh log file to answer the following questions.',
                'Question 15': 'What is the hostname of the ssh server that was compromised?',
                'Question 16': "What was the first IP address to attack the server?",
                'Question 17': "What was the second IP address to attack the server?",
                'Question 18': "What was the third IP address to attack the server?",
                'Question 19': "Which user was targeted in the attack?",
            },
        ]

        # for each challange within the list of challanges, 
        for challenge in challenges:
            # if theres not file, then don't send one, if there is, then do
            if challenge['filename'] != "":
                file_path = os.path.join('ctf/', challenge['filename'])
                with open(file_path, 'rb') as file:
                    embed = discord.Embed(title=challenge['title'])
                    await user.send(embed=embed)
                    await asyncio.sleep(0.2)  # Wait

                    await user.send(file=discord.File(file, filename=challenge['filename']))
                    print(f'Sent {challenge["filename"]} to {user.name}')
            else: # send with out file
                embed = discord.Embed(title=challenge['title'])
                await user.send(embed=embed)
                await asyncio.sleep(0.2)  # Wait
                
                
            # create an array of questions and grab each question that starts with 'Question'
            questions = [q for q in challenge if q.startswith('Question')]
            # go through each question number
            for question_num, question in enumerate(questions, start=1):

                await user.send(f"**{question_num}. {challenge[question]}**")

        while points <= 19:
            #get an answer from the user this prevents multiple questions from being asked
            answer = await self.wait_for_answer(user) 

            # validation of that question
            if self.is_answer_correct(challenge, question, answer.content):
                    # if user not in scores dictoinary add them
                    if user.id not in self.user_scores:
                        self.user_scores[user.id] = 0

                    self.user_scores[user.id] += 1  # Increment score for the user
                    await user.send(f"✅ Correct answer! +1")
                    await user.send(f"Your score: {self.user_scores[user.id]}")
            else: #incorrect answer, enter while loop again
                await user.send(f"❌ Incorrect answer. Please try again.")
        
        #ending user message once all CTFs completed
        await user.send(f'CTF Completed! come get your prize!')
        print(f'{user.name} Has completed all the CTFS')
                

    # bot waits for an answer
    async def wait_for_answer(self, user):
        def check(message):
            return message.author == user and message.channel == user.dm_channel
        return await self.wait_for('message', check=check)

    # need to make this track which question has already been answered or not
    def is_answer_correct(self, challenge, question, answer):
        
        global question1
        global question2
        global question3
        global question4
        global question5
        global question6
        global question7
        global question8
        global question9
        global question10
        global question11
        global question12
        global question13
        global question14 
        global question15
        global question16
        global question17 
        global question18
        global question19 


        if not question1 and answer == "csec{1N_2040_AI_wi11_D3BU6_our_C0de}":
            question1 = True
            return True
        elif not question2 and answer == "2015:05:15:02:14":
            question2 = True
            return True
        elif not question3 and answer == "1024x768":
            question3 = True
            return True
        elif not question4 and answer == "Apple":
            question4 = True
            return True
        elif not question5 and answer == "Apple iPhone 5":
            question5 = True
            return True
        elif not question6 and answer == "1/640":
            question6 = True
            return True
        elif not question7 and answer == "scorpion":
            question7 = True
            return True
        elif not question8 and answer == "scribble":
            question8 = True
            return True
        elif not question9 and answer == "securely":
            question9 = True
            return True
        elif not question10 and answer == "lollipop":
            question10 = True
            return True
        elif not question11 and answer == "gpeterson@mpd.hacknet.cityinthe.cloud":
            question11 = True
            return True
        elif not question12 and answer == "-SKY-LRHX-4910":
            question12 = True
            return True
        elif not question13 and answer == "Facebook":
            question13 = True
            return True
        elif not question14 and answer == "waffles85":
            question14 = True
            return True
        elif not question15 and answer == "myraptor":
            question15 = True
            return True
        elif not question16 and answer == "169.139.243.218":
            question16 = True
            return True
        elif not question17 and answer == "56.13.188.38":
            question17 = True
            return True
        elif not question18 and answer == "30.167.206.91":
            question18 = True
            return True
        elif not question19 and answer == "harvey":
            question19 = True
            return True
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