#Necessary libraries to import
import discord
from discord.ext import commands
import os
import qbittorrentapi
import plexapi
from plexapi import myplex
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.settings import Settings
import shutil
import asyncio

#Place your bot's token here, or put it in a .env file to be referenced.
TOKEN = '<YOUR TOKEN HERE>'

#initialize the bot's prefix to be '!', can be changed if desired.
bot = commands.Bot(command_prefix='!')

#removes the default help command
bot.remove_command('help')

#declaration of custom help command
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="Help", description='Use !help <command> for extended information on a specific command.')
    em.add_field(name='Torrents Commands', value='`addtor`, `viewtorrents`, `checktor`')
    em.add_field(name='Plex Commands', value='`updateplex`')
    em.add_field(name='PC Commands', value='`restartpc`, `checkstorage`')
    await ctx.channel.send(embed=em)
    
#!addtor
#DOCUMENTATION:
#Use - Adds a torrent to begin downloading in QBitTorrent. 
#Syntax - !addtor <TORRENT INFO HASH> <DIRECTORY>
#Notes - Remember to fill out the parameters for <QBITTORRENT USERNAME> and <QBITTORRENT PASSWORD>, else the command will not work properly.
@bot.command(aliases=['toradd', 'addtorrent', 'torrentadd'])
#@commands.has_role('<ROLE NAME>') : Add if you'd like to restrict this command to a specific role.
async def addtor(ctx, torHash, filePath):
    print('Adding torrent with hash', torHash, 'to qBitTorrent downloads...')
    cli = qbittorrentapi.Client(host='localhost:8080', username = '<QBITTORRENT USERNAME>', password = '<QBITTORRENT PASSWORD>')
    try:
        cli.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)
    print(f'qBittorrent: {cli.app.version}')
    cli.torrents_add(urls=torHash, save_path=filePath)
    print('Added successfully.')
    await ctx.channel.send('Download begun. Use `!viewtorrents` to check the status.')    
@help.command()
async def addtor(ctx):
    em = discord.Embed(title='Add Torrent', description='Takes a torrent hash and save path from the user and starts downloading the contents to the host PC. <torHash> should be a valid torrent info hash, and <directory> should be a valid directory on the host PC.', color=ctx.author.color)
    em.add_field(name='**Syntax**', value='!addtor <torrent hash> <directory>')
    em.add_field(name='**Example directories**', value='''C:\Users\<username>\Downloads
                                                          D:\TorrentDownloads\MyCollection''')
    em.add_field(name='**Aliases**', value='`!addtor`, `!addtorrent`, `!toradd`, `!torrentadd`')
    await ctx.channel.send(embed=em)
    
#!checktor
#DOCUMENTATION:
#Use - Checks the status of a specified torrent. Status taken directly from the dictonary of the torrent info, so it may be very hard to read.
#Syntax - !checktor <TORRENT INFO HASH>
#Notes - Remember to fill out the parameters for <QBITTORRENT USERNAME> and <QBITTORRENT PASSWORD>, else the command will not work properly.
@bot.command(aliases=['checktorrent'])
#@commands.has_role('<ROLE NAME>') : Add if you'd like to restrict this command to a specific role.
async def checktor(ctx, torHash):
    cli = qbittorrentapi.Client(host='localhost:8080', username = '<QBITTORRENT USERNAME>', password = '<QBITTORRENT PASSWORD>')
    try:
        cli.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)
    await ctx.channel.send(str(cli.torrents_info(torrent_hashes=torHash)))
@help.command()
async def checktor(ctx):
    em = discord.Embed(title='Check Torrent', description='Displays an enormous text wall of the torrent info dictionary, telling everything about a specified torrent. Hard to read, only to be used by those who know what they\'re looking at.')
    em.add_field(name='**Syntax**', value='!checktor <torrent hash>')
    em.add_field(name='**Aliases**', value='`!checktor`, `!checktorrent`')
    await ctx.channel.send(embed=em)
    
#!updateplex
#DOCUMENTATION:
#Use - Updates a plex account to refresh all libraries on a given server. 
#Notes - Make sure the parameters <PLEX USERENAME>, <PLEX PASSWORD>, and <PLEX SERVER NAME> are filled out correctly, else the command will not work.
@bot.command(aliases=['up','plexupdate'])
#@commands.has_role('<ROLE NAME>') : Add if you'd like to restrict this command to a specific role.
async def updateplex(ctx):
    account = MyPlexAccount('<PLEX USERNAME>', '<PLEX PASSWORD>')
    plex = account.resource('<PLEX SERVER NAME>').connect()
    plex.library.update()
    await ctx.channel.send('Updated plex successfully. If new files do not show up, use !restartpc.')
@help.command()
async def updateplex(ctx):
    em = discord.Embed(title='Update Plex', description='Updates the Plex media listings in the case that newly torrented files are not showing up. May require a PC reboot.', color=ctx.author.color)
    em.add_field(name='**Aliases**', value='`!updateplex`, `!up`, `!plexupdate`')
    await ctx.channel.send(embed=em)
    
#!restartpc
#DOCUMENTATION:
#Use - Restarts the host PC after waiting three seconds.
@bot.command(aliases=['rpc', 'resetcomputer'])
#@commands.has_role('<ROLE NAME>') : Add if you'd like to restrict this command to a specific role.
async def restartpc(ctx):
    await ctx.channel.send("Restarting computer... Be back shortly!")
    os.system("shutdown /r /t 3")
@help.command()
async def restartpc(ctx):
    em = discord.Embed(title='Restart PC', description='Restarts the host PC in which the bot is running from.', color=ctx.author.color)
    em.add_field(name='**Aliases**', value='`!restartpc`, `!rpc`, `!restartcomputer`')
    await ctx.channel.send(embed=em)
    
#!viewtorrents
#DOCUMENTATION:
#Use - Neatly displays the file location and name of all completed torrents, as well as the percent complete of all in progress torrents.
#Notes - Remember to fill out the parameters for <QBITTORRENT USERNAME> and <QBITTORRENT PASSWORD>, else the command will not work properly.
@bot.command(aliases=['vt','torrentstatus','downloadstatus'])
#@commands.has_role('<ROLE NAME>') : Add if you'd like to restrict this command to a specific role.
async def viewtorrents(ctx):
    cli = qbittorrentapi.Client(host='localhost:8080', username = '<QBITTORRENT USERNAME>', password = '<QBITTORRENT PASSWORD>')
    try:
        cli.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    cStr = ''
    dStr = ''
    completeStr = cli.torrents_info(status_filter='completed')
    downloadStr = cli.torrents_info(status_filter='downloading')
    print(downloadStr)

    cStr += '```COMPLETED:\n'
    if (not completeStr):
        sendStr += 'None.'
    for i in range(len(completeStr)):
        cStr += 'Location and Name:\t'
        cStr += (completeStr[i]['content_path']) + '\n'
    cStr +='```'
    
    dStr += '```DOWNLOADING:\n'
    if (not downloadStr):
        dStr += 'None.'
    for j in range(len(downloadStr)):
        dStr += 'Location and Name:\t'
        dStr += (downloadStr[j]['content_path']) + '\n'
        dStr += 'Progress Decimal Percent:\t'
        dStr += str((downloadStr[j]['progress'])) + '\n'
    dStr += '```'
    await ctx.channel.send(cStr)
    await ctx.channel.send(dStr)
@help.command()
async def viewtorrents(ctx):
    em = discord.Embed(title='View Torrents', description='View status of all current torrents.', color=ctx.author.color)
    em.add_field(name='**Aliases**', value='`!viewtorrents`, `!vt`, `!torrentstatus`, `!downloadstatus`')
    await ctx.channel.send(embed=em)

#!checkstorage
#DOCUMENTATION:
#Use - Checks the total, used, and free space of a given drive.
#Syntax - !checkstorage <DRIVE NAME>
@bot.command(aliases=['storage','checkspace','space','checkdirectory','dirspace'])
#@commands.has_role('<ROLE NAME>') : Add if you'd like to restrict this command to a specific role.
async def checkstorage(ctx, drivename):
    sendStr = '```Space remaining on disk ' + drivename + '\n'
    total, used, free = shutil.disk_usage(drivename)
    sendStr += ("Total %d GiB" % (total // (2**30))) + '\n'
    sendStr += ("Used %d GiB" % (used // (2**30))) + '\n'
    sendStr += ("Free %d GiB" % (free // (2**30))) + '```'
    await ctx.channel.send(sendStr)
@help.command()
async def checkstorage(ctx):
    em = discord.Embed(title='Check Storage', description='Returns the total storage, used storage, and free storage of a given drive.', color=ctx.author.color)
    em.add_field(name='**Aliases**', value='`!checkstorage`, `!storage`, `!checkspace`, `!space`, `!checkdirectory`, `!dirspace`')
    em.add_field(name='**Syntax**', value='!checkstorage <drivename>'
    await ctx.channel.send(embed=em)

#login
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------')

bot.run(TOKEN)
