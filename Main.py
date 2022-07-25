from ast import Num, Return
from code import interact
from curses.ascii import FF, isalnum, isdigit
from locale import currency
from logging import fatal
from multiprocessing import context
from platform import python_version
from pydoc import cli
from socket import timeout
from tokenize import group
from unicodedata import name
from urllib import response
from discord import ChannelType, Embed, InteractionResponse, Object, __version__ as discord_version, ui
from httpcore import Origin
from psutil import Process, virtual_memory
import datetime
from datetime import datetime, timedelta, date
import time
from time import sleep
from re import A
from sqlite3.dbapi2 import Cursor
import discord
import random
from typing import Final, Optional, Type, Union
from discord import embeds
from discord import channel
from discord import member
from discord.enums import try_enum
from discord.errors import PrivilegedIntentsRequired
from discord.ext import commands
import asyncio
import certifi
import aiohttp
from psycopg2 import connect
from collections import defaultdict
import discord.http, discord.state
from discord.utils import MISSING
from typing import Literal
import os
from pyparsing import col
import roblox
from roblox import Client, AvatarThumbnailType
import easy_pil
from easy_pil import *
import secrets
from secrets import * 
from discord import app_commands
from discord.app_commands import CommandTree


client = Client(os.environ['Roblox_TOKEN'])
Client_Bot = commands.Bot(command_prefix=',',case_insensitive=True,intents=discord.Intents.all())
Client_Bot.remove_command("help")
Database = connect(host="containers-us-west-90.railway.app", database="railway", user="postgres", password=os.environ['Password'])
Cursor = Database.cursor()
Guild = object()

Blacklisted = []



async def RoleChecker(ctx, User):


    role1 = [
        discord.utils.get(ctx.guild.roles, id=995333270789165106), # Tester
        discord.utils.get(ctx.guild.roles, id=995333471289495652), # Supervisor
        discord.utils.get(ctx.guild.roles, id=995333162160894083), # Dev
    ]
    for Main in role1:
        for member in ctx.guild.members:
            if User == member:
                for role in member.roles:
                    if role == Main:
                        return True
    if User.id == 565558626048016395:
        return True
async def MissingPermission(ctx, Author):
    Embed = discord.Embed(title="Missing Permissions", description='You should contact a system developer if you think this is a mistake', color=0xe67e22)
    Embed.add_field(name='You are not authorised to use this command on this user', value='Permission 400', inline=False)
    Embed.set_author(name='Permission Error', icon_url=ctx.author.avatar.url)
    Embed.set_thumbnail(url=ctx.author.avatar.url)
    Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar.url)
    await ctx.channel.send(embed=Embed)
async def Logging(ctx, cmd, author: None, effected_member: None, Reason: None, Channelused: None):
    Channel = Client_Bot.get_channel(995410641630269561)
    today = date.today()
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d %Y")

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

@Client_Bot.event
async def on_ready():
    
    await Client_Bot.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = "Zo Staff"))
    guild = Client_Bot.get_guild(995332563281383508)
    for black in Blacklisted:
        User = await Client_Bot.fetch_user(black)
        print(User)
        await guild.ban(User)
    print(f'Logged in')
    print('------------------------------')

# __________ System ___________ # 

@Client_Bot.event
async def on_message_delete(message):
    if not message.author.bot:
        Channel = Client_Bot.get_channel(995409633936158761)
        today = date.today()
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        current_Date = today.strftime("%B %d %Y")

        Embed = discord.Embed(title="Message Logs", description=f'Message were sent by <@{message.author.id}>')
        Embed.add_field(name='Deleted message: ', value=f'''
```
{message.content}
```
        ''', inline=False)
        Embed.add_field(name='Channel: ', value=f'<#{message.channel.id}>', inline=False)
        Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        await Channel.send(embed=Embed)

@Client_Bot.event
async def on_message_edit(before,after):
    if not before.author.bot:
        Channel = Client_Bot.get_channel(995409633936158761)
        today = date.today()
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        current_Date = today.strftime("%B %d %Y")

        Embed = discord.Embed(title="Message Logs", description=f'Message were edited by <@{before.author.id}>')
        Embed.add_field(name='Before: ', value=f'''
{before.content}
        ''', inline=False)
        Embed.add_field(name='After: ', value=f'''
{after.content}
        ''', inline=False)
        Embed.add_field(name='Channel: ', value=f'<#{before.channel.id}>', inline=False)
        Embed.add_field(name='Jump to message: ', value=f'[Message link](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id})', inline=False)
        Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        await Channel.send(embed=Embed)
        await Client_Bot.process_commands(before)

tree = Client_Bot.tree

@Client_Bot.command(aliases = ['Sync'])
async def _SyncApp(ctx):
    if ctx.author.guild_permissions.administrator:
        Channel = Client_Bot.get_channel(995409465509691412)
        Sync_Message = await tree.sync(guild=discord.Object(995332563281383508))
        Embed = discord.Embed(title="Console Report", color=0x44ff81)
        Embed.add_field(name='Application Synced by: ', value=f'{ctx.author.mention}/`{ctx.author.id}`')
        Embed.add_field(name='Successful? ', value=f'`True`')
        await ctx.message.reply('Synced!')
        await Channel.send(embed=Embed)
    else:
        Channel = Client_Bot.get_channel(995409465509691412)
        Embed = discord.Embed(title="Console Report", color=0xff4d44)
        Embed.add_field(name='Application Synced by: ', value=f'{ctx.author.mention}/`{ctx.author.id}`')
        Embed.add_field(name='Successful? ', value=f'`False`')
        await ctx.message.reply('You are not allowed to use this command!')
        await Channel.send(embed=Embed)

@Client_Bot.tree.context_menu(name='Message Report', guild=discord.Object(id=995332563281383508))
async def message_report(interaction: discord.Interaction, message: discord.Message):  
    Channel = Client_Bot.get_channel(995408854449918083)
    Time3 = f'{message.created_at.timestamp()}'
    Time2 = None
    for i in Time3.splitlines():
        Time2 = i.split('.')[0]
    Time5 = f'{interaction.created_at.timestamp()}'
    Time4 = None
    for i in Time5.splitlines():
        Time4 = i.split('.')[0]
    # Function Code #
    Message = discord.Embed(title="Moderation Alert", description='All active moderators, please handle the situation: ', color=0x546e7a)
    Message.add_field(name='Message ID: ', value=f'`{message.id}`', inline=False)
    Message.add_field(name='Who wrote the message? ', value=f'`{message.author}/`<@{message.author.id}>', inline=False)
    Message.add_field(name='Who reported the message? ', value=f'`{interaction.user}/`<@{interaction.user.id}>', inline=False)
    Message.add_field(name='When? ', value=f'<t:{Time2}:F> <t:{Time2}:R>', inline=False)
    Message.add_field(name='Where? ', value=f'<#{message.channel.id}>', inline=False)
    Message.add_field(name='Date of the report: ', value=f'<t:{Time4}:F> <t:{Time4}:R>', inline=False)
    Message.add_field(name='Message:', value=f'''
```
{message.content}
```
    ''', inline=False)
    Message.add_field(name='Jump to message: ', value=f'[Message link](https://discord.com/channels/{interaction.guild.id}/{message.channel.id}/{message.id})', inline=False)
    await Channel.send("All active <@&995333270789165106>, please handle this situation: ", embed=Message)
    await interaction.response.send_message(f'Thanks for your report! Reported Message: `{message.content}`', ephemeral=True) 

@Client_Bot.tree.context_menu(name='Get User ID', guild=discord.Object(id=995332563281383508))
async def userId(interaction: discord.Interaction, member: discord.User):  
    await interaction.response.send_message(f'`{member.id}`', ephemeral=True)

@Client_Bot.tree.context_menu(name='Get User Information', guild=discord.Object(id=995332563281383508))
async def userId(interaction: discord.Interaction, member: discord.User):  
    Time3 = f'{member.created_at.timestamp()}'
    Time2 = None
    for i in Time3.splitlines():
        Time2 = i.split('.')[0]
    Time4 = f'{member.joined_at.timestamp()}'
    Time5 = None
    for i in Time4.splitlines():
        Time5 = i.split('.')[0]

    Main = discord.Embed(title="**User Information**", description=f"Information on <@{member.id}>: ")
    Main.add_field(name='Discord: ', value=f'''
User Id: {member.id}
User Tag: {member}
User: <@{member.id}>
Nickname: {member.display_name}
Joined: <t:{Time5}:F> <t:{Time5}:R>
Created at: <t:{Time2}:F> <t:{Time2}:R>
    ''', inline=True)
    Main.set_author(name=f'{member.id}', icon_url=member.avatar.url)
    Main.set_thumbnail(url=member.avatar.url)

    await interaction.response.send_message(embed=Main,ephemeral=True)

@tree.command(guild=discord.Object(id=995332563281383508), description='Fetch user information!')
@app_commands.describe(user='The user you want to fetch their data.')
async def user(interaction: discord.Interaction, user: discord.User):
    in_group = False
    Time2 = None
    Time3 = f'{user.created_at.timestamp()}'
    for i in Time3.splitlines():
        Time2 = i.split('.')[0]
    for v in interaction.guild.members:
        if v.id == user.id:
            in_group = True

    # ____ Variables ____ #
    await interaction.response.defer(thinking=True)
    Main = discord.Embed(title="**User Information**", description=f"Information on <@{user.id}>: ")
    if in_group == True:
        Time4 = f'{user.joined_at.timestamp()}'
        Time5 = None
        for i in Time4.splitlines():
            Time5 = i.split('.')[0]
        Main.add_field(name='Discord: ', value=f'''
User Id: {user.id}
User Tag: {user}
User: <@{user.id}>
Nickname: {user.display_name}
Joined: <t:{Time5}:F> <t:{Time5}:R>
Created at: <t:{Time2}:F> <t:{Time2}:R>
    ''', inline=True)
    elif in_group == False:
        Main.add_field(name='Discord: ', value=f'''
User Id: {user.id}
User Tag: {user}
User: <@{user.id}>
Nickname: {user.display_name}
Created at: <t:{Time2}:F> <t:{Time2}:R>
    ''', inline=True)
    Main.set_author(name=f'{user.id}', icon_url=user.avatar.url)
    Main.set_thumbnail(url=user.avatar.url)
    await interaction.followup.send(embed=Main,ephemeral=False)

@tree.command(guild=discord.Object(id=995332563281383508), description='Administrative Command to Sync all Applications!')
async def sync(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    if interaction.user.guild_permissions.administrator:
        Channel = Client_Bot.get_channel(995409465509691412)
        Sync_Message = await tree.sync(guild=discord.Object(995332563281383508))
        Embed = discord.Embed(title="Console Report", color=0x44ff81)
        Embed.add_field(name='Application Synced by: ', value=f'{interaction.user.mention}/`{interaction.user.id}`')
        Embed.add_field(name='Successful? ', value=f'`True`')
        await interaction.followup.send(content='Synced', ephemeral=True)
        await Channel.send(embed=Embed)
    else:
        Channel = Client_Bot.get_channel(995409465509691412)
        Embed = discord.Embed(title="Console Report", color=0xff4d44)
        Embed.add_field(name='Application Synced by: ', value=f'{interaction.user.mention}/`{interaction.user.id}`')
        Embed.add_field(name='Successful? ', value=f'`False`')
        await interaction.followup.send('You are not allowed to use this command!')
        await Channel.send(embed=Embed)

@tree.command(guild=discord.Object(id=995332563281383508), description='Creates private channels for premium users!')
@app_commands.describe(channel_type='What channel do you want to be made?', channel_name='What do you want to name your channel?')
async def create(interaction2: discord.Interaction, channel_type: Literal['Thread', 'Voice Channel'], channel_name: str):
    class Button(discord.ui.View):
        @discord.ui.button(label='Archive Thread', style=discord.ButtonStyle.red)
        async def archive_button(self, interaction: discord.Interaction, archived_button_thread: discord.ui.Button):  
            if interaction.user.id == interaction2.user.id:
                await interaction.response.edit_message(view=view)
                await Thread.edit(name=f'Archived: {channel_name}', archived=True)
            else:
                await interaction.response.send_message("You're not allowed to use this command!", ephemeral=True)
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 

    Is_Allowed = False
    role = [
        discord.utils.get(interaction2.guild.roles, id=995333270789165106), # Tester
        discord.utils.get(interaction2.guild.roles, id=995333471289495652), # Supervisor
        discord.utils.get(interaction2.guild.roles, id=995333162160894083), # Dev
    ]
    for Main in role:
        for member in interaction2.guild.members:
            if interaction2.user == member:
                for role in member.roles:
                    if role == Main:
                        Is_Allowed = True

    if Is_Allowed == True:
        if channel_type == 'Thread':
            if interaction2.guild.premium_tier == 2 or interaction2.guild.premium_tier == 3:
                Thread_Embed = discord.Embed(title=F"{interaction2.user}'s Thread", description=f"""
Welcome {interaction2.user} to your private thread, here you're can talk about anything you want **but NSFW**. You can add anyone by mentioning them in the thread and they will be added. 

<:dot:997510484112724109> To report a user, please contact a developer and mention them in this thread so they can be added. 
<:dot:997510484112724109> If the channel was archived, moderators are allowed to review it for any hostile/NSFW behaviour.
        
                """,color=0x60ff6e)
                Thread = await interaction2.channel.create_thread(name=F"{channel_name}", message=None, auto_archive_duration=10080, type=ChannelType.private_thread, reason=None)
                view = Button(timeout=15780000)
                view.message = await Thread.send(f'{interaction2.user.mention}', embed=Thread_Embed, view=view)
            elif interaction2.guild.premium_tier == 1 or interaction2.guild.premium_tier == 0:
                Thread_Embed = discord.Embed(title=F"{interaction2.user}'s Thread", description=f"""
            
Welcome {interaction2.user} to your thread, here you're can talk about anything you want **but NSFW**. You can add anyone by mentioning them in the thread and they will be added. 

<:dot:997510484112724109> To report a user, please contact a developer and mention them in this thread so they can be added. 
<:dot:997510484112724109> If the channel was archived, moderators are allowed to review it for any hostile/NSFW behaviour.
        
                """,color=0x60ff6e)
                Thread = await interaction2.channel.create_thread(name=F"{channel_name}", message=None, auto_archive_duration=10080, type=ChannelType.public_thread, reason=None)
                await interaction2.response.send_message('Thread created!', ephemeral=True)
                view = Button(timeout=15780000)
                view.message = await Thread.send(f'{interaction2.user.mention}', embed=Thread_Embed, view=view)
        elif channel_type == 'Voice Channel':
            VC = await interaction2.guild.create_voice_channel(name=f'{channel_name}', category=discord.utils.get(interaction2.guild.categories, id=995332563864408195))
            await VC.set_permissions(target=interaction2.user, manage_channels=True, connect=True, manage_permissions=True, deafen_members=False, mute_members=False)
            await interaction2.response.send_message('VC created!', ephemeral=True)
    else:
            await interaction2.response.send_message("You're not allowed to use this command!", ephemeral=True)

@tree.command()
async def robloxs(interaction: discord.Interaction):
    await interaction.response.send_message("Roblox Command Activated",ephemeral=True)

group2 = app_commands.Group(name="roblox", description="Roblox related Command!")

@group2.command(description='Fetch Roblox information about a user!', name='search')
@app_commands.describe(data_type='Do you want to search by Roblox ID or Username?', target='The targeted user to fetch their data.')
async def search(interaction: discord.Interaction, data_type: Literal['Roblox ID', 'Username'], target: str):
    class options(discord.ui.Select):
        def __init__(self):
            Options = [
                discord.SelectOption(label='Friend List'),
                discord.SelectOption(label='Home Page'),
            ]
            super().__init__(placeholder='Pick an Option: ', min_values=1, max_values=1, options=Options)
        async def callback(self, interaction2: discord.Interaction):
            if interaction2.user.id == interaction.user.id:
                if self.values[0] == 'Home Page':
                    if target.isdigit() == True and data_type == 'roblox id':
                        fetched_data = await client.get_user(target)
                        # ———————————————————————- Data ————————————————————————— #
                        badge_list = []
                        fetched_friend = await fetched_data.get_friend_count()
                        badges = await fetched_data.get_roblox_badges()
                        totalstamp = f'{fetched_data.created.timestamp()}'
                        followers = await fetched_data.get_follower_count()
                        following = await fetched_data.get_following_count()
                        timestamp1 = None
                        for v in badges:
                            badge_list.append(v.name)
                        for i in totalstamp:
                            timestamp1 = totalstamp.split('.')[0]
                        user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(users=[fetched_data], type=AvatarThumbnailType.headshot, size=(420, 420))
                        # ———————————————————————- Variables ————————————————————————— #
                        data_embed = discord.Embed(title=f'Information on {fetched_data.name}', description=f"""

__Roblox Username:__ [{fetched_data.name}](https://www.roblox.com/users/{fetched_data.id}/profile)
__Roblox ID:__ {fetched_data.id}
__Display Name:__ {fetched_data.display_name}
__Creation Date:__ <t:{timestamp1}:F>
_ _

                        
                        """, color=0xffad00)
                        data_embed.set_footer(text=f'Requested by {interaction.user}!', icon_url=user_thumbnails[0].image_url)
                        data_embed.set_thumbnail(url=user_thumbnails[0].image_url)
                        data_embed.add_field(name='Friend List:', value=f"There is [{fetched_friend} Friend](https://www.roblox.com/users/{fetched_data.id}/friends#!/friends) on {fetched_data.name}'s  Friend List!", inline=False)
                        data_embed.add_field(name='Description:', value=f"""

```
{fetched_data.description}
```     
                        """, inline=False)
                        data_embed.add_field(name='Badges:', value=f"""

```
{badge_list}
```     
                        """, inline=False)  
                        data_embed.add_field(name='Is banned?', value=f"`{fetched_data.is_banned}`", inline=False)
                        data_embed.add_field(name='Following/Followers:', value=f"The {fetched_data.name} has [{followers} Followers](https://www.roblox.com/users/{fetched_data.id}/friends#!/followers) and [Following {following}](https://www.roblox.com/users/{fetched_data.id}/friends#!/following)", inline=False)
                        await interaction2.response.edit_message(embed=data_embed)
                    elif target.isdigit() == False and data_type == 'username':
                        fetched_data = await client.get_user_by_username(target)
                        # ———————————————————————- Data ————————————————————————— #
                        badge_list = []
                        fetched_friend = await fetched_data.get_friend_count()
                        badges = await fetched_data.get_roblox_badges()
                        totalstamp = f'{fetched_data.created.timestamp()}'
                        followers = await fetched_data.get_follower_count()
                        following = await fetched_data.get_following_count()
                        timestamp1 = None
                        for v in badges:
                            badge_list.append(v.name)
                        for i in totalstamp:
                            timestamp1 = totalstamp.split('.')[0]
                        user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(users=[fetched_data], type=AvatarThumbnailType.headshot, size=(420, 420))
                        # ———————————————————————- Variables ————————————————————————— #
                        data_embed = discord.Embed(title=f'Information on {fetched_data.name}', description=f"""

__Roblox Username:__ [{fetched_data.name}](https://www.roblox.com/users/{fetched_data.id}/profile)
__Roblox ID:__ {fetched_data.id}
__Display Name:__ {fetched_data.display_name}
__Creation Date:__ <t:{timestamp1}:F>
_ _

                        
                        """, color=0xffad00)
                        data_embed.set_footer(text=f'Requested by {interaction.user}!', icon_url=user_thumbnails[0].image_url)
                        data_embed.set_thumbnail(url=user_thumbnails[0].image_url)
                        data_embed.add_field(name='Friend List:', value=f"There is [{fetched_friend} Friend](https://www.roblox.com/users/{fetched_data.id}/friends#!/friends) on {fetched_data.name}'s  Friend List!", inline=False)
                        data_embed.add_field(name='Description:', value=f"""

```
{fetched_data.description}
```     
                        """, inline=False)
                        data_embed.add_field(name='Badges:', value=f"""

```
{badge_list}
```     
                        """, inline=False)  
                        data_embed.add_field(name='Is banned?', value=f"`{fetched_data.is_banned}`", inline=False)
                        data_embed.add_field(name='Following/Followers:', value=f"The {fetched_data.name} has [{followers} Followers](https://www.roblox.com/users/{fetched_data.id}/friends#!/followers) and [Following {following}](https://www.roblox.com/users/{fetched_data.id}/friends#!/following)", inline=False)
                        await interaction2.response.edit_message(embed=data_embed)
                elif self.values[0] == 'Friend List':
                    fetched_data2 = None
                    if data_type == 'roblox id':
                        fetched_data2 = await client.get_user(target)
                    elif data_type == 'username':
                        fetched_data2 = await client.get_user_by_username(target)
                    totalstamp1 = f'{fetched_data2.created.timestamp()}'
                    timestamp2 = None
                    for i in totalstamp1:
                        timestamp2 = totalstamp1.split('.')[0]
                    
                    friend_list = []
                    friend_fetched_List = await fetched_data2.get_friends()
                    for v in friend_fetched_List:
                        friend_list.append(v.name)
                    user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(users=[fetched_data2], type=AvatarThumbnailType.headshot, size=(420, 420))
                    friend_count = await fetched_data2.get_friend_count()
                    # ———————————————————————- Variables ————————————————————————— #
                    if friend_count == 0:
                        friend_embed = discord.Embed(title=f'Information on {fetched_data2.name}', description=f"""

__Roblox Username:__ [{fetched_data2.name}](https://www.roblox.com/users/{fetched_data2.id}/profile)
__Roblox ID:__ {fetched_data2.id}
__Display Name:__ {fetched_data2.display_name}
__Creation Date:__ <t:{timestamp2}:F>
_ _

**Friend List:** `This user has no friends!`
        
                        """, color=0xffad00)
                    else:
                        friend_embed = discord.Embed(title=f'Information on {fetched_data2.name}', description=f"""

__Roblox Username:__ [{fetched_data2.name}](https://www.roblox.com/users/{fetched_data2.id}/profile)
__Roblox ID:__ {fetched_data2.id}
__Display Name:__ {fetched_data2.display_name}
__Creation Date:__ <t:{fetched_data2}:F>
_ _

**Friend List: **
```{friend_list}```
        
                        """, color=0xffad00)
                    friend_embed.set_footer(text=f'Requested by {interaction.user}!', icon_url=user_thumbnails[0].image_url)
                    friend_embed.set_thumbnail(url=user_thumbnails[0].image_url)
                    await interaction2.response.edit_message(embed=friend_embed)
    class ListView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(options())

    Rolling_View = ListView()
    if target.isdigit() == True and data_type == 'Roblox ID':
        fetched_data = await client.get_user(target)
        # ———————————————————————- Data ————————————————————————— #
        badge_list = []
        fetched_friend = await fetched_data.get_friend_count()
        badges = await fetched_data.get_roblox_badges()
        totalstamp = f'{fetched_data.created.timestamp()}'
        followers = await fetched_data.get_follower_count()
        following = await fetched_data.get_following_count()
        timestamp1 = None
        for v in badges:
            badge_list.append(v.name)
        for i in totalstamp:
            timestamp1 = totalstamp.split('.')[0]
        user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(users=[fetched_data], type=AvatarThumbnailType.headshot, size=(420, 420))
        # ———————————————————————- Variables ————————————————————————— #
        data_embed = discord.Embed(title=f'Information on {fetched_data.name}', description=f"""

__Roblox Username:__ [{fetched_data.name}](https://www.roblox.com/users/{fetched_data.id}/profile)
__Roblox ID:__ {fetched_data.id}
__Display Name:__ {fetched_data.display_name}
__Creation Date:__ <t:{timestamp1}:F>
_ _

        
        """, color=0xffad00)
        data_embed.set_footer(text=f'Requested by {interaction.user}!', icon_url=user_thumbnails[0].image_url)
        data_embed.set_thumbnail(url=user_thumbnails[0].image_url)
        data_embed.add_field(name='Friend List:', value=f"There is [{fetched_friend} Friend](https://www.roblox.com/users/{fetched_data.id}/friends#!/friends) on {fetched_data.name}'s  Friend List!", inline=False)
        data_embed.add_field(name='Description:', value=f"""

```
{fetched_data.description}
```     
        """, inline=False)
        data_embed.add_field(name='Badges:', value=f"""

```
{badge_list}
```     
        """, inline=False)  
        data_embed.add_field(name='Is banned?', value=f"`{fetched_data.is_banned}`", inline=False)
        data_embed.add_field(name='Following/Followers:', value=f"The {fetched_data.name} has [{followers} Followers](https://www.roblox.com/users/{fetched_data.id}/friends#!/followers) and [Following {following}](https://www.roblox.com/users/{fetched_data.id}/friends#!/following)", inline=False)
        await interaction.response.send_message(embed=data_embed, view=Rolling_View)
    elif target.isdigit() == False and data_type == 'Username':
        fetched_data = await client.get_user_by_username(target)
        # ———————————————————————- Data ————————————————————————— #
        badge_list = []
        fetched_friend = await fetched_data.get_friend_count()
        badges = await fetched_data.get_roblox_badges()
        totalstamp = f'{fetched_data.created.timestamp()}'
        followers = await fetched_data.get_follower_count()
        following = await fetched_data.get_following_count()
        timestamp1 = None
        for v in badges:
            badge_list.append(v.name)
        for i in totalstamp:
            timestamp1 = totalstamp.split('.')[0]
        user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(users=[fetched_data], type=AvatarThumbnailType.headshot, size=(420, 420))
        # ———————————————————————- Variables ————————————————————————— #
        data_embed = discord.Embed(title=f'Information on {fetched_data.name}', description=f"""

__Roblox Username:__ [{fetched_data.name}](https://www.roblox.com/users/{fetched_data.id}/profile)
__Roblox ID:__ {fetched_data.id}
__Display Name:__ {fetched_data.display_name}
__Creation Date:__ <t:{timestamp1}:F>
_ _

        
        """, color=0xffad00)
        data_embed.set_footer(text=f'Requested by {interaction.user}!', icon_url=user_thumbnails[0].image_url)
        data_embed.set_thumbnail(url=user_thumbnails[0].image_url)
        data_embed.add_field(name='Friend List:', value=f"There is [{fetched_friend} Friend](https://www.roblox.com/users/{fetched_data.id}/friends#!/friends) on {fetched_data.name}'s  Friend List!", inline=False)
        data_embed.add_field(name='Description:', value=f"""

```
{fetched_data.description}
```     
        """, inline=False)
        data_embed.add_field(name='Badges:', value=f"""

```
{badge_list}
```     
        """, inline=False)  
        data_embed.add_field(name='Is banned?', value=f"`{fetched_data.is_banned}`", inline=False)
        data_embed.add_field(name='Following/Followers:', value=f"The {fetched_data.name} has [{followers} Followers](https://www.roblox.com/users/{fetched_data.id}/friends#!/followers) and [Following {following}](https://www.roblox.com/users/{fetched_data.id}/friends#!/following)", inline=False)
        await interaction.response.send_message(embed=data_embed, view=Rolling_View)
    else:
        await interaction.response.send_message('There was an error!')

tree.add_command(group2, guild=discord.Object(id=995332563281383508))

@tree.command(guild=discord.Object(id=995332563281383508), description='Testing command', name='test')
async def testing(interaction: discord.Interaction):
    background = Editor(Canvas((900, 200), color="#333333"))
    profile_pic = await load_image_async(str(interaction.user.avatar.url))
    image1 = await load_image_async('https://media.discordapp.net/attachments/986039876413694012/992548800877039667/unknown.png')
    profile = Editor(profile_pic).resize((110, 110)).rounded_corners()

    background.paste(image1,(-60, -170))
    background.paste(profile,(30, 55))
    background.text((157,100),f'{interaction.user}',font=Font.montserrat(size=30, variant='bold'),color="#FFFFFF")
    background.text((265,145),f'Rank 69',font=Font.montserrat(size=22, variant='bold'),color="#FFFFFF")
    background.text((158,145),f'Level 69',font=Font.montserrat(size=22, variant='bold'),color="#FFFFFF")
    background.text((600,145),f'69/96',font=Font.montserrat(size=22, variant='bold'),color="#FFFFFF")
    background.rectangle((157,130),width=60,height=2,color="#FFFFFF")
    background.rectangle((0,0),width=6,height=280,color="#FFFFFF")
    background.bar((30,170),max_width=650,height=20,color="#FFFFFF",radius=20,percentage=100)
    background.bar((30,170),max_width=650,height=20,color="#7671fd",radius=20,percentage=68) 
    file = discord.File(fp=background.image_bytes,filename="card.png")
    await interaction.response.send_message(file=file)

@tree.command()
async def temp(interaction: discord.Interaction):
    await interaction.response.send_message("Temp Command Activated",ephemeral=True)

group = app_commands.Group(name="temporary", description="Creates a temporary Channel/Voice/Role!")

@group.command(description='Creates a temporary Channel/Voice/Role!', name='create')
@app_commands.describe(data_type='What do you want to create.', length='For how long do you want it to last.', name='What do you want to call it.')
async def create(interaction: discord.Interaction, data_type: Literal['Channel', 'Voice', 'Role'], length: str, name: str = None):
    await RoleChecker(interaction, interaction.user)
    results = await RoleChecker(interaction, interaction.user)
    length_split = length.split()
    final_length = 0
    for word in length_split:
        print(length_split[0])
        if length_split[-1].startswith('w') or length_split[-1].startswith('weeks'):
            return
        elif length_split[-1].startswith('d') or length_split[-1].startswith('days'):
            return
        elif length_split[-1].startswith('h') or length_split[-1].startswith('hours'):
            int_seconds = int(length_split[0])
            time_in_seconds = int_seconds * 3600
            await interaction.response.send_message(f"Time in seconds: {time_in_seconds}(s) and time in hours {length_split[0]}(s) ")
            return
        else:
            await interaction.response.send_message('There was an error with the length please try again! Example: [10 hours]', ephemeral=True)
            return

    # _____________ Variables __________ #  
    if results == True or interaction.user.guild_permissions.administrator:
        if data_type == 'Channel':
            Channel = await interaction.guild.create_text_channel(name=f'{name}', category=discord.utils.get(interaction.guild.categories, id=996550874233053224))
            await Channel.set_permissions(target=interaction.user, manage_channels=True, manage_permissions=True)
            await interaction.response.send_message('Channel created!', ephemeral=True)
    else:
        await MissingPermission(interaction, interaction.user)


tree.add_command(group, guild=discord.Object(id=995332563281383508))


@tree.command()
async def count(interaction: discord.Interaction):
    await interaction.response.send_message("Staff Command Activated",ephemeral=True)

group1 = app_commands.Group(name="count", description="Role related Command!")

@group1.command(description='Counts how many members have that role!', name='members')
async def members(interaction: discord.Interaction, data: discord.Role):
    total_users = 0
    for member in interaction.guild.members:
        for role in member.roles:
            if role.id == data.id:
                total_users = total_users + 1
    await interaction.response.send_message(f'There are {total_users} member(s) with {data.mention}!', ephemeral=True)

@group1.command(description='Counts how many staff members there is!', name='staff')
async def staff(interaction: discord.Interaction):
    total_users = 0
    super_total_users = 0
    testers_total_users = 0
    management_total_users = 0
    for member in interaction.guild.members:
        for role in member.roles:
            if role.id == 995333270789165106:
                total_users = total_users + 1
    for member in interaction.guild.members:
        for role in member.roles:
            if role.id == 995333270789165106: # Tester
                testers_total_users = testers_total_users + 1
    for member in interaction.guild.members:
        for role in member.roles:
            if role.id == 995333471289495652: # Supervisor
                super_total_users = super_total_users + 1
    for member in interaction.guild.members:
        for role in member.roles:
            if role.id == 995333162160894083: #Management
                management_total_users = management_total_users + 1
    class options(discord.ui.Select):
        def __init__(self):
            Options = [
                discord.SelectOption(label='More Information'),
                discord.SelectOption(label='Home Page'),
            ]
            super().__init__(placeholder='Pick an Option: ', min_values=1, max_values=1, options=Options)
        async def callback(self, interaction2: discord.Interaction):
            if self.values[0] == 'Home Page':
                await interaction2.response.edit_message(embed=home_page, view=List_View)
            elif self.values[0] == 'More Information':
                await interaction2.response.send_message('Coming soon...', ephemeral=True)
    class ListView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(options())
    List_View = ListView()

    # ___________ Variables ___________ # 
    home_page = discord.Embed(title='Staff Statistics', description=f"""
    
<:dot:997510484112724109><@&995333270789165106>: `{testers_total_users}`
<:dot:997510484112724109><@&995333471289495652>: `{super_total_users}`
<:dot:997510484112724109><@&995333162160894083>: `{management_total_users}`
<:dot:997512758675378326> __Total Staff__: `{total_users}`
    
    
    """, color=0x992efc)
    await interaction.response.send_message(embed=home_page, view=List_View, ephemeral=True)

tree.add_command(group1, guild=discord.Object(id=995332563281383508))

@tree.command()
async def set(interaction: discord.Interaction):
    await interaction.response.send_message("Staff Command Activated",ephemeral=True)

group_set = app_commands.Group(name="set", description="Management related Command!")

@group_set.command(description='Sets inactivity notice for staff!', name='inactivity')
@app_commands.describe(start_date='When is your inactivity starts.', end_date='When is your inactivity ends.', reason='What is the reason for your inactivity.', note='Anything you wanted to add.')
async def inactivity(interaction: discord.Interaction, start_date: str, end_date: str, reason: str, note: str = None):
    await RoleChecker(interaction, interaction.user)
    results = await RoleChecker(interaction, interaction.user)
    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def approve_button(self, interaction2: discord.Interaction,approve: discord.ui.Button):  
            await RoleChecker(interaction, interaction.user)
            results2 = await RoleChecker(interaction, interaction.user)

            if results2 == True:
                approve.label = F'Approved by {interaction2.user}'
                for child in view.children:
                    child.disabled = True
                await interaction2.response.edit_message(view=view)
            else:
                await interaction2.response.send_message("You're not allowed to use this command", ephemeral=True)
        @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
        async def deny_button(self, interaction2: discord.Interaction,deny: discord.ui.Button):  
            await RoleChecker(interaction, interaction.user)
            results2 = await RoleChecker(interaction, interaction.user)

            if results2 == True:
                deny.label = F'Denied by {interaction2.user}'
                for child in view.children:
                    child.disabled = True
                await interaction2.response.edit_message(view=view)
            else:
                await interaction2.response.send_message("You're not allowed to use this command", ephemeral=True)
        @discord.ui.button(label='Get User', style=discord.ButtonStyle.blurple)
        async def user_button(self, interaction2: discord.Interaction,user: discord.ui.Button):  
            member = interaction.user
            Time3 = f'{member.created_at.timestamp()}'
            Time2 = None
            for i in Time3.splitlines():
                Time2 = i.split('.')[0]

            Main = discord.Embed(title="**User Information**", description=f"Information on <@{member.id}>: ")
            Main.add_field(name='Discord: ', value=f'''
User Id: {member.id}
User Tag: {member}
User: <@{member.id}>
Nickname: {member.display_name}
Created at: <t:{Time2}:F> <t:{Time2}:R>
            ''', inline=True)
            await interaction2.response.send_message(embed=Main, ephemeral=True)
            Main.set_author(name=f'{member.id}', icon_url=member.avatar.url)
            Main.set_thumbnail(url=member.avatar.url)
        @discord.ui.button(label=f'Notice from {interaction.user}/{interaction.user.id}', style=discord.ButtonStyle.gray, disabled=True)
        async def notice_from(self, interaction2: discord.Interaction,notice: discord.ui.Button):  
            await interaction2.response.send_message('If you get this message report it to the system developer!', ephemeral=True)
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 
        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    class Button2(discord.ui.View):
        @discord.ui.button(label='Post', style=discord.ButtonStyle.green)
        async def approve_button(self, interaction3: discord.Interaction,approve: discord.ui.Button):  
            for v in view2.children:
                v.disabled = True
            channel = interaction.guild.get_channel(998229994356609156)
            await channel.send(embed=notice, view=view)
            await interaction3.response.edit_message(view=view2)
        @discord.ui.button(label='Reject', style=discord.ButtonStyle.red)
        async def deny_button(self, interaction3: discord.Interaction,deny: discord.ui.Button):  
            for v in view2.children:
                v.disabled = True
            await interaction3.response.edit_message(view=view2)
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 

        # __________ Variables __________ #
    if results == True or interaction.user.guild_permissions.administrator:
        view2 = Button2(timeout=15780000)
        view = Button(timeout=15780000)
        notice = discord.Embed(title='Inactivity Notice', description=
f'''
<:dot:997510484112724109> Start Date: {start_date}
<:dot:997510484112724109> End Date: {end_date}

        
           ''', color=0xff4649)
        notice.add_field(name='Reason:', value=reason, inline=False)
        notice.add_field(name='Note:', value=note, inline=False)
        message = await interaction.response.send_message(embed=notice, view=view2, ephemeral=True)
    
tree.add_command(group_set, guild=discord.Object(id=995332563281383508))

@tree.command(guild=discord.Object(id=995332563281383508), description='Send a feedback to improve the quality of the development.', name='feedback')
@app_commands.describe(anonymous='Would you like the feedback to send anonymously or not.')
async def feedback(interaction: discord.Interaction, anonymous: Literal['True', 'False']):
    today = date.today()
    class feedback_page(ui.Modal, title='Feedback Page'):
        name = ui.TextInput(label='Title', placeholder='What is the feedback topic about?', max_length=180)
        answer = ui.TextInput(label='Feedback', style=discord.TextStyle.paragraph, placeholder='Place your entire feedback here', max_length=1500, min_length=10)

        async def on_submit(self, interaction2: discord.Interaction):
            if anonymous == 'True':
                channel = interaction.guild.get_channel(998365209016156270)
                anonymous_embed = discord.Embed(title=f"{self.name}", description=f"{self.answer}", color=0x36393F)
                anonymous_embed.set_footer(text=f'Anonymous Feedback • {today.day}/{today.month}/{today.year}')
                await channel.send(embed=anonymous_embed)
                await interaction2.response.send_message("Thanks for your feedback, your feedback was posted anonymously!", ephemeral=True)
            elif anonymous == 'False':
                channel = interaction.guild.get_channel(998365209016156270)
                public_embed = discord.Embed(title=f"{self.name}", description=f"{self.answer}", color=0x36393F)
                public_embed.set_footer(text=f'Feedback by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
                await channel.send(embed=public_embed)
                await interaction2.response.send_message("Thanks for your feedback!", ephemeral=True)


    await interaction.response.send_modal(feedback_page())

@tree.command(guild=discord.Object(id=995332563281383508), description='Calculate how much USD is to Robux!')
@app_commands.describe(payment_method= 'Fees and Payment method for the exchange.',value='What is the value you are trying to calculate.', currency='What is the currency you want to convert into.')
async def devex(interaction: discord.Interaction, currency: Literal['USD', 'Robux'],value: int, payment_method: Literal['Paypal', 'Wire Transfer', 'Check', 'Local bank / SEPA transfer / eCheck'] = None):
    today = date.today()
    if currency == 'Robux':
        total_value3 = value * 0.0035
        total_value4 = value * 0.0035
        total_value = round(total_value3)
        total_value2 = round(total_value4)
        if payment_method == 'Paypal':
            total_value = total_value - 1
            robux_devex = discord.Embed(title='Developer Exchange', description=f'''
`{value}` Robux converts to `{total_value}` USD **with** the fees
`{value}` Robux converts to `{total_value2}` USD **without** the fees
Fee Value: `1 USD`
            ''', color=0x54e445)
            robux_devex.set_footer(text=f'Requested by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=robux_devex, ephemeral=False)
        elif payment_method == 'Wire Transfer':
            total_value = total_value - 26
            robux_devex = discord.Embed(title='Developer Exchange', description=f'''
`{value}` Robux converts to `{total_value} USD` **with** the fees
`{value}` Robux converts to `{total_value2} USD` **without** the fees
Fee Value: `26 USD`
            ''', color=0x54e445)
            robux_devex.set_footer(text=f'Requested by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=robux_devex, ephemeral=False)
        elif payment_method == 'Check':
            total_value = total_value - 6
            robux_devex = discord.Embed(title='Developer Exchange', description=f'''
`{value}` Robux converts to `{total_value}` USD **with** the fees
`{value}` Robux converts to `{total_value2}` USD **without** the fees
Fee Value: `6 USD`
            ''', color=0x54e445)
            robux_devex.set_footer(text=f'Requested by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=robux_devex, ephemeral=False)
        elif payment_method == 'Local bank / SEPA transfer / eCheck':
            total_value = total_value - 5
            robux_devex = discord.Embed(title='Developer Exchange', description=f'''
`{value}` Robux converts to `{total_value}` USD **with** the fees
`{value}` Robux converts to `{total_value2}` USD **without** the fees
Fee Value: `5 USD`
            ''', color=0x54e445)
            robux_devex.set_footer(text=f'Requested by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=robux_devex, ephemeral=False)
        elif payment_method == None:
            robux_devex = discord.Embed(title='Developer Exchange', description=f'''
`{value}` Robux converts to `{total_value}` USD.
            ''', color=0x54e445)
            robux_devex.set_footer(text=f'Requested by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=robux_devex, ephemeral=False)
    elif currency == 'USD':
        total_value1 = value * 285.71
        total_value = round(total_value1)
        usd_devex = discord.Embed(title='Developer Exchange', description=f'''
`{value}` USD converts to `{total_value}` Robux.
            ''', color=0x54e445)
        usd_devex.set_footer(text=f'Requested by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=usd_devex)

@tree.command()
async def moderate(interaction: discord.Interaction):
    await interaction.response.send_message("Moderation Command Activated",ephemeral=True)

group_moderation = app_commands.Group(name="moderation", description="Moderation related Command!")

@group_moderation.command(description='Posts a moderation log.', name='create')
@app_commands.describe(username= 'The username of the Suspect.',reason='What did they do to get punished.', length='For how long is the ban going to stay.', note='Anything you want to add.', evidence='Evidence for your claims (links only)')
async def create(interaction: discord.Interaction, username: str, reason: Literal['Exploiting', 'Advertising', 'Excessive Spam', 'Inappropriate/Discriminatory Username/Display name', 'Misuse of Custom Kill Sound', 'Discriminatory Remarks', 'Inappropriate Remarks', 'Nudity', 'Inappropriate Avatar', 'Intentionally Impersonating a Community Member', 'Admission of the use of Exploits', 'Distribution of Exploits', 'Death Threats', 'Predatory Behaviour', 'Buying/Selling Accounts', 'Intentionally Impersonating a Staff Member', 'Stealing Works of Others', 'Grab/Leak Classified/Private Information', 'DDoS Attack/Threat', 'Bribery', 'Ban Evasion'], length: Literal['1 Day', '2 Days', '3 Days', '4 Days', '5 Days', '6 Days', '7 Days', 'Permanent'], evidence: str, note: str = None):
    today = datetime.today()
    Time2 = None
    BigSize = False
    Time3 = f'{today.timestamp()}'
    code1 = secrets.token_hex(4)
    code2 = secrets.token_hex(4)
    code3 = secrets.token_hex(4)
    code4 = secrets.token_hex(4)
    for i in Time3.splitlines():
        Time2 = i.split('.')[0]
    List = []
    NumberNew = 0
    evidence_split = evidence.split()
    for word in evidence_split:
        if word.startswith('https'):
            NumberNew = NumberNew + 1
            List.append(word)
    await RoleChecker(interaction, interaction.user)
    channel = interaction.guild.get_channel(1000449228662898768)
    results = await RoleChecker(interaction, interaction.user)
    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def approve_button(self, interaction2: discord.Interaction,approve: discord.ui.Button):  
            await RoleChecker(interaction, interaction.user)
            results2 = await RoleChecker(interaction, interaction.user)

            if results2 == True:
                approve.label = F'Approved by {interaction2.user}'
                for child in view.children:
                    child.disabled = True
                await interaction2.response.edit_message(view=view)
            else:
                await interaction2.response.send_message("You're not allowed to use this command", ephemeral=True)
        @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
        async def deny_button(self, interaction2: discord.Interaction,deny: discord.ui.Button):  
            await RoleChecker(interaction, interaction.user)
            results2 = await RoleChecker(interaction, interaction.user)

            if results2 == True:
                deny.label = F'Denied by {interaction2.user}'
                for child in view.children:
                    child.disabled = True
                await interaction2.response.edit_message(view=view)
            else:
                await interaction2.response.send_message("You're not allowed to use this command", ephemeral=True)
        @discord.ui.button(label='Get User', style=discord.ButtonStyle.blurple)
        async def user_button(self, interaction2: discord.Interaction,user: discord.ui.Button):  
            member = interaction.user
            Time3 = f'{member.created_at.timestamp()}'
            Time2 = None
            for i in Time3.splitlines():
                Time2 = i.split('.')[0]

            Main = discord.Embed(title="**User Information**", description=f"Information on <@{member.id}>: ")
            Main.add_field(name='Discord: ', value=f'''
User Id: {member.id}
User Tag: {member}
User: <@{member.id}>
Nickname: {member.display_name}
Created at: <t:{Time2}:F> <t:{Time2}:R>
            ''', inline=True)
            await interaction2.response.send_message(embed=Main, ephemeral=True)
            Main.set_author(name=f'{member.id}', icon_url=member.avatar.url)
            Main.set_thumbnail(url=member.avatar.url)
        @discord.ui.button(label=f'Notice from {interaction.user}/{interaction.user.id}', style=discord.ButtonStyle.gray, disabled=True)
        async def notice_from(self, interaction2: discord.Interaction,notice: discord.ui.Button):  
            await interaction2.response.send_message('If you get this message report it to the system developer!', ephemeral=True)
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 
        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    
    class Button2(discord.ui.View):
        @discord.ui.button(label='Post', style=discord.ButtonStyle.green)
        async def approve_button(self, interaction3: discord.Interaction,approve: discord.ui.Button):  
            for v in view2.children:
                v.disabled = True
            await channel.send(embed=Log, view=view)
            await interaction3.response.edit_message(view=view2)
        @discord.ui.button(label='Reject', style=discord.ButtonStyle.red)
        async def deny_button(self, interaction3: discord.Interaction,deny: discord.ui.Button):  
            for v in view2.children:
                v.disabled = True
            await interaction3.response.edit_message(view=view2)
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    # _____ Setup _____ #

    if results == True or interaction.user.guild_permissions.administrator:
        fetched_data = await client.get_user_by_username(username)
        if fetched_data:
            totalstamp = f'{fetched_data.created.timestamp()}'
            for i in totalstamp:
                timestamp1 = totalstamp.split('.')[0]
            user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(users=[fetched_data], type=AvatarThumbnailType.headshot, size=(420, 420))
            await interaction.response.defer(ephemeral=True, thinking=True)
            Log = discord.Embed(title=f'Punishment Code: {code1}-{code2}-{code3}-{code4}', description=f"""
<:dot:997510484112724109> Start Date: <t:{Time2}:F>
<:dot:997510484112724109> End Date: `{length}`
            """, color=0xfc393a)
            Log.add_field(name='Reason:', value=reason, inline=True)
            if NumberNew == 0:
                Log.add_field(name='Files: ', value='<:dot:997510484112724109> None', inline=True)
            elif NumberNew == 1:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]})', inline=True)
            elif NumberNew == 2:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]})', inline=True)
            elif NumberNew == 3:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=True)
            elif NumberNew == 4: 
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=True)
            elif NumberNew == 5:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=True)
            else:
                BigSize = True

            Log.add_field(name='Note:', value=note, inline=False)
            Log.add_field(name='User Information:', value=f"""
Roblox Username: [{fetched_data.name}](https://www.roblox.com/users/{fetched_data.id}/profile)
Roblox ID: `{fetched_data.id}`
Display Name: `{fetched_data.display_name}`
Creation Date: <t:{timestamp1}:F>
Description: `{fetched_data.description}`
        
        
        """, inline=False)
            Log.set_footer(text=f'Moderation by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
            Log.set_thumbnail(url=user_thumbnails[0].image_url)
            view2 = Button2(timeout=15780000)
            view = Button(timeout=15780000)
            if BigSize == True:
                await interaction.followup.send('Too many files/links (Only 5).', ephemeral=True)
            else:
                await interaction.followup.send(embed=Log, ephemeral=True, view=view2)
        else:
            await interaction.response.send_message('Invalid User!', ephemeral=True)
    else:
        await interaction.response.send_message("You're not allowed to use this command", ephemeral=True)

@group_moderation.command(description='Edits a moderation log.', name='edit')
@app_commands.describe(username= 'The username of the Suspect.',reason='Reason to adjust the punishment.', old_length='Previous moderation length.', length='For how long is the ban going to stay.', note='Anything you want to add/If you picked Others add the reason here.', evidence='Evidence for your claims (links only)', code='The previous punishment code.')
async def edit(interaction: discord.Interaction, username: str, reason: Literal['Exploiting', 'Ban Evasion', 'False Penalty','Ban Appeal', 'Other'], old_length: Literal['1 Day', '2 Days', '3 Days', '4 Days', '5 Days', '6 Days', '7 Days', 'Permanent'] ,length: Literal['1 Day', '2 Days', '3 Days', '4 Days', '5 Days', '6 Days', '7 Days', 'Permanent', 'Unban'], evidence: str, code: str,note: str = None):
    today = datetime.today()
    Time2 = None
    BigSize = False
    Time3 = f'{today.timestamp()}'
    for i in Time3.splitlines():
        Time2 = i.split('.')[0]
    List = []
    NumberNew = 0
    evidence_split = evidence.split()
    for word in evidence_split:
        if word.startswith('https'):
            NumberNew = NumberNew + 1
            List.append(word)
    await RoleChecker(interaction, interaction.user)
    channel = interaction.guild.get_channel(1000449228662898768)
    results = await RoleChecker(interaction, interaction.user)
    class Button(discord.ui.View):
        @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
        async def approve_button(self, interaction2: discord.Interaction,approve: discord.ui.Button):  
            await RoleChecker(interaction, interaction.user)
            results2 = await RoleChecker(interaction, interaction.user)

            if results2 == True:
                approve.label = F'Approved by {interaction2.user}'
                for child in view.children:
                    child.disabled = True
                await interaction2.response.edit_message(view=view)
            else:
                await interaction2.response.send_message("You're not allowed to use this command", ephemeral=True)
        @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
        async def deny_button(self, interaction2: discord.Interaction,deny: discord.ui.Button):  
            await RoleChecker(interaction, interaction.user)
            results2 = await RoleChecker(interaction, interaction.user)

            if results2 == True:
                deny.label = F'Denied by {interaction2.user}'
                for child in view.children:
                    child.disabled = True
                await interaction2.response.edit_message(view=view)
            else:
                await interaction2.response.send_message("You're not allowed to use this command", ephemeral=True)
        @discord.ui.button(label='Get User', style=discord.ButtonStyle.blurple)
        async def user_button(self, interaction2: discord.Interaction,user: discord.ui.Button):  
            member = interaction.user
            Time3 = f'{member.created_at.timestamp()}'
            Time2 = None
            for i in Time3.splitlines():
                Time2 = i.split('.')[0]

            Main = discord.Embed(title="**User Information**", description=f"Information on <@{member.id}>: ")
            Main.add_field(name='Discord: ', value=f'''
User Id: {member.id}
User Tag: {member}
User: <@{member.id}>
Nickname: {member.display_name}
Created at: <t:{Time2}:F> <t:{Time2}:R>
            ''', inline=True)
            await interaction2.response.send_message(embed=Main, ephemeral=True)
            Main.set_author(name=f'{member.id}', icon_url=member.avatar.url)
            Main.set_thumbnail(url=member.avatar.url)
        @discord.ui.button(label=f'Notice from {interaction.user}/{interaction.user.id}', style=discord.ButtonStyle.gray, disabled=True)
        async def notice_from(self, interaction2: discord.Interaction,notice: discord.ui.Button):  
            await interaction2.response.send_message('If you get this message report it to the system developer!', ephemeral=True)
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 
        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    
    class Button2(discord.ui.View):
        @discord.ui.button(label='Post', style=discord.ButtonStyle.green)
        async def approve_button(self, interaction3: discord.Interaction,approve: discord.ui.Button):  
            for v in view2.children:
                v.disabled = True
            await channel.send(embed=Log, view=view)
            await interaction3.response.edit_message(view=view2)
        @discord.ui.button(label='Reject', style=discord.ButtonStyle.red)
        async def deny_button(self, interaction3: discord.Interaction,deny: discord.ui.Button):  
            for v in view2.children:
                v.disabled = True
            await interaction3.response.edit_message(view=view2)
        def __init__(self, timeout):
            super().__init__(timeout=timeout)
            self.response = None 

        async def on_timeout(self):
            for child in self.children: 
                child.disabled = True
            await self.message.edit(view=self) 
    # _____ Setup _____ #

    if results == True or interaction.user.guild_permissions.administrator:
        fetched_data = await client.get_user_by_username(username)
        if fetched_data:
            totalstamp = f'{fetched_data.created.timestamp()}'
            for i in totalstamp:
                timestamp1 = totalstamp.split('.')[0]
            user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(users=[fetched_data], type=AvatarThumbnailType.headshot, size=(420, 420))
            await interaction.response.defer(ephemeral=True, thinking=True)
            Log = discord.Embed(title=f'Punishment Code: {code}', description=f"""

__Penalty Adjusted__ at <t:{Time2}:F>
<:dot:997510484112724109> From: `{old_length}`
<:dot:997510484112724109> To: `{length}`
            """, color=0xfc393a)
            Log.add_field(name='Reason:', value=reason, inline=True)
            if NumberNew == 0:
                Log.add_field(name='Files: ', value='<:dot:997510484112724109> None', inline=True)
            elif NumberNew == 1:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]})', inline=True)
            elif NumberNew == 2:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]})', inline=True)
            elif NumberNew == 3:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]}) / [File]({List[2]})', inline=True)
            elif NumberNew == 4: 
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]})', inline=True)
            elif NumberNew == 5:
                Log.add_field(name='Files: ', value=f'<:dot:997510484112724109> [File]({List[0]}) / [File]({List[1]}) / [File]({List[2]}) / [File]({List[3]}) / [File]({List[4]})', inline=True)
            else:
                BigSize = True

            Log.add_field(name='Note:', value=note, inline=False)
            Log.add_field(name='User Information:', value=f"""
Roblox Username: [{fetched_data.name}](https://www.roblox.com/users/{fetched_data.id}/profile)
Roblox ID: `{fetched_data.id}`
Display Name: `{fetched_data.display_name}`
Creation Date: <t:{timestamp1}:F>
Description: `{fetched_data.description}`
        
        
        """, inline=False)
            Log.set_footer(text=f'Moderation by {interaction.user} • {today.day}/{today.month}/{today.year}', icon_url=interaction.user.avatar.url)
            Log.set_thumbnail(url=user_thumbnails[0].image_url)
            view2 = Button2(timeout=15780000)
            view = Button(timeout=15780000)
            if BigSize == True:
                await interaction.followup.send('Too many files/links (Only 5).', ephemeral=True)
            else:
                await interaction.followup.send(embed=Log, ephemeral=True, view=view2)
        else:
            await interaction.response.send_message('Invalid User!', ephemeral=True)
    else:
        await interaction.response.send_message("You're not allowed to use this command", ephemeral=True)

tree.add_command(group_moderation, guild=discord.Object(id=995332563281383508))


# _______ Profile ________ #



@tree.command()
async def profile(interaction: discord.Interaction):
    await interaction.response.send_message("Profile Command Activated",ephemeral=True)

group_profile = app_commands.Group(name="profile", description="Profile related Command!")

@group_profile.command(description='Set up a profile for Staff Member!', name='create')
@app_commands.describe(user='Which Staff Member is the profile for.')
async def create(interaction: discord.Interaction, user: discord.Member = None):
    await interaction.response.defer(thinking=True, ephemeral=True)
    await RoleChecker(interaction, interaction.user)
    results = await RoleChecker(interaction, interaction.user)
    Selected_Code = "select id from staff"
    Cursor.execute(Selected_Code)
    records = Cursor.fetchall()
    record = None
    for record in records:
        print(record)
        print(record[-1])
        if user == None and record == interaction.user.id:
            await interaction.followup.send("You already have a profile on the Database.", ephemeral=True)
        elif user and record == user.id:
            await interaction.followup.send("This user already have a profile on the Database.", ephemeral=True)
    # _____ Variabls ______ #
    if results == True or interaction.user.guild_permissions.administrator:
        if user == None:
            Cursor.execute(f"insert into staff (id) values ({interaction.user.id})")
            Database.commit()
            await interaction.followup.send('Profile creation was successful for your account.', ephemeral=True)
        else:
            await RoleChecker(interaction, interaction.user)
            results2 = await RoleChecker(interaction, user) 
            if results2 == True:
                Cursor.execute(f"insert into staff (id) values ({user.id})")
                Database.commit()
                await interaction.followup.send(f'Profile creation was successful for {user}.', ephemeral=True)
            else:
                await interaction.followup.send(f'{user} is not a Staff Member, you can only set up a profile for Staff Members.', ephemeral=True)
    else:
        await interaction.followup.send("You're not allowed to use this command.", ephemeral=True)

@group_profile.command(description='Remove the setup for the Staff Member, but logs remain!', name='remove')
@app_commands.describe(user='Which Staff Member do you want to remove.')
async def remove(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message('Coming Soon')

@group_profile.command(description='View the profile of the chosen Staff Member.', name='view')
@app_commands.describe(user='Which Staff Member do you want to view.')
async def view(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message('Coming Soon')

tree.add_command(group_profile, guild=discord.Object(id=995332563281383508))



Client_Bot.run(os.environ['Token']) 


#    Selected_Code = "select thing from strike_logs"
#    Cursor.execute(Selected_Code)
#    records = Cursor.fetchall()

#    Cursor.execute(f"insert into ticket_logs (ticket) values ({random.randint(0,999999999999999999)})")
#    Database.commit()