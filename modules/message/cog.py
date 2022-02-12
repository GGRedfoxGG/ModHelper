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
import interactions
from interactions import *
from interactions.api.models.member import Member
from interactions.ext.wait_for import wait_for, setup
import asyncio
import certifi
import aiohttp
from sqlite3 import connect
from datetime import date, datetime
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


class Alert(slash_util.Cog):
    def __init__(self, bot: commands.bot):
        super().__init__(bot)

    @slash_util.message_command(guild_id=900845173989339186)
    async def Alert(self, ctx: slash_util.Context, message: discord.Message): 
        await ctx.send(message)




def setup(bot):
    bot.add_cog(Alert(bot))