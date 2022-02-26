import discord
from discord.ext import commands
from console import Console

console = Console(True)

class on_ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        console.info(f'{self.client.user.name} is online!')

def setup(client):
    client.add_cog(on_ready(client))