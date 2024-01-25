import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import time
import discord
from discord.ext import commands
import os

chromedriver_autoinstaller.install()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Instagram"))
    print("ok")

@client.event
async def on_message(message):
    if message.content.startswith("!test"):
        await message.channel.send("ok")
    if message.content.startswith("!image") and len(message.content) > 9:
        #tag = input("Entrez le tag à rechercher : ")
        #tag = "landscapes"
        tag = message.content[7:]

        url=f"https://www.instagram.com/explore/tags/{tag}/"

        driver = webdriver.Chrome()

        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        #print(html)

        soup = bs(html, "html.parser")
        images = soup.find_all('img',class_='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3')
        #images = soup.find_all("div",class_="_aagv")

        # affichage super stylé des alts + liens des images ^^
        for img in images :
            #for letter in f"{img['alt']}\n\033[32m{img['src']}\033[0m\n":
                #print("\033[3"+str(ord(letter)%8)+"m"+letter+"\033[0m",end="")
            embed = discord.Embed(title=f"{tag.capitalize()}", description=f"{img['alt']}", color=0x00ff00)
            embed.set_image(url=f"{img['src']}")
            await message.channel.send(embed=embed)
            #print("\n")
        driver.close()

bot_token = os.environ.get("BOT_TOKEN_IMG")
client.run(bot_token)
