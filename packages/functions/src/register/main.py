import argparse
import requests
import yaml
import os
import time
import logging
import json

parser = argparse.ArgumentParser()
parser.add_argument("--local", type=bool, default=False)
args = parser.parse_args()

logger = logging.getLogger("function-register")
logger.setLevel(logging.INFO)

if args.local: # pragma: no cover
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../configs/config.json'))
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    TOKEN = config.get("token")
    APPLICATION_ID = config.get("application_id")
else:
    TOKEN = os.environ.get("TOKEN")
    APPLICATION_ID = os.environ.get("APPLICATION_ID")

URL = f"https://discord.com/api/v9/applications/{APPLICATION_ID}/commands"

with open("discord_commands.yaml", "r") as file:
    yaml_content = file.read()

commands = yaml.safe_load(yaml_content)
headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

failed = None

def upload_command(command):
    global failed
    response = requests.post(URL, json=command, headers=headers)
    command_name = command["name"]
        
    if response.status_code == 201 or response.status_code == 200:
        failed = None
        logger.info(f"Command {command_name} created: {response.status_code}")
    elif response.status_code == 429:
        failed = command
        logger.warning(f"Command {command_name} failed: {response.status_code} Pausing for 5 seconds...")
        time.sleep(5)
    else:
        logger.error(f"Failed to create command {command_name}: {response.status_code}")

def handler(event, context):
    for command in commands:
        upload_command(command)
        if failed is not None:
            upload_command(failed)

if __name__ == '__main__': # pragma: no cover
    handler(None, None)
