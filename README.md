# Zoe Bot <img src=favicon.ico width="50" height="50">

## Description

Discord bot that traverses through the Riot Games API to find information about players of the game League of Legends.

If a username has spaces, make sure to enclose it in quotes. Ex: /adduser "user name"

## Prerequisites

Zoe is an IaC application that utilizes SST and Discord. Make sure to have the following installed and configured.

- [Node.js / npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

## Bot deployment

### Configuration

1. Set global configuration [config.json](configs/config.json)

```
{
  "aws_region": "<AWS REGION>",
  "riot_key": "<RIOT API KEY>"
}
```

2. Set dev configuration [config-dev.json](configs/config-dev.json)

```
{
  "discord_public_key": "<DISCORD PUBLIC KEY>",
  "application_id": "<DISCORD APPLICATION ID>",
  "token": "<DISCORD BOT TOKEN>"
}

```

3. Set prod configuration [config-prod.json](configs/config-prod.json)

```
{
  "discord_public_key": "<DISCORD PUBLIC KEY>",
  "application_id": "<DISCORD APPLICATION ID>",
  "token": "<DISCORD BOT TOKEN>"
}
```

- aws_region - Region that AWS resources will be deployed to
- riot_key - obtained from [Riot Developer Portal](https://developer.riotgames.com/)
- discord_public_key - found in [Discord Developer Portal](https://discord.com/developers/applications) under General Information
- application_id - found in [Discord Developer Portal](https://discord.com/developers/applications) under General Information
- token - found in [Discord Developer Portal](https://discord.com/developers/applications) under Bot > Reset Token

### Startup

The bot is configured to be able to deploy to multiple stages. This changes configurations in the AWS stack.

- `npm run deploy` - deploy dev stack, returns InteractionsEndpoint
- `npm run deploy:prod` - deploy prod stack, returns InteractionsEndpoint, URL

### Create Discord Application

1. Create a new [Application](https://discord.com/developers/applications)
2. Enable _Privileged Gateway Intents_ under Bot
3. Invite to server with `https://discord.com/oauth2/authorize?client_id=<client_id>&permissions=536870912&scope=applications.commands%20bot`

   Note: Replace **<client_id>** with _Application ID_

4. After deploying the bot to AWS using either `npm run deploy` or `npm run deploy:prod`, paste InteractionsEndpoint into _Interactions Endpoint URL_ under General Information

### Bot commands

- /help - command list
- /setup - create guild instance
- /reset - reset instance
- /region \<region> - change guild region
- /acknowledge - acknowledge dangerous commands
- /adduser \<username> - add user to guild, user must be a valid League of Legends username
- /deluser \<username> - delete user from guild, user must be a valid League of Legends username and exist
- /userlist - display guild userlist
- /speak - zoe will talk to you

## Production deployment

### Create redirect

1. In the Discord Application on [Discord Developer Portal](https://discord.com/developers/applications) under OAuth2, create a redirect using URL/load

   The URL will be something like this `https://abcdefghijklm.cloudfront.net/load`

2. Under Authorization Method, choose _In-app Authorization_
3. Enable Scopes: _bot_, _application.commands_
4. Enable Bot Permissions: _Manage Webhooks_

### Configure login button

1. In [Header.tsx](/packages/frontend/app/components/Header.tsx), update redirect with URL
2. Redeploy to production using `npm run deploy:prod`

## Integrate with GitHub Actions

### Create IAM role

### Create secrets

### Configure deployment region
