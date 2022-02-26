import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from console import Console
import sql

console = Console(True)

class config_class(commands.Cog):

    def __init__(self, client):
        self.client = client
 
    @slash_command(name="config", description="Decide what channel the bot posts news to.")
    async def config(self, ctx, channel: Option(discord.TextChannel, "The channel where the news will go.")):
        if ctx.author.guild_permissions.administrator:
            sql.edit_server(ctx.guild.id, channel.id)
            await ctx.respond(f"The news will now be posted to {channel.mention}.", ephemeral=True)
            console.log(f"{ctx.author.id} changed the news channel to {channel.name}({channel.id}) in {ctx.guild.id}.")

        else:
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)

def setup(client):
    client.add_cog(config_class(client))