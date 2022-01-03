from __future__ import annotations
from logging import fatal
from re import A
from sqlite3.dbapi2 import Cursor
import discord
import time
import random
from typing import Final, Union
from discord import embeds
from discord import channel
from discord import member
from discord.enums import try_enum
from discord.errors import PrivilegedIntentsRequired
from discord.ext import commands
from discord.ext.commands.core import command
from discord_components import ButtonStyle, Button, Select, SelectOption, ComponentsClient, DiscordComponents, client, component, Interaction, interaction 
import asyncio
import certifi
import aiohttp
from sqlite3 import connect
from datetime import date, datetime
import praw
import re
import string
#

import inspect
import json
import traceback
import sys
from collections import defaultdict

import discord, discord.channel, discord.http, discord.state
from discord.ext import commands
from discord.utils import MISSING

from typing import Coroutine, TypeVar, Union, get_args, get_origin, overload, Generic, TYPE_CHECKING

BotT = TypeVar("BotT", bound='Bot')
CtxT = TypeVar("CtxT", bound='Context')
CogT = TypeVar("CogT", bound='ApplicationCog')
NumT = Union[int, float]

__all__ = ['describe', 'SlashCommand', 'ApplicationCog', 'Range', 'Context', 'Bot', 'slash_command', 'message_command', 'user_command']

if TYPE_CHECKING:
    from typing import Any, Awaitable, Callable, ClassVar
    from typing_extensions import Concatenate, ParamSpec, Self

    CmdP = ParamSpec("CmdP")
    CmdT = Callable[Concatenate[CogT, CtxT, CmdP], Awaitable[Any]]
    MsgCmdT = Callable[[CogT, CtxT, discord.Message], Awaitable[Any]]
    UsrCmdT = Callable[[CogT, CtxT, discord.Member], Awaitable[Any]]
    CtxMnT = Union[MsgCmdT, UsrCmdT]
    
    RngT = TypeVar("RngT", bound='Range')

command_type_map: dict[type[Any], int] = {
    str: 3,
    int: 4,
    bool: 5,
    discord.User: 6,
    discord.Member: 6,
    discord.TextChannel: 7,
    discord.VoiceChannel: 7,
    discord.CategoryChannel: 7,
    discord.Role: 8,
    float: 10
}

channel_filter: dict[type[discord.abc.GuildChannel], int] = {
    discord.TextChannel: 0,
    discord.VoiceChannel: 2,
    discord.CategoryChannel: 4
}

def describe(**kwargs):
    """
    Sets the description for the specified parameters of the slash command. Sample usage:
    ```python
    @slash_util.slash_command()
    @describe(channel="The channel to ping")
    async def mention(self, ctx: slash_util.Context, channel: discord.TextChannel):
        await ctx.send(f'{channel.mention}')
    ```
    If this decorator is not used, parameter descriptions will be set to "No description provided." instead."""
    def _inner(cmd):
        func = cmd.func if isinstance(cmd, SlashCommand) else cmd
        for name, desc in kwargs.items():
            try:
                func._param_desc_[name] = desc
            except AttributeError:
                func._param_desc_ = {name: desc}
        return cmd
    return _inner

def slash_command(**kwargs) -> Callable[[CmdT], SlashCommand]:
    """
    Defines a function as a slash-type application command.
    
    Parameters:
    - name: ``str``
    - - The display name of the command. If unspecified, will use the functions name.
    - guild_id: ``Optional[int]``
    - - The guild ID this command will belong to. If unspecified, the command will be uploaded globally.
    - description: ``str``
    - - The description of the command. If unspecified, will use the functions docstring, or "No description provided" otherwise.
    """
    def _inner(func: CmdT) -> SlashCommand:
        return SlashCommand(func, **kwargs)
    return _inner
    
def message_command(**kwargs) -> Callable[[MsgCmdT], MessageCommand]:
    """
    Defines a function as a message-type application command.
    
    Parameters:
    - name: ``str``
    - - The display name of the command. If unspecified, will use the functions name.
    - guild_id: ``Optional[int]``
    - - The guild ID this command will belong to. If unspecified, the command will be uploaded globally.
    """
    def _inner(func: MsgCmdT) -> MessageCommand:
        return MessageCommand(func, **kwargs)
    return _inner

def user_command(**kwargs) -> Callable[[UsrCmdT], UserCommand]:
    """
    Defines a function as a user-type application command.
    
    Parameters:
    - name: ``str``
    - - The display name of the command. If unspecified, will use the functions name.
    - guild_id: ``Optional[int]``
    - - The guild ID this command will belong to. If unspecified, the command will be uploaded globally.
    """
    def _inner(func: UsrCmdT) -> UserCommand:
        return UserCommand(func, **kwargs)
    return _inner

class _RangeMeta(type):
    @overload
    def __getitem__(cls: type[RngT], max: int) -> type[int]: ...
    @overload
    def __getitem__(cls: type[RngT], max: tuple[int, int]) -> type[int]: ...
    @overload
    def __getitem__(cls: type[RngT], max: float) -> type[float]: ...
    @overload
    def __getitem__(cls: type[RngT], max: tuple[float, float]) -> type[float]: ...

    def __getitem__(cls, max):
        if isinstance(max, tuple):
            return cls(*max)
        return cls(None, max)

class Range(metaclass=_RangeMeta):
    """
    Defines a minimum and maximum value for float or int values. The minimum value is optional.
    ```python
    async def number(self, ctx, num: slash_util.Range[0, 10], other_num: slash_util.Range[10]):
        ...
    ```"""
    def __init__(self, min: NumT | None, max: NumT):
        if min is not None and min >= max:
            raise ValueError("`min` value must be lower than `max`")
        self.min = min
        self.max = max

class Bot(commands.Bot):
    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await self.login(token)
        
        app_info = await self.application_info()
        self._connection.application_id = app_info.id

        await self.sync_commands()
        await self.connect(reconnect=reconnect)

    def get_application_command(self, name: str) -> Command | None:
        """
        Gets and returns an application command by the given name.

        Parameters:
        - name: ``str``
        - - The name of the command.

        Returns:
        - [Command](#deco-slash_commandkwargs)
        - - The relevant command object
        - ``None``
        - - No command by that name was found.
        """

        for c in self.cogs.values():
            if isinstance(c, ApplicationCog):
                c = c._commands.get(name)
                if c:
                    return c

    async def delete_all_commands(self, guild_id: int | None = None):
        """
        Deletes all commands on the specified guild, or all global commands if no guild id was given.
        
        Parameters:
        - guild_id: ``Optional[str]``
        - - The guild ID to delete from, or ``None`` to delete global commands.
        """
        path = f'/applications/{self.application_id}'
        if guild_id is not None:
            path += f'/guilds/{guild_id}'
        path += '/commands'

        route = discord.http.Route("GET", path)
        data = await self.http.request(route)

        for cmd in data:
            snow = cmd['id']
            await self.delete_command(snow, guild_id=guild_id)

    async def delete_command(self, id: int, *, guild_id: int | None = None):
        """
        Deletes a command with the specified ID. The ID is a snowflake, not the name of the command.
        
        Parameters:
        - id: ``int``
        - - The ID of the command to delete.
        - guild_id: ``Optional[str]``
        - - The guild ID to delete from, or ``None`` to delete a global command.
        """
        route = discord.http.Route('DELETE', f'/applications/{self.application_id}{f"/guilds/{guild_id}" if guild_id else ""}/commands/{id}')
        await self.http.request(route)
 
    async def sync_commands(self) -> None:
        """
        Uploads all commands from cogs found and syncs them with discord.
        Global commands will take up to an hour to update. Guild specific commands will update immediately.
        """
        if not self.application_id:
            raise RuntimeError("sync_commands must be called after `run`, `start` or `login`")

        for cog in self.cogs.values():
            if not isinstance(cog, ApplicationCog):
                continue

            for cmd in cog._commands.values():
                cmd.cog = cog
                route = f"/applications/{self.application_id}"

                if cmd.guild_id:
                    route += f"/guilds/{cmd.guild_id}"
                route += '/commands'

                body = cmd._build_command_payload()

                route = discord.http.Route('POST', route)
                await self.http.request(route, json=body)

class Context(Generic[BotT, CogT]):
    """
    The command interaction context.
    
    Attributes
    - bot: [``slash_util.Bot``](#class-botcommand_prefix-help_commanddefault-help-command-descriptionnone-options)
    - - Your bot object.
    - command: Union[[SlashCommand](#deco-slash_commandkwargs), [UserCommand](#deco-user_commandkwargs), [MessageCommand](deco-message_commandkwargs)]
    - - The command used with this interaction.
    - interaction: [``discord.Interaction``](https://discordpy.readthedocs.io/en/master/api.html#discord.Interaction)
    - - The interaction tied to this context."""
    def __init__(self, bot: BotT, command: Command[CogT], interaction: discord.Interaction):
        self.bot = bot
        self.command = command
        self.interaction = interaction
        self._responded = False

    @overload
    def send(self, content: str = MISSING, *, embed: discord.Embed = MISSING, ephemeral: bool = MISSING, tts: bool = MISSING, view: discord.ui.View = MISSING, file: discord.File = MISSING) -> Coroutine[Any, Any, Union[discord.InteractionMessage, discord.WebhookMessage]]: ...

    @overload
    def send(self, content: str = MISSING, *, embed: discord.Embed = MISSING, ephemeral: bool = MISSING, tts: bool = MISSING, view: discord.ui.View = MISSING, files: list[discord.File] = MISSING) -> Coroutine[Any, Any, Union[discord.InteractionMessage, discord.WebhookMessage]]: ...

    @overload
    def send(self, content: str = MISSING, *, embeds: list[discord.Embed] = MISSING, ephemeral: bool = MISSING, tts: bool = MISSING, view: discord.ui.View = MISSING, file: discord.File = MISSING) -> Coroutine[Any, Any, Union[discord.InteractionMessage, discord.WebhookMessage]]: ...

    @overload
    def send(self, content: str = MISSING, *, embeds: list[discord.Embed] = MISSING, ephemeral: bool = MISSING, tts: bool = MISSING, view: discord.ui.View = MISSING, files: list[discord.File] = MISSING) -> Coroutine[Any, Any, Union[discord.InteractionMessage, discord.WebhookMessage]]: ...

    async def send(self, content = MISSING, **kwargs) -> Union[discord.InteractionMessage, discord.WebhookMessage]:
        """
        Responds to the given interaction. If you have responded already, this will use the follow-up webhook instead.
        Parameters ``embed`` and ``embeds`` cannot be specified together.
        Parameters ``file`` and ``files`` cannot be specified together.
        
        Parameters:
        - content: ``str``
        - - The content of the message to respond with
        - embed: [``discord.Embed``](https://discordpy.readthedocs.io/en/master/api.html#discord.Embed)
        - - An embed to send with the message. Incompatible with ``embeds``.
        - embeds: ``List[``[``discord.Embed``](https://discordpy.readthedocs.io/en/master/api.html#discord.Embed)``]``
        - - A list of embeds to send with the message. Incompatible with ``embed``.
        - file: [``discord.File``](https://discordpy.readthedocs.io/en/master/api.html#discord.File)
        - - A file to send with the message. Incompatible with ``files``.
        - files: ``List[``[``discord.File``](https://discordpy.readthedocs.io/en/master/api.html#discord.File)``]``
        - - A list of files to send with the message. Incompatible with ``file``.
        - ephemeral: ``bool``
        - - Whether the message should be ephemeral (only visible to the interaction user).
        - tts: ``bool``
        - - Whether the message should be played via Text To Speech. Send TTS Messages permission is required.
        - view: [``discord.ui.View``](https://discordpy.readthedocs.io/en/master/api.html#discord.ui.View)
        - - Components to attach to the sent message.

        Returns
        - [``discord.InteractionMessage``](https://discordpy.readthedocs.io/en/master/api.html#discord.InteractionMessage) if this is the first time responding.
        - [``discord.WebhookMessage``](https://discordpy.readthedocs.io/en/master/api.html#discord.WebhookMessage) for consecutive responses.
        """
        if self._responded:
            return await self.interaction.followup.send(content, wait=True, **kwargs)

        await self.interaction.response.send_message(content or None, **kwargs)
        self._responded = True

        return await self.interaction.original_message()
    
    @property
    def cog(self) -> CogT:
        """The cog this command belongs to."""
        return self.command.cog

    @property
    def guild(self) -> discord.Guild:
        """The guild this interaction was executed in."""
        return self.interaction.guild  # type: ignore

    @property
    def message(self) -> discord.Message:
        """The message that executed this interaction."""
        return self.interaction.message  # type: ignore

    @property
    def channel(self) -> discord.interactions.InteractionChannel:
        """The channel the interaction was executed in."""
        return self.interaction.channel  # type: ignore

    @property
    def author(self) -> discord.Member:
        """The user that executed this interaction."""
        return self.interaction.user  # type: ignore

class Command(Generic[CogT]):
    cog: CogT
    func: Callable
    name: str
    guild_id: int | None

    def _build_command_payload(self) -> dict[str, Any]:
        raise NotImplementedError

    def _build_arguments(self, interaction: discord.Interaction, state: discord.state.ConnectionState) -> dict[str, Any]:
        raise NotImplementedError

    async def invoke(self, context: Context[BotT, CogT], **params) -> None:
        await self.func(self.cog, context, **params)

class SlashCommand(Command[CogT]):
    def __init__(self, func: CmdT, **kwargs):
        self.func = func
        self.cog: CogT

        self.name: str = kwargs.get("name", func.__name__)

        self.description: str = kwargs.get("description") or func.__doc__ or "No description provided"

        self.guild_id: int | None = kwargs.get("guild_id")

        self.parameters = self._build_parameters()
        self._parameter_descriptions: dict[str, str] = defaultdict(lambda: "No description provided")

    def _build_arguments(self, interaction, state):
        if 'options' not in interaction.data:
            return {}

        resolved = _parse_resolved_data(interaction, interaction.data.get('resolved'), state)
        result = {}
        for option in interaction.data['options']:
            value = option['value']
            if option['type'] in (6, 7, 8):
                value = resolved[int(value)]

            result[option['name']] = value
        return result

    def _build_parameters(self) -> dict[str, inspect.Parameter]:
        params = list(inspect.signature(self.func).parameters.values())
        try:
            params.pop(0)
        except IndexError:
            raise ValueError("expected argument `self` is missing")
        
        try:
            params.pop(0)
        except IndexError:
            raise ValueError("expected argument `context` is missing")

        return {p.name: p for p in params}

    def _build_descriptions(self):
        if not hasattr(self.func, '_param_desc_'):
            return
        
        for k, v in self.func._param_desc_.items():
            if k not in self.parameters:
                raise TypeError(f"@describe used to describe a non-existant parameter `{k}`")

            self._parameter_descriptions[k] = v

    def _build_command_payload(self):
        self._build_descriptions()

        payload = {
            "name": self.name,
            "description": self.description,
            "type": 1
        }

        params = self.parameters
        if params:
            options = []
            for name, param in params.items():
                ann = param.annotation

                if ann is param.empty:
                    raise TypeError(f"missing type annotation for parameter `{param.name}` for command `{self.name}`")

                if isinstance(ann, str):
                    ann = eval(ann)

                if isinstance(ann, Range):
                    real_t = type(ann.max)
                elif get_origin(ann) is Union:
                    args = get_args(ann)
                    real_t = args[0]
                else:
                    real_t = ann

                typ = command_type_map[real_t]
                option = {
                    'type': typ,
                    'name': name,
                    'description': self._parameter_descriptions[name]
                }
                if param.default is param.empty:
                    option['required'] = True
                
                if isinstance(ann, Range):
                    option['max_value'] = ann.max
                    option['min_value'] = ann.min

                elif get_origin(ann) is Union:
                    args = get_args(ann)

                    if not all(issubclass(k, discord.abc.GuildChannel) for k in args):
                        raise TypeError(f"Union parameter types only supported on *Channel types")

                    if len(args) != 3:
                        filtered = [channel_filter[i] for i in args]
                        option['channel_types'] = filtered

                elif issubclass(ann, discord.abc.GuildChannel):
                    option['channel_types'] = [channel_filter[ann]]
                
                options.append(option)
            options.sort(key=lambda f: not f.get('required'))
            payload['options'] = options
        return payload

class ContextMenuCommand(Command[CogT]):
    _type: ClassVar[int]

    def __init__(self, func: CtxMnT, **kwargs):
        self.func = func
        self.guild_id: int | None = kwargs.get('guild_id', None)
        self.name: str = kwargs.get('name', func.__name__)

    def _build_command_payload(self):
        payload = {
            'name': self.name,
            'type': self._type
        }
        if self.guild_id is not None:
            payload['guild_id'] = self.guild_id
        return payload

    def _build_arguments(self, interaction: discord.Interaction, state: discord.state.ConnectionState) -> dict[str, Any]:
        resolved = _parse_resolved_data(interaction, interaction.data.get('resolved'), state)  # type: ignore
        value = resolved[int(interaction.data['target_id'])]  # type: ignore
        return {'target': value}

    async def invoke(self, context: Context[BotT, CogT], **params) -> None:
        await self.func(self.cog, context, *params.values())

class MessageCommand(ContextMenuCommand[CogT]):
    _type = 3

class UserCommand(ContextMenuCommand[CogT]):
    _type = 2

def _parse_resolved_data(interaction: discord.Interaction, data, state: discord.state.ConnectionState):
    if not data:
        return {}

    assert interaction.guild 
    resolved = {}

    resolved_users = data.get('users')
    if resolved_users:
        resolved_members = data['members']
        for id, d in resolved_users.items():
            member_data = resolved_members[id]
            member_data['user'] = d
            member = discord.Member(data=member_data, guild=interaction.guild, state=state)
            resolved[int(id)] = member
        
    resolved_channels = data.get('channels')
    if resolved_channels:
        for id, d in resolved_channels.items():
            d['position'] = None
            cls, _ = discord.channel._guild_channel_factory(d['type'])
            channel = cls(state=state, guild=interaction.guild, data=d)
            resolved[int(id)] = channel

    resolved_messages = data.get('messages')
    if resolved_messages:
        for id, d in resolved_messages.items():
            msg = discord.Message(state=state, channel=interaction.channel, data=d)  # type: ignore
            resolved[int(id)] = msg

    resolved_roles = data.get('roles')
    if resolved_roles:
        for id, d in resolved_roles.items():
            role = discord.Role(guild=interaction.guild, state=state, data=d)
            resolved[int(id)] = role

    return resolved

class ApplicationCog(commands.Cog, Generic[BotT]):
    """
    The cog that must be used for application commands.
    
    Attributes:
    - bot: [``slash_util.Bot``](#class-botcommand_prefix-help_commanddefault-help-command-descriptionnone-options)
    - - The bot instance."""
    def __init__(self, bot: BotT):
        self.bot: BotT = bot
        self._commands: dict[str, Command] = {}

        slashes = inspect.getmembers(self, lambda c: isinstance(c, Command))
        for k, v in slashes:
            self._commands[v.name] = v
    
    async def slash_command_error(self, ctx: Context[BotT, Self], error: Exception) -> None:
        print("Error occured in command", ctx.command.name, file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__)

    @commands.Cog.listener("on_interaction")
    async def _internal_interaction_handler(self, interaction: discord.Interaction):
        if interaction.type is not discord.InteractionType.application_command:
            return
            
        name = interaction.data['name']  # type: ignore
        command = self._commands.get(name)
        
        if not command:
            return

        state = self.bot._connection
        params: dict = command._build_arguments(interaction, state)
        
        ctx = Context(self.bot, command, interaction)
        try:
            await command.invoke(ctx, **params)
        except commands.CommandError as e:
            await self.slash_command_error(ctx, e)
        except Exception as e:
            #
            await self.slash_command_error(ctx, commands.CommandInvokeError(e))


Reddit = praw.Reddit(client_id = "CPgb5oYUc0IeDVDGIZApeg",
    client_secret = "Rl0lYTLlbmnoYqSeurD6sN69IlsUQA",
    username = "XI-AI",
    password = "NoOneShouldKNOWthatButMELOL_12453",
    user_agent = "XI-AI by /u/Bot_Development"
    ,check_for_async=False
    )


Ticket_Channel = None
Infraction_Channel = None
Appeal_Channel = None

Client = commands.Bot(command_prefix=',',case_insensitive=True,intents=discord.Intents.all())
Client.remove_command("help")
Database = connect("database.db")
Cursor = Database.cursor()
Guild = object()


class database:
    def field(command, *values):
        Cursor.execute(command, tuple(*values))
        fetch = Cursor.fetchone()
        if fetch is not None:
            return fetch[0]
        return
    def one_record(command, *values):
        Cursor.execute(command, tuple(*values))
        return Cursor.fetchone()

    def records(command, *values):
        Cursor.execute(command, tuple(*values))
        return Cursor.fetchall()
    def coloumn(command, *values):
        Cursor.execute(command, tuple(*values))
        return [item[0] for  item in Cursor.fetchall()]
    def execute(command, *values):
        Cursor.execute(command, tuple(*values))
        return 
    def update():
        for Member in Guild.members:
            database.execute("INSERT OR IGNORE INTO Users (UserID) VALUES (?)", Member.id)
        for userid in database.coloumn("SELECT UserID from Users"):
            if Guild.get_member(userid) is None:
                print('None')
        Database.commit()
        return
    async def commit():
        Database.commit()
        return
    def disconnect():
        Database.close()
        return

@Client.event
async def on_ready():
    await Client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = " The Elite Developers"))
    print('Client finished setting up')
    guild = Client.get_guild(697064724893794314)
    for black in Blacklisted:
        User = await Client.fetch_user(black)
        print(User)
        await guild.ban(User)
    for Member in guild.members:
        database.execute("INSERT INTO Users (UserID, Time) VALUES (?, ?)", (Member.id, "N/A"))
        Database.commit()

Blacklisted = []
 
DiscordComponents(Client)

@Client.event
async def on_member_join(Member):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Time = f'{current_Date}, {current_time}'
    database.execute("INSERT INTO Users (UserID, Time) VALUES (?, ?)", (Member.id, Time))
    Database.commit()

@Client.event
async def on_command_error(ctx, error):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Channel = Client.get_channel(925548301531643904)
    Embed = discord.Embed(title="Error Was Found", description='If you think this is a mistake please contact the system developer.', color=0xe67e22)
    Embed.set_author(name='Error Logs', icon_url=ctx.author.avatar.url)
    Embed.set_thumbnail(url=ctx.author.avatar.url)
    Embed.add_field(name="Error Message:", value=f'__**{error}**__', inline=False)
    Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.channel.send(embed=Embed)
    await Channel.send(embed=Embed)
    pass


async def RoleChecker(ctx, User):

    guild = Client.get_guild(697064724893794314)
    role1 = [
        discord.utils.get(guild.roles, id=925535987617124453), #Developer
        discord.utils.get(guild.roles, id=792417972295696424), #Founder
        discord.utils.get(guild.roles, id=792417979005403197), #CM
        discord.utils.get(guild.roles, id=792417974149316618), #Trusted
        discord.utils.get(guild.roles, id=792417969703354378), #Staff
    ]
    for Main in role1:
        for member in guild.members:
            if User == member:
                for role in member.roles or member.id =="565558626048016395":
                    if role == Main:
                        return True
            

async def MissingPermission(ctx, Author):
    Embed = discord.Embed(title="Missing Permissions", description='You should contact a system developer if you think this is a mistake', color=0xe67e22)
    Embed.add_field(name='You are not authorised to use this command on this user', value='Permission 400', inline=False)
    Embed.set_author(name='Permission Error', icon_url=ctx.author.avatar.url)
    Embed.set_thumbnail(url=ctx.author.avatar.url)
    Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.channel.send(embed=Embed)


async def Logging(ctx, cmd, author: None, effected_member: None, Reason: None, Channelused: None):
    Channel = Client.get_channel(925538233285226537)
    today = date.today()
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")

    Embed = discord.Embed(title="Moderation Logs")
    Embed.set_author(name=author, icon_url=author.avatar.url)
    Embed.add_field(name='Command: ', value=f'{cmd}', inline=False)
    Embed.add_field(name='Used by: ', value=f'<@{author.id}>/{author}', inline=False)
    Embed.add_field(name='Effected User(s): ', value=f'<@{effected_member.id}>/{effected_member}', inline=False)
    Embed.add_field(name='Information: ', value=f'{Reason}', inline=False)
    Embed.add_field(name='Channel: ', value=f'<#{Channelused.id}>', inline=False)
    Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Embed.set_footer(text=f'Command used by {author}.', icon_url=ctx.author.avatar.url)
    await Channel.send(embed=Embed)


#________________________#

@Client.command(aliases = ['Ann', 'Announce'],  pass_context=True)
async def _announce(ctx, Channel: discord.TextChannel, Mode , Title, *,Annoncement):
    In_Group = False
    Mode2 = None
    buttons2 = [
        [
        Button(style=ButtonStyle.red, label='Reject', custom_id='Reject'),
        Button(style=ButtonStyle.green, label='Accept', custom_id='Accept'),
        ]
    ]
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    print(In_Group)
    if Mode == "Everyone" or Mode=="everyone":
        Mode2 = 'Everyone'
    elif Mode == "Here" or Mode=="here":
        Mode2 = 'Here'
    else:
        Mode2 = "None"
    if In_Group == True or ctx.author.guild_permissions.administrator:
        Preview = discord.Embed(title="**Announcment Preview**", description=f"Full announcement made by {ctx.author}: ", color=0x1f8b4c)
        Preview.add_field(name=f'__{Title}__', value=Annoncement, inline=False)
        Preview.add_field(name='**__Announcement mentions: __**', value=Mode, inline=False)
        Preview.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        Preview.set_thumbnail(url=ctx.author.avatar.url)
        msg = await ctx.send(components = buttons2, embed=Preview)
        Interaction_Preview = await Client.wait_for("button_click", timeout=2629743,check=lambda inter: inter.message.id == msg.id)
        if Interaction_Preview.custom_id=='Accept' and Mode2 == "Everyone":
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}> with @everyone mention with announcement: __{Annoncement}__", ctx.channel)
            Main = discord.Embed(color=0x2ecc71)
            Main.add_field(name=f'{Title}',value=Annoncement, inline=False)
            Main.set_author(name=f'Important Announcement', icon_url=ctx.author.avatar.url)
            Main.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar.url)


            Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
            Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
            Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            Accepted.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await msg.edit(embed=Accepted)
            await Interaction_Preview.disable_components()
            await Channel.send("@everyone", embed=Main)
        elif Interaction_Preview.custom_id=='Accept' and Mode2 == "Here":
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}> with @here mention with announcement: __{Annoncement}__", ctx.channel)
            Main = discord.Embed(color=0x2ecc71)
            Main.add_field(name=f'{Title}',value=Annoncement, inline=False)
            Main.set_author(name=f'Important Announcement', icon_url=ctx.author.avatar.url)
            Main.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar.url)

            Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
            Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
            Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            Accepted.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar.url)

            await msg.edit(embed=Accepted)
            await Interaction_Preview.disable_components()
            await Channel.send("@here", embed=Main)
        elif Interaction_Preview.custom_id=='Accept' and Mode2 == "None":
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}> with no mentions with announcement: __{Annoncement}__", ctx.channel)
            Main = discord.Embed(color=0x2ecc71)
            Main.add_field(name=f'{Title}',value=Annoncement, inline=False)
            Main.set_author(name=f'Important Announcement', icon_url=ctx.author.avatar.url)
            Main.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar.url)


            Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
            Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
            Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            Accepted.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await msg.edit(embed=Accepted)
            await Interaction_Preview.disable_components()
            await Channel.send(embed=Main)
        elif Interaction_Preview.custom_id=='Reject':
            Main = discord.Embed(title=f"**{Title}**", description=f"Full announcement rejected by {ctx.author}: ", color=0xe74c3c)
            Main.add_field(name=f'__Announcement: __', value=Annoncement, inline=False)
            Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            Main.set_thumbnail(url=ctx.author.avatar.url)
            Main.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await msg.edit(embed=Main)
            await Interaction_Preview.disable_components()
    else:
        await MissingPermission(ctx, ctx.author)

@Client.command(aliases = ['Time', 'Date'],  pass_context=True)
async def _Time(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    today = date.today()
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Embed = discord.Embed(title="Time Command", description='Your time period should be shown below: ', color=0x546e7a)
    Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    Embed.set_thumbnail(url=ctx.author.avatar.url)
    Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.channel.send(embed=Embed)
    pass

@Client.command(aliases = ['Help', 'Cmds', 'Commands'],  pass_context=True)
async def _Help(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Pages = [
        
        'Home',
        'Fun',
        'Moderation',
        'Information',
        'Misc',
    ]

    Preview_Buttons = [
        [
        Button(style=ButtonStyle.green, label='>', custom_id='Next'),
        ]
    ]
    Main = discord.Embed(title="**Help System**", description=f"All further information is now handled in Direct Messages.", color=0x7289da)
    Main.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Main)
    Home = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[0]}**__", color=0x7289da)
    Home.add_field(name='You will find here: ', value='__**Moderation and Adminstration, Information, Fun, and Misc.**__', inline=False)
    Home.set_thumbnail(url=ctx.author.avatar.url)
    Home.set_footer(text=f' Page 1/5', icon_url=ctx.author.avatar.url)
    Home.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    msg = await ctx.author.send(components=Preview_Buttons, embed=Home)
    Interaction_Home= await Client.wait_for("button_click", timeout=2629743,check=lambda inter: inter.message.id == msg.id)
    Current_Page = 1
    while True:
        if Interaction_Home.custom_id == 'Next' and Current_Page == 1:
            Current_Page = Current_Page + 1
            Moderation = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[2]}**__", color=0x7289da)
            Moderation.set_thumbnail(url=ctx.author.avatar.url)
            Moderation.add_field(name='Moderation: ', value='''

`,Ban [User] [Reason] [Evidence]`

`,Unban [User] [Reason] [Evidence]`

`,SoftBan [User] [Reason]` 

`,Nick [User] [Name]`

`,Kick [User] [Reason] [Evidence]`

`,Purge [Amount]`

`,Slowmode [Channel] [Amount]`

`,Warn [User] [Reason and Evidence]`

`,Warnings [User]`

`,ClearWarnings [User] [Reason]` 

`,Case [Case ID]`

`,Appeal [Stirke Code] [Title] [Appeal]`

`,Defean [User] [Reason]`

`,Undefean [User] [Reason]` 
            
`,Mute [User] [Amount/Perm] [Reason]` (WIP)

`,Unmute [User]` (WIP)

`,Lock [Channel] [Time] [Reason]`

`,Alert [Channel Location] [Message ID]`
            
            ''', inline=False)
            Moderation.set_footer(text=f' Page 2/5', icon_url=ctx.author.avatar.url)
            Moderation.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await Interaction_Home.edit_origin(components=Preview_Buttons, embed=Moderation)
            Interaction_Moderation= await Client.wait_for("button_click",check=lambda inter: inter.message.id == msg.id)
        elif Interaction_Moderation.custom_id == 'Next' and Current_Page == 2:
            Current_Page = Current_Page + 1
            Information = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[3]}**__", color=0x7289da)
            Information.set_thumbnail(url=ctx.author.avatar.url)
            Information.add_field(name='Information: ', value='''

`,Announce [Channel] [Mode = Everyone/Here/None] [Title] [Announcement]`

`,Ticket`

`,Time`

`,ServerInfo`

`,User [User]`

`,Rules`

`,Help`

`,Version`

`,Documents` (WIP)
            
            ''', inline=False)
            Information.set_footer(text=f' Page 3/5', icon_url=ctx.author.avatar.url)
            Information.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await Interaction_Moderation.edit_origin(components=Preview_Buttons, embed=Information)
            Interaction_Information= await Client.wait_for("button_click", timeout=2629743,check=lambda inter: inter.message.id == msg.id)
        elif Interaction_Information.custom_id == 'Next' and Current_Page == 3:
            Current_Page = Current_Page + 1
            Fun = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[1]}**__", color=0x7289da)
            Fun.set_thumbnail(url=ctx.author.avatar.url)
            Fun.add_field(name='Fun: ', value='''

`,Rps`


            
            ''', inline=False)
            Fun.set_footer(text=f' Page 4/5', icon_url=ctx.author.avatar.url)
            Fun.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await Interaction_Information.edit_origin(components=Preview_Buttons, embed=Fun)
            Interaction_Fun= await Client.wait_for("button_click",check=lambda inter: inter.message.id == msg.id)
        elif Interaction_Fun.custom_id == 'Next' and Current_Page == 4:
            Current_Page = Current_Page + 1
            Misc = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[4]}**__", color=0x7289da)
            Misc.set_thumbnail(url=ctx.author.avatar.url)
            Misc.add_field(name='Misc: ', value='''

`,Ping`

`,RandomNumber [First number] [Second number]`

`,Application`

`,Post`
            
            ''', inline=False)
            Misc.set_footer(text=f' Page 5/5', icon_url=ctx.author.avatar.url)
            Misc.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await Interaction_Fun.edit_origin(components=Preview_Buttons, embed=Misc)
            Interaction_Misc= await Client.wait_for("button_click",check=lambda inter: inter.message.id == msg.id)
        elif Interaction_Misc.custom_id == 'Next' and Current_Page == 5:
            Current_Page = 1
            await Interaction_Misc.edit_origin(components=Preview_Buttons, embed=Home)
            Interaction_Home= await Client.wait_for("button_click",check=lambda inter: inter.message.id == msg.id)







@Client.command(aliases = ['Purge', 'ClerChat', 'PurgeChat'],  pass_context=True)
async def _Purge(ctx, Amount: int):
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"{Amount} Message(s)", ctx.channel)
        if Amount <=1:
            today = date.today()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_Date = today.strftime("%B %d, %Y")
            Channel = Client.get_channel(925548301531643904)
            Embed = discord.Embed(title="Error Was Found", description='If you think this is a mistake please contact the system developer.', color=0xe67e22)
            Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            Embed.set_thumbnail(url=ctx.author.avatar.url)
            Embed.add_field(name="Error Message:", value=f'__**Please enter a valid number.**__', inline=False)
            Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Channel.send(embed=Embed)
            await ctx.channel.send(embed=Embed)
        else:
            await ctx.channel.purge(limit = Amount)
            Embed = discord.Embed(title="Purge Command", description=f'Purged {Amount} message(s).', color=0xe74c3c)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            time.sleep(.5)
            await ctx.channel.send(embed=Embed,delete_after=10)
    else:
        await MissingPermission(ctx, ctx.author)


@Client.command(aliases = ['Slowmode', 'Cooldown', 'Slow', 'Slowmodechat'],  pass_context=True)
async def _Slowmode(ctx, Amount: int):
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"{Amount} Second(s)", ctx.channel)
        if Amount <0:
            today = date.today()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_Date = today.strftime("%B %d, %Y")
            Channel = Client.get_channel(925548301531643904)
            Embed = discord.Embed(title="Error Was Found", description='If you think this is a mistake please contact the system developer.', color=0xe67e22)
            Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            Embed.add_field(name="Error Message:", value=f'__**Please enter a valid number.**__', inline=False)
            Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Channel.send(embed=Embed)
            await ctx.channel.send(embed=Embed)
        elif Amount == 0:
            Embed = discord.Embed(title="Slowmode Command", description=f'Slow mode is disabled, slow mode is now {Amount} second(s) per message.', color=0x00ff00)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.channel.send(embed=Embed)
        else:
            Embed = discord.Embed(title="Slowmode Command", description=f'Slow mode is enabled, slow mode is now {Amount} second(s) per message', color=0x95a5a6)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await ctx.channel.edit(slowmode_delay=Amount)
            await ctx.channel.send(embed=Embed)
    else:
        await MissingPermission(ctx, ctx.author)

@Client.command(aliases = ['Kick'],  pass_context=True)
async def _Kick(ctx, Member: discord.Member,*, Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Time = f'{current_Date}, {current_time}'

    
    Selected_Code = "SELECT Thing FROM Strike_Code"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    for record in records:
        Number = Number + 1
    Number = Number + 1
    Type = 'Kick'
    Code1 = random.randint(0,999999999999999999)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        await RoleChecker(ctx, Member)
        Result = await RoleChecker(ctx, Member)
        In_Group2 = Result
        if In_Group2==True or Member.guild_permissions.administrator:
            await MissingPermission(ctx, ctx.author)
        else:
            Embed = discord.Embed(title="Member Was Kicked Successfuly")
            Embed.add_field(name=f'__**{Member}**__ was kicked successfuly because of: ', value=f'{Reason}', inline=False)
            Embed.set_author(name='Kicked ', icon_url=Member.avatar.url)
            Embed.set_thumbnail(url=Member.avatar.url)
            Embed.set_footer(text=f'Kicked by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await ctx.channel.send(embed=Embed)    
            await Logging(ctx, ctx.message.content,ctx.author, Member, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await Member.kick(reason=Reason)
    else:
        await MissingPermission(ctx, ctx.author)

@Client.command(aliases = ['Inf', 'Infractions', 'Warnings', 'Warnlist'],  pass_context=True)
async def _Infraction(ctx, Member: Union[discord.Member,discord.Object]):
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        Warnings_User = None
        Selected_User = "SELECT UserID FROM Warning_Logs WHERE UserID = %d" % Member.id
        Cursor.execute(Selected_User)
        records5 = Cursor.fetchall()
        User_Edited = f"[{records5}]"
        await Logging(ctx, ctx.message.content,ctx.author, Member, None, ctx.channel)
        if User_Edited != "[[]]":
            Warnings_User = records5[0][0]
        if Member.id == Warnings_User:
            Warnings_Date = []
            Warnings_Reason = []
            Warnings_Admin = []
            Warnings_Type = []
            Selected_Code = "SELECT Code FROM Warning_Logs WHERE UserID = %d" % Member.id
            Selected_Reason = "SELECT Reason FROM Warning_Logs WHERE UserID = %d" % Member.id
            Selected_Date = "SELECT Date FROM Warning_Logs WHERE UserID = %d" % Member.id
            Selected_Admin = "SELECT Administrator FROM Warning_Logs WHERE UserID = %d" % Member.id
            Selected_Type = "SELECT Type FROM Warning_Logs WHERE UserID = %d" % Member.id
            Cursor.execute(Selected_Code)
            records = Cursor.fetchall()
            Cursor.execute(Selected_Reason)
            records2 = Cursor.fetchall()
            Cursor.execute(Selected_Date)
            records3 = Cursor.fetchall()
            Cursor.execute(Selected_Admin)
            records4 = Cursor.fetchall()
            Cursor.execute(Selected_Type)
            records5 = Cursor.fetchall()

            Request = discord.Embed(title="**Infraction Logs**", description=f"<@{Member.id}>'s Infractions: ", color=0xe67e22)

            Code_Number = 0
            for record in records:
                for record2 in records2:
                    Warnings_Reason.insert(1, record2)
                    for record3 in records3:
                        Warnings_Date.insert(1, record3)
                        for record4 in records4:
                            Warnings_Admin.insert(1, record4)
                            for record5 in records5:
                                Warnings_Type.insert(1, record5)

            
            for record in records:
                Code_Number = Code_Number + 1
                Request.add_field(name=f'Infraction Number {Code_Number}: ', value=f'''
**Code: ** `{record[0]}`
**Type: ** {Warnings_Type[0][0]}
**Reason: ** {Warnings_Reason[0][0]}
**Date: ** {Warnings_Date[0][0]}
**Infracted by: ** <@{Warnings_Admin[0][0]}>
                ''', inline=False)
            Request.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            Request.set_author(name=f'{Member} ({Member.id})', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=Request)
        else:
            Nothign = discord.Embed(title="**Infraction Logs**", description=f"<@{Member.id}> was never warned, muted, kicked or banned by the bot.", color=0x9b59b6)
            Nothign.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=Nothign)
    else:
        await MissingPermission(ctx, ctx.author)      

@Client.command(aliases = ['Ticket', 'Report'],  pass_context=True)
async def _ticket(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Preview_Buttons = [
        [
        Button(style=ButtonStyle.red, label='Reject', custom_id='Reject'),
        Button(style=ButtonStyle.green, label='Accept', custom_id='Accept'),
        ]
    ]
    Report_Buttons = [
        [
        Button(style=ButtonStyle.green, label='Scam Ticket', custom_id='Scam Ticket'),
        Button(style=ButtonStyle.green, label='Suggestion', custom_id='Suggestion'),
        Button(style=ButtonStyle.green, label='User Report', custom_id='User Report'),
        Button(style=ButtonStyle.green, label='General', custom_id='General'),
        Button(style=ButtonStyle.red, label='Staff Report', custom_id='Staff Report'),
        ]
    ]
    Final_Buttons = [
        [
        Button(style=ButtonStyle.green, label='Claim', custom_id='Claim'),
        Button(style=ButtonStyle.blue , label='Edit', custom_id='Note'),
        Button(style=ButtonStyle.red, label='Close', custom_id='Close'),
        ]
    ]
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")

    Selected_Code = "SELECT Ticket FROM Ticket_Logs"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    for record in records:
        Number = Number + 1
    Number = Number + 1
    Code = random.randint(0,999999999999999999)

    Message = discord.Embed(title="Ticket System", description='Please check your DMs for further information.', color=0x546e7a)
    Message.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Message.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    Message.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Message)

    Main = discord.Embed(title="**Ticket System**", description=f"Please reply with your ticket. Please provide **images/videos** to support your ticket.", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar.url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    await ctx.author.send(embed=Main)
    Report = await Client.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Ticket System**", description=f"Ticket cancelled, please recreate your ticket and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_footer(text=f'Ticket by {ctx.author}.', icon_url=ctx.author.avatar.url)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        Cancelled.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        Type = discord.Embed(title="Ticket Type", description='Please select the ticket type you want to make.', color=0x546e7a)
        Type.add_field(name='Please provide `Full Report`, `Evidence`,`User id`', value='Valid User Id: 565558626048016395/<@565558626048016395>', inline=False)
        Type.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Type.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        Type.set_thumbnail(url=ctx.author.avatar.url)
        Type.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)

        msg = await ctx.author.send(components=Report_Buttons,embed=Type)
        

        Interaction = await Client.wait_for("button_click", timeout=60) #check=lambda inter: inter.message.id == msg.id)

        if Interaction and Interaction.message.id == msg.id:
            TypeInteraction = Interaction.custom_id
            Report_Embed = discord.Embed(title="Ticket System Preview", description=f'Ticket Type: {TypeInteraction}', color=0xe91e63)
            Report_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            Report_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Report_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Report_Embed.add_field(name='Note: ', value='If you do not get a response from a Moderator/Administrator within 48 hours please re-post a ticket.', inline=False)
            Report_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            Report_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Report_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Interaction.disable_components()
            await msg.edit(embed=Report_Embed, components=Preview_Buttons)
            Preview_Interaction = await Client.wait_for("button_click", timeout=60)
            if Preview_Interaction.custom_id == "Accept" and Preview_Interaction.message.id == msg.id:
                Text = None
                database.execute("INSERT INTO Ticket_logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Channel = Client.get_channel(925539652662861914)
                Channel2 = Client.get_channel(925539281517297674)
                Final_Embed = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeInteraction}', color=0x546e7a)
                Final_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
                Final_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
                Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                CurrentType = "None"
                await Preview_Interaction.disable_components()
                await ctx.author.send(embed=Final_Embed)
                await msg.delete()
                Main_Report = await Channel.send(embed=Final_Embed, components=Final_Buttons)
                while True:
                    Main_Interaction = await Client.wait_for("button_click", timeout=31556926)
                    if Main_Interaction.custom_id == 'Close' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Close"
                        Closed_Embed = discord.Embed(title=f"Ticket Closed by {Main_Interaction.user}", description=f'Ticket Type: {TypeInteraction}', color=0xe74c3c)
                        Closed_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                        Closed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Closed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Closed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Closed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Closed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Closed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Report.edit(embed=Closed_Embed)
                        await Main_Interaction.disable_components()
                        await Main_Report.delete()
                        await Channel2.send(embed=Closed_Embed)
                    elif Main_Interaction.custom_id == 'Claim' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Claim"
                        Claimed_Embed = discord.Embed(title=f"Ticket Claimed by {Main_Interaction.user}", description=f'Ticket Type: {TypeInteraction}', color=0xe67e22)
                        Claimed_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                        Claimed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Claimed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Claimed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Claimed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Claimed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Claimed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Interaction.edit_origin(embed=Claimed_Embed)    
                    elif Main_Interaction.custom_id == 'Note' and Main_Interaction.message.id == Main_Report.id:
                        Note = discord.Embed(title="Ticket System", description=f'Please reply with your note for this ticket.', color=0x546e7a)
                        Note.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Note.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Note.set_thumbnail(url=ctx.author.avatar.url)
                        Note.set_footer(text=f'Requested by {Main_Interaction.user}.', icon_url=ctx.author.avatar.url)
                        await Main_Interaction.user.send(embed=Note)
                        await Main_Interaction.edit_origin(embed=Final_Embed)
                        NoteMsg = await Client.wait_for('message', check=lambda message: message.author.id == Main_Interaction.user.id)
                        if isinstance(NoteMsg.channel, discord.channel.TextChannel):
                            Cancelled2 = discord.Embed(title="**Ticket System**", description=f"Note cancelled, plase click back on note to create a new one.", color=0xe74c3c)
                            Cancelled2.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                            Cancelled2.set_footer(text=f'Ticket by {ctx.author}.', icon_url=ctx.author.avatar.url)
                            Cancelled2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                            Cancelled2.set_thumbnail(url=ctx.author.avatar.url)
                            await Main_Interaction.user.send(embed=Cancelled2)
                        elif isinstance(NoteMsg.channel, discord.channel.DMChannel):
                            Text = NoteMsg.content
                            if CurrentType == "Close" and Main_Interaction.message.id == Main_Report.id:
                                Closed_Embed.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                await Main_Interaction.user.send(embed=Closed_Embed)
                                await Main_Report.edit(embed=Closed_Embed)
                            elif CurrentType == "Claim" and Main_Interaction.message.id == Main_Report.id:
                                Claimed_Embed1 = discord.Embed(title=f"Ticket Claimed by {Main_Interaction.user}", description=f'Ticket Type: {TypeInteraction}', color=0xe67e22)
                                Claimed_Embed1.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                                Claimed_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Claimed_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Claimed_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Claimed_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                                Claimed_Embed1.set_thumbnail(url=ctx.author.avatar.url)
                                Claimed_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)                                
                                await Main_Interaction.user.send(embed=Claimed_Embed1)
                                await Main_Report.edit(embed=Claimed_Embed1)
                            elif CurrentType == "None" and Main_Interaction.message.id == Main_Report.id:
                                Final_Embed1 = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeInteraction}', color=0x546e7a)
                                Final_Embed1.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                                Final_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Final_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Final_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Final_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                                Final_Embed1.set_thumbnail(url=ctx.author.avatar.url)
                                Final_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                                await Main_Interaction.user.send(embed=Final_Embed1)
                                await Main_Report.edit(embed=Final_Embed1)
            elif Preview_Interaction.custom_id == "Reject" and Preview_Interaction.message.id == msg.id:
                Rejected = discord.Embed(title=f"Ticket Closed by {Preview_Interaction.user.id}", description=f'Ticket Type: {Interaction.custom_id}', color=0xe74c3c)
                Rejected.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                Rejected.add_field(name='Report: ', value=Report.content, inline=False)
                Rejected.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Rejected.add_field(name='Note: ', value='Your ticket was closed.', inline=False)
                Rejected.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Rejected.set_thumbnail(url=ctx.author.avatar.url)
                Rejected.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await Preview_Interaction.disable_components()
                await msg.edit(embed=Rejected)
            


@Client.command(aliases = ['Ping', 'MS'],  pass_context=True)
async def _Ping(ctx):
    await ctx.channel.send(f"Your ping is __{round(Client.latency*500)}__ millisecond.")
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)

@Client.command(aliases = ['Ban'],  pass_context=True)
async def _Ban(ctx, Member: Union[discord.Member,discord.Object],*, Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Time = f'{current_Date}, {current_time}'


    
    Selected_Code = "SELECT Thing FROM Strike_Code"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    for record in records:
        Number = Number + 1
    Number = Number + 1
    Type = 'Ban'
    Code1 = random.randint(0,999999999999999999)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    User = await Client.fetch_user(Member.id) 

    if In_Group == True or ctx.author.guild_permissions.administrator:
        await RoleChecker(ctx, Member)
        Result = await RoleChecker(ctx, Member)
        In_Group2 = Result
        if In_Group2==True:
            await MissingPermission(ctx, ctx.author)
        else:
            print(User)
            Embed = discord.Embed(title="Ban System")
            Embed.add_field(name=f'__**{User}**__ was banned successfuly because of: ', value=f'{Reason}', inline=False)
            Embed.set_author(name=f'{User} ({User.id})', icon_url=User.avatar.url)
            Embed.set_thumbnail(url=User.avatar.url)
            Embed.set_footer(text=f'Banned by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await ctx.channel.send(embed=Embed)

            await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await ctx.guild.ban(User, reason=Reason)
    else:
        await MissingPermission(ctx, ctx.author)

@Client.command(aliases = ['Appeal'],  pass_context=True)
async def _Appeal(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Preview_Buttons = [
        [
        Button(style=ButtonStyle.red, label='Reject', custom_id='Reject'),
        Button(style=ButtonStyle.green, label='Accept', custom_id='Accept'),
        ]
    ]
    Report_Buttons = [
        [
        Button(style=ButtonStyle.green, label='In-Game', custom_id='In-Game'),
        Button(style=ButtonStyle.green, label='Discord', custom_id='Discord'),
        Button(style=ButtonStyle.red, label='Others', custom_id='Others'),
        ]
    ]
    Final_Buttons = [
        [
        Button(style=ButtonStyle.gray, label='Claim', custom_id='Claim'),
        Button(style=ButtonStyle.blue , label='Edit', custom_id='Note'),
        Button(style=ButtonStyle.green, label='Approve', custom_id='Approve'),
        Button(style=ButtonStyle.red, label='Revoke', custom_id='Revoke'),
        ]
    ]
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")

    Selected_Code = "SELECT Ticket FROM Appeal_Logs"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    for record in records:
        Number = Number + 1
    Number = Number + 1
    Code = random.randint(0,999999999999999999)

    Message = discord.Embed(title="Appeal System", description='Please check your DMs for further information.', color=0x546e7a)
    Message.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Message.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    Message.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Message)

    Main = discord.Embed(title="**Appeal System**", description=f"Please reply with your appeal. Please provide **images/videos** to support your appeal.", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar.url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    await ctx.author.send(embed=Main)
    Report = await Client.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Appeal System**", description=f"Appeal cancelled, please recreate your appeal and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar.url)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        Cancelled.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        Type = discord.Embed(title="Appeal Type", description='Please select the appeal type you want to make.', color=0x546e7a)
        Type.add_field(name='Please provide `Full Report`, `Evidence`,`User id`', value='Valid User Id: 565558626048016395/<@565558626048016395>', inline=False)
        Type.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Type.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        Type.set_thumbnail(url=ctx.author.avatar.url)
        Type.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)

        msg = await ctx.author.send(components=Report_Buttons,embed=Type)
        

        Interaction = await Client.wait_for("button_click", timeout=60) #check=lambda inter: inter.message.id == msg.id)

        if Interaction and Interaction.message.id == msg.id:
            TypeInteraction = Interaction.custom_id
            Report_Embed = discord.Embed(title="Appeal System Preview", description=f'Appeal Type: {TypeInteraction}', color=0xe91e63)
            Report_Embed.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
            Report_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Report_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Report_Embed.add_field(name='Note: ', value='If you do not get a response from a Moderator/Administrator within 48 hours please re-post a appeal.', inline=False)
            Report_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            Report_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Report_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Interaction.disable_components()
            await msg.edit(embed=Report_Embed, components=Preview_Buttons)
            Preview_Interaction = await Client.wait_for("button_click", timeout=60)
            if Preview_Interaction.custom_id == "Accept" and Preview_Interaction.message.id == msg.id:
                Text = None
                database.execute("INSERT INTO Appeal_Logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Channel = Client.get_channel(704274570143858758)
                Channel2 = Client.get_channel(925539281517297674)
                Final_Embed = discord.Embed(title="Appeal System", description=f'Appeal Type: {TypeInteraction}', color=0x546e7a)
                Final_Embed.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
                Final_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
                Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                CurrentType = "None"
                await Preview_Interaction.disable_components()
                await ctx.author.send(embed=Final_Embed)
                await msg.delete()
                Main_Report = await Channel.send(embed=Final_Embed, components=Final_Buttons)
                while True:
                    Main_Interaction = await Client.wait_for("button_click", timeout=31556926)
                    if Main_Interaction.custom_id == 'Revoke' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Close"
                        Closed_Embed = discord.Embed(title=f"Appeal Revoked by {Main_Interaction.user}", description=f'Appeal Type: {TypeInteraction}', color=0xe74c3c)
                        Closed_Embed.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                        Closed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Closed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Closed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Closed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Closed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Closed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Report.edit(embed=Closed_Embed)
                        await Main_Interaction.disable_components()
                        await Main_Report.delete()
                        await Channel2.send(embed=Closed_Embed)
                    elif Main_Interaction.custom_id == 'Approve' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Claim"
                        Approved_Embed = discord.Embed(title=f"Appeal Approved by {Main_Interaction.user}", description=f'Appeal Type: {TypeInteraction}', color=0x00ff00)
                        Approved_Embed.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                        Approved_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Approved_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Approved_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Approved_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Approved_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Approved_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Report.edit(embed=Approved_Embed)
                        await Main_Interaction.disable_components()
                        await Main_Report.delete()
                        await Channel2.send(embed=Approved_Embed)
                    elif Main_Interaction.custom_id == 'Claim' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Claim"
                        Claimed_Embed = discord.Embed(title=f"Appeal Claimed by {Main_Interaction.user}", description=f'Appeal Type: {TypeInteraction}', color=0xe67e22)
                        Claimed_Embed.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                        Claimed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Claimed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Claimed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Claimed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Claimed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Claimed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Interaction.edit_origin(embed=Claimed_Embed)    
                    elif Main_Interaction.custom_id == 'Note' and Main_Interaction.message.id == Main_Report.id:
                        Note = discord.Embed(title="Appeal System", description=f'Please reply with your note for this appeal.', color=0x546e7a)
                        Note.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Note.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Note.set_thumbnail(url=ctx.author.avatar.url)
                        Note.set_footer(text=f'Requested by {Main_Interaction.user}.', icon_url=ctx.author.avatar.url)
                        await Main_Interaction.user.send(embed=Note)
                        await Main_Interaction.edit_origin(embed=Final_Embed)
                        NoteMsg = await Client.wait_for('message', check=lambda message: message.author.id == Main_Interaction.user.id)
                        if isinstance(NoteMsg.channel, discord.channel.TextChannel):
                            Cancelled2 = discord.Embed(title="**Appeal System**", description=f"Note cancelled, plase click back on note to create a new one.", color=0xe74c3c)
                            Cancelled2.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                            Cancelled2.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar.url)
                            Cancelled2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                            Cancelled2.set_thumbnail(url=ctx.author.avatar.url)
                            await Main_Interaction.user.send(embed=Cancelled2)
                        elif isinstance(NoteMsg.channel, discord.channel.DMChannel):
                            Text = NoteMsg.content
                            if CurrentType == "Close" and Main_Interaction.message.id == Main_Report.id:
                                Closed_Embed.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                await Main_Interaction.user.send(embed=Closed_Embed)
                                await Main_Report.edit(embed=Closed_Embed)
                            elif CurrentType == "Claim" and Main_Interaction.message.id == Main_Report.id:
                                Claimed_Embed1 = discord.Embed(title=f"Appeal Claimed by {Main_Interaction.user}", description=f'Appeal Type: {TypeInteraction}', color=0xe67e22)
                                Claimed_Embed1.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                                Claimed_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Claimed_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Claimed_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Claimed_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                                Claimed_Embed1.set_thumbnail(url=ctx.author.avatar.url)
                                Claimed_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)                                
                                await Main_Interaction.user.send(embed=Claimed_Embed1)
                                await Main_Report.edit(embed=Claimed_Embed1)
                            elif CurrentType == "None" and Main_Interaction.message.id == Main_Report.id:
                                Final_Embed1 = discord.Embed(title="Appeal System", description=f'Appeal Type: {TypeInteraction}', color=0x546e7a)
                                Final_Embed1.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                                Final_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Final_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Final_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Final_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                                Final_Embed1.set_thumbnail(url=ctx.author.avatar.url)
                                Final_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                                await Main_Interaction.user.send(embed=Final_Embed1)
                                await Main_Report.edit(embed=Final_Embed1)
            elif Preview_Interaction.custom_id == "Reject" and Preview_Interaction.message.id == msg.id:
                Rejected = discord.Embed(title=f"Appeal Closed by {Preview_Interaction.user.id}", description=f'Appeal Type: {Interaction.custom_id}', color=0xe74c3c)
                Rejected.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                Rejected.add_field(name='Report: ', value=Report.content, inline=False)
                Rejected.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Rejected.add_field(name='Note: ', value='Your appeal was closed.', inline=False)
                Rejected.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Rejected.set_thumbnail(url=ctx.author.avatar.url)
                Rejected.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await Preview_Interaction.disable_components()
                await msg.edit(embed=Rejected)
    

@Client.command(aliases = ['Version'],  pass_context=True)
async def _Version(ctx):
    await ctx.channel.send(f"The bot is version 0.1.9.4 Alpha.")
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)


@Client.command(aliases = ['Warn', 'Strike', 'Infract'],  pass_context=True)
async def _Warn(ctx, Member: discord.Member, *, Reason):

    Revoke_Buttons = [
        [
        Button(style=ButtonStyle.red, label='Revoke', custom_id='Revoke'),
        ]
    ] 

    Selected_Code = "SELECT Thing FROM Strike_Code"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    for record in records:
        Number = Number + 1
    Number = Number + 1
    Type = 'Warning'
    Code1 = random.randint(0,999999999999999999)

    In_Group = False
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    Channel = Client.get_channel(704274108283748373)
    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, Member, Reason, ctx.channel)
        Main = discord.Embed(title="**Infraction System**", description=f"Warned <@{Member.id}> successfully.")
        Main.add_field(name='Reason: ', value=f'__{Reason}__', inline=False)
        Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)

        
        User = discord.Embed(title="**Infraction System**", description=f"You've received a warning.")
        User.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
        User.add_field(name='Reason: ', value=f'__{Reason}__', inline=False)
        User.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        User.set_author(name=f'{Member} ({Member.id})', icon_url=Member.avatar.url)

        Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> warned <@{Member.id}>.")
        Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
        Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
        Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
        Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=Main)
        Msg = await Channel.send(components=Revoke_Buttons, embed=Infraction)
        database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Reason, Date, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Reason,f'{current_Date}, {current_time}', Type))
        database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
        Database.commit()


        while True:
            Interaction = await Client.wait_for("button_click")
                
            if Interaction and Interaction.message.id == Msg.id:
                Infraction1 = discord.Embed(title="**Infraction System**", description=f"Infraction was revoked by {Interaction.user}.", color=0x992d22)
                Infraction1.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
                Infraction1.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
                Infraction1.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
                await Msg.edit(embed=Infraction1)
                await Interaction.disable_components()

        

    else:
        await MissingPermission(ctx, ctx.author)



@Client.command(aliases = ['Clearwarnings', 'Clr', 'Clear'],  pass_context=True)
async def _ClearWarnings(ctx, Member: discord.Member, *, Reason):
    
    Selected_Code = "SELECT UserID FROM Warning_Logs"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    Type = 'Clear Warnings'
    Code1 = random.randint(0,999999999999999999)

    In_Group = False
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, Member, Reason, ctx.channel)
        Main = discord.Embed(title="**Infraction System**", description=f"Cleared <@{Member.id}>'s warning logs.")
        Main.add_field(name='Reason: ', value=f'__{Reason}__', inline=False)
        Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=Main)
        for record in records:
            database.execute("DELETE FROM Warning_Logs WHERE UserID=?", (Member.id,))


@Client.command(aliases = ['U', 'User', 'UserInfo'],  pass_context=True)
async def _User(ctx, Member: Union[discord.Member,discord.Object]):
    User = await Client.fetch_user(Member.id)
    User = "SELECT UserID FROM Users WHERE UserID = %d" % Member.id
    Time = "SELECT Time FROM Users WHERE UserID = %d" % Member.id
    Cursor.execute(User)
    records = Cursor.fetchall()
    Cursor.execute(Time)
    records1 = Cursor.fetchall()
    records0 = ["N/A"]
    for record in records:
        pass
    for records0 in records1:
        pass
    User_Edited = f"[{records}]"
    In_Group = False
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    print(records0)

    if In_Group == True or ctx.author.guild_permissions.administrator:
        MemberTag = await Client.fetch_user(Member.id)
        await Logging(ctx, ctx.message.content,ctx.author, MemberTag, None, ctx.channel)
        Main = discord.Embed(title="**Information System**", description=f"Information on <@{Member.id}>")
        Main.add_field(name='Discord: ', value=f'''
User Id: {Member.id}
User Tag: {MemberTag}
User: <@{Member.id}>
Status: {Member.activity}
Nickname: {Member.display_name}
Joined: {Member.joined_at} UCT
Created at: {Member.created_at}
''', inline=False)

        Main.set_author(name=f'{Member.id}', icon_url=MemberTag.avatar.url)
        Main.set_image(url=MemberTag.avatar.url)
        await ctx.channel.send(embed=Main)
    else:
        await MissingPermission(ctx, ctx.author)


@Client.command(aliases = ['Case'], pass_context=True)
async def _Case(ctx, Code):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Code Case reviewd: {Code}", ctx.channel)
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        Cursor.execute("SELECT UserID FROM Warning_Logs WHERE Code=?", [Code])
        records = Cursor.fetchall()
        Cursor.execute("SELECT Administrator FROM Warning_Logs WHERE Code=?", [Code])
        records2 = Cursor.fetchall()
        Cursor.execute("SELECT Type FROM Warning_Logs WHERE Code=?", [Code])
        records3 = Cursor.fetchall()
        Cursor.execute("SELECT Reason FROM Warning_Logs WHERE Code=?", [Code])
        records4 = Cursor.fetchall()
        Cursor.execute("SELECT Date FROM Warning_Logs WHERE Code=?", [Code])
        records5 = Cursor.fetchall()
        for record4 in records5:
            pass
        for record3 in records4:
            pass
        for record in records:
            pass
        for record1 in records2:
            pass
        for record2 in records3:
            pass
        

        Final_Embed = discord.Embed(title="Case System", description=f'Case Type: {record2[0]}', color=0x546e7a)
        Final_Embed.add_field(name=f'Code:', value=Code,inline=False)
        Final_Embed.add_field(name=f'Infracted:',value=f'<@{record[0]}>',inline=False)
        Final_Embed.add_field(name=f'Infracted for:',value=record3[0] , inline=False)
        Final_Embed.add_field(name=f'Infracted by:',value=f'<@{record1[0]}>', inline=False)
        Final_Embed.add_field(name='Date: ', value=f'{record4[0]}', inline=False)
        Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=Final_Embed)



@Client.command(aliases = ['Rule', 'Rules'], pass_context=True)
async def _Rule(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Main2 = discord.Embed(title="**Rules**", description=f"All further information was directed into your Direct Messages/DMs.", color=0x7289da)
    Main2.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Main2)

    Main = discord.Embed(title="**__Rules__**", description=f"All rules must be followed at all times. Not doing so will result in any type of punishments.", color = 0x9b59b6)
    Main.add_field(name='Rules: ', value=f'''


`+` 1. All chat rooms are to remain clean. __(No dramas, no toxicity, no fights, no arguments)__

`+` 2. You are to respect yourself and those with you.

`+` 3. __Toxicity__ shall not be tolerated in any form.

`+` 4. __Harassment__ shall not be tolerated.

`+` 5. __Leaking__ any **personal information** is not tolerated, and will lead to your removal **permanently**.

`+` 6. Make sure to use each text chat for their correct purpose.

`+` 7. Don’t “ @ “ someone without a good reason, the majority of people dislike being ‘pinged’.

`+` 9. __Blackmail__ and threats will not be tolerated, punishments will be held against you.

`+` 10. __Swearing__ is allowed but do not do it excessively or use it to offend or insult someone.

`+` 11. Do not __spam__ in any channel or mic spam in any VC.

`+` 12. Refrain from using __sexual remarks__ (sexual joking, sexual comments etc...)

`+` 13. All commands used should be used in its right [channels](https://discord.com/channels/697064724893794314/704653260333645844)

''', inline=False)
    Main.set_image(url="https://media.discordapp.net/attachments/843439250817286164/925560535230062632/DevLogo2.0.png?width=169&height=169")
    await ctx.author.send(embed=Main)


@Client.command(aliases = ['Lock', 'LockChannel'], pass_context=True)
async def _Lock(ctx, Channel: discord.TextChannel, Amount: int, *,Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Time = f'{current_Date}, {current_time}'
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        if Amount <=9:
            Close_Embed = discord.Embed(title="Lock System", description=f'The minutes picked is too short, please use 10 seconds or more.', color=0xe67e22)
            Close_Embed.set_footer(text=f'You should contact a system developer if you think this is a mistake.', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=Close_Embed)
        else:
            Final_Embed = discord.Embed(title="Lock System", description=f'<#{Channel.id}> was locked for {Amount} seconds.', color=0x546e7a)
            Final_Embed.set_footer(text=f'Locked by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, f"Affected channel is <#{Channel.id}> for {Amount} seconds with the reason: {Reason}", ctx.channel)
            overwrite = Channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await Channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await Channel.send(embed=Final_Embed)
            time.sleep(Amount)
            Embed = discord.Embed(title="Lock System", description=f'<#{Channel.id}> was unlocked.', color=0x546e7a)
            Embed.set_footer(text=f'Locked by {ctx.author}.', icon_url=ctx.author.avatar.url)
            overwrite2 = Channel.overwrites_for(ctx.guild.default_role)
            overwrite2.send_messages = True
            await Channel.set_permissions(ctx.guild.default_role, overwrite=overwrite2)
            await Channel.send(embed=Embed)
    else:
        await MissingPermission(ctx, ctx.author)



@Client.command(aliases = ['Unban'], pass_context=True)
async def _Unban(ctx, Member: Union[discord.Member,discord.Object],*,Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    User = await Client.fetch_user(Member.id) 
    Time = f'{current_Date}, {current_time}'

    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank

    if In_Group == True or ctx.author.guild_permissions.administrator:
        banned_members = await ctx.guild.bans()
        for ban_entry in banned_members:
            user = ban_entry.user
            if user.id == User.id:
                await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
                Embed = discord.Embed(title="Ban System")
                Embed.add_field(name=f'__**{User}**__ was unbanned successfuly with the reason: ', value=f'{Reason}', inline=False)
                Embed.set_author(name=f'{User} ({User.id})', icon_url=User.avatar.url)
                Embed.set_thumbnail(url=User.avatar.url)
                Embed.set_footer(text=f'Unbanned by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await ctx.channel.send(embed=Embed)
                await ctx.guild.unban(user)
                break
            elif User not in banned_members:
                Embed2 = discord.Embed(title="Ban System")
                Embed2.add_field(name=f'__**{User}**__ can not be unbanned because he wasn not banned in the first place.', value=f'{Reason}', inline=False)
                Embed2.set_author(name=f'{User} ({User.id})', icon_url=User.avatar.url)
                Embed2.set_thumbnail(url=User.avatar.url)
                Embed2.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await ctx.channel.send(embed=Embed2)
                break
    else:
        await MissingPermission(ctx, ctx.author)

@Client.command(aliases = ['Nick', 'Nickname', 'Name'], pass_context=True)
async def _Nick(ctx, Member: Union[discord.Member,discord.Object],*,Nick):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    User = await Client.fetch_user(Member.id) 
    Time = f'{current_Date}, {current_time}'

    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank

    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, User, f'Nickname is now changed to: {Nick}', ctx.channel)
        await Member.edit(nick=Nick)
        Embed = discord.Embed(title="Nickname System")
        Embed.add_field(name=f'__**{User}**__ username was successfuly changed to ', value=f'{Nick}', inline=False)
        Embed.set_author(name=f'{User} ({User.id})', icon_url=User.avatar.url)
        Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=Embed)
    else:
        await MissingPermission(ctx, ctx.author)


@Client.command(aliases = ['Softban', 'Sb','Sban'],  pass_context=True)
async def _SoftBan(ctx, Member: Union[discord.Member,discord.Object],*, Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Time = f'{current_Date}, {current_time}'


    
    Selected_Code = "SELECT Thing FROM Strike_Code"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    for record in records:
        Number = Number + 1
    Number = Number + 1
    Type = 'Soft Ban'
    Code1 = random.randint(0,999999999999999999)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    User = await Client.fetch_user(Member.id) 

    if In_Group == True or ctx.author.guild_permissions.administrator:
        await RoleChecker(ctx, Member)
        Result = await RoleChecker(ctx, Member)
        In_Group2 = Result
        if In_Group2==True:
            await MissingPermission(ctx, ctx.author)
        else:
            Embed = discord.Embed(title="Soft Ban System")
            Embed.add_field(name=f'__**{User}**__ was soft banned successfuly for: ', value=f'{Reason}', inline=False)
            Embed.set_author(name=f'{User} ({User.id})', icon_url=User.avatar.url)
            Embed.set_thumbnail(url=User.avatar.url)
            Embed.set_footer(text=f'Soft Banned by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await ctx.channel.send(embed=Embed)

            await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await ctx.guild.ban(User,reason=Reason, delete_message_days=7)
            await ctx.guild.unban(User)
    else:
        await MissingPermission(ctx, ctx.author)


@Client.command(aliases = ['ServerInfo', 'Sinfo'],  pass_context=True)
async def _ServerInfo(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Number2 = 1
    Number3 = 1
    for Channels in ctx.guild.channels:
        Number2 = Number2 + 1
    for Roles in ctx.guild.roles:
        Number3 = Number3 + 1
    Embed = discord.Embed(title="Server Information")
    Embed.add_field(name=f'Server is owned by: ', value=f'{ctx.guild.owner}/{ctx.guild.owner_id}/<@{ctx.guild.owner_id}>', inline=False)
    Embed.add_field(name=f'The server region is: ', value=f'{ctx.guild.region}', inline=False)
    Embed.add_field(name=f'The server description: ', value=f'{ctx.guild.description}', inline=False)
    Embed.add_field(name=f'The server Creation Date: ', value=f'{ctx.guild.created_at}', inline=False)
    Embed.add_field(name=f'The server default notifications: ', value=f'{ctx.guild.default_notifications}', inline=False)
    Embed.add_field(name=f'Amount of members in the guild: ', value=f'{ctx.guild.member_count}', inline=False)
    Embed.add_field(name=f'Amount of channels in the guild: ', value=f'{Number2}', inline=False)
    Embed.add_field(name=f'Amount of roles in the guild: ', value=f'{Number3}', inline=False)
    Embed.add_field(name=f'The server max presences: ', value=f'{ctx.guild.max_presences}', inline=False)
    Embed.add_field(name=f'The server verification level: ', value=f'{ctx.guild.verification_level}', inline=False)
    Embed.add_field(name=f'The server AFK channel is: ', value=f'{ctx.guild.afk_channel}', inline=False)
    Embed.set_author(name=f'{ctx.guild.name} ({ctx.guild.id})', icon_url=ctx.guild.icon_url)
    Embed.set_thumbnail(url=ctx.guild.icon_url)
    Embed.set_footer(text=f'Requested {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Embed)


@Client.command(aliases = ['Rps'],  pass_context=True)
async def _RPS(ctx):
    Number = random.randint(1,3)
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    if Number == 1:
        await ctx.send('Rock')
    elif Number == 2:
        await ctx.send('Paper')
    elif Number == 3:
        await ctx.send('Scissors')

@Client.command(aliases = ['RandomNumber', 'Rn', 'RandomN'],  pass_context=True)
async def _RandomNumber(ctx, First_Number: int, Second_Number:int):
    if First_Number >= Second_Number:
        await ctx.send('First number should be less than the second number, e.g: 1 to 6')
    else:
        Number = random.randint(First_Number,Second_Number)
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F'Random number: {Number}', ctx.channel)
        await ctx.send(Number)
    

@Client.command(aliases = ['Deaf', 'VoiceDeafen', 'Deafen'], pass_context=True)
async def _Deafen(ctx, Member: Union[discord.Member,discord.Object], *,Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Time = f'{current_Date}, {current_time}'
    Code1 = random.randint(0,999999999999999999)
    Type = 'Deafen'
    Selected_Code = "SELECT Thing FROM Strike_Code"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    User = await Client.fetch_user(Member.id)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank

    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
        Embed = discord.Embed(title="Deafen System")
        Embed.add_field(name=f'__**{Member}**__ was successfuly voice deafened and muted.', value=f'Reason: {Reason}', inline=False)
        Embed.set_author(name=f'{Member} ({Member.id})', icon_url=User.avatar.url)
        Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
        database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
        database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
        await ctx.send(embed=Embed)
        await Member.edit(deafen = True)
        await Member.edit(mute = True)


@Client.command(aliases = ['Undeaf', 'UnVoiceDeafen', 'UnDeafen'], pass_context=True)
async def _Undeafen(ctx, Member: Union[discord.Member,discord.Object], *,Reason):
    User = await Client.fetch_user(Member.id)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank

    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
        Embed = discord.Embed(title="Deafen System")
        Embed.add_field(name=f'__**{Member}**__ was successfuly voice undeafened and unmuted.',value=f'Reason: {Reason}', inline=False)
        Embed.set_author(name=f'{Member} ({Member.id})', icon_url=User.avatar.url)
        Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=Embed)
        await Member.edit(deafen = False)
        await Member.edit(mute = False)





@Client.command(aliases = ['Post'],  pass_context=True)
async def _Post(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Preview_Buttons = [
        [
        Button(style=ButtonStyle.red, label='Reject', custom_id='Reject'),
        Button(style=ButtonStyle.green, label='Accept', custom_id='Accept'),
        ]
    ]
    Report_Buttons = [
        [
        Button(style=ButtonStyle.green, label='Sound Editing', custom_id='Sound Editing'),
        Button(style=ButtonStyle.green, label='3D Modeller', custom_id='3D Modeller'),
        Button(style=ButtonStyle.green, label='2D Modeller', custom_id='2D Modeller'),
        Button(style=ButtonStyle.red, label='Others', custom_id='Others'),
        ],
        [
        Button(style=ButtonStyle.green, label='Programming', custom_id='Programming'),
        Button(style=ButtonStyle.green, label='Building', custom_id='Building'),
        Button(style=ButtonStyle.green, label='Interface', custom_id='Interface'),
        Button(style=ButtonStyle.green, label='Scripting', custom_id='Scripting'),
        ]
    ]
    Final_Buttons = [
        [
        Button(style=ButtonStyle.gray, label='Claim', custom_id='Claim'),
        Button(style=ButtonStyle.green, label='Approve', custom_id='Approve'),
        Button(style=ButtonStyle.red, label='Revoke', custom_id='Revoke'),
        ]
    ]
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")

    Code = random.randint(0,999999999999999999)

    Message = discord.Embed(title="Market System", description='Please check your DMs for further information.', color=0x546e7a)
    Message.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Message.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    Message.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Message)

    Main = discord.Embed(title="**Market System**", description=f"Please reply with your post. Please provide **images/videos** to support your post.", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Market by {ctx.author}.', icon_url=ctx.author.avatar.url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    await ctx.author.send(embed=Main)
    Report = await Client.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Market System**", description=f"Market cancelled, please recreate your post and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_footer(text=f'Market by {ctx.author}.', icon_url=ctx.author.avatar.url)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        Cancelled.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        Type = discord.Embed(title="Marketplace post Type", description='Please select the Marketplace post type you want to make.', color=0x546e7a)
        Type.add_field(name='Please provide `Full post`, `Evidence`,`User id`', value='Valid User Id: 565558626048016395/<@565558626048016395>', inline=False)
        Type.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Type.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        Type.set_thumbnail(url=ctx.author.avatar.url)
        Type.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)

        msg = await ctx.author.send(components=Report_Buttons,embed=Type)
        

        Interaction = await Client.wait_for("button_click", timeout=60) #check=lambda inter: inter.message.id == msg.id)

        if Interaction and Interaction.message.id == msg.id:

            TypeInteraction = Interaction.custom_id
            Report_Embed = discord.Embed(title="Market System Preview", description=f'Market Type: {TypeInteraction}', color=0xe91e63)
            Report_Embed.add_field(name='Market Code: ', value=f'#{Code}', inline=False)
            Report_Embed.add_field(name='Post: ', value=Report.content, inline=False)
            Report_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Report_Embed.add_field(name='Note: ', value='If you do not get a response from a Moderator/Administrator within 48 hours please re-post a appeal.', inline=False)
            Report_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            Report_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Report_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Interaction.disable_components()
            await msg.edit(embed=Report_Embed, components=Preview_Buttons)
            Preview_Interaction = await Client.wait_for("button_click", timeout=60)
            if Preview_Interaction.custom_id == "Accept" and Preview_Interaction.message.id == msg.id:
                Text = None
                Channel = Client.get_channel(925540050186403860)
                Channel2 = Client.get_channel(925539281517297674)
                Final_Embed = discord.Embed(title="Market System", description=f'Market Type: {TypeInteraction}', color=0x546e7a)
                Final_Embed.add_field(name='Market Code: ', value=f'#{Code}', inline=False)
                Final_Embed.add_field(name='Post: ', value=Report.content, inline=False)
                Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
                Final_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
                Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                CurrentType = "None"
                await Preview_Interaction.disable_components()
                await ctx.author.send(embed=Final_Embed)
                await msg.delete()
                Main_Report = await Channel.send(embed=Final_Embed, components=Final_Buttons)
                while True:
                    Main_Interaction = await Client.wait_for("button_click", timeout=31556926)
                    if Main_Interaction.custom_id == 'Revoke' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Close"
                        Closed_Embed = discord.Embed(title=f"Market Revoked by {Main_Interaction.user}", description=f'Post Type: {TypeInteraction}', color=0xe74c3c)
                        Closed_Embed.add_field(name='Market Code: ', value=f'#{Code}', inline=False)
                        Closed_Embed.add_field(name='Post: ', value=Report.content, inline=False)
                        Closed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Closed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Closed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Closed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Closed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Report.edit(embed=Closed_Embed)
                        await Main_Interaction.disable_components()
                        await Main_Report.delete()
                        await Channel2.send(embed=Closed_Embed)
                    elif Main_Interaction.custom_id == 'Approve' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Claim"
                        Approved_Embed = discord.Embed(title=f"Market Approved by {Main_Interaction.user}", description=f'Post Type: {TypeInteraction}', color=0x00ff00)
                        Approved_Embed.add_field(name='Market Code: ', value=f'#{Code}', inline=False)
                        Approved_Embed.add_field(name='Post: ', value=Report.content, inline=False)
                        Approved_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Approved_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Approved_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Approved_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Approved_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)

                        Post_Embed = discord.Embed(title=f"Market Post by {ctx.author}/({ctx.author.id})", description=f'Post Type: {TypeInteraction}')
                        Post_Embed.add_field(name='Post: ', value=Report.content, inline=False)
                        Post_Embed.add_field(name='Contact Information: ', value=f'<@{ctx.author.id}>', inline=False)
                        Post_Embed.add_field(name='Payment Type: ', value=f'Upon completion', inline=False)
                        Post_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Post_Embed.set_footer(text=f'Approved by {Main_Interaction.user} ({Main_Interaction.user.id})', icon_url=Main_Interaction.user.avatar.url )


                        await Main_Report.edit(embed=Approved_Embed)
                        await Main_Interaction.disable_components()
                        await Main_Report.delete()
                        await Channel2.send(embed=Approved_Embed)
                        if TypeInteraction == "Sound Editing":
                            Channel3 = Client.get_channel(925542713808539678)
                            await Channel3.send(embed=Post_Embed)
                        elif TypeInteraction == "3D Modeller":
                            Channel3 = Client.get_channel(925542908772364359)
                            await Channel3.send(embed=Post_Embed)
                        elif TypeInteraction == "2D Modeller":
                            Channel3 = Client.get_channel(925542880985112648)
                            await Channel3.send(embed=Post_Embed)
                        elif TypeInteraction == "Programming":
                            Channel3 = Client.get_channel(925542611450748998)
                            await Channel3.send(embed=Post_Embed)
                        elif TypeInteraction == "Scripting":
                            Channel3 = Client.get_channel(925542639615500299)
                            await Channel3.send(embed=Post_Embed)
                        elif TypeInteraction == "Building":
                            Channel3 = Client.get_channel(925542683693441074)
                            await Channel3.send(embed=Post_Embed)
                        elif TypeInteraction == "Others":
                            Channel3 = Client.get_channel(925543049763913779)
                            await Channel3.send(embed=Post_Embed)
                        elif TypeInteraction == "Interface":
                            Channel3 = Client.get_channel(925542562377371719)
                            await Channel3.send(embed=Post_Embed)
                        
                    elif Main_Interaction.custom_id == 'Claim' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Claim"
                        Claimed_Embed = discord.Embed(title=f"Appeal Claimed by {Main_Interaction.user}", description=f'Post Type: {TypeInteraction}', color=0xe67e22)
                        Claimed_Embed.add_field(name='Appeal Code: ', value=f'#{Code}', inline=False)
                        Claimed_Embed.add_field(name='Post: ', value=Report.content, inline=False)
                        Claimed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Claimed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Claimed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Claimed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Claimed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Interaction.edit_origin(embed=Claimed_Embed)    
            elif Preview_Interaction.custom_id == "Reject" and Preview_Interaction.message.id == msg.id:
                Rejected = discord.Embed(title=f"Appeal Closed by {Preview_Interaction.user.id}", description=f'Post Type: {Interaction.custom_id}', color=0xe74c3c)
                Rejected.add_field(name='Appeal Code: ', value=f'#{Code}', inline=False)
                Rejected.add_field(name='Post: ', value=Report.content, inline=False)
                Rejected.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Rejected.add_field(name='Note: ', value='Your appeal was closed.', inline=False)
                Rejected.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Rejected.set_thumbnail(url=ctx.author.avatar.url)
                Rejected.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await Preview_Interaction.disable_components()
                await msg.edit(embed=Rejected)


@Client.command(aliases = ['Application', 'Apply'],  pass_context=True)
async def _Application(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Preview_Buttons = [
        [
        Button(style=ButtonStyle.red, label='Reject', custom_id='Reject'),
        Button(style=ButtonStyle.green, label='Accept', custom_id='Accept'),
        ]
    ]
    Report_Buttons = [
        [
        Button(style=ButtonStyle.green, label='Visual Effects', custom_id='Visual Effects'),
        Button(style=ButtonStyle.red, label='Content Creator', custom_id='Content Creator'),
        Button(style=ButtonStyle.green, label='2D Graphics', custom_id='2D Graphics'),
        Button(style=ButtonStyle.green, label='3D Graphics', custom_id='3D Graphics'),
        ],
        [
        Button(style=ButtonStyle.green, label='Sound Editing', custom_id='Sound Editing'),
        Button(style=ButtonStyle.green, label='Animator', custom_id='Animator'),
        Button(style=ButtonStyle.green, label='Terrain builder', custom_id='Terrain builder'),
        Button(style=ButtonStyle.red, label='Tester', custom_id='Tester'),
        ],
        [
        Button(style=ButtonStyle.green, label='Plot writer', custom_id='Plot writer'),
        Button(style=ButtonStyle.green, label='Interface Designer', custom_id='Interface Designer'),
        Button(style=ButtonStyle.green, label='Modeller', custom_id='Modeller'),
        Button(style=ButtonStyle.green, label='Voice Actor', custom_id='Voice Actor'),
        ],
        [
        Button(style=ButtonStyle.green, label='Builder', custom_id='Builder'),
        Button(style=ButtonStyle.green, label='Programmer', custom_id='Programmer'),
        Button(style=ButtonStyle.green, label='Music Composer', custom_id='Music Composer'),
        Button(style=ButtonStyle.green, label='Clothing', custom_id='Clothing'),
        ]
    ]
    Final_Buttons = [
        [
        Button(style=ButtonStyle.gray, label='Claim', custom_id='Claim'),
        Button(style=ButtonStyle.blue , label='Edit', custom_id='Note'),
        Button(style=ButtonStyle.green, label='Approve', custom_id='Approve'),
        Button(style=ButtonStyle.red, label='Revoke', custom_id='Revoke'),
        ]
    ]
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")

    Selected_Code = "SELECT Application FROM Appliaction_Logs"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    Number = 0
    for record in records:
        Number = Number + 1
    Number = Number + 1
    Code = random.randint(0,999999999999999999)

    Message = discord.Embed(title="Application System", description='Please check your DMs for further information.', color=0x546e7a)
    Message.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Message.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    Message.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Message)

    Main = discord.Embed(title="**Application System**", description=f"Please reply with your Application. Please provide **images/videos** of your portfolio to support your Application.", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Application by {ctx.author}.', icon_url=ctx.author.avatar.url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    await ctx.author.send(embed=Main)
    Report = await Client.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Application System**", description=f"Application cancelled, please recreate your Application and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_footer(text=f'Application by {ctx.author}.', icon_url=ctx.author.avatar.url)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        Cancelled.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        Type = discord.Embed(title="Application Type", description='Please select the Application type you want to make.', color=0x546e7a)
        Type.add_field(name='Please provide `Full Report`, `Evidence`,`User id`', value='Valid User Id: 565558626048016395/<@565558626048016395>', inline=False)
        Type.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Type.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        Type.set_thumbnail(url=ctx.author.avatar.url)
        Type.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)

        msg = await ctx.author.send(components=Report_Buttons,embed=Type)
        

        Interaction = await Client.wait_for("button_click", timeout=60) #check=lambda inter: inter.message.id == msg.id)

        if Interaction and Interaction.message.id == msg.id:
            TypeInteraction = Interaction.custom_id
            Report_Embed = discord.Embed(title="Application System Preview", description=f'Application Type: {TypeInteraction}', color=0xe91e63)
            Report_Embed.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
            Report_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Report_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Report_Embed.add_field(name='Note: ', value='If you do not get a response from a Moderator/Administrator within 48 hours please re-post a Application.', inline=False)
            Report_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            Report_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Report_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Interaction.disable_components()
            await msg.edit(embed=Report_Embed, components=Preview_Buttons)
            Preview_Interaction = await Client.wait_for("button_click", timeout=60)
            if Preview_Interaction.custom_id == "Accept" and Preview_Interaction.message.id == msg.id:
                Text = None
                database.execute("INSERT INTO Appliaction_Logs (Application) VALUES (?)", (Text,))
                Database.commit()
                Channel = Client.get_channel(925539955428696064)
                Channel2 = Client.get_channel(925539281517297674)
                Final_Embed = discord.Embed(title="Application System", description=f'Application Type: {TypeInteraction}', color=0x546e7a)
                Final_Embed.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
                Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
                Final_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
                Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                CurrentType = "None"
                await Preview_Interaction.disable_components()
                await ctx.author.send(embed=Final_Embed)
                await msg.delete()
                Main_Report = await Channel.send(embed=Final_Embed, components=Final_Buttons)
                while True:
                    Main_Interaction = await Client.wait_for("button_click", timeout=31556926)
                    if Main_Interaction.custom_id == 'Revoke' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Close"
                        Closed_Embed = discord.Embed(title=f"Application Revoked by {Main_Interaction.user}", description=f'Application Type: {TypeInteraction}', color=0xe74c3c)
                        Closed_Embed.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
                        Closed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Closed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Closed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Closed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Closed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Closed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Report.edit(embed=Closed_Embed)
                        await Main_Interaction.disable_components()
                        await Main_Report.delete()
                        await ctx.author.send(embed=Closed_Embed)
                        await Channel2.send(embed=Closed_Embed)
                    elif Main_Interaction.custom_id == 'Approve' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Claim"
                        Approved_Embed = discord.Embed(title=f"Application Approved by {Main_Interaction.user}", description=f'Application Type: {TypeInteraction}', color=0x00ff00)
                        Approved_Embed.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
                        Approved_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Approved_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Approved_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Approved_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Approved_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Approved_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Report.edit(embed=Approved_Embed)
                        await Main_Interaction.disable_components()
                        await Main_Report.delete()
                        await ctx.author.send(embed=Approved_Embed)
                        await Channel2.send(embed=Approved_Embed)
                    elif Main_Interaction.custom_id == 'Claim' and Main_Interaction.message.id == Main_Report.id:
                        CurrentType = "Claim"
                        Claimed_Embed = discord.Embed(title=f"Application Claimed by {Main_Interaction.user}", description=f'Application Type: {TypeInteraction}', color=0xe67e22)
                        Claimed_Embed.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
                        Claimed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                        Claimed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Claimed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
                        Claimed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Claimed_Embed.set_thumbnail(url=ctx.author.avatar.url)
                        Claimed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                        await Main_Interaction.edit_origin(embed=Claimed_Embed)    
                    elif Main_Interaction.custom_id == 'Note' and Main_Interaction.message.id == Main_Report.id:
                        Note = discord.Embed(title="Application System", description=f'Please reply with your note for this Application.', color=0x546e7a)
                        Note.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Note.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                        Note.set_thumbnail(url=ctx.author.avatar.url)
                        Note.set_footer(text=f'Requested by {Main_Interaction.user}.', icon_url=ctx.author.avatar.url)
                        await Main_Interaction.user.send(embed=Note)
                        await Main_Interaction.edit_origin(embed=Final_Embed)
                        NoteMsg = await Client.wait_for('message', check=lambda message: message.author.id == Main_Interaction.user.id)
                        if isinstance(NoteMsg.channel, discord.channel.TextChannel):
                            Cancelled2 = discord.Embed(title="**Application System**", description=f"Note cancelled, plase click back on note to create a new one.", color=0xe74c3c)
                            Cancelled2.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                            Cancelled2.set_footer(text=f'Application by {ctx.author}.', icon_url=ctx.author.avatar.url)
                            Cancelled2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                            Cancelled2.set_thumbnail(url=ctx.author.avatar.url)
                            await Main_Interaction.user.send(embed=Cancelled2)
                        elif isinstance(NoteMsg.channel, discord.channel.DMChannel):
                            Text = NoteMsg.content
                            if CurrentType == "Close" and Main_Interaction.message.id == Main_Report.id:
                                Closed_Embed.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                await Main_Interaction.user.send(embed=Closed_Embed)
                                await Main_Report.edit(embed=Closed_Embed)
                            elif CurrentType == "Claim" and Main_Interaction.message.id == Main_Report.id:
                                Claimed_Embed1 = discord.Embed(title=f"Application Claimed by {Main_Interaction.user}", description=f'Application Type: {TypeInteraction}', color=0xe67e22)
                                Claimed_Embed1.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
                                Claimed_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Claimed_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Claimed_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Claimed_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                                Claimed_Embed1.set_thumbnail(url=ctx.author.avatar.url)
                                Claimed_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)                                
                                await Main_Interaction.user.send(embed=Claimed_Embed1)
                                await Main_Report.edit(embed=Claimed_Embed1)
                            elif CurrentType == "None" and Main_Interaction.message.id == Main_Report.id:
                                Final_Embed1 = discord.Embed(title="Application System", description=f'Application Type: {TypeInteraction}', color=0x546e7a)
                                Final_Embed1.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
                                Final_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Final_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Final_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Final_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                                Final_Embed1.set_thumbnail(url=ctx.author.avatar.url)
                                Final_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                                await Main_Interaction.user.send(embed=Final_Embed1)
                                await Main_Report.edit(embed=Final_Embed1)
            elif Preview_Interaction.custom_id == "Reject" and Preview_Interaction.message.id == msg.id:
                Rejected = discord.Embed(title=f"Application Closed by {Preview_Interaction.user.id}", description=f'Application Type: {Interaction.custom_id}', color=0xe74c3c)
                Rejected.add_field(name='Application Code: ', value=f'#{Number}/{Code}', inline=False)
                Rejected.add_field(name='Report: ', value=Report.content, inline=False)
                Rejected.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Rejected.add_field(name='Note: ', value='Your Application was closed.', inline=False)
                Rejected.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                Rejected.set_thumbnail(url=ctx.author.avatar.url)
                Rejected.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await Preview_Interaction.disable_components()
                await msg.edit(embed=Rejected)





@Client.command(aliases = ['Alert', 'ModReq'], pass_context=True)
async def _Alert(ctx, Channel_Location: discord.TextChannel,Message_Id:int): 
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    msg = await Channel_Location.fetch_message(Message_Id)
    Channel = Client.get_channel(927606540440076328)
    Message = discord.Embed(title="Moderation Alert", description='All active moderators, please handle the situation.', color=0x546e7a)
    Message.add_field(name='Message ID: ', value=f'`{Message_Id}`', inline=False)
    Message.add_field(name='Who wrote the message? ', value=f'`{msg.author}/`<@{msg.author.id}>', inline=False)
    Message.add_field(name='Who reported the message? ', value=f'`{ctx.author}/`<@{ctx.author.id}>', inline=False)
    Message.add_field(name='When? ', value=f'`{msg.created_at}`', inline=False)
    Message.add_field(name='Where? ', value=f'<#{Channel_Location.id}>', inline=False)
    Message.add_field(name='Date of the report: ', value=f'{current_time}, {current_Date}', inline=False)
    Message.add_field(name='Message:', value=f'''
```
{msg.content}
```
    ''', inline=False)
    await Channel.send("All active <@&792423903284822037>, please handle this situation", embed=Message)


Client.run('OTI1NTQ1MjkxNTMxMzA0OTYw.YcurOQ.u4NkEE8jgXhFEzBDs_mQEwIb-S4') 





# ODkxNjcyNzE0ODk5NzYzMjIw.YVBw7Q.PJ_8PKH3u4vgwm6uZvixO4bKZCQ

# OTA0NDUwODE0NjE2MTQxODI1.YX7tdg.f9kR32IFT7-AY9q2bm3qnkhEQt8


