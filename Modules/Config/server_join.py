import discord
from discord.ext import commands
from console import Console
import sql

console = Console(True)

class guild_join(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        sql.add_server(guild.id)
        console.log(f"Bot joined {guild.id}.")

def setup(client):
    client.add_cog(guild_join(client))