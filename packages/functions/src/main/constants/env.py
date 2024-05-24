import os
import json

from argument_parser import get_local_status

if get_local_status():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../configs/config.json'))
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    AWS_REGION = config.get("aws_region")
    DISCORD_PUBLIC_KEY = config.get("discord_public_key")
    RIOT_KEY = config.get("riot_key")
    TOKEN = config.get("token")
    STAGE = "dev"
else:
    if os.environ.get("SET_AWS_REGION") != None:
        AWS_REGION = os.environ.get("SET_AWS_REGION")
    else: 
        AWS_REGION = "us-east-1"
    DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
    RIOT_KEY = os.environ.get("RIOT_KEY")
    TOKEN = os.environ.get("TOKEN")
    STAGE = os.environ.get("STAGE")
