# pubg-reports
A Python-based Discord bot that tracks users from a given server in PUBG to automatically send their post-match stats to a pre-specified Discord channel.

## Prerequisites
* **Python 3.5.3 or higher is required**
* **PUBG API Key**
    * [Get yours here](https://developer.pubg.com/)
* **Discord API key**
    * A Discord application needs to be created in order to create a bot, [you can create a new Discord application here](https://discordapp.com/developers/applications)
    * There are two keys for Discord, please disregard the client key and use the bot key
    * [A useful guide on how to create a bot](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro)
* **Discord server & channel IDs**
    * The channel IDs are going to be used by the bot to
        1. Register new users
        2. Send reports for solo, duo and squad PUBG rounds
    * To acquire an ID for a given channel, please enabled developer mode in your Discord user settings, then simply right click a channel and there will be an option to **copy ID**

## Installation
OS X & Linux:
```sh
$ python3 -m pip install -U pubg-reports
```
Windows:
```sh
$ py -3 -m pip install -U pubg-reports
```

## Configuration
To configure the **tokens** that are __required to run the bot__
```sh
$ bot-config-tokens
```
To configure the **Discord channels** that are __required for the bot to send reports at__
```sh
$ bot-config-channels
```
To configure the tokens and channels in one go
```sh
$ bot-config-all
```
## Running the bot
To run the bot, simply do
```sh
$ bot-run
```
## Usage
* To use the bot, a user must register by typing **!reg PUBG-IGN** [Case sensitive]

<p align="center">
  <img src="https://sulimancs.github.io/pubg-reports/img/Example-reg.jpg">
</p>

* To check all the registered users within the server, type **!users**

<p align="center">
  <img src="https://sulimancs.github.io/pubg-reports/img/Example-users2.jpg">
</p>

* After a PUBG round ends, a user can get the top 3 players kill-wise in that round by typing **!top3**

<p align="center">
  <img src="https://sulimancs.github.io/pubg-reports/img/Example-top3-2.jpg">
</p>


## Example Match Report

* This is how a post match report looks like

<p align="center">
  <img src="https://sulimancs.github.io/pubg-reports/img/Example-report.png" height=600 width=607>
</p>

## Known Issues

* A round of PUBG will not get reported for one of the teams if team A is playing against team B and they are both on the same Discord server.
* The bot supports up to one Discord server. There are plans to expand the capabilities of the bot to support multi servers.
