# TODO: Integrate with CDK deployment

import requests
import yaml
import os


TOKEN = os.environ.get("TOKEN")
APPLICATION_ID = os.environ.get("APPLICATION_ID")
GUILD_ID = os.environ.get("GUILD_ID")

URL = f"https://discord.com/api/v9/applications/{APPLICATION_ID}/commands"
URL_TEST = f"https://discord.com/api/v9/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"


with open("discord_commands.yaml", "r") as file:
    yaml_content = file.read()

commands = yaml.safe_load(yaml_content)
headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

# Send the POST request for each command
for command in commands:
    response = requests.post(URL, json=command, headers=headers)
    command_name = command["name"]
    print(f"Command {command_name} created: {response.status_code}")