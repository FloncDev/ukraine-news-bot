import discord
from discord.ext import commands, tasks
from console import Console
import news
import json
from datetime import datetime
import sql
import random

console = Console(True)

with open("config.json", "r") as f:
    config = json.load(f)

class get_data_class(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.get_data.start()

    @tasks.loop(minutes=1)
    async def get_data(self):
        data = await news.get_data()
        if data:
            posted_in = 0
            guilds = []

            #Make our embed
            embed = discord.Embed(title=data["title"], description=data["content"])
            if data["image"]: embed.set_image(url=data["image"])
            if data["is_breaking"]: embed.set_author(name="BREAKING")
            embed.set_footer(text="🔴 Live News")
            
            locator = data["locator"]
            news_url = data["news_url"]
            embed.url = f"https://www.bbc.co.uk/news/live/world-europe-{news_url}?pinned_post_locator={locator}"
            embed.timestamp = datetime.now()

            for guild in self.client.guilds:
                news_channel = sql.get_server_id(guild.id)
                role_id = sql.get_role_id(guild.id)
                if news_channel:
                    #Still keep random color per server as I like it
                    embed.color=(0xeb144c if data["is_breaking"] else random.choice([0x0057b7, 0xffd700]))
                    
                    try:
                        if role_id != guild.default_role.id: await self.client.get_channel(news_channel).send((f"<@&{role_id}>" if role_id and data["is_breaking"] else None), embed=embed)
                        else: await self.client.get_channel(news_channel).send(guild.default_role, embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True));
                        posted_in += 1
                    
                    except:
                        guilds.append(str(guild.id))

            console.log(f"Posted data in {posted_in}/{len(self.client.guilds)} servers.")
            
            if guilds:
                console.warn(f"Could not post data in {len(guilds)} servers.")
                console.toFile(guilds, "WARN")

    @get_data.before_loop
    async def before_data(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(get_data_class(client))
