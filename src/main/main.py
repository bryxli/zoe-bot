import os
import json
import random
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator

from constants.env import DISCORD_PUBLIC_KEY
from constants.main import *

import commands.server_commands
import commands.league_commands

with open("template.json") as file:
    template = json.load(file)

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)


@app.route("/", methods=["POST"])
async def interactions():
    print(f"👉 Request: {request.json}")
    raw_request = request.json
    return interact(raw_request)


@verify_key_decorator(DISCORD_PUBLIC_KEY)
def interact(raw_request):
    if raw_request["type"] == 1:
        response_data = {"type": 1} 
    else:
        data = raw_request["data"]
        command_name = data["name"]

        if command_name == "help":
            message_content = HELP_RESPONSE
        elif command_name == "speak":
            response = template['response']
            message_content = random.choice(response)
        elif command_name in SERVER_COMMANDS:
            message_content = commands.server_commands.init(command_name, raw_request)
        elif command_name in LEAGUE_COMMANDS:
            message_content = commands.league_commands.init(command_name, raw_request)

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }

    return jsonify(response_data)
