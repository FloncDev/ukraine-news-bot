import discord
from discord.ext import commands
from console import Console
import sql

console = Console(True)

class server_check(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            if not sql.is_registered(guild.id):
                sql.add_server(guild.id)
                console.log(f"Bot joined guild while offline. Added {guild.id} to the database.")

def setup(client):
    client.add_cog(server_check(client))