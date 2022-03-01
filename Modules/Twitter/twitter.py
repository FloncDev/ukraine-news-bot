import discord
from discord.ext import commands, tasks
from console import Console
import tweepy
import json

console = Console(True)

with open("config.json", "r") as f:
    config = json.load(f)

try:
    t_api = tweepy.OAuthHandler(
        consumer_key=config["twitter"]["consumer_key"],
        consumer_secret=config["twitter"]["consumer_secret"],
        access_token=config["twitter"]["access_token"],
        access_token_secret=config["twitter"]["access_token_secret"]
    )

    t = tweepy.API(t_api)
except: t = None

class get_tweets_class(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Data check

        # Check latest.json
        try:
            with open("latest.json", "r") as f:
                latest = json.load(f)

            if latest["twitter"]:
                pass
            else:
                return
        except: return

        # Check config.json
        try:
            with open("config.json", "r") as f:
                config = json.load(f)

            if config["twitter"]:
                pass
            else:
                return
        except: return

        if t: self.get_tweets.start()

    @tasks.loop(minutes=1)
    async def get_tweets(self):
        tweet = t.user_timeline(screen_name="",count=1)
        console.log("Tweet: " + tweet[0].text)

    @get_tweets.before_loop
    async def before_data(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(get_tweets_class(client))