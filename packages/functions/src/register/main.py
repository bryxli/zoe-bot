import requests
import yaml
import os
import time
import logging

logger = logging.getLogger("function-register").setLevel(logging.INFO)

TOKEN = os.environ.get("TOKEN")
APPLICATION_ID = os.environ.get("APPLICATION_ID")

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
        logging.info(f"Command {command_name} created: {response.status_code}")
    elif response.status_code == 429:
        failed.append(command)
        logging.warning(f"Command {command_name} failed: {response.status_code} Pausing for 5 seconds...")
        time.sleep(5)
    else:
        logging.error(f"Failed to create command {command_name}: {response.status_code}")


def handler(event, context):
    for command in commands:
        upload_command(command)
        if len(failed) > 0:
            upload_command(failed.pop())
