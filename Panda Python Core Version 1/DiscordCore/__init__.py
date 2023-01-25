import os
import discord
from discord.ext import commands

class DiscordCore(discord.Client):
    def __init__(self, command_prefix="!", intents=None, on_member_join_method=None):
        if intents == None:
            intents = discord.Intents.all()
        self.command_prefix = command_prefix
        self.on_member_join_method = on_member_join_method
        super().__init__(intents=intents)

    async def on_ready(self):
        print("Successfully logged in as {0.user}".format(self))

    async def on_member_join(self, member):
        if not self.on_member_join_method == None:
            self.on_member_join_method(member, member.guild)