import os
import json

import logging
logging.basicConfig(level=logging.WARNING)

if os.environ.get("SET_AWS_REGION") is None:
    logging.warning('this should not be ran in actions workflow')
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../configs/config.json'))
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    AWS_REGION = config.get("aws_region")
    DISCORD_PUBLIC_KEY = config.get("discord_public_key")
    RIOT_KEY = config.get("riot_key")
    TOKEN = config.get("token")
    STAGE = "dev"
else:
    AWS_REGION = os.environ.get("SET_AWS_REGION")
    DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
    RIOT_KEY = os.environ.get("RIOT_KEY")
    TOKEN = os.environ.get("TOKEN")
    STAGE = os.environ.get("STAGE")
    logging.warning(f'env stage: {STAGE}')
