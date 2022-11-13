import discord
from discord import app_commands
from commands import COMMANDS, MESSAGE_HANDLERS


class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        tree = app_commands.CommandTree(self)
        self._tree = tree

        for command in COMMANDS:
            tree.add_command(command)

    async def on_ready(self):
        await self._tree.sync()
        print('Ready!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        print(f'Message from {message.author}: {message.content}')

        for handler in MESSAGE_HANDLERS:
            handled = await handler(message.author, message.content)
            if handled:
                break
