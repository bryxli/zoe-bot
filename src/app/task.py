import json
import os
import random
import requests
from string import Template

import wrappers.dynamo as db
import wrappers.league as lol

with open("template.json") as file:
    template = json.load(file)

TOKEN = os.environ.get("TOKEN")


def run():
    data = db.get_all()['Items']
    for guild in data:
        guild_id = guild['guild_id']['N']
        channel_id = guild['channel_id']['N']
        print(f'checking in {guild_id}:{channel_id}')

        try:
            for user_data in guild['userlist']['L']:
                account_id = list(user_data['M'].keys())[0]
                print(f'found user {account_id}')

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
                        print('found new match')

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

                        data = {
                            "content": message_content
                        }
                        headers = {
                            "Authorization": f"Bot {TOKEN}", # TODO: is there a way to send message without TOKEN? how are messages sent with discord_interactions?
                            "Content-Type": "application/json"
                        }
                        url = f"https://discord.com/api/v10/guilds/{guild_id}/channels/{channel_id}/messages"

                        response = requests.post(url, data=json.dumps(data), headers=headers) # TODO: test that this request posts to respective channels

                        if response.status_code == 200:
                            print("Message sent successfully")
                        else:
                            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(e)