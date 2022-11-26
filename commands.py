import bcrypt
from discord import User, Member, Interaction
from discord.app_commands import command, Command
import hashlib
from typing import Callable, Coroutine, Any

from storage import Storage, Entry

_pending_entries: list[Entry] = []


@command(name='register', description='Register on minecraft server')
async def register(interaction: Interaction, name: str):
    user: User | Member = interaction.user
    if isinstance(user, User):
        await interaction.response.send_message(f"Can't register from DM!")
        return

    registered_with_name = _entries_with_name(Storage().entries, name)
    if len(registered_with_name) != 0:
        await interaction.response.send_message(f'Already registered {name}!')
        return

    discord_id = str(user.id)

    pending_with_name = _entries_with_name(_pending_entries, name)
    if len(pending_with_name) != 0:
        if pending_with_name[0].discord_id == discord_id:
            await interaction.response.send_message(f'Finish registration process for {name}!')
        else:
            await interaction.response.send_message(f'Already registered {name}!')
        return

    pending_with_id = _entries_with_id(_pending_entries, discord_id)
    if len(pending_with_id) != 0:
        await interaction.response.send_message(f'First finish registration process for {pending_with_id[0]}!')
        return

    _pending_entries.append(Entry(username=name, discord_id=discord_id))

    await interaction.response.send_message(f'Registered {name}')

    dm_channel = await user.create_dm()
    await dm_channel.send("Send me a password")


async def handle_registration_message(author: User | Member, content: str) -> bool:
    if isinstance(author, Member):
        return False

    discord_id = str(author.id)
    pending_with_id = _entries_with_id(_pending_entries, discord_id)
    if len(pending_with_id) == 0:
        return False

    salt = bcrypt.gensalt().hex()
    salted_password_bytes = str.encode(content + salt)
    print(f"salt: {salt}\npassword and salt: {content + salt}\npassword and salt bytes: {salted_password_bytes}")

    sha256 = hashlib.sha256()
    sha256.update(salted_password_bytes)
    password_hash = sha256.hexdigest()

    pending = pending_with_id[0]
    pending.passwordHash = password_hash
    pending.salt = salt
    _pending_entries.remove(pending)

    Storage().entries.append(pending)
    Storage().save()

    dm_channel = await author.create_dm()
    await dm_channel.send("Registration finished!")

    return True


@command(name='unregister', description='Unregister on minecraft server')
async def unregister(interaction: Interaction, name: str):
    user: User | Member = interaction.user
    if isinstance(user, User):
        await interaction.response.send_message(f"Can't unregister from DM!")
        return

    discord_id = str(user.id)

    registered_with_name = _entries_with_name(Storage().entries, name)
    registered_with_id = _entries_with_id(registered_with_name, discord_id)
    if len(registered_with_id) == 0:
        await interaction.response.send_message(f"You don't have an account with such name!")
        return

    entry = registered_with_id[0]
    Storage().entries.remove(entry)
    Storage().save()

    await interaction.response.send_message(f'Successfully unregistered {name}')


def _entries_with_id(entries: list[Entry], discord_id: str):
    return list(filter(lambda e: e.discord_id == discord_id, entries))


def _entries_with_name(entries: list[Entry], name: str):
    return list(filter(lambda e: e.username == name, entries))


COMMANDS: list[Command] = [
    register,
    unregister
]

MESSAGE_HANDLERS: list[Callable[[User | Member, str], Coroutine[Any, Any, bool]]] = [
    handle_registration_message
]
