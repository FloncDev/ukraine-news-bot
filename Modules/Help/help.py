import discord
from discord.ext import commands
from discord.commands import slash_command
from console import Console
import random

console = Console(True)

class help_class(commands.Cog):

    def __init__(self, client):
        self.client = client
 
    @slash_command(name="help", description="Send help message.")
    async def help(self, ctx):
        colour = random.choice([0x0057b7, 0xffd700])
        embed=discord.Embed(title="UNB Help", description="To configure the bot, use ...\n /config \n  - channel {channel} - Set the channel for the bot to post news in\n  - ping_roles {role} - Set the role to ping when breaking news is posted", colour=random.choice([0x0057b7, 0xffd700]))
        embed.add_field(name="Still not working?", value="Make sure the bot has permissions to send messages in the channel you set it for.", inline=False)
        embed.add_field(name="If you need more help..", value="Join the support server [here](https://discord.gg/9k59NxQ9wf)", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)

def setup(client):
    client.add_cog(help_class(client))
