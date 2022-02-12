from logging import fatal
from platform import python_version
from discord import Embed, __version__ as discord_version
from psutil import Process, virtual_memory
import datetime
from datetime import datetime, timedelta, date
import time
from time import time
from re import A
from sqlite3.dbapi2 import Cursor
import discord
import random
from typing import Final, Union
from discord import embeds
from discord import channel
from discord import member
from discord.enums import try_enum
from discord.errors import PrivilegedIntentsRequired
from discord.ext import commands
import asyncio
import certifi
import aiohttp
from sqlite3 import connect
import praw
import re
import string
import inspect
import json
import traceback
import sys
from collections import defaultdict
import discord.http, discord.state
from discord.utils import MISSING
from typing import Literal
import slash_util
import os


class MyBot(slash_util.Bot):
    def __init__(self):
        super().__init__(command_prefix=',',case_insensitive=True,intents=discord.Intents.all())  

        #for folder in os.listdir("modules"):
            #if os.path.exists(os.path.join("modules", folder, "cog.py")):
                #self.load_extension(f"modules.{folder}.cog") 
        self.load_extension(f"modules.message.cog") 


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
Blacklisted = []


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(','))

    async def on_ready(self):
        await Client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = " The Sith Order"))
        guild = Client.get_guild(900845173989339186)
        for black in Blacklisted:
            User = await Client.fetch_user(black)
            print(User)
            await guild.ban(User)
        for Member in guild.members:
            database.execute("INSERT INTO Users (UserID, Time) VALUES (?, ?)", (Member.id, "N/A"))
            Database.commit()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------------------------------')

@Client.event
async def on_ready():
    await Client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = " The Sith Order"))
    guild = Client.get_guild(900845173989339186)
    for black in Blacklisted:
        User = await Client.fetch_user(black)
        print(User)
        await guild.ban(User)
    for Member in guild.members:
        database.execute("INSERT INTO Users (UserID, Time) VALUES (?, ?)", (Member.id, "N/A"))
        Database.commit()
    print(f'Logged in')
    print('------------------------------')


bot = Bot()

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
    Channel = Client.get_channel(941411413468016760)
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

    guild = Client.get_guild(900845173989339186)
    role1 = [
        discord.utils.get(guild.roles, id=909918257312595968), 
        discord.utils.get(guild.roles, id=901486515249635388),
        discord.utils.get(guild.roles, id=905125340622508112),
        discord.utils.get(guild.roles, id=906498226931245056),
        discord.utils.get(guild.roles, id=901486515975229480),
        discord.utils.get(guild.roles, id=901486518915448902),
        discord.utils.get(guild.roles, id=901486518080786474),
        discord.utils.get(guild.roles, id=901486519552995348),
        discord.utils.get(guild.roles, id=901486517380345926),
    ]
    for Main in role1:
        for member in guild.members:
            if User == member:
                for role in member.roles: #or member.id =="565558626048016395":
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
    Channel = Client.get_channel(941411399597445252)
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

@Client.command(aliases = ['Ann', 'Announce'])
async def _announce(ctx, Channel: discord.TextChannel, Title, *,Annoncement):
    class Button(discord.ui.View):
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def Confirm(self, Confirm_Button: discord.ui.Button, interaction: discord.Interaction):        
            print('Working on it')
            Main = discord.Embed(color=0x2ecc71)
            Main.add_field(name=f'{Title}',value=Annoncement, inline=False)
            Main.set_author(name=f'Important Announcement', icon_url=ctx.author.avatar.url)
            Confirm_Button.disabled = True
            await Channel.send(embed=Main)
            await interaction.message.edit(view=self)
            print('Finished')

        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 

        
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    print(In_Group)
    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}>: __{Annoncement}__", ctx.channel)
        Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
        Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
        Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        view = Button(timeout=20)
        view.message = await ctx.send('Preview!',embed=Accepted, view=view)
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
    Embed.set_author(name=f'{ctx.guild.name} ({ctx.guild.id})', icon_url=ctx.guild.icon.url)
    Embed.set_thumbnail(url=ctx.guild.icon.url)
    Embed.set_footer(text=f'Requested {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Embed)

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
        Channel = Client.get_channel(941611620344406026)
        Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> VoiceDeafened <@{Member.id}>.")
        Infraction.add_field(name='**Infraction Code: **', value=f'{Code1}', inline=False)
        Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
        Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
        Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        await Channel.send(embed=Infraction)
        database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
        database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
        await ctx.send(embed=Embed)
        await Member.edit(deafen = True)
        await Member.edit(mute = True)
    else:
        await MissingPermission(ctx, ctx.author) 


@Client.command(aliases = ['Undeaf', 'UnVoiceDeafen', 'UnDeafen'], pass_context=True)
async def _Undeafen(ctx, Member: Union[discord.Member,discord.Object], *,Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
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
        Channel = Client.get_channel(941611620344406026)
        Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> UnvoiceDeafened <@{Member.id}>.")
        Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
        Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
        Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        await Channel.send(embed=Infraction)
        await ctx.send(embed=Embed)
        await Member.edit(deafen = False)
        await Member.edit(mute = False)
    else:
        await MissingPermission(ctx, ctx.author) 



@Client.command(aliases = ['Alert', 'ModReq'], pass_context=True)
async def _Alert(ctx, Channel_Location: discord.TextChannel,Message_Id:int): 
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    msg = await Channel_Location.fetch_message(Message_Id)
    Channel = Client.get_channel(941411399597445252)
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
    await Channel.send("All active <@&901486519552995348>, please handle this situation", embed=Message)

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
            await ctx.send(embed=Final_Embed)
            time.sleep(Amount)
            Embed = discord.Embed(title="Lock System", description=f'<#{Channel.id}> was unlocked.', color=0x546e7a)
            Embed.set_footer(text=f'Locked by {ctx.author}.', icon_url=ctx.author.avatar.url)
            overwrite2 = Channel.overwrites_for(ctx.guild.default_role)
            overwrite2.send_messages = True
            await Channel.set_permissions(ctx.guild.default_role, overwrite=overwrite2)
            await Channel.send(embed=Embed)
    else:
        await MissingPermission(ctx, ctx.author)

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
                Channel = Client.get_channel(941611620344406026)
                Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> unbanned <@{Member.id}>.")
                Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
                Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
                Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await Channel.send(embed=Infraction)
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

@Client.command(aliases = ['Clearwarnings'],  pass_context=True)
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
        Channel = Client.get_channel(941611620344406026)
        Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> cleared <@{Member.id}>'s warnings.")
        Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
        Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
        Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
        Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        await Channel.send(embed=Infraction)
        await ctx.channel.send(embed=Main)
        for record in records:
            database.execute("DELETE FROM Warning_Logs WHERE UserID=?", (Member.id,))
    else:
        await MissingPermission(ctx, ctx.author) 

@Client.command(aliases = ['Version'],  pass_context=True)
async def _Version(ctx):
    await ctx.channel.send(f"The bot is version 0.2.0 Alpha.")
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
            Channel = Client.get_channel(941611620344406026)
            Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> banned <@{Member.id}>.")
            Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await Channel.send(embed=Infraction)
            await ctx.channel.send(embed=Embed)

            await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await ctx.guild.ban(User, reason=Reason)
    else:
        await MissingPermission(ctx, ctx.author)

@Client.command(aliases = ['Inf', 'Infractions', 'Warnings', 'Warnlist', 'i'],  pass_context=True)
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
            Channel = Client.get_channel(941611620344406026)
            Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> kicked <@{Member.id}>.")
            Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await Channel.send(embed=Infraction)
            await ctx.channel.send(embed=Embed)    
            await Logging(ctx, ctx.message.content,ctx.author, Member, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await Member.kick(reason=Reason)
    else:
        await MissingPermission(ctx, ctx.author)


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
            Channel = Client.get_channel(941411413468016760)
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
            Channel = Client.get_channel(941411413468016760)
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

@Client.command(aliases = ['Warn', 'Strike', 'Infract'],  pass_context=True)
async def _Warn(ctx, Member: discord.Member, *, Reason):
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
    Channel = Client.get_channel(941611620344406026)
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
        Msg = await Channel.send(embed=Infraction)
        database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Reason, Date, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Reason,f'{current_Date}, {current_time}', Type))
        database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
        Database.commit()
    else:
        await MissingPermission(ctx, ctx.author)

@Client.command(aliases = ['Stats'])
async def _Stats(ctx):
    Proc = Process()
    with Proc.oneshot():
        cpu_Time = timedelta(seconds=(cpu := Proc.cpu_times().system))
        uptime = timedelta(seconds=time()-Proc.create_time())
        MemoryTotal = virtual_memory().total / (1024**3)
        MemoryOf = Proc.memory_percent()
        Memory_Usage = MemoryTotal * (MemoryOf / 100)
    Start_Response = time()
    message = await ctx.send("Waiting for a response")
    end = time()
    StatsE = discord.Embed(title="**Stats System**")
    StatsE.add_field(name='**Ping: **', value=f'{Client.latency*1000:,.0f} ms', inline=False)
    StatsE.add_field(name='**Response Time: **', value=f'{(end-Start_Response)*1000:,.0f} ms', inline=False)
    StatsE.add_field(name='**TimeStamp: **', value=f'{datetime.utcnow()}', inline=False)
    StatsE.add_field(name='**Uptime: **', value=f'{uptime}', inline=False)
    StatsE.add_field(name='**CPU Time: **', value=f'{cpu_Time}', inline=False)
    StatsE.add_field(name='**Memory: **', value=f'{Memory_Usage:,.2f} / {MemoryTotal:,.0f} / {MemoryOf}%', inline=False)
    StatsE.add_field(name='**Python Version: **', value=f'{python_version}', inline=False)
    StatsE.add_field(name='**Discord Version: **', value=f'{discord_version}', inline=False)
    StatsE.add_field(name='**Members: **', value=f'{ctx.guild.member_count:,}', inline=False)
    await message.edit(embed=StatsE)

if __name__ == "__main__": 
    MyBot()

Client.run('ODkxNjcyNzE0ODk5NzYzMjIw.YVBw7Q.7E4la6ihkgAtWQMz9SLfDysEyd4') 
# ODkxNjcyNzE0ODk5NzYzMjIw.YVBw7Q.PJ_8PKH3u4vgwm6uZvixO4bKZCQ

# OTA0NDUwODE0NjE2MTQxODI1.YX7tdg.f9kR32IFT7-AY9q2bm3qnkhEQt8
