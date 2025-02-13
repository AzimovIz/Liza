from .userbot import run_bot, acceptor

acceptor = acceptor

sender = run_bot

intents = [
    {
        "name": "enable_tg_userbot",
        "queue": "tg_userbot",
        "purpose": "enable"
    },
    {
        "name": "disable_tg_userbot",
        "queue": "tg_userbot",
        "purpose": "disable"
    }
]