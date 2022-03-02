import discord
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup
from console import Console
import sql

console = Console(True)

class config_class(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    group = SlashCommandGroup("config", "Configure the bot.")
 
    @group.command(name="channel", description="Set the channel for news announcements.")
    async def channel(self, ctx, channel: Option(discord.TextChannel, "The channel where the news will go.")):
        if ctx.author.guild_permissions.administrator:
            sql.edit_server(ctx.guild.id, channel_id=channel.id)
            await ctx.respond(f"The news will now be posted to {channel.mention}.", ephemeral=True)
            console.log(f"{ctx.author.id} changed the news channel to {channel.name}({channel.id}) in {ctx.guild.id}.")

        else:
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)

    @group.command(name="ping_roles",description="Set the role to ping when the news is posted.")
    async def ping(self, ctx, role: Option(discord.Role, "The role to ping when the news is posted. To remove ping role, leave blank.") = None):
        if ctx.author.guild_permissions.administrator:
            if role is None:
                sql.edit_server(ctx.guild.id, role_id=None)
                await ctx.respond("The ping role has been removed.", ephemeral=True)
                console.log(f"{ctx.author.id} removed the ping role from {ctx.guild.id}.")
            else:
                sql.edit_server(ctx.guild.id, role_id=role.id)
                await ctx.respond(f"The ping role has been set to `{role}`.", ephemeral=True)
                console.log(f"{ctx.author.id} set the ping role to {role.name}({role.id}) in {ctx.guild.id}.")
        
        else:
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)

def setup(client):
    client.add_cog(config_class(client))