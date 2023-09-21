# TODO: Integrate with CDK deployment
# TODO: Not every command is uploaded successfully - have to switch around command order resulting in multiple uploads due to 429 errors

import requests
import yaml
import os
import time


TOKEN = os.environ.get("TOKEN")
TOKEN = 'MTA4Mjg0NjIyODY3MDMyNDc4Ng.GBJoxJ.M7u83GfB5C3-XRgqOonX2eGwkRId3xBNxZfysc'
APPLICATION_ID = os.environ.get("APPLICATION_ID")
APPLICATION_ID= '1082846228670324786'

URL = f"https://discord.com/api/v9/applications/{APPLICATION_ID}/commands"


with open("discord_commands.yaml", "r") as file:
    yaml_content = file.read()

commands = yaml.safe_load(yaml_content)
headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}


failed = []


def upload_command(command):
    global failed
    response = requests.post(URL, json=command, headers=headers)
    command_name = command["name"]
        
    if response.status_code == 201 or response.status_code == 200:
        print(f"Command {command_name} created: {response.status_code}")
    elif response.status_code == 429:
        failed.append(command)
        # Rate limited, sleep and retry after the reset time
        print(f"Command {command_name} failed: {response.status_code} Pausing for 5 seconds...")
        time.sleep(5)
    else:
        print(f"Failed to create command {command_name}: {response.status_code}")


for command in commands:
    upload_command(command)
    if len(failed) > 0:
        upload_command(failed.pop())
