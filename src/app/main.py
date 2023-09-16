import os
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator

import json
import random

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
SERVER_COMMANDS = ['setup','reset','region']
LEAGUE_COMMANDS = ['adduser','deluser','userlist']

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
            message_content = 'TODO'
        elif command_name == "speak":
            response = template['response']
            message_content = random.choice(response)
        elif command_name in SERVER_COMMANDS:
            message_content = data["options"][0]["value"]
        elif command_name in LEAGUE_COMMANDS:
            message_content = data["options"][0]["value"]    

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
