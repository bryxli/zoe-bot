import json
import os
import random
import requests
import logging
from string import Template

from dynamo import ZoeBotTable
from league import RiotAPI

logger = logging.getLogger("function-main")
logger.setLevel(logging.INFO)

AWS_REGION = os.environ.get("SET_AWS_REGION")
RIOT_KEY = os.environ.get("RIOT_KEY")
STAGE = os.environ.get("STAGE")

db = ZoeBotTable(AWS_REGION, STAGE)
lol = RiotAPI(RIOT_KEY)

with open("template.json") as file:
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

                    summoner_name = participant["summonerName"]
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