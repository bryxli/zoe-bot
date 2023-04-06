# Zoe Bot  <img src=favicon.ico width="50" height="50">

## Description

Discord bot that traverses through the Riot Games API to find information about players of the game League of Legends. Hosted on AWS EC2 with a DynamoDB instance.

If a username has spaces, make sure to enclose it in quotes. Ex: ?adduser "user name"

## Prerequisites

Zoe is an IaC application that utilizes AWS CDK and Discord. Make sure to have the following installed and configured.
 * [Node.js / npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
 * [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
 * [AWS CDK (TypeScript)](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
 * [Discord Application](https://discord.com/developers/docs/getting-started)

## Running the bot

### Startup commands
 
 * `npm install`   install Node.js dependencies
 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access


### UserData Script

You can check to see if [startup.sh](./startup.sh) ran by seeing if python3 is installed.
```
python3
```
If python3 is not installed, you will have to run [startup.sh](./startup.sh) manually before creating the config. I am unsure why this is happening, please message me if you know why!

### Create config.json

```
cd /home/ssm-user/zoe-bot
sudo touch config.json
sudo vim config.json
```

Enter config.json (see below), then `:wq`

### Run

```
python3 src/app.py
```

## Extras

### Example [config.json](config.json)

```
{
    "prefix": "?",
    "token": "",
    "permissions": "2048",
    "application_id": "",
    "riot_key": ""
}
```

### Example [template.json](template.json)

Template to give Zoe custom responses! Responses are picked randomly based on game outcome.
```
{
    "win": ["you","can","have","an","arbitrary"],
    "lose": ["amount","of"],
    "response": ["string","values","in","each","list","of","bot","responses"]
}
```

### Region

Currently, boto3 is set to the region `us-east-1`. You may have to change this [here](src/db_wrapper.py) depending on the configuration of the AWS CLI.

### Linux Screen

It is recommended to use Linux Screen so the bot stays alive upon exit.
```
sudo screen -S zoe
```

After initializing the bot, detach from the screen and exit the session.
```
Ctrl-a d
exit
```

Reattachment
```
sudo screen -r zoe
```

### NPM

If you want to run the bot using `npm run python3` from the project directory, this is how to install NPM.
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
. ~/.nvm/nvm.sh
nvm install 16
npm install -g npm
```