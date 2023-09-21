import json
import random
import requests
from string import Template

import wrappers.dynamo as db
import wrappers.league as lol

with open("template.json") as file:
    template = json.load(file)


def handler(event, context):
    data = db.get_all()['Items']
    for guild in data:
        guild_id = guild['guild_id']['N']
        webhook_url = guild['webhook_url']['S']

        try:
            for user_data in guild['userlist']['L']:
                account_id = list(user_data['M'].keys())[0]

                summoner = lol.find_player_by_accountid(account_id, guild['region']['S'])

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

                        player = match.participants[id]
                        summoner_name = summoner.name
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
                            'avatar_url': 'https://raw.githubusercontent.com/bryxli/zoe-bot/main/src/task/app/zoe.png',
                            "content": message_content
                        }
                        requests.post(webhook_url, headers=headers, data=json.dumps(data))
        except Exception as e:
            print(e)