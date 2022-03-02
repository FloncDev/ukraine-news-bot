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

        for guild_id in sql.get_guilds():
            guild_id = guild_id[0]
            if guild_id not in [guild.id for guild in self.client.guilds]:
                sql.remove_server(guild_id)
                console.log(f"Bot left guild while offline. Removed {guild_id} from the database.")

def setup(client):
    client.add_cog(server_check(client))