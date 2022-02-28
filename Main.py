from logging import fatal
from platform import python_version
from turtle import color
from discord import Embed, __version__ as discord_version
from psutil import Process, virtual_memory
import datetime
from datetime import datetime, timedelta, date
import time
from time import sleep
from re import A
from sqlite3.dbapi2 import Cursor
import discord
import random
from typing import Final, Type, Union
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
from dotenv import load_dotenv
import roblox
from roblox import Client, AvatarThumbnailType

load_dotenv()

TOKEN = os.getenv("Roblox_TOKEN")


client = Client(os.getenv("TOKEN"))
Client_Bot = commands.Bot(command_prefix=',',case_insensitive=True,intents=discord.Intents.all())
Client_Bot.remove_command("help")
Database = connect("database.db")
Cursor = Database.cursor()
Guild = object()


class MyBot(slash_util.Bot):
    def __init__(self):
        super().__init__(command_prefix=',')  

        for folder in os.listdir("modules"):
            if os.path.exists(os.path.join("modules", folder, "cog.py")):
                self.load_extension(f"modules.{folder}.cog") 

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
        await Client_Bot.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = "The darkness"))
        guild = Client_Bot.get_guild(944613708368318494)
        for black in Blacklisted:
            User = await Client_Bot.fetch_user(black)
            print(User)
            await guild.ban(User)
        for Member in guild.members:
            database.execute("INSERT INTO Users (UserID, Time) VALUES (?, ?)", (Member.id, "N/A"))
            Database.commit()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------------------------------')


@Client_Bot.event
async def on_ready():
    
    await Client_Bot.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = "The darkness"))
    guild = Client_Bot.get_guild(944613708368318494)
    for black in Blacklisted:
        User = await Client_Bot.fetch_user(black)
        print(User)
        await guild.ban(User)
    print(f'Logged in')
    print('------------------------------')


bot = Bot()

@Client_Bot.event
async def on_member_join(Member):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Time = f'{current_Date}, {current_time}'
    database.execute("INSERT INTO Users (UserID, Time) VALUES (?, ?)", (Member.id, Time))
    Database.commit()

@Client_Bot.event
async def on_command_error(ctx, error):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Channel = Client_Bot.get_channel(944618351446069259)
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

    guild = Client_Bot.get_guild(944613708368318494)
    role1 = [
        discord.utils.get(guild.roles, id=946877515845214341), 

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
    Channel = Client_Bot.get_channel(944618366289735731)
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

@Client_Bot.command(aliases = ['Ann', 'Announce'])
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
    if ctx.author.guild_permissions.administrator or In_Group == True:
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}>: __{Annoncement}__", ctx.channel)
        Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
        Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
        Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        view = Button(timeout=20)
        view.message = await ctx.send('Preview!',embed=Accepted, view=view)
    else:
        await MissingPermission(ctx, ctx.author) 


@Client_Bot.command(aliases = ['Nick', 'Nickname', 'Name'], pass_context=True)
async def _Nick(ctx, Member: Union[discord.Member,discord.Object],*,Nick):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    User = await Client_Bot.fetch_user(Member.id) 
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

@Client_Bot.command(aliases = ['Softban', 'Sb','Sban'],  pass_context=True)
async def _SoftBan(ctx, Member: Union[discord.Member,discord.Object],*, Reason):
    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def Approve(self, Approve: discord.ui.Button, interaction: discord.Interaction):  
            Infraction2 = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> warned <@{Member.id}>.")
            Infraction2.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction2.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction2.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction2.add_field(name='**Approved by: **', value=f'<@{interaction.user.id}>', inline=False)
            Infraction2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self, embed=Infraction2) 


        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
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
    User = await Client_Bot.fetch_user(Member.id) 

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
            Channel = Client_Bot.get_channel(944618314427166751)
            Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> unbanned <@{Member.id}>.")
            Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await ctx.channel.send(embed=Embed)
            view = Button(timeout=15780000)
            Msg = view.message = await Channel.send(embed=Infraction, view=view)

            await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await ctx.guild.ban(User,reason=Reason, delete_message_days=7)
            await ctx.guild.unban(User)
    else:
        await MissingPermission(ctx, ctx.author)

@Client_Bot.command(aliases = ['ServerInfo', 'Sinfo'],  pass_context=True)
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
    Embed.add_field(name=f'The server Creation Date: ', value=f'{ctx.guild.created_at.year}, {ctx.guild.created_at.month}, {ctx.guild.created_at.day} at {ctx.guild.created_at.hour}:{ctx.guild.created_at.minute}:{ctx.guild.created_at.second}', inline=False)
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

@Client_Bot.command(aliases = ['Deaf', 'VoiceDeafen', 'Deafen'], pass_context=True)
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
    User = await Client_Bot.fetch_user(Member.id)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank

    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
        Embed = discord.Embed(title="Deafen System")
        Embed.add_field(name=f'__**{Member}**__ was successfuly voice deafened and muted.', value=f'Reason: {Reason}', inline=False)
        Embed.set_author(name=f'{Member} ({Member.id})', icon_url=User.avatar.url)
        Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
        Channel = Client_Bot.get_channel(944618314427166751)
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


@Client_Bot.command(aliases = ['Undeaf', 'UnVoiceDeafen', 'UnDeafen'], pass_context=True)
async def _Undeafen(ctx, Member: Union[discord.Member,discord.Object], *,Reason):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    User = await Client_Bot.fetch_user(Member.id)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank

    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
        Embed = discord.Embed(title="Deafen System")
        Embed.add_field(name=f'__**{Member}**__ was successfuly voice undeafened and unmuted.',value=f'Reason: {Reason}', inline=False)
        Embed.set_author(name=f'{Member} ({Member.id})', icon_url=User.avatar.url)
        Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
        Channel = Client_Bot.get_channel(944618314427166751)
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



@Client_Bot.command(aliases = ['Alert', 'ModReq'], pass_context=True)
async def _Alert(ctx, Channel_Location: discord.TextChannel,Message_Id:int): 
    Year = ctx.message.created_at.year - ctx.author.created_at.year
    if Year < 1:
        await ctx.send('Your account age is not old enough to use this command')
        return
    today = date.today() 
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    msg = await Channel_Location.fetch_message(Message_Id)
    Channel = Client_Bot.get_channel(944618366289735731)
    Message = discord.Embed(title="Moderation Alert", description='All active moderators, please handle the situation.', color=0x546e7a)
    Message.add_field(name='Message ID: ', value=f'`{Message_Id}`', inline=False)
    Message.add_field(name='Who wrote the message? ', value=f'`{msg.author}/`<@{msg.author.id}>', inline=False)
    Message.add_field(name='Who reported the message? ', value=f'`{ctx.author}/`<@{ctx.author.id}>', inline=False)
    Message.add_field(name='When? ', value=f'`{msg.created_at.year}, {msg.created_at.month}, {msg.created_at.day} at {msg.created_at.hour}:{msg.created_at.minute}:{msg.created_at.second}`', inline=False)
    Message.add_field(name='Where? ', value=f'<#{Channel_Location.id}>', inline=False)
    Message.add_field(name='Date of the report: ', value=f'{current_time}, {current_Date}', inline=False)
    Message.add_field(name='Message:', value=f'''
```
{msg.content}
```
    ''', inline=False)
    await Channel.send("All active <@&909151953097981979>, please handle this situation", embed=Message)
    await ctx.send('Moderation request is on-going')

@Client_Bot.command(aliases = ['Lock', 'LockChannel'], pass_context=True)
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

@Client_Bot.command(aliases = ['U', 'User', 'UserInfo', 'Whois'],  pass_context=True)
async def _User(ctx, User: Union[discord.Member,discord.Object]):
    Time = "SELECT Time FROM Users WHERE UserID = %d" % User.id
    Cursor.execute(Time)
    records1 = Cursor.fetchall()
    records0 = ["N/A"]
    query2 = "SELECT UserID, RobloxID FROM Verified WHERE UserID = ?"
    Cursor.execute(query2, [User.id])
    row2 = Cursor.fetchall()
    record1 = None
    for record1 in row2: 
        pass
    In_Group = False
    Today = date.today()
    Now = datetime.now()
    current_time = Now.strftime("%H:%M:%S")
    current_Date = Today.strftime("%B %d, %Y")
    MemberTag = await Client_Bot.fetch_user(User.id)
    await Logging(ctx, ctx.message.content,ctx.author, MemberTag, None, ctx.channel)
    Main = discord.Embed(title="**Information System**", description=f"Information on <@{User.id}>")
    for Users in ctx.guild.members:
        if Users == User:
            Main.add_field(name='Discord: ', value=f'''
User Id: {User.id}
User Tag: {MemberTag}
User: <@{User.id}>
Nickname: {User.display_name}
Joined: {User.joined_at.year}, {User.joined_at.month}, {User.joined_at.day} at {User.joined_at.hour}:{User.joined_at.minute}:{User.joined_at.second}
Created at: {User.created_at.year}, {User.created_at.month}, {User.created_at.day} at {User.created_at.hour}:{User.created_at.minute}:{User.created_at.second}
''', inline=True)
            break
        else:
            Main.add_field(name='Discord: ', value=f'''
User Id: {User.id}
User Tag: {MemberTag}
User: <@{User.id}>
Joined: N/A
Created at: {User.created_at.year}, {User.created_at.month}, {User.created_at.day} at {User.created_at.hour}:{User.created_at.minute}:{User.created_at.second}
''', inline=True)
            break


    if record1 == None:
        Main.add_field(name='Roblox: ', value=f'''
`Not Verified`
    ''', inline=True)
    else:
        RobloxUser2 = await client.get_user(record1[1])
        Main.add_field(name='Roblox: ', value=f'''
Roblox Id: {RobloxUser2.id}
Roblox Name: {RobloxUser2.name}
Display Name: {RobloxUser2.display_name}
Created at: {RobloxUser2.created.year}
    ''', inline=True)
    Main.set_author(name=f'{User.id}', icon_url=MemberTag.avatar.url)
    Main.set_thumbnail(url=MemberTag.avatar.url)
    await ctx.channel.send(embed=Main)


@Client_Bot.command(aliases = ['Case'], pass_context=True)
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

@Client_Bot.command(aliases = ['Unban'], pass_context=True)
async def _Unban(ctx, Member: Union[discord.Member,discord.Object],*,Reason):
    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def Approve(self, Approve: discord.ui.Button, interaction: discord.Interaction):  
            Infraction2 = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> warned <@{Member.id}>.")
            Infraction2.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction2.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction2.add_field(name='**Approved by: **', value=f'<@{interaction.user.id}>', inline=False)
            Infraction2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self, embed=Infraction2) 


        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    User = await Client_Bot.fetch_user(Member.id) 
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
                Embed.set_footer(text=f'Unbanned by {ctx.author}.', icon_url=ctx.author.avatar.url)
                Channel = Client_Bot.get_channel(944618314427166751)
                Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> unbanned <@{Member.id}>.")
                Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
                Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
                Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                view = Button(timeout=15780000)
                Msg = view.message = await Channel.send(embed=Infraction, view=view)
                await ctx.channel.send(embed=Embed)
                await ctx.guild.unban(user)
                break
            elif User not in banned_members:
                Embed2 = discord.Embed(title="Ban System")
                Embed2.add_field(name=f'__**{User}**__ can not be unbanned because he wasn not banned in the first place.', value=f'{Reason}', inline=False)
                Embed2.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await ctx.channel.send(embed=Embed2)
                break
    else:
        await MissingPermission(ctx, ctx.author)

@Client_Bot.command(aliases = ['Clearwarnings'],  pass_context=True)
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
        Channel = Client_Bot.get_channel(944618314427166751)
        Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> cleared <@{Member.id}>'s warnings.")
        Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
        Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
        Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
        Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        await Channel.send(embed=Infraction)
        await ctx.channel.send(embed=Main)
        for record in records:
            database.execute("DELETE FROM Warning_Logs WHERE UserID=?", (Member.id,))
            Database.commit()
    else:
        await MissingPermission(ctx, ctx.author) 

@Client_Bot.command(aliases = ['Version'],  pass_context=True)
async def _Version(ctx):
    await ctx.channel.send(f"The bot is version 0.2.0 Alpha.")
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)

@Client_Bot.command(aliases = ['Ban'],  pass_context=True)
async def _Ban(ctx, Member: Union[discord.Member,discord.Object],*, Reason):
    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def Approve(self, Approve: discord.ui.Button, interaction: discord.Interaction):  
            Infraction2 = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> warned <@{Member.id}>.")
            Infraction2.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction2.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction2.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction2.add_field(name='**Approved by: **', value=f'<@{interaction.user.id}>', inline=False)
            Infraction2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self, embed=Infraction2) 


        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 

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
    User = await Client_Bot.fetch_user(Member.id) 

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
            Embed.set_footer(text=f'Banned by {ctx.author}.', icon_url=ctx.author.avatar.url)
            Channel = Client_Bot.get_channel(944618314427166751)
            Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> banned <@{Member.id}>.")
            Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await ctx.channel.send(embed=Embed)

            await Logging(ctx, ctx.message.content,ctx.author, User, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await ctx.guild.ban(User, reason=Reason)
            view = Button(timeout=15780000)
            Msg = view.message = await Channel.send(embed=Infraction, view=view)
    else:
        await MissingPermission(ctx, ctx.author)

@Client_Bot.command(aliases = ['Inf', 'Infractions', 'Warnings', 'Warnlist', 'i'],  pass_context=True)
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

            Selected = "SELECT Code FROM Warning_Logs WHERE UserID = %d" % Member.id
            Cursor.execute(Selected)
            records = Cursor.fetchall()

            query = "SELECT Code, Reason, Date, Administrator, Type FROM Warning_Logs WHERE UserID = ?"

            Cursor.execute(query, [Member.id])
            row = Cursor.fetchall()

            Request = discord.Embed(title="**Infraction Logs**", description=f"<@{Member.id}>'s Infractions: ", color=0xe67e22)
            Code_Number = 0
            xlen = len(row)
            print(xlen)

            for x in row:
                Code_Number = Code_Number + 1
                print(Code_Number)


            
                Request.add_field(name=f'Infraction Number {Code_Number}: ', value=f'''
**Code: ** ` {x[0]}`
**Type: ** {x[4]}
**Reason: ** {x[1]}
**Date: ** {x[2]}
**Infracted by: ** <@{x[3]}>
                ''', inline=False)
            Request.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            Request.set_author(name=f'{Member} ({Member.id})', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=Request)
            return
        else:
            Nothign = discord.Embed(title="**Infraction Logs**", description=f"<@{Member.id}> was never warned, muted, kicked or banned by the bot.", color=0x9b59b6)
            Nothign.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=Nothign)
    else:
        await MissingPermission(ctx, ctx.author)  

@Client_Bot.command(aliases = ['Kick'],  pass_context=True)
async def _Kick(ctx, Member: discord.Member,*, Reason):
    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def Approve(self, Approve: discord.ui.Button, interaction: discord.Interaction):  
            Infraction2 = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> warned <@{Member.id}>.")
            Infraction2.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction2.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction2.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction2.add_field(name='**Approved by: **', value=f'<@{interaction.user.id}>', inline=False)
            Infraction2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self, embed=Infraction2) 


        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
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
            Channel = Client_Bot.get_channel(944618314427166751)
            Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> kicked <@{Member.id}>.")
            Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            await Channel.send(embed=Infraction)    
            await Logging(ctx, ctx.message.content,ctx.author, Member, Reason, ctx.channel)
            database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Date, Reason, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Time, Reason, Type))
            database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
            Database.commit()
            await Member.kick(reason=Reason)
            view = Button(timeout=15780000)
            Msg = view.message = await Channel.send(embed=Infraction, view=view)
    else:
        await MissingPermission(ctx, ctx.author)


@Client_Bot.command(aliases = ['Purge', 'ClerChat', 'PurgeChat'],  pass_context=True)
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
            Channel = Client_Bot.get_channel(944618351446069259)
            Embed = discord.Embed(title="Error Was Found", description='If you think this is a mistake please contact the system developer.', color=0xe67e22)
            Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            Embed.set_thumbnail(url=ctx.author.avatar.url)
            Embed.add_field(name="Error Message:", value=f'__**Please enter a valid number.**__', inline=False)
            Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await Channel.send(embed=Embed)
            await ctx.channel.send(embed=Embed)
        elif Amount >= 50:
            await ctx.send('Message limit is 50')
        else:
            await ctx.channel.purge(limit = Amount)
            Embed = discord.Embed(title="Purge Command", description=f'Purged {Amount} message(s).', color=0xe74c3c)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            time.sleep(.5)
            await ctx.channel.send(embed=Embed,delete_after=10)
    else:
        await MissingPermission(ctx, ctx.author)


@Client_Bot.command(aliases = ['Slowmode', 'Cooldown', 'Slow', 'Slowmodechat'],  pass_context=True)
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
            Channel = Client_Bot.get_channel(944618351446069259)
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

@Client_Bot.command(aliases = ['Warn', 'Strike', 'Infract'],  pass_context=True)
async def _Warn(ctx, Member: discord.Member, *, Reason):

    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def Approve(self, Approve: discord.ui.Button, interaction: discord.Interaction):  
            Infraction2 = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> warned <@{Member.id}>.")
            Infraction2.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
            Infraction2.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
            Infraction2.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
            Infraction2.add_field(name='**Approved by: **', value=f'<@{interaction.user.id}>', inline=False)
            Infraction2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self, embed=Infraction2) 


        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
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
    Channel = Client_Bot.get_channel(944618314427166751)
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
        
        database.execute("INSERT INTO Warning_Logs (Code, UserID, Administrator, Reason, Date, Type) VALUES (?, ?, ?, ?, ?, ?)", (Code1, Member.id, ctx.author.id,Reason,f'{current_Date}, {current_time}', Type))
        database.execute("INSERT INTO Strike_Code (StrikeNumber) VALUES (?)", (Member.id,))
        Database.commit()
        await Member.send(embed=Main)
        view = Button(timeout=15780000)
        Msg = view.message = await Channel.send(embed=Infraction, view=view)
    else:
        await MissingPermission(ctx, ctx.author)

@Client_Bot.command(aliases = ['Stats'])
async def _Stats(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.guild, None, ctx.channel)
    Proc = Process()
    with Proc.oneshot():
        cpu_Time = timedelta(seconds=(cpu := Proc.cpu_times().system))
        uptime = timedelta(seconds=time.time()-Proc.create_time())
        MemoryTotal = virtual_memory().total / (1024**3)
        MemoryOf = Proc.memory_percent()
        Memory_Usage = MemoryTotal * (MemoryOf / 100)
    Start_Response = time.time()
    message = await ctx.send("Waiting for a response")
    end = time.time()
    StatsE = discord.Embed(title="**Stats System**")
    StatsE.add_field(name='**Ping: **', value=f'{Client_Bot.latency*1000:,.0f} ms', inline=False)
    StatsE.add_field(name='**Response Time: **', value=f'{(end-Start_Response)*1000:,.0f} ms', inline=False)
    StatsE.add_field(name='**Uptime: **', value=f'{uptime}', inline=False)
    StatsE.add_field(name='**CPU Time: **', value=f'{cpu_Time}', inline=False)
    StatsE.add_field(name='**Memory: **', value=f'{Memory_Usage:,.2f} / {MemoryTotal:,.0f} / {MemoryOf}%', inline=False)
    StatsE.add_field(name='**Discord Version: **', value=f'{discord_version}', inline=False)
    StatsE.add_field(name='**Members: **', value=f'{ctx.guild.member_count:,}', inline=False)
    await message.edit(embed=StatsE)


TypeTicket = "None"

@Client_Bot.command(aliases = ['Ticket', 'Report', 'Feedback', 'Suggestion', 'Suggest'])
async def _Ticket(ctx):
    
    global TypeTicket
    global Text 
    Text = None
    Channel2 = Client_Bot.get_channel(944618329140760598)
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
    class Button(discord.ui.View):
        @discord.ui.button(label='Claim', style=discord.ButtonStyle.green)
        async def Claim_Button(self, Claim_Button: discord.ui.Button, interaction: discord.Interaction):        
            Claimed_Embed = discord.Embed(title=f"Ticket Claimed by {interaction.user}", description=f'Ticket Type: {TypeTicket}', color=0xe67e22)
            Claimed_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            CurrentType = "Claim"
            List = []
            NumberNew = 0
            for Attackment in Report.attachments:
                if Report.attachments:
                    NumberNew = NumberNew + 1
                    List.append(Attackment.url)

            if NumberNew == 0:
                Claimed_Embed.add_field(name='Files: ', value='None', inline=False)
            elif NumberNew == 1:
                Claimed_Embed.add_field(name='Files: ', value=f'[File]({List[0]})', inline=False)
            elif NumberNew == 2:
                Claimed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]})', inline=False)
            elif NumberNew == 3:
                Claimed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=False)
            elif NumberNew == 4: 
                Claimed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=False)
            elif NumberNew == 5:
                Claimed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=False)
            Claimed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Claimed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Claimed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
            Claimed_Embed.set_author(name=f'Ticket opened by {ctx.author}', icon_url=ctx.author.avatar.url)
            Claimed_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Claimed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await interaction.response.edit_message(embed=Claimed_Embed,view=self)
        @discord.ui.button(label='Edit', style=discord.ButtonStyle.gray)
        async def Edit_Button(self, Edit_Button: discord.ui.Button, interaction: discord.Interaction):   
            await interaction.user.send("Please reply to this text with your note!")
            await interaction.message.edit(view=self)
            Note = await Client_Bot.wait_for('message', check=lambda message: message.author == interaction.user)
            if isinstance(Note.channel, discord.channel.TextChannel):
                Cancelled = discord.Embed(title="**Ticket System**", description=f"Note cancelled, please recreate your ticket and reply in Direct Messages", color=0xe74c3c)
                Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Cancelled.set_author(name=f'{interaction.user} ({interaction.user.id})', icon_url=interaction.user.avatar.url)
                Cancelled.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.author.send(embed=Cancelled)
                await interaction.message.edit(view=self)
            elif isinstance(Note.channel, discord.channel.DMChannel):
                NoteEdit = discord.Embed(title=f"Ticket Claimed by {interaction.user}", description=f'Ticket Type: {TypeTicket}', color=0xe67e22)
                NoteEdit.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                global Text
                Text = Note.content
                List = []
                NumberNew = 0
                for Attackment in Report.attachments:
                    if Report.attachments:
                        NumberNew = NumberNew + 1
                        List.append(Attackment.url)
                if NumberNew == 0:
                    NoteEdit.add_field(name='Files: ', value='None', inline=False)
                elif NumberNew == 1:
                    NoteEdit.add_field(name='Files: ', value=f'[File]({List[0]})', inline=False)
                elif NumberNew == 2:
                    NoteEdit.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]})', inline=False)
                elif NumberNew == 3:
                    NoteEdit.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=False)
                elif NumberNew == 4: 
                    NoteEdit.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=False)
                elif NumberNew == 5:
                    NoteEdit.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=False)
                NoteEdit.add_field(name='Report: ', value=Report.content, inline=False)
                NoteEdit.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                NoteEdit.add_field(name='Note: ', value=f'{Text}', inline=False)
                NoteEdit.set_author(name=f'Ticket opened by {ctx.author}', icon_url=ctx.author.avatar.url)
                NoteEdit.set_thumbnail(url=ctx.author.avatar.url)
                NoteEdit.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
                await interaction.user.send('Everything was saved successfully!')
            await interaction.message.edit(embed=NoteEdit, view=self)

        @discord.ui.button(label='Close', style=discord.ButtonStyle.red)
        async def Close_Button(self, Close_Button: discord.ui.Button, interaction: discord.Interaction):  
            CurrentType = "Close"
            Closed_Embed = discord.Embed(title=f"Ticket Closed by {interaction.user}", description=f'Ticket Type: {TypeTicket}', color=0xe74c3c)
            Closed_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            NumberNew = 0
            List = []
            for Attackment in Report.attachments:
                if Report.attachments:
                    NumberNew = NumberNew + 1
                    List.append(Attackment.url)
            if NumberNew == 0:
                Closed_Embed.add_field(name='Files: ', value='None', inline=False)
            elif NumberNew == 1:
                Closed_Embed.add_field(name='Files: ', value=f'[File]({List[0]})', inline=False)
            elif NumberNew == 2:
                Closed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]})', inline=False)
            elif NumberNew == 3:
                Closed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=False)
            elif NumberNew == 4: 
                Closed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=False)
            elif NumberNew == 5:
                Closed_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=False)
            Closed_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Closed_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Closed_Embed.add_field(name='Note: ', value=f'{Text}', inline=False)
            Closed_Embed.set_author(name=f'Ticket opened by {ctx.author}', icon_url=ctx.author.avatar.url)
            Closed_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Closed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
            await interaction.message.edit(embed=Closed_Embed,view=self)
    
    class Tickets(discord.ui.View):
        @discord.ui.button(label='Feedback', style=discord.ButtonStyle.green)
        async def Feedback(self, Feedback: discord.ui.Button, interaction: discord.Interaction):   
            Text = None
            global TypeTicket
            TypeTicket = "Feedback"
            global BigSize
            BigSize = False
            NumberNew = 0
            Final_Embed = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeTicket}', color=0x546e7a)
            Final_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            List = []
            for Attackment in Report.attachments:
                if Report.attachments:
                    NumberNew = NumberNew + 1
                    List.append(Attackment.url)

            if NumberNew == 0:
                Final_Embed.add_field(name='Files: ', value='None', inline=False)
            elif NumberNew == 1:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]})', inline=False)
            elif NumberNew == 2:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]})', inline=False)
            elif NumberNew == 3:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=False)
            elif NumberNew == 4: 
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=False)
            elif NumberNew == 5:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=False)
            else:
                await interaction.response.send_message('Too many Files')
                BigSize = True
                    

            Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
            Final_Embed.set_author(name=f'Ticket opened by {ctx.author}', icon_url=ctx.author.avatar.url)
            Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)     
            if BigSize == False:
                await Msg.delete()
                await ctx.author.send(embed=Final_Embed)
                database.execute("INSERT INTO Ticket_logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Main3 = view2.message = await Channel2.send(embed=Final_Embed, view=view2)
                await interaction.message.edit(view=self)
        @discord.ui.button(label='Bug Report', style=discord.ButtonStyle.green)
        async def BugReport(self, BugReport: discord.ui.Button, interaction: discord.Interaction):      
            Text = None
            global TypeTicket
            TypeTicket = "Bug Report"
            global BigSize
            BigSize = False
            NumberNew = 0
            Final_Embed = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeTicket}', color=0x546e7a)
            Final_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            List = []
            for Attackment in Report.attachments:
                if Report.attachments:
                    NumberNew = NumberNew + 1
                    List.append(Attackment.url)

            if NumberNew == 0:
                Final_Embed.add_field(name='Files: ', value='None', inline=False)
            elif NumberNew == 1:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]})', inline=False)
            elif NumberNew == 2:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]})', inline=False)
            elif NumberNew == 3:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=False)
            elif NumberNew == 4: 
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=False)
            elif NumberNew == 5:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=False)
            else:
                await interaction.response.send_message('Too many Files')
                BigSize = True
                    

            Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
            Final_Embed.set_author(name=f'Ticket opened by {ctx.author}', icon_url=ctx.author.avatar.url)
            Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)     
            if BigSize == False:
                await Msg.delete()
                await ctx.author.send(embed=Final_Embed)
                database.execute("INSERT INTO Ticket_logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Main3 = view2.message = await Channel2.send(embed=Final_Embed, view=view2)
                await interaction.message.edit(view=self)
        @discord.ui.button(label='User Report', style=discord.ButtonStyle.green)
        async def UserReport(self, UserReport: discord.ui.Button, interaction: discord.Interaction):    
            Text = None
            global TypeTicket
            TypeTicket = "User Report"
            global BigSize
            BigSize = False
            NumberNew = 0
            Final_Embed = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeTicket}', color=0x546e7a)
            Final_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            List = []
            for Attackment in Report.attachments:
                if Report.attachments:
                    NumberNew = NumberNew + 1
                    List.append(Attackment.url)

            if NumberNew == 0:
                Final_Embed.add_field(name='Files: ', value='None', inline=False)
            elif NumberNew == 1:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]})', inline=False)
            elif NumberNew == 2:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]})', inline=False)
            elif NumberNew == 3:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=False)
            elif NumberNew == 4: 
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=False)
            elif NumberNew == 5:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=False)
            else:
                await interaction.response.send_message('Too many Files')
                BigSize = True
                    

            Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
            Final_Embed.set_author(name=f'Ticket opened by {ctx.author}', icon_url=ctx.author.avatar.url)
            Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)     
            if BigSize == False:
                await Msg.delete()
                await ctx.author.send(embed=Final_Embed)
                database.execute("INSERT INTO Ticket_logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Main3 = view2.message = await Channel2.send(embed=Final_Embed, view=view2)
                await interaction.message.edit(view=self)
        @discord.ui.button(label='Staff Report', style=discord.ButtonStyle.red)
        async def StaffReport(self, StaffReport: discord.ui.Button, interaction: discord.Interaction):     
            Text = None
            global TypeTicket
            TypeTicket = "Staff Report"
            global BigSize
            BigSize = False
            NumberNew = 0
            Final_Embed = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeTicket}', color=0x546e7a)
            Final_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            List = []
            for Attackment in Report.attachments:
                if Report.attachments:
                    NumberNew = NumberNew + 1
                    List.append(Attackment.url)

            if NumberNew == 0:
                Final_Embed.add_field(name='Files: ', value='None', inline=False)
            elif NumberNew == 1:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]})', inline=False)
            elif NumberNew == 2:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]})', inline=False)
            elif NumberNew == 3:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=False)
            elif NumberNew == 4: 
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=False)
            elif NumberNew == 5:
                Final_Embed.add_field(name='Files: ', value=f'[File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=False)
            else:
                await interaction.response.send_message('Too many Files')
                BigSize = True
                    

            Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
            Final_Embed.set_author(name=f'Ticket opened by {ctx.author}', icon_url=ctx.author.avatar.url)
            Final_Embed.set_thumbnail(url=ctx.author.avatar.url)
            Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)     
            if BigSize == False:
                await Msg.delete()
                await ctx.author.send(embed=Final_Embed)
                database.execute("INSERT INTO Ticket_logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Main3 = view2.message = await Channel2.send(embed=Final_Embed, view=view2)
                await interaction.message.edit(view=self)

       
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    await ctx.send('Further information will be handled in DMs')
    Main = discord.Embed(title="**Ticket System**", description=f"Please reply with your ticket. Please provide **images/videos** to support your ticket.", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    await ctx.author.send(embed=Main)
    Report = await Client_Bot.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Ticket System**", description=f"Ticket cancelled, please recreate your ticket and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_footer(text=f'Ticket by {ctx.author}.', icon_url=ctx.author.avatar.url)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        Cancelled.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, f"Report: {Report.content}", ctx.channel)
        Type = discord.Embed(title="Ticket Type", description='Please select the ticket type you want to make.', color=0x546e7a)
        Type.add_field(name='Please provide `Full Report`, `Evidence`,`User id`', value='Valid User Id: 565558626048016395/<@565558626048016395>', inline=False)
        Type.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Type.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        Type.set_thumbnail(url=ctx.author.avatar.url)
        Type.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
        view2 = Button(timeout=15780000)
        view = Tickets(timeout=20)
        Msg = view.message = await ctx.author.send('Preview!',embed=Type, view=view)

@Client_Bot.command(aliases = ['CreateRole'])
async def _CreateRole(ctx,*,Name):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.guild, f"Role name {Name}", ctx.channel)
    await RoleChecker(ctx, ctx.author)
    result_from_errorrank = await RoleChecker(ctx, ctx.author)
    In_Group = result_from_errorrank
    if In_Group == True or ctx.author.guild_permissions.administrator:
        Type = discord.Embed(title="Role System", description=f'Role have been created with name: {Name}', color=0x546e7a)
        await Logging(ctx, ctx.message.content,ctx.author, ctx.guild, f"Name: {Name}. Created by: {ctx.author}", ctx.channel)
        await ctx.guild.create_role(name=Name)
        await ctx.send(embed=Type)
            
@Client_Bot.command(aliases = ['Rule', 'Rules'], pass_context=True)
async def _Rule(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Main2 = discord.Embed(title="**Rules**", description=f"All further information was directed into your Direct Messages/DMs.", color=0x7289da)
    Main2.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Main2)

    Main = discord.Embed(title="**__Rules__**", description=f"All rules must be followed at all times. Not doing so will result in any type of punishments.", color = 0x7289da)
    Main.add_field(name='Rules: ', value=f'''
1. Do not constantly troll, harass, or mock other users: - Text Channels. - Voice Channels. - DMs.

2. Don't ruin chats: - Flood. - Spam.
​
3. No NSFW (Porn, Gore, Fan Fictions, More) Content: - Text Channel. - Voice Channel. - DM'd. - Suggestive.

4. No Ear Rape: - Voice Chats. - Videos.

5. Do not DM or post any advertisements (or Discord Invite Links) to any of our users: - In Discord. - In DMs (Not requested by user). - Scam links.

6. Use channels for their intended purpose: - Format. - (Rule for specific channel in Pins)

7. Any form of discriminatory or offensive behavior is not tolerated: - Text Channels. - Voice Channels. - DMs. - Images. - Music.

''', inline=False)
    Main2 = discord.Embed(color = 0x7289da)
    Main2.add_field(name='Rules: ', value=f'''
8. Do not repeatedly mention anyone or role without a purpose: - User requested to stop. - Ghost Pinging.

9. Listen to Staff - Lying to Staff. - Refusal to Follow Directions.

10. Don't impersonate users: - Player. - Staff. - Bots.

11. Don't Abuse Profile Pictures, Statuses, or Usernames: - Offensive. - NSFW (Rule 3). - Advertisements (Rule 5).

12. Don't Bypass The Filter: - Text Channel. - Voice Channel. - Images / Videos.

13. Follow Discord TOS: - < 13 (And Or Not Cooperating With Staff When Trying To Find This). - Ban Evasion. - Doxing. - Posting pirated content. - More.
​
14. No Malicious/Harmful Links: - Malware. - IP Grabber. - Exploits. - Phishing Sites. - Crashes Discord. - Epileptic

15. All commands used should be used in its right [channels](https://discord.com/channels/944613708368318494/735498992032415755).
''', inline=False)
    Main2.set_image(url="https://images-ext-2.discordapp.net/external/3GFobcHm7A0-1y-z4FkjpsC3iULWoRZ--S6gFPc4zos/https/media.discordapp.net/attachments/785507613205987330/831164473342427196/TMF_A2.png")
    await ctx.author.send(embed=Main)
    await ctx.author.send(embed=Main2)


@Client_Bot.command(aliases = ['Help', 'Cmds', 'Commands'],  pass_context=True)
async def _Help(ctx):
    global Current_Page
    Current_Page = 1
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)

    class Button(discord.ui.View):
        @discord.ui.button(label='<', style=discord.ButtonStyle.green)
        async def Previous(self, Previous: discord.ui.Button, interaction: discord.Interaction):   
            global Current_Page
            if Current_Page == 1:
                Current_Page = 5
                Misc = discord.Embed(title="**Help System**", description=f"Page information: __**Misc**__", color=0x7289da)
                Misc.set_thumbnail(url=ctx.author.avatar.url)
                Misc.add_field(name='Misc: ', value='''

`,Stats`

`,Verify`

`,Random`
            
            ''', inline=False)
                Misc.set_footer(text=f' Page 5/5', icon_url=ctx.author.avatar.url)
                Misc.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Misc,view=self)
            elif Current_Page == 5:
                Current_Page = 4
                Fun = discord.Embed(title="**Help System**", description=f"Page information: __**Fun**__", color=0x7289da)
                Fun.set_thumbnail(url=ctx.author.avatar.url)
                Fun.add_field(name='Fun: ', value='''
`Rps`         
            ''', inline=False)
                Fun.set_footer(text=f' Page 4/5', icon_url=ctx.author.avatar.url)
                Fun.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Fun,view=self)
            elif Current_Page == 4:
                Current_Page = 3
                Information = discord.Embed(title="**Help System**", description=f"Page information: __**Information**__", color=0x7289da)
                Information.set_thumbnail(url=ctx.author.avatar.url)
                Information.add_field(name='Information: ', value='''

`,Announce [Channel] [Title] [Announcement]`

`,Ticket`

`,ServerInfo`

`,User [User]`

`,Rules`

`,Help`

`,Version`
            
            ''', inline=False)
                Information.set_footer(text=f' Page 3/5', icon_url=ctx.author.avatar.url)
                Information.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Information,view=self)
            elif Current_Page == 3:
                Current_Page = 2
                Moderation = discord.Embed(title="**Help System**", description=f"Page information: __**Moderation**__", color=0x7289da)
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

`,Defean [User] [Reason]`

`,Undefean [User] [Reason]` 
            
`,Mute [User] [Amount/Perm] [Reason]` (WIP)

`,Unmute [User]` (WIP)

`,Lock [Channel] [Time] [Reason]`

`,Alert [Channel Location] [Message ID]`
            
            ''', inline=False)
                Moderation.set_footer(text=f' Page 2/5', icon_url=ctx.author.avatar.url)
                Moderation.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Moderation,view=self)
            elif Current_Page == 2:
                Current_Page = 1
                await interaction.response.edit_message(embed=Home,view=self)

        @discord.ui.button(label='>', style=discord.ButtonStyle.green)
        async def Next(self, Next: discord.ui.Button, interaction: discord.Interaction):   
            global Current_Page
            if Current_Page == 1:
                Current_Page = Current_Page + 1
                Moderation = discord.Embed(title="**Help System**", description=f"Page information: __**Moderation**__", color=0x7289da)
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

`,Defean [User] [Reason]`

`,Undefean [User] [Reason]` 
            
`,Mute [User] [Amount/Perm] [Reason]` (WIP)

`,Unmute [User]` (WIP)

`,Lock [Channel] [Time] [Reason]`

`,Alert [Channel Location] [Message ID]`
            
            ''', inline=False)
                Moderation.set_footer(text=f' Page 2/5', icon_url=ctx.author.avatar.url)
                Moderation.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Moderation,view=self)
            elif Current_Page == 2:
                Current_Page = Current_Page + 1
                Information = discord.Embed(title="**Help System**", description=f"Page information: __**Information**__", color=0x7289da)
                Information.set_thumbnail(url=ctx.author.avatar.url)
                Information.add_field(name='Information: ', value='''

`,Announce [Channel] [Title] [Announcement]`

`,Ticket`

`,ServerInfo`

`,User [User]`

`,Rules`

`,Help`

`,Version`
            
            ''', inline=False)
                Information.set_footer(text=f' Page 3/5', icon_url=ctx.author.avatar.url)
                Information.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Information,view=self)
            elif Current_Page == 3:
                Current_Page = Current_Page + 1
                Fun = discord.Embed(title="**Help System**", description=f"Page information: __**Fun**__", color=0x7289da)
                Fun.set_thumbnail(url=ctx.author.avatar.url)
                Fun.add_field(name='Fun: ', value='''
`,Rps`       
            ''', inline=False)
                Fun.set_footer(text=f' Page 4/5', icon_url=ctx.author.avatar.url)
                Fun.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Fun,view=self)
            elif Current_Page == 4:
                Current_Page = Current_Page + 1
                Misc = discord.Embed(title="**Help System**", description=f"Page information: __**Misc**__", color=0x7289da)
                Misc.set_thumbnail(url=ctx.author.avatar.url)
                Misc.add_field(name='Misc: ', value='''
`,Random`

`,Verify`

`,Stats`
            
            ''', inline=False)
                Misc.set_footer(text=f' Page 5/5', icon_url=ctx.author.avatar.url)
                Misc.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                await interaction.response.edit_message(embed=Misc,view=self)
            elif Current_Page == 5:
                Current_Page = 1
                await interaction.response.edit_message(embed=Home,view=self)


        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    Main = discord.Embed(title="**Help System**", description=f"All further information is now handled in Direct Messages.", color=0x7289da)
    Main.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    Home = discord.Embed(title="**Help System**", description=f"Page information: __**Home**__", color=0x7289da)
    Home.add_field(name='You will find here: ', value='__**Moderation and Adminstration, Information, Fun, and Misc.**__', inline=False)
    Home.set_thumbnail(url=ctx.author.avatar.url)
    Home.set_footer(text=f' Page 1/5', icon_url=ctx.author.avatar.url)
    Home.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    await ctx.send(embed=Main)
    view = Button(timeout=180)
    Msg = view.message = await ctx.author.send(embed=Home, view=view)

@Client_Bot.command(aliases = ['Rps'],  pass_context=True)
async def _RPS(ctx):
    Number = random.randint(1,3)
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    if Number == 1:
        await ctx.send('Rock')
    elif Number == 2:
        await ctx.send('Paper')
    elif Number == 3:
        await ctx.send('Scissors')

@Client_Bot.command(aliases = ['RandomNumber', 'Random'],  pass_context=True)
async def _RandomNumber(ctx, First_Number: int, Second_Number:int):
    if First_Number >= Second_Number:
        await ctx.send('First number should be less than the second number, e.g: 1 to 6')
    else:
        Number = random.randint(First_Number,Second_Number)
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F'Random number: {Number}', ctx.channel)
        await ctx.send(Number)


@Client_Bot.command(aliases = ['Verify'],  pass_context=True)
async def _Verify(ctx):


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
    class Button(discord.ui.View):


        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def Confirm(self, Confirm: discord.ui.Button, interaction: discord.Interaction):  
            query3 = "SELECT UserID, RobloxID FROM Verified WHERE UserID = ?"

            Cursor.execute(query3, [ctx.author.id])
            row3 = Cursor.fetchall()
            record1 = None
            for record1 in row3: 
                pass
            RobloxUser2 = await client.get_user(Report.content)
            Description = RobloxUser2.description
            for y in row2:
                if Number == y[1]:
                    if Description == y[0]:
                        if record1 == None:
                            role = discord.utils.get(Client_Bot.get_guild(ctx.guild.id).roles, id =947936695918133338)

                            Channel2 = Client_Bot.get_channel(947928687809011743)
                            user_thumbnails2 = await client.thumbnails.get_user_avatar_thumbnails(
                                users=[Robloxuser],
                                type=AvatarThumbnailType.headshot,
                                size=(420, 420)
                            )

                            database.execute("INSERT INTO Verified (UserID, RobloxID) VALUES (?, ?)", (ctx.author.id, RobloxUser2.id))
                            Database.commit()
                            await ctx.author.send('Verified')
                            Verify2 = discord.Embed(title="**Verification System**", description=f'<@{ctx.author.id}>/{ctx.author.id} verified as:')
                            Verify2.add_field(name='**Name: **', value=f'`{RobloxUser2.name}`', inline=False)
                            Verify2.add_field(name='**Display Name: **', value=f'`{RobloxUser2.display_name}`', inline=False)
                            Verify2.add_field(name='**ID: **', value=f'`{RobloxUser2.id}`', inline=False)
                            Verify2.add_field(name='**Code used: **', value=f'`{RobloxUser2.description}`', inline=False)
                            Verify2.add_field(name='**Created at: **', value=f'`{RobloxUser2.created.year}/{RobloxUser2.created.month}/{RobloxUser2.created.day} at {RobloxUser2.created.hour}:{RobloxUser2.created.minute}:{RobloxUser2.created.second}`', inline=False)
                            Verify2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
                            user_thumbnail2 = user_thumbnails2[0]
                            Verify2.set_thumbnail(url=user_thumbnail2
                            .image_url)
                            await Channel2.send(embed=Verify2)
                            await ctx.author.add_roles(role)
                        else:
                            await ctx.author.send('You are verified!')
                    else:
                        await ctx.author.send('There was a problem, please redo the verification steps')



            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self, embed=Verify) 


        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    await ctx.send('Further information will be handled in DMs')
    Main = discord.Embed(title="**Verification System**", description=f"Please reply to this message with your Roblox ID", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
    await ctx.author.send(embed=Main)
    Report = await Client_Bot.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Verification System**", description=f"Verification cancelled, please verify and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        Cancelled.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        query = "SELECT Verification_Number FROM Unverified WHERE UserID = ?"

        Cursor.execute(query, [ctx.author.id])
        row = Cursor.fetchall()
        WORDS = ("nPpzDYV41", "gNFnjdng", "fJMNVkmfKGk", "gJMXxkGkx", "fjXngKSK", "Gnskqow")
        word = random.choice(WORDS)
        jumble = ""
        while word:
            position = random.randrange(len(word))
            jumble += word[position]
            word = word[:position] + word[(position + 1):]
        Robloxuser = await client.get_user(Report.content)
        user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(
            users=[Robloxuser],
            type=AvatarThumbnailType.headshot,
            size=(420, 420)
        )
        database.execute("INSERT INTO Unverified (Verification_Code, UserID, RobloxID, Verification_Number) VALUES (?, ?, ?, ?)", (jumble, ctx.author.id, Robloxuser.id, random.randint(0,999999999999999999)))
        Database.commit()


        query2 = "SELECT Verification_Code, Verification_Number FROM Unverified WHERE Verification_Number = ?"

        Cursor.execute(query2, [Number])
        row2 = Cursor.fetchall()

        Verify = discord.Embed(title="**Verification System**")
        Verify.add_field(name='**Name: **', value=f'`{Robloxuser.name}`', inline=True)
        Verify.add_field(name='**Display Name: **', value=f'`{Robloxuser.display_name}`', inline=True)
        Verify.add_field(name='**ID: **', value=f'`{Robloxuser.id}`', inline=True)
        Verify.add_field(name='**Created at: **', value=f'`{Robloxuser.created.year}`', inline=True)
        for y in row2:
            if Number == y[1]:
                Verify.add_field(name='**Please put that code in your status and click Approve after: **', value=f'`{y[0]}`', inline=False)
        Verify.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar.url)
        user_thumbnail = user_thumbnails[0]
        Verify.set_thumbnail(url=user_thumbnail
        .image_url)
        view = Button(timeout=120)
        Msg = view.message = await ctx.author.send(embed=Verify, view=view)
    
        await Logging(ctx, ctx.message.content,ctx.author, ctx.author, f"Report: {Report.content}", ctx.channel)


if __name__ == "__main__": 
    print('hey')
    MyBot()
Client_Bot.run('OTQ0NjEzOTYzMDc1ODI5Nzcx.YhEKTg.R5YKtPQhUhaUDuOMz52wzwKNchk') 

