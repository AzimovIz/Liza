import asyncio
import logging
import pathlib
from pyrogram import Client, filters, types
from event import Event, EventTypes

logger = logging.getLogger("root")

input_queue: asyncio.Queue = None


async def acceptor(
        queue: asyncio.Queue = None,
        config: dict = None,
):
    global input_queue
    input_queue = queue


async def incoming(client, message: types.Message):
    if str(message.from_user.id) in client.allowed_chats:
        await message.reply("Hello from Liza!")
        event = Event(
            event_type=EventTypes.text,
            value=message.text,
            purpose="incoming_tg_bot",
            out_queue=None
        )


async def incoming_trust(client, message):
    await message.reply("Hello from Liza!")


async def run_bot(
        queue: asyncio.Queue = None,
        config: dict = None,
):
    global input_queue
    allowed_chats = config["allowed_chats"]
    app_id = config["APP_ID"]
    app_hash = config["APP_HASH"]

    app = Client(
        api_id=app_id,
        api_hash=app_hash,
        name=f"{pathlib.Path(__file__).absolute().parent}/user_data",
        device_model="Liza",
        system_version="Assistant"
    )
    app.output_queue = queue
    app.allowed_chats = allowed_chats

    async with app:
        app.on_message(filters.chat(allowed_chats) & filters.incoming)(incoming)
        while True:
            if input_queue is None:
                await asyncio.sleep(1)
                continue

            if not input_queue.empty():
                event: Event = await queue.get()
                data = event.value
                if data["type"] == "text":
                    await app.send_message(chat_id=data["chat_id"], text=data["value"])
                elif data["type"] == "file":
                    await app.send_document(chat_id=data["chat_id"], document=data["value"])
                else:
                    logger.warning(f"Unknown event type for tg_userbot, event: {str(event.to_dict())}")
