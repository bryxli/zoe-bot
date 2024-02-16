# Zoe Bot <img src=favicon.ico width="50" height="50">

## Description

Discord bot that traverses through the Riot Games API to find information about players of the game League of Legends.

# Table of Contents

- [Prerequisites](#prerequisites)
- [Bot Deployment](#bot-deployment)
  - [Configuration](#configuration)
  - [Startup](#startup)
  - [Create Discord Application](#create-discord-application)
  - [Bot Commands](#bot-commands)
- [Production Deployment](#production-deployment)
  - [Create Redirect](#create-redirect)
  - [Configure Login Button](#configure-login-button)
- [Integrate with GitHub Actions](#integrate-with-github-actions)
  - [Create IAM Role](#create-iam-role)
  - [Create Secrets](#create-secrets)
    - [Automated Setup](#automated-setup)
    - [Manual Setup](#manual-setup)

## Prerequisites

Zoe is an IaC application that utilizes SST and Discord. Make sure to have the following installed and configured.

- [Node.js / npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
- [Docker](https://docs.docker.com/engine/install)

## Bot Deployment

### Configuration

Set environment configuration [config.json](configs/config.json)

```
{
  "aws_region": "<AWS REGION>",
  "riot_key": "<RIOT API KEY>",
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

- `npm run deploy` - deploy dev stack, returns **InteractionsEndpoint**
- `npm run deploy:prod` - deploy prod stack, returns **InteractionsEndpoint**, **URL**

### Create Discord Application

1. Create a new [Application](https://discord.com/developers/applications)
2. Enable _Privileged Gateway Intents_ under Bot
3. Invite to server with `https://discord.com/oauth2/authorize?client_id=<client_id>&permissions=536870912&scope=applications.commands%20bot`

   Note: Replace **<client_id>** with _Application ID_

4. After deploying the bot to AWS using either `npm run deploy` or `npm run deploy:prod`, paste **InteractionsEndpoint** into _Interactions Endpoint URL_ under General Information

### Bot Commands

- /help - command list
- /setup - create guild instance
- /reset - reset instance
- /region \<region> - change guild region
- /acknowledge - acknowledge dangerous commands
- /adduser \<username> - add user to guild, user must be a valid League of Legends username
- /deluser \<username> - delete user from guild, user must be a valid League of Legends username and exist
- /userlist - display guild userlist
- /speak - zoe will talk to you

## Production Deployment

### Create Redirect

1. In the Discord Application on [Discord Developer Portal](https://discord.com/developers/applications) under OAuth2, create a redirect URL using **URL**/load

   The redirect URL will look like this `https://abcdefghijklm.cloudfront.net/load`

2. Under Authorization Method, choose _In-app Authorization_
3. Enable Scopes: _bot_, _application.commands_
4. Enable Bot Permissions: _Manage Webhooks_

### Configure Login Button

1. In [Header.tsx](/packages/frontend/app/components/Header.tsx#L11), update _url_ with redirect URL created in previous step
2. Redeploy to production using `npm run deploy:prod`

## Integrate with GitHub Actions

### Create IAM Role

Instructions to deploy SST apps using GitHub Actions can be found [here](https://docs.sst.dev/going-to-production#deploy-from-github-actions)

- [aws-github-actions](https://github.com/bryxli/aws-github-actions)

### Create Secrets

#### Automated Setup

1. Set environment configuration [config.actions.json](configs/config.actions.json)

```
{
  "pat": "<GITHUB TOKEN>",
  "owner": "<GITHUB REPO OWNER>",
  "repo": "<GITHUB REPO>",
  "aws_account_id": "<AWS ACCOUNT ID>",
  "aws_region": "<AWS REGION>",
  "riot_key": "<RIOT API KEY>",
  "dev": {
    "discord_public_key": "<DISCORD PUBLIC KEY>",
    "application_id": "<DISCORD APPLICATION ID>",
    "token": "<DISCORD BOT TOKEN>"
  },
  "prod": {
    "discord_public_key": "<DISCORD PUBLIC KEY>",
    "application_id": "<DISCORD APPLICATION ID>",
    "token": "<DISCORD BOT TOKEN>"
  }
}
```

2. In [configs](configs), create secrets used by GitHub Actions using `npm run start`

#### Manual Setup

1. In the repo, under Settings > Secrets and variables > Actions, create three new repository secrets

   - AWS_ACCOUNT_ID
   - AWS_REGION
   - RIOT_KEY

2. Repeat step 1 for Secrets and variables > Dependabot

3. Additionally, create a new environment called dev and create three new environment secrets

   - APPLICATION_ID
   - DISCORD_PUBLIC_KEY
   - TOKEN

4. Repeat step 3 for prod
