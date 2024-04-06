import discord

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
intents.message_content = True
client = MyClient(intents=intents)
client.run("MTIyNjI5ODA4NDU4NjI5MTI0MQ.G81y2l.U3QB0u36D0LbF3bo0hyqxl2Q5xcotqHaBm3skE")
