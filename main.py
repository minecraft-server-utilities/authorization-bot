import discord
from discord import app_commands

from client import Client
from config import Config
from storage import Storage


# intents = discord.Intents.default()
# client = discord.Client(intents=intents)
# tree = app_commands.CommandTree(client)
#
#
# @app_commands.command(name='register', description='Register on minecraft server')
# async def register(interaction, name: str):
#     a = 1
#     await interaction.response.send_message(f'Registered {name}')
#     dm_channel = await interaction.user.create_dm()
#     await dm_channel.send("Send me a password")
#
#
# @client.event
# async def on_ready():
#     await tree.sync()
#     print('Ready!')
#
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     print(f'Message from {message.author}: {message.content}')


def main():
    config = Config.load('config.json')

    Storage().init(config.db_file)

    client = Client()
    client.run(config.token)


if __name__ == '__main__':
    main()

