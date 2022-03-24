import discord
from discord.ext import commands
from console import Console

console = Console(True)

class on_ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        console.info(f'{self.client.user.name} is online! Currently in {len(self.client.guilds)} guilds and serving {sum([guild.member_count for guild in self.client.guilds])} users.')
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/config (to configure)"))

def setup(client):
    client.add_cog(on_ready(client))