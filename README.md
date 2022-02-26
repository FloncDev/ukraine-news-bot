# Ukraine News Bot

Thanks to @MrBober for the idea and for figuring out how to use the api. Also suggestions for the bot.


This is a janky bot that gets the live updates from the [BBC News Feed](https://www.bbc.co.uk/news/live/world-europe-60517447). Currently servers have to hose their own instances of the bot, but this should change soon.

Has no commands but there is a config.json
```
{
    token: str,
    news_channel: int
}