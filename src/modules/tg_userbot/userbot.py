import asyncio
import logging
import os

from pyrogram import Client, filters

logger = logging.getLogger("root")


async def hello(client, message):
    await message.reply("Hello from Liza!")


async def run_bot(
        queue: asyncio.Queue = None,
        config: dict = None,
):
    allowed_chats = config["allowed_chats"]
    app_id = config["APP_ID"]
    app_hash = config["APP_HASH"]
    #use_qdrant = config["use_qdrant"]

    app = Client(
        api_id=app_id,
        api_hash=app_hash,
        name="modules/tg_userbot/user_data",
        device_model="Liza",
        system_version="Assistant"
    )

    async with app:
        app.on_message(filters.chat(allowed_chats) & filters.incoming)(hello)

        while True:
            await asyncio.sleep(0)
