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
    await Client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = " TM's Community"))
    print('Client finished setting up')
    guild = Client.get_guild(923982879082561627)
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
    Channel = Client.get_channel(923990187812474900)

    Embed = discord.Embed(title="Member Joined", description=f'<@{Member.id}> joined our awesome community.', color=0x00ff00)
    Embed.add_field(name='Date of Assignation:', value=f'{Time}', inline=False)
    Embed.set_author(name='Welcome to TM Community', icon_url=Member.avatar_url)
    Embed.set_thumbnail(url=Member.avatar_url)

    Embed2 = discord.Embed(title="Welcome to TMFaisal's Discord Community", description=f'Please check our information and join the group. Also do not forget to invite a friend if you like it here!')
    Embed2.add_field(name='Information:', value='Our main [Discord](https://discord.gg/mfJ3UhXAJg)', inline=False)
    Embed2.set_author(name='Official TMFaisal Discord Community', icon_url=Member.avatar_url)
    Embed2.set_thumbnail(url=Member.avatar_url)

    await Channel.send(embed=Embed)
    await Member.send(embed=Embed2)
    database.execute("INSERT INTO Users (UserID, Time) VALUES (?, ?)", (Member.id, Time))
    Database.commit()

@Client.event
async def on_command_error(ctx, error):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")
    Channel = Client.get_channel(923989641160454174)
    Embed = discord.Embed(title="Error Was Found", description='If you think this is a mistake please contact the system developer.', color=0xe67e22)
    Embed.set_author(name='Error Logs', icon_url=ctx.author.avatar_url)
    Embed.set_thumbnail(url=ctx.author.avatar_url)
    Embed.add_field(name="Error Message:", value=f'__**{error}**__', inline=False)
    Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=Embed)
    await Channel.send(embed=Embed)
    pass


async def RoleChecker(ctx, User):

    guild = Client.get_guild(923982879082561627)
    role1 = [
        discord.utils.get(guild.roles, id=923986255933480960), #Developer
        discord.utils.get(guild.roles, id=923984807095058442), #Founder
        discord.utils.get(guild.roles, id=923985905570680872), #CM
        discord.utils.get(guild.roles, id=923985832338157608), #Trusted
        discord.utils.get(guild.roles, id=923985729976139797), #Staff
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
    Embed.set_author(name='Permission Error', icon_url=ctx.author.avatar_url)
    Embed.set_thumbnail(url=ctx.author.avatar_url)
    Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=Embed)


async def Logging(ctx, cmd, author: None, effected_member: None, Reason: None, Channelused: None):
    Channel = Client.get_channel(923989662333272164)
    today = date.today()
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    current_Date = today.strftime("%B %d, %Y")

    Embed = discord.Embed(title="Moderation Logs")
    Embed.set_author(name=author, icon_url=author.avatar_url)
    Embed.add_field(name='Command: ', value=f'{cmd}', inline=False)
    Embed.add_field(name='Used by: ', value=f'<@{author.id}>/{author}', inline=False)
    Embed.add_field(name='Effected User(s): ', value=f'<@{effected_member.id}>/{effected_member}', inline=False)
    Embed.add_field(name='Information: ', value=f'{Reason}', inline=False)
    Embed.add_field(name='Channel: ', value=f'<#{Channelused.id}>', inline=False)
    Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Embed.set_footer(text=f'Command used by {author}.', icon_url=ctx.author.avatar_url)
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
        Preview.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
        Preview.set_thumbnail(url=ctx.author.avatar_url)
        msg = await ctx.send(components = buttons2, embed=Preview)
        Interaction_Preview = await Client.wait_for("button_click", timeout=2629743,check=lambda inter: inter.message.id == msg.id)
        if Interaction_Preview.custom_id=='Accept' and Mode2 == "Everyone":
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}> with @everyone mention with announcement: __{Annoncement}__", ctx.channel)
            Main = discord.Embed(color=0x2ecc71)
            Main.add_field(name=f'{Title}',value=Annoncement, inline=False)
            Main.set_author(name=f'Important Announcement', icon_url=ctx.author.avatar_url)
            Main.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar_url)


            Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
            Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
            Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
            Accepted.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await msg.edit(embed=Accepted)
            await Interaction_Preview.disable_components()
            await Channel.send("@everyone", embed=Main)
        elif Interaction_Preview.custom_id=='Accept' and Mode2 == "Here":
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}> with @here mention with announcement: __{Annoncement}__", ctx.channel)
            Main = discord.Embed(color=0x2ecc71)
            Main.add_field(name=f'{Title}',value=Annoncement, inline=False)
            Main.set_author(name=f'Important Announcement', icon_url=ctx.author.avatar_url)
            Main.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar_url)

            Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
            Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
            Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
            Accepted.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar_url)

            await msg.edit(embed=Accepted)
            await Interaction_Preview.disable_components()
            await Channel.send("@here", embed=Main)
        elif Interaction_Preview.custom_id=='Accept' and Mode2 == "None":
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, F"Announced in <#{Channel.id}> with no mentions with announcement: __{Annoncement}__", ctx.channel)
            Main = discord.Embed(color=0x2ecc71)
            Main.add_field(name=f'{Title}',value=Annoncement, inline=False)
            Main.set_author(name=f'Important Announcement', icon_url=ctx.author.avatar_url)
            Main.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar_url)


            Accepted = discord.Embed(title=f"**{Title}**", description=f"Full announcement made by {ctx.author}: ", color=0x3498db)
            Accepted.add_field(name=f'__Announcement Accepted__', value=f'Announcement View: {Annoncement}', inline=False)
            Accepted.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
            Accepted.set_footer(text=f'Announced by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await msg.edit(embed=Accepted)
            await Interaction_Preview.disable_components()
            await Channel.send(embed=Main)
        elif Interaction_Preview.custom_id=='Reject':
            Main = discord.Embed(title=f"**{Title}**", description=f"Full announcement rejected by {ctx.author}: ", color=0xe74c3c)
            Main.add_field(name=f'__Announcement: __', value=Annoncement, inline=False)
            Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
            Main.set_thumbnail(url=ctx.author.avatar_url)
            Main.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
    Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    Embed.set_thumbnail(url=ctx.author.avatar_url)
    Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
    Main.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=Main)
    Home = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[0]}**__", color=0x7289da)
    Home.add_field(name='You will find here: ', value='__**Moderation and Adminstration, Information, Fun, and Misc.**__', inline=False)
    Home.set_thumbnail(url=ctx.author.avatar_url)
    Home.set_footer(text=f' Page 1/5', icon_url=ctx.author.avatar_url)
    Home.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
    msg = await ctx.author.send(components=Preview_Buttons, embed=Home)
    Interaction_Home= await Client.wait_for("button_click", timeout=2629743,check=lambda inter: inter.message.id == msg.id)
    Current_Page = 1
    while True:
        if Interaction_Home.custom_id == 'Next' and Current_Page == 1:
            Current_Page = Current_Page + 1
            Moderation = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[2]}**__", color=0x7289da)
            Moderation.set_thumbnail(url=ctx.author.avatar_url)
            Moderation.add_field(name='Moderation: ', value='''

`,Ban [User] [Reason] [Evidence]`

`,Unban [User] [Reason] [Evidence]`

`,SoftBan [User] [Reason]` (WIP) 

`,Kick [User] [Reason] [Evidence]`

`,Purge [Amount]`

`,Slowmode [Channel] [Amount]`

`,Warn [User] [Reason and Evidence]`

`,Warnings [User]`

`,ClearWarnings [User] [Reason]` 

`,Case [Case ID]`

`,Appeal [Stirke Code] [Title] [Appeal]`

`,Defean [User] [Reason]` (WIP)

`,Undefean [User] [Reason]` (WIP)
            
`,Mute [User] [Amount/Perm] [Reason]` (WIP)

`,Lock [Channel] [Time] [Reason]`

`,Unmute [User]` (WIP)
            
            ''', inline=False)
            Moderation.set_footer(text=f' Page 2/5', icon_url=ctx.author.avatar_url)
            Moderation.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
            await Interaction_Home.edit_origin(components=Preview_Buttons, embed=Moderation)
            Interaction_Moderation= await Client.wait_for("button_click",check=lambda inter: inter.message.id == msg.id)
        elif Interaction_Moderation.custom_id == 'Next' and Current_Page == 2:
            Current_Page = Current_Page + 1
            Information = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[3]}**__", color=0x7289da)
            Information.set_thumbnail(url=ctx.author.avatar_url)
            Information.add_field(name='Information: ', value='''

`,Announce [Channel] [Mode = Everyone/Here/None] [Title] [Announcement]`

`,Time`

`,User [User]`

`,Rules`

`,Help`

`,Version`

`,Documents` (WIP)
            
            ''', inline=False)
            Information.set_footer(text=f' Page 3/5', icon_url=ctx.author.avatar_url)
            Information.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
            await Interaction_Moderation.edit_origin(components=Preview_Buttons, embed=Information)
            Interaction_Information= await Client.wait_for("button_click", timeout=2629743,check=lambda inter: inter.message.id == msg.id)
        elif Interaction_Information.custom_id == 'Next' and Current_Page == 3:
            Current_Page = Current_Page + 1
            Fun = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[1]}**__", color=0x7289da)
            Fun.set_thumbnail(url=ctx.author.avatar_url)
            Fun.add_field(name='Fun: ', value='''

`None`

            
            ''', inline=False)
            Fun.set_footer(text=f' Page 4/5', icon_url=ctx.author.avatar_url)
            Fun.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
            await Interaction_Information.edit_origin(components=Preview_Buttons, embed=Fun)
            Interaction_Fun= await Client.wait_for("button_click",check=lambda inter: inter.message.id == msg.id)
        elif Interaction_Fun.custom_id == 'Next' and Current_Page == 4:
            Current_Page = Current_Page + 1
            Misc = discord.Embed(title="**Help System**", description=f"Page information: __**{Pages[4]}**__", color=0x7289da)
            Misc.set_thumbnail(url=ctx.author.avatar_url)
            Misc.add_field(name='Misc: ', value='''

`,Ping`

            
            ''', inline=False)
            Misc.set_footer(text=f' Page 5/5', icon_url=ctx.author.avatar_url)
            Misc.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
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
            Channel = Client.get_channel(923989641160454174)
            Embed = discord.Embed(title="Error Was Found", description='If you think this is a mistake please contact the system developer.', color=0xe67e22)
            Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            Embed.set_thumbnail(url=ctx.author.avatar_url)
            Embed.add_field(name="Error Message:", value=f'__**Please enter a valid number.**__', inline=False)
            Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await Channel.send(embed=Embed)
            await ctx.channel.send(embed=Embed)
        else:
            await ctx.channel.purge(limit = Amount)
            Embed = discord.Embed(title="Purge Command", description=f'Purged {Amount} message(s).', color=0xe74c3c)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
            Channel = Client.get_channel(923989641160454174)
            Embed = discord.Embed(title="Error Was Found", description='If you think this is a mistake please contact the system developer.', color=0xe67e22)
            Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            Embed.add_field(name="Error Message:", value=f'__**Please enter a valid number.**__', inline=False)
            Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await Channel.send(embed=Embed)
            await ctx.channel.send(embed=Embed)
        elif Amount == 0:
            Embed = discord.Embed(title="Slowmode Command", description=f'Slow mode is disabled, slow mode is now {Amount} second(s) per message.', color=0x00ff00)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.channel.send(embed=Embed)
        else:
            Embed = discord.Embed(title="Slowmode Command", description=f'Slow mode is enabled, slow mode is now {Amount} second(s) per message', color=0x95a5a6)
            Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
            Embed.set_author(name='Kicked ', icon_url=Member.avatar_url)
            Embed.set_thumbnail(url=Member.avatar_url)
            Embed.set_footer(text=f'Kicked by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
            Request.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
            Request.set_author(name=f'{Member} ({Member.id})', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=Request)
        else:
            Nothign = discord.Embed(title="**Infraction Logs**", description=f"<@{Member.id}> was never warned, muted, kicked or banned by the bot.", color=0x9b59b6)
            Nothign.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
        Button(style=ButtonStyle.green, label='Bug Report', custom_id='Bug Report'),
        Button(style=ButtonStyle.green, label='Suggestion', custom_id='Suggestion'),
        Button(style=ButtonStyle.green, label='Moderation', custom_id='Moderation'),
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
    Message.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    Message.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=Message)

    Main = discord.Embed(title="**Ticket System**", description=f"Please reply with your ticket. Please provide **images/videos** to support your ticket.", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar_url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
    await ctx.author.send(embed=Main)
    Report = await Client.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Ticket System**", description=f"Ticket cancelled, please recreate your ticket and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_footer(text=f'Ticket by {ctx.author}.', icon_url=ctx.author.avatar_url)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
        Cancelled.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        Type = discord.Embed(title="Ticket Type", description='Please select the ticket type you want to make.', color=0x546e7a)
        Type.add_field(name='Please provide `Full Report`, `Evidence`,`User id`', value='Valid User Id: 565558626048016395/<@565558626048016395>', inline=False)
        Type.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Type.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        Type.set_thumbnail(url=ctx.author.avatar_url)
        Type.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)

        msg = await ctx.author.send(components=Report_Buttons,embed=Type)
        

        Interaction = await Client.wait_for("button_click", timeout=60) #check=lambda inter: inter.message.id == msg.id)

        if Interaction and Interaction.message.id == msg.id:
            TypeInteraction = Interaction.custom_id
            Report_Embed = discord.Embed(title="Ticket System Preview", description=f'Ticket Type: {TypeInteraction}', color=0xe91e63)
            Report_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
            Report_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Report_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Report_Embed.add_field(name='Note: ', value='If you do not get a response from a Moderator/Administrator within 48 hours please re-post a ticket.', inline=False)
            Report_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            Report_Embed.set_thumbnail(url=ctx.author.avatar_url)
            Report_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await Interaction.disable_components()
            await msg.edit(embed=Report_Embed, components=Preview_Buttons)
            Preview_Interaction = await Client.wait_for("button_click", timeout=60)
            if Preview_Interaction.custom_id == "Accept" and Preview_Interaction.message.id == msg.id:
                Text = None
                database.execute("INSERT INTO Ticket_logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Channel = Client.get_channel(923989676677812244)
                Channel2 = Client.get_channel(923989737130307605)
                Final_Embed = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeInteraction}', color=0x546e7a)
                Final_Embed.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
                Final_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                Final_Embed.set_thumbnail(url=ctx.author.avatar_url)
                Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
                        Closed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        Closed_Embed.set_thumbnail(url=ctx.author.avatar_url)
                        Closed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
                        Claimed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        Claimed_Embed.set_thumbnail(url=ctx.author.avatar_url)
                        Claimed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
                        await Main_Interaction.edit_origin(embed=Claimed_Embed)    
                    elif Main_Interaction.custom_id == 'Note' and Main_Interaction.message.id == Main_Report.id:
                        Note = discord.Embed(title="Ticket System", description=f'Please reply with your note for this ticket.', color=0x546e7a)
                        Note.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Note.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        Note.set_thumbnail(url=ctx.author.avatar_url)
                        Note.set_footer(text=f'Requested by {Main_Interaction.user}.', icon_url=ctx.author.avatar_url)
                        await Main_Interaction.user.send(embed=Note)
                        await Main_Interaction.edit_origin(embed=Final_Embed)
                        NoteMsg = await Client.wait_for('message', check=lambda message: message.author.id == Main_Interaction.user.id)
                        if isinstance(NoteMsg.channel, discord.channel.TextChannel):
                            Cancelled2 = discord.Embed(title="**Ticket System**", description=f"Note cancelled, plase click back on note to create a new one.", color=0xe74c3c)
                            Cancelled2.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                            Cancelled2.set_footer(text=f'Ticket by {ctx.author}.', icon_url=ctx.author.avatar_url)
                            Cancelled2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
                            Cancelled2.set_thumbnail(url=ctx.author.avatar_url)
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
                                Claimed_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                Claimed_Embed1.set_thumbnail(url=ctx.author.avatar_url)
                                Claimed_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)                                
                                await Main_Interaction.user.send(embed=Claimed_Embed1)
                                await Main_Report.edit(embed=Claimed_Embed1)
                            elif CurrentType == "None" and Main_Interaction.message.id == Main_Report.id:
                                Final_Embed1 = discord.Embed(title="Ticket System", description=f'Ticket Type: {TypeInteraction}', color=0x546e7a)
                                Final_Embed1.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                                Final_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Final_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Final_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Final_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                Final_Embed1.set_thumbnail(url=ctx.author.avatar_url)
                                Final_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
                                await Main_Interaction.user.send(embed=Final_Embed1)
                                await Main_Report.edit(embed=Final_Embed1)
            elif Preview_Interaction.custom_id == "Reject" and Preview_Interaction.message.id == msg.id:
                Rejected = discord.Embed(title=f"Ticket Closed by {Preview_Interaction.user.id}", description=f'Ticket Type: {Interaction.custom_id}', color=0xe74c3c)
                Rejected.add_field(name='Ticket Code: ', value=f'#{Number}/{Code}', inline=False)
                Rejected.add_field(name='Report: ', value=Report.content, inline=False)
                Rejected.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Rejected.add_field(name='Note: ', value='Your ticket was closed.', inline=False)
                Rejected.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                Rejected.set_thumbnail(url=ctx.author.avatar_url)
                Rejected.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
            Embed.set_author(name=f'{User} ({User.id})', icon_url=User.avatar_url)
            Embed.set_thumbnail(url=User.avatar_url)
            Embed.set_footer(text=f'Banned by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
    Message.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    Message.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=Message)

    Main = discord.Embed(title="**Appeal System**", description=f"Please reply with your appeal. Please provide **images/videos** to support your appeal.", color=0xe67e22)
    Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
    Main.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar_url)
    Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
    await ctx.author.send(embed=Main)
    Report = await Client.wait_for('message', check=lambda message: message.author == ctx.author)

    if isinstance(Report.channel, discord.channel.TextChannel):
        Cancelled = discord.Embed(title="**Appeal System**", description=f"Appeal cancelled, please recreate your appeal and reply in Direct Messages", color=0xe74c3c)
        Cancelled.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Cancelled.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar_url)
        Cancelled.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
        Cancelled.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.author.send(embed=Cancelled)
    elif isinstance(Report.channel, discord.channel.DMChannel):
        Type = discord.Embed(title="Appeal Type", description='Please select the appeal type you want to make.', color=0x546e7a)
        Type.add_field(name='Please provide `Full Report`, `Evidence`,`User id`', value='Valid User Id: 565558626048016395/<@565558626048016395>', inline=False)
        Type.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Type.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        Type.set_thumbnail(url=ctx.author.avatar_url)
        Type.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)

        msg = await ctx.author.send(components=Report_Buttons,embed=Type)
        

        Interaction = await Client.wait_for("button_click", timeout=60) #check=lambda inter: inter.message.id == msg.id)

        if Interaction and Interaction.message.id == msg.id:
            TypeInteraction = Interaction.custom_id
            Report_Embed = discord.Embed(title="Appeal System Preview", description=f'Appeal Type: {TypeInteraction}', color=0xe91e63)
            Report_Embed.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
            Report_Embed.add_field(name='Report: ', value=Report.content, inline=False)
            Report_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
            Report_Embed.add_field(name='Note: ', value='If you do not get a response from a Moderator/Administrator within 48 hours please re-post a appeal.', inline=False)
            Report_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            Report_Embed.set_thumbnail(url=ctx.author.avatar_url)
            Report_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await Interaction.disable_components()
            await msg.edit(embed=Report_Embed, components=Preview_Buttons)
            Preview_Interaction = await Client.wait_for("button_click", timeout=60)
            if Preview_Interaction.custom_id == "Accept" and Preview_Interaction.message.id == msg.id:
                Text = None
                database.execute("INSERT INTO Appeal_Logs (Ticket) VALUES (?)", (Text,))
                Database.commit()
                Channel = Client.get_channel(923989721833672714)
                Channel2 = Client.get_channel(923989737130307605)
                Final_Embed = discord.Embed(title="Appeal System", description=f'Appeal Type: {TypeInteraction}', color=0x546e7a)
                Final_Embed.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                Final_Embed.add_field(name='Report: ', value=Report.content, inline=False)
                Final_Embed.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Final_Embed.add_field(name='Note: ', value=f'None', inline=False)
                Final_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                Final_Embed.set_thumbnail(url=ctx.author.avatar_url)
                Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
                        Closed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        Closed_Embed.set_thumbnail(url=ctx.author.avatar_url)
                        Closed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
                        Approved_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        Approved_Embed.set_thumbnail(url=ctx.author.avatar_url)
                        Approved_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
                        Claimed_Embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        Claimed_Embed.set_thumbnail(url=ctx.author.avatar_url)
                        Claimed_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
                        await Main_Interaction.edit_origin(embed=Claimed_Embed)    
                    elif Main_Interaction.custom_id == 'Note' and Main_Interaction.message.id == Main_Report.id:
                        Note = discord.Embed(title="Appeal System", description=f'Please reply with your note for this appeal.', color=0x546e7a)
                        Note.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                        Note.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        Note.set_thumbnail(url=ctx.author.avatar_url)
                        Note.set_footer(text=f'Requested by {Main_Interaction.user}.', icon_url=ctx.author.avatar_url)
                        await Main_Interaction.user.send(embed=Note)
                        await Main_Interaction.edit_origin(embed=Final_Embed)
                        NoteMsg = await Client.wait_for('message', check=lambda message: message.author.id == Main_Interaction.user.id)
                        if isinstance(NoteMsg.channel, discord.channel.TextChannel):
                            Cancelled2 = discord.Embed(title="**Appeal System**", description=f"Note cancelled, plase click back on note to create a new one.", color=0xe74c3c)
                            Cancelled2.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                            Cancelled2.set_footer(text=f'Appeal by {ctx.author}.', icon_url=ctx.author.avatar_url)
                            Cancelled2.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
                            Cancelled2.set_thumbnail(url=ctx.author.avatar_url)
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
                                Claimed_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                Claimed_Embed1.set_thumbnail(url=ctx.author.avatar_url)
                                Claimed_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)                                
                                await Main_Interaction.user.send(embed=Claimed_Embed1)
                                await Main_Report.edit(embed=Claimed_Embed1)
                            elif CurrentType == "None" and Main_Interaction.message.id == Main_Report.id:
                                Final_Embed1 = discord.Embed(title="Appeal System", description=f'Appeal Type: {TypeInteraction}', color=0x546e7a)
                                Final_Embed1.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                                Final_Embed1.add_field(name='Report: ', value=Report.content, inline=False)
                                Final_Embed1.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                                Final_Embed1.add_field(name='Note: ', value=f'{NoteMsg.content}', inline=False)
                                Final_Embed1.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                Final_Embed1.set_thumbnail(url=ctx.author.avatar_url)
                                Final_Embed1.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
                                await Main_Interaction.user.send(embed=Final_Embed1)
                                await Main_Report.edit(embed=Final_Embed1)
            elif Preview_Interaction.custom_id == "Reject" and Preview_Interaction.message.id == msg.id:
                Rejected = discord.Embed(title=f"Appeal Closed by {Preview_Interaction.user.id}", description=f'Appeal Type: {Interaction.custom_id}', color=0xe74c3c)
                Rejected.add_field(name='Appeal Code: ', value=f'#{Number}/{Code}', inline=False)
                Rejected.add_field(name='Report: ', value=Report.content, inline=False)
                Rejected.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
                Rejected.add_field(name='Note: ', value='Your appeal was closed.', inline=False)
                Rejected.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                Rejected.set_thumbnail(url=ctx.author.avatar_url)
                Rejected.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
    Channel = Client.get_channel(923989753098035290)
    if In_Group == True or ctx.author.guild_permissions.administrator:
        await Logging(ctx, ctx.message.content,ctx.author, Member, Reason, ctx.channel)
        Main = discord.Embed(title="**Infraction System**", description=f"Warned <@{Member.id}> successfully.")
        Main.add_field(name='Reason: ', value=f'__{Reason}__', inline=False)
        Main.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)

        
        User = discord.Embed(title="**Infraction System**", description=f"You've received a warning.")
        User.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
        User.add_field(name='Reason: ', value=f'__{Reason}__', inline=False)
        User.add_field(name='Date: ', value=f'{current_time}, {current_Date}', inline=False)
        User.set_author(name=f'{Member} ({Member.id})', icon_url=Member.avatar_url)

        Infraction = discord.Embed(title="**Infraction System**", description=f"<@{ctx.author.id}> warned <@{Member.id}>.")
        Infraction.add_field(name='**Infraction Code: **', value=f'{Number}/{Code1}', inline=False)
        Infraction.add_field(name='**Reason: **', value=f'__{Reason}__', inline=False)
        Infraction.add_field(name='**Date: **', value=f'{current_time}, {current_Date}', inline=False)
        Infraction.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
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
async def _ClearWarmomgs(ctx, Member: discord.Member, *, Reason):
    
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
        Main.set_author(name=f'{ctx.author} ({ctx.author.id})', icon_url=ctx.author.avatar_url)
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
Joined: {records0[0]}
''', inline=False)

        Main.set_author(name=f'{Member.id}', icon_url=MemberTag.avatar_url)
        Main.set_image(url=MemberTag.avatar_url)
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
        Final_Embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=Final_Embed)



@Client.command(aliases = ['Rule', 'Rules'], pass_context=True)
async def _Rule(ctx):
    await Logging(ctx, ctx.message.content,ctx.author, ctx.author, None, ctx.channel)
    Main2 = discord.Embed(title="**Rules**", description=f"All further information was directed into your Direct Messages/DMs.", color=0x7289da)
    Main2.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
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

`+` 13. All commands used should be used in its right [channels](https://discord.com/channels/923982879082561627/923999679358857276)

''', inline=False)
    Main.set_image(url="https://media.discordapp.net/attachments/857789246333386792/923983433292718160/31904e92-0548-45d2-962c-67af5e39ed11-profile_image-300x300.png?width=169&height=169")
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
            Close_Embed.set_footer(text=f'You should contact a system developer if you think this is a mistake.', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=Close_Embed)
        else:
            Final_Embed = discord.Embed(title="Lock System", description=f'<#{Channel.id}> was locked for {Amount} seconds.', color=0x546e7a)
            Final_Embed.set_footer(text=f'Locked by {ctx.author}.', icon_url=ctx.author.avatar_url)
            await Logging(ctx, ctx.message.content,ctx.author, ctx.author, f"Affected channel is <#{Channel.id}> for {Amount} seconds with the reason: {Reason}", ctx.channel)
            overwrite = Channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await Channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await Channel.send(embed=Final_Embed)
            time.sleep(Amount)
            Embed = discord.Embed(title="Lock System", description=f'<#{Channel.id}> was unlocked.', color=0x546e7a)
            Embed.set_footer(text=f'Locked by {ctx.author}.', icon_url=ctx.author.avatar_url)
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
                Embed.set_author(name=f'{User} ({User.id})', icon_url=User.avatar_url)
                Embed.set_thumbnail(url=User.avatar_url)
                Embed.set_footer(text=f'Unbanned by {ctx.author}.', icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=Embed)
                await ctx.guild.unban(user)
            elif User not in banned_members:
                Embed2 = discord.Embed(title="Ban System")
                Embed2.add_field(name=f'__**{User}**__ can not be unbanned because he wasn not banned in the first place.', value=f'{Reason}', inline=False)
                Embed2.set_author(name=f'{User} ({User.id})', icon_url=User.avatar_url)
                Embed2.set_thumbnail(url=User.avatar_url)
                Embed2.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=Embed2)



    
Client.run('OTIzOTg1MjU2NjExMjA5Mjc2.YcX-Uw.mDWA48vkeEMxPHPq3DGcoLDHdV0') 





# ODkxNjcyNzE0ODk5NzYzMjIw.YVBw7Q.PJ_8PKH3u4vgwm6uZvixO4bKZCQ

# OTA0NDUwODE0NjE2MTQxODI1.YX7tdg.f9kR32IFT7-AY9q2bm3qnkhEQt8


