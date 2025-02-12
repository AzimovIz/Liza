import pathlib
import json
from pyrogram import Client

with open(f"{pathlib.Path(__file__).parent.absolute()}/settings.json", "r") as f:
    settings = json.load(f)

config = settings["config"]

app_id = config["APP_ID"]
app_hash = config["APP_HASH"]

app = Client(
    api_id=app_id,
    api_hash=app_hash,
    name=f"{pathlib.Path(__file__).absolute().parent}/user_data",
    device_model="Liza",
    system_version="Assistant"
)

with app:
    pass

print("Session created!")