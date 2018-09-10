import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import os
import youtube_dl
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

Client = discord.Client()
client = commands.Bot(command_prefix = '?')
players = {}

@client.event
async def on_ready():
    print("bot is ready")
    print("Im " + client.user.name)
    print("with the ID: " + client.user.id)
    print("Discord Version: " + discord.__version__)
    print("Discord.py owner: " + discord.__author__)

@client.event
async def on_message (message):
    if message.content.startswith(";restart"):
        os.execv('C:/Users/sanju/Documents/topi/Topi.py', [''])
        print("Bot Restarting...")
    
    if message.content.startswith(";help"):
        await client.send_message(message.channel, "```For now only some useless commands :sweat_smile: \n ;coin \n ;say \n ;shout \n ;ping \n ;user \n ;join \n ;play \n ;pause \n ;resume \n ;stop```")

    if message.content.startswith("cookie"):
        await client.send_message(message.channel, ":cookie:")

    if message.content.upper().startswith("ARIGATO GOZAIMASU"):
        await client.send_message(message.channel, "Arigato! :slight_smile:")

    if message.content.startswith(";coin"):
        flip = random.choice(["Its Heads!", "It's Tails!"])
        await client.send_message(message.channel, flip)

    if message.content.startswith (";ask"):
        ask = message.content.split(" ")
        ques = ask[1:]
        if not ques:
            await client.send_message(message.channel, "you have nothing to ask?")
        else:
            answer = random.choice(["Yes", "No", "Probably", "Probably not"])
            await client.send_message(message.channel, answer)

    if message.content.startswith("cookies"):
        await client.send_message(message.channel, ":cookie: Lots of cookies :D :cookie: :cookie: :cookie:")

    if message.content.upper().startswith("HI TOPI"):
        await client.send_message(message.channel, "Hi! :smile:")
    
    if message.content.upper().startswith("THINK"):
        await client.send_message(message.channel, "I am Thinking :thinking:")
    
    if message.content.startswith("cake"):
        await client.send_message(message.channel, ":cake:")
    
    if message.content.startswith("cat"):
        await client.send_message(message.channel, ":cat:")

    if message.content.startswith("owo"):
        await client.send_message(message.channel, "OwO")

    if message.content.upper().startswith(";SAY"):
        args = message.content.split(" ")
        await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

    if message.content.upper().startswith(";SHOUT"):
        echo = message.content.split(" ")
        await client.send_message(message.channel, "**%s!**" % (" ".join(echo[1:])))
    
    if message.content.startswith(';user'):
        try:
            user = message.mentions[0]
            userjoinedat = str(user.joined_at).split('.', 1)[0]
            usercreatedat = str(user.created_at).split('.', 1)[0]
 
            userembed = discord.Embed(
                title="Username:",
                description=user.name,
                color=0xe67e22
            )
            userembed.set_author(
                name="User Info"
            )
            userembed.add_field(
                name="Joined the server at:",
                value=userjoinedat
            )
            userembed.add_field(
                name="User Created at:",
                value=usercreatedat
            )
            userembed.add_field(
                name="Discriminator:",
                value=user.discriminator
            )
            userembed.add_field(
                name="User ID:",
                value=user.id
            )
            userembed.set_thumbnail(
                url=user.avatar_url
            )
 
            await client.send_message(message.channel, embed=userembed)
        except IndexError:
            await client.send_message(message.channel, "Ich konnte den User nicht finden.")
        except:
            await client.send_message(message.channel, "Sorry Error")
        finally:
            pass
    
    if message.content.startswith(";createwatchlist"):
        user = message.author
        id = user.id
        newf = open("%s.txt" % (id), "w")
        newf.write("**%s's Watch List:** \n" % (user.name))
        newf.close
        await client.send_message(message.channel, "Your Watch List is succesfully Created. Use ;add to add your pending shows.")
    if message.content.startswith(";add"):
        add = message.content.split(" ")
        user = message.author
        id = user.id
        f = open("%s.txt" % (id), "a")
        f.write(" %s\n" % (" ".join(add[1:])))
        f.close
        await client.send_message(message.channel, "%s successfully added to your watchlist." % (" ".join(add[1:])))
    if message.content.startswith(";showlist"):
        user = message.author
        openf = open("%s.txt" % (user.id), "r")
        lines = openf.readlines()
        for line in lines:
            await client.send_message(message.channel, " " +line)

    if message.content.startswith(";join"):
        channel = message.author.voice.voice_channel
        if not channel:
            await client.send_message(message.channel, "You must be in a voice chanel.")
        else:
            await client.join_voice_channel(channel)

    if message.content.startswith(";dc"):
        server = message.server
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()

    if message.content.startswith(";disconnect"):
        server = message.server
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()

    if message.content.startswith(";play"):
        server = message.server
        contents = message.content.split(" ")
        query = contents[1:]
        voice_client = client.voice_client_in(server)
        if not query:
            await client.send_message(message.channel, "**Usage:** ;play `Youtube URL or Search query(search query currently not available)`")
        else:
            player = await voice_client.create_ytdl_player(" ".join(contents[1:]))
            players[server.id] = player
            player.start()
            print("Player Started")

    if message.content.startswith(";pause"):
        id = message.server.id
        players[id].pause()
        print("player Paused")

    if message.content.startswith(";stop"):
        id = message.server.id
        players[id].stop()
        print("Player Stopped")

    if message.content.startswith(";resume"):
        id = message.server.id
        players[id].resume()
        print("Player Resumed")


    if message.content.startswith(";serverinfo"):
        user = message.author
        server = user.server.name
        region = user.server.region
        userembed = discord.Embed(title ="Server Info:", discription=server)
        userembed.set_author(name=user)
        userembed.set_thumbnail(url=user.server.icon_url)
        await client.send_message(message.channel, embed=userembed)

    
client.run("NDMyOTM1OTc5MTU4OTk0OTY0.DdlGuA.AW3_D_aGV_h0MEOAJtIEV1qVl6c")
