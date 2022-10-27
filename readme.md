# Zoe Bot <img src=public/favicon.ico width="50" height="50">
**[Discord Invite Link](https://discord.com/api/oauth2/authorize?client_id=1014214102459093105&permissions=2048&scope=bot)**  

## Description

Zoe is a Discord bot that traverses through the Riot Games API to find information about players of the game *League of Legends*. Users of a Discord server can see real-time updates on played games of registered player names. Currently, Zoe is hosted on GCP using Compute Engine.  

After registering a text channel and adding a username (see [Usage](#Usage)), Zoe will start to output game results into that channel.  
Note: Zoe will only check once every five minutes.

Currently, the bot is being transitioned into a full-stack containerized application using Docker, React.js, and Quart.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

Before you start to work with this project, Docker has to be installed and all dependencies be provided as described in the following sections.
Check the official [Docker documentation](https://docs.docker.com/engine/) for information how to install Docker on your operating system. And then install Docker and supporting tools.

1. Configure [config.json](backend/config%20-%20Copy.json)  
<img src=public/config.png align='left'>
prefix - bot command prefix (?help)<br>
league_token - Riot API key<br>
token - Discord API key<br>
permissions - Discord bot permission id<br>
application id - Discord application id

<br clear='left'/>

2. Configure [custom.json](backend/templates/custom%20-%20Copy.json) (Optional - Gives Zoe custom messages)  
<img src=public/custom.png align='left'>
&dollar;summonername - replaced with player's name<br>
&dollar;championname - replaced with the champion played<br> 
&dollar;kda - replaced with the calculated KDA of the game

<br clear='left'/>

3. Run Docker container  
Launch terminal in project directory and run ```docker compose up```  

Zoe should now be running on [localhost:3000](http://localhost:3000)

## Usage

### Discord Commands

<img src=public/setup.png align='left'>
&emsp;?help - help menu<br>
&emsp;?setup - zoe will speak in this channel<br>
&emsp;?speak - zoe will talk to you

<br clear='left'/>

### Unlockable Commands (after running ?setup)

<img src=public/adduser.png align='left'>
&emsp;?reset - wipe server from database<br>
&emsp;?region - list current region and region codes<br> 
&emsp;?setregion &lt;region&gt; - set server region<br>
&emsp;?adduser &lt;league username&gt; - add to server database<br>
&emsp;?deluser &lt;league username&gt; - delete from server database<br>
&emsp;?userlist - show server userlist<br>

<br clear='left'/>

### Bot Output

<img src=public/output.png>

After Zoe outputs in a channel somewhere, it will become available to be shown on the website!

### Website

<img src=public/webpage.png>
The webpage will display ten random Zoe outputs from the database.

## License

The MIT License (MIT)

Copyright (c) 2015 Chris Kibble

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---
