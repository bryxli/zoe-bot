import argparse
import json
import os
import random
import requests
import logging
import sys
import json
from string import Template

parser = argparse.ArgumentParser()
parser.add_argument("--local", type=bool, default=False)

args = parser.parse_args()

if args.local: # pragma: no cover
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../layers/dynamo/python')))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../layers/league/python')))

    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../configs/config.json'))
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    AWS_REGION = config.get("aws_region")
    RIOT_KEY = config.get("riot_key")
    STAGE = "dev"
else:
    AWS_REGION = os.environ.get("SET_AWS_REGION")
    RIOT_KEY = os.environ.get("RIOT_KEY")
    STAGE = os.environ.get("STAGE")

from dynamo import ZoeBotTable
from league import RiotAPI

logger = logging.getLogger("function-main")
logger.setLevel(logging.INFO)

db = ZoeBotTable(AWS_REGION, STAGE)
lol = RiotAPI(RIOT_KEY)

template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'template.json')

with open(template_path) as file:
    template = json.load(file)

def process_guild(guild):
    try:
        guild_id = guild['guild_id']['N']
        webhook_url = guild['webhook_url']['S']

        logger.info(f"Found guild: {guild_id}")

        for user_data in guild['userlist']['L']:
            puuid = list(user_data['M'].keys())[0]
            match = lol.get_match_by_puuid(puuid, guild['region']['S'])['info']

            logger.info(f"Found user: {puuid}")

            process_user_data(user_data, guild_id, webhook_url, puuid, match)
    except Exception as e:
        logger.error(f"An exception occured when fetching guild data: {e}")

def process_user_data(user_data, guild_id, webhook_url, puuid, match):
    try:
        gameId_old = user_data['M'][puuid]['S']
        gameId = str(match["gameId"])
                        
        if gameId != gameId_old:
            logger.info(f"Found match: {gameId}")

            for participant in match["participants"]:
                if participant["puuid"] == puuid:

                    summoner_name = participant["riotIdGameName"]
                    champion_name = participant["championName"]
                    kda = str(round(participant["challenges"]["kda"], 2))
                    win = participant["win"]
                    if win:
                        t = Template(random.choice(template['win']))
                    else:
                        t = Template(random.choice(template['lose']))

                    db.update_user(guild_id, puuid, gameId)
                    message_content = t.substitute(summoner_name=summoner_name, kda=kda, champion_name=champion_name)

                    headers = {
                    "Content-Type": "application/json"
                    }
                    data = {
                        'username': 'zœ',
                        'avatar_url': 'https://raw.githubusercontent.com/bryxli/zoe-bot/main/packages/functions/src/task/zoe.png',
                        "content": message_content
                    }
                    requests.post(webhook_url, headers=headers, data=json.dumps(data))

                    break
    except Exception as e:
        logger.error(f"An exception occured when fetching user data: {e}")

def handler(event, context):
    data = db.get_all()['Items']
    for guild in data:
        process_guild(guild)

if __name__ == '__main__': # pragma: no cover
    handler(None, None)
