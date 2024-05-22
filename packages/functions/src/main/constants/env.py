import os

from argument_parser import get_local_status

if get_local_status():
    AWS_REGION = "config"
    DISCORD_PUBLIC_KEY = "config"
    RIOT_KEY = "config"
    TOKEN = "config"
    STAGE = "config"
else:
    AWS_REGION = os.environ.get("SET_AWS_REGION")
    DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
    RIOT_KEY = os.environ.get("RIOT_KEY")
    TOKEN = os.environ.get("TOKEN")
    STAGE = os.environ.get("STAGE")
