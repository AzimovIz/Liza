import asyncio

import pyautogui
from event import Event


def press(key):
    async def wrapper(event: Event):
        pyautogui.keyDown(key)
        await asyncio.sleep(0.1)
        pyautogui.keyUp(key)

    return wrapper
