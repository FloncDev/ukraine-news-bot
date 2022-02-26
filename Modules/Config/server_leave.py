import discord
from discord.ext import commands
from console import Console
import sql

console = Console(True)

class guild_remove(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        sql.remove_server(guild.id)
        console.log(f"Bot left {guild.id}.")

def setup(client):
    client.add_cog(guild_remove(client))