import discord
from discord.ext import commands
import json

class embed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def embed(self, ctx, *, embedthing):
        if ctx.channel.id == 946912545720123422:
            embedthing = json.loads(embedthing)
            sendembed = discord.Embed.from_dict(embedthing)
            await ctx.send(embed=sendembed)

def setup(client):
    client.add_cog(embed(client))