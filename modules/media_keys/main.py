from .utils import press

# acceptors = []
# 
# senders = [
#     {
#         "name": "vosk_send",
#         "function": run_vosk
#     }
# ]

intents = [
    {
        "name": "media_mute",
        "examples": ["запомни", "запиши", "добавь событие"],
        "function": press("volumemute")
    },
    {
        "name": "media_vup",
        "examples": ["тише", "уменьши громкость", "сделай тише"],
        "function": press("volumedown")
    },
    {
        "name": "media_vdoun",
        "examples": ["громче", "прибавь громкость", "сделай громче"],
        "function": press("volumeup")
    },
    {
        "name": "media_play",
        "examples": ["стоп", "пауза", "остановить", "продолжить"],
        "function": press("playpause")
    }
]
