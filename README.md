# QBTBot

# Initial Notes
- This code was made in Python 3.9. If your bot is running with JavaScript or some other language, this code is incompatible. You may use my code as a base to translate it into other languages, if you wish.
- These functions are intended to be implemented into a preexisting bot. If you simply copy and paste this code, it will not work.
- These functions are intended to be implemented into a bot that runs off of a local host PC, likely for personal use. Granting lange amounts of people access to these commands could be detrimental to one's security, as they require login information to be used, and allow the user to directly control the host's PC in ways they may not want. PLEASE be careful when implementing into your own bot.
- I do not condone using this code to torrent any sort of copyrighted material, thus I do not take responsibility for how this code is used. The responsibility is in the hands of the user whom hosts the bot running this code and the developers of the APIs used.
- The torrent software that these functions use is QBitTorrent. Please do not try to use them with anything else without modification, else they will not work as intended.

# Description
Have you ever wanted to remotely be able to control QBitTorrent and Plex from a simple Discord message? These commands let you do just that! In `bot.py`, I have supplied my code that allows for multiple functions regarding the QBitTorrent application, as well as a function to help it coexist with Plex. This code is designed to work entirely remotely, though it is helpful to have eyes on the comupter you are using it with in the case that something goes wrong.

# Instructions
1. Ensure that your bot is written in Python 3.9
2. Install the libraries used in the code (more details below)
3. Copy and paste the desired functions into your bot's file
4. Change the parameters the function may require
5. Run your bot and enjoy!

# Brief Documentation
If the information here is does not suffice, more information can be found in the code itself and within the `!help` command for each function.

## Library Installation
Please ensure that the following libraries are all installed on your local machine that you are hosting your bot from

Linux users may use:
```
pip install discord.py
pip install plexapi
pip install qbittorrent-api
```
Windows users may use:
```
py -3 -m pip install -U discord.py
py -3 -m pip install -U plexapi
py -3 -m pip install -U qbittorrent-api
```

## !addtor
This function takes in a torrent info hash and begins downloading it to QBitTorrent. If you're unsure what an info hash is, it's the long string of characters that is best thought of as a unique ID for the torrent you are downloading. Make sure that QBitTorrent is running on your host PC, else the torrent may not be added to your downloads. The syntax for this command is as follows:

`!addtor <TORRENT INFO HASH>`

## !viewtorrents
This function lists all the currently active torrents in your QBitTorrent client. It will send one message for completed torrents, listing the file location and the name of the folder the torrent has downloaded to. It will then send another message for downloading torrents, listing te file location and name of the folder the torrent is downloading to, as well as the percentage the torrent is complete.

## !checktor
This function takes in a torrent info hash and returns a *LOT* of information pertaining to said torrent. The torrent hash must be of a torrent that is currently on your host PC. This command is best used only by those familiar with QBitTorrent's API, as it is hard to read, though it will give some useful information. The syntax for this command is as follows:

`!checktor <TORRENT INFO HASH>`

## !updateplex
This function is used to scan all libraries on a given Plex server. You must make sure that the parameters in the code are filled out with your Plex username, password, and server name for it to work. 

## !restartpc
A simple command to restart the PC that the bot is hosted on. Can be used for various things, but mostly for if `!updateplex` doesn't work immediately. 

## !checkstorage
Returns the total, used, and free storage of a given drive. The syntax for this command is as follows:

`!checkstorage <DRIVE NAME>`

## Allowing Your Bot to Access QBitTorrent
1. Navigate to the Web UI tab in settings
2. Click the box at the top
3. Make sure that you have a valid username and password, and use them in the bot's parameters where necessary

## Allowing Your Bot to Access Plex
1. Create a Plex username if you are only using your email to log in
2. Provide the parameters of your username, password, and server name to the code. The server name can be found near the top left of your screen on Plex's main page.
3. Enable Remote Access in Plex settings
