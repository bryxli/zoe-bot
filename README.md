# Zoe Bot

## Description

Discord bot that traverses through the Riot Games API to find information about players of the game League of Legends. Hosted on AWS EC2 with a DynamoDB instance.

## Prerequisites

Zoe is an IaC application that utilizes AWS CDK. Make sure to have the following installed and configured.
 * [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
 * [AWS CDK (TypeScript)](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

## Running the bot

### Startup commands

 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access

### Start session

```
aws ssm start-session --target i-089afc155a2e07d22
```

### Create config.json

```
cd /home/ssm-user/zoe-bot/src
sudo touch config.json
sudo vim config.json
```

Enter config.json, then `:wq`

### Run

```
python3 app.py
```

## Extras

### Example config.json (put this file in [src/](src/))

```
{
    "prefix": "?",
    "token": "",
    "permissions": "2048",
    "application_id": "",
    "riot_key": ""
}
```

### Example [template.json](src/template.json)

Template to give Zoe custom responses! Responses are picked randomly based on game outcome.
```
{
    "win": ["you","can","have","an","arbitrary"],
    "lose": ["amount","of"],
    "response": ["string","values","in","each","list","of","bot","responses"]
}
```
