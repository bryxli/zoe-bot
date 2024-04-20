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

def handler(event, context): # TODO: configure task to use new RiotAPI
    data = db.get_all()['Items']
    for guild in data:
        try:
            guild_id = guild['guild_id']['N']
            webhook_url = guild['webhook_url']['S']

            logger.info(f"Found guild: {guild_id}")

            for user_data in guild['userlist']['L']:
                try:
                    account_id = list(user_data['M'].keys())[0]

                    summoner = lol.find_player_by_accountid(account_id, guild['region']['S'])

                    logger.info(f"Found summoner: {summoner}")

                    match_history = summoner.match_history
                    if (match_history.count > 0):
                        match = match_history[0]
                        for participant in match.participants:
                            if participant.summoner.account_id == summoner.account_id:
                                id = match.participants.index(participant)
                                break

                        last_created_old = user_data['M'][account_id]['S']
                        last_created = str(match.creation)
                        if last_created != last_created_old:
                            logger.info(f"New match found at {last_created}")
                            player = match.participants[id]
                            try:
                                summoner_name = lol.find_account_by_puuid(summoner.puuid)["gameName"]
                            except:
                                raise Exception("Summoner name not found")
                            champion_name = player.champion.name
                            kda = str(round(player.stats.kda, 2))
                            win = player.stats.win

                            if win:
                                t = Template(random.choice(template['win']))
                            else:
                                t = Template(random.choice(template['lose']))

                            db.update_user(guild_id, account_id, last_created)

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
                except Exception as e:
                    logger.error(f"An exception occured when fetching user data: {e}")
        except Exception as e:
            logger.error(f"An exception occured when fetching guild data: {e}")