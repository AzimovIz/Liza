import asyncio
import logging
import pathlib
from pyrogram import Client, filters, types
from event import Event, EventTypes

logger = logging.getLogger("root")

input_queue: asyncio.Queue = None
is_enable = True


async def acceptor(
        queue: asyncio.Queue = None,
        config: dict = None,
):
    global input_queue
    input_queue = queue


async def incoming(client, message: types.Message):
    global is_enable
    if is_enable:
        logger.info(
            f"tg_userbot: Incoming Message from {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.id})")
        # await message.reply("Hello from Liza!")
        # return
        event = Event(
            event_type=EventTypes.text,
            value=message.text,
            purpose="incoming_tg_bot",
            out_queue=None
        )
        event.reply = message.reply
        await client.output_queue.put(event)


async def incoming_trust(client, message):
    await message.reply("Hello from Liza!")


async def run_bot(
        queue: asyncio.Queue = None,
        config: dict = None,
):
    global input_queue, is_enable
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
        app.on_message(filters.chat([int(i) for i in allowed_chats.keys()]) & filters.incoming)(incoming)
        while input_queue is None:
            logger.info("tg_userbot: wait input")
            await asyncio.sleep(1)

        while True:
            await asyncio.sleep(0)

            if not input_queue.empty():
                event: Event = await input_queue.get()

                if event.purpose in ["enable", "disable"]:
                    logger.info(f"tg_userbot: set userbot {bool(event.purpose == 'enable')}")
                    is_enable = event.purpose == "enable"
                    await event.reply(f"Автоответчик {'включен' if event.purpose == 'enable' else 'выключен'}")

                elif event.purpose == "outcoming_tg_userbot":
                    pass
                    # event.allowed_chats = str(app.allowed_chats)
                    # await app.output_queue.put(event)

                elif event.purpose == "send_message":
                    data = event.value
                    if data["type"] == "text":
                        await app.send_message(chat_id=data["chat_id"], text=data["value"])
                    elif data["type"] == "file":
                        await app.send_document(chat_id=data["chat_id"], document=data["value"])
                    else:
                        logger.warning(f"Unknown event type for tg_userbot, event: {str(event.to_dict())}")
                else:
                    logger.warning(f"Unknown event purpose for tg_userbot, event: {str(event.to_dict())}")
