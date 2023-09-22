# Zoe Bot <img src=favicon.ico width="50" height="50">

## Description

Discord bot that traverses through the Riot Games API to find information about players of the game League of Legends.

If a username has spaces, make sure to enclose it in quotes. Ex: /adduser "user name"

## Prerequisites

Zoe is an IaC application that utilizes AWS CDK and Discord. Make sure to have the following installed and configured.

- [Node.js / npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [AWS CDK (TypeScript)](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

## Running the bot

### Configuration

Initialize config.json in root directory using this JSON template.

```
{
    "aws_region": "",
    "discord_public_key": "",
    "application_id": "",
    "token": "",
    "riot_key": ""
}
```

- aws_region - AWS region that CDK will be deployed to
- discord_public_key - found in [Discord Developer Portal](https://discord.com/developers/applications) under General Information [after this step](#initiating-the-bot)
- application_id - found in [Discord Developer Portal](https://discord.com/developers/applications) under General Information [after this step](#initiating-the-bot)
- token - found in [Discord Developer Portal](https://discord.com/developers/applications) under Bot > Reset Token [after this step](#initiating-the-bot)
- riot_key - obtained from [Riot Developer Portal](https://developer.riotgames.com/)

### Startup

1.  `npm install` - install Node.js dependencies
2.  `cdk bootstrap` - initialize assets before deploy
3.  `cdk deploy` - deploy this stack to your default AWS account/region

### Initiating the bot

1. Create a new [Application](https://discord.com/developers/applications)
2. Enable _Privileged Gateway Intents_ under Bot
3. Save Changes
4. Paste URL output into _Interactions Endpoint URL_ under General Information
5. Save Changes
6. Invite to server with `https://discord.com/api/oauth2/authorize?client_id=<client_id>&scope=applications.commands`

   Note: Replace **<client_id>** with _Application ID_

### Getting the webhook URL

1. Open Discord context menu of respective server
2. Create a new webhook under Server Settings > Integrations > Webhooks > New Webhook
3. Change the channel to desired output channel
4. If channel was changed, Save Changes
5. Copy Webhook URL

### Using the bot

- /setup \<webhook url> - create guild instance
- /reset - reset instance
- /region \<region> - change guild region
- /adduser \<username> - add user to guild
- /deluser \<username> - delete user from guild
- /userlist - display guild userlist
- /speak - zoe will talk to you
