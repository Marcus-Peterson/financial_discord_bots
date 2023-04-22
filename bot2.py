import os
import discord
from discord.ext import commands
from newsapi import NewsApiClient
TOKEN = 'MTA0NTg2NDI5Njk4ODU0MTAyOA.GUe2XV.7dND-qC6jZIfoQ1v9xI31nP8OW7ZI8uwdEnltg'
NEWS_API_KEY = 'eeba792485e14d7bad769601f6ccf404'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
@bot.command(name='news', help='Fetch financial news')
async def fetch_news(ctx, *args):
    if not args:
        query = 'finance'
    else:
        query = ' '.join(args)

    try:
        news = newsapi.get_everything(q=query, language='en', sort_by='relevancy', page_size=5)

        if news['status'] == 'ok' and news['totalResults'] > 0:
            embeds = []

            for article in news['articles']:
                embed = discord.Embed(title=article['title'], url=article['url'], description=article['description'], color=discord.Color.blue())
                embed.set_author(name=article['source']['name'])
                embed.set_thumbnail(url=article['urlToImage'])
                embed.set_footer(text=article['publishedAt'])
                embeds.append(embed)

            for embed in embeds:
                await ctx.send(embed=embed)
        else:
            await ctx.send('No news found for the given query.')

    except Exception as e:
        print(e)
        await ctx.send('Error while fetching news.')
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)
