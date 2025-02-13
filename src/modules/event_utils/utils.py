from num2words import num2words
import logging
from event import Event, EventTypes

logger = logging.getLogger("root")

def num_to_word(event: Event):
    raw_text = event.value
    text = ""
    for i in raw_text.split(" "):
        text += " " + num2words(int(i), lang='ru') if i.isdigit() else i
    event.value = text

    return event


def change_type(event: Event, new_type: str = EventTypes.text):
    logger.info(f"Changing event type from {event.event_type} to {new_type}")
    event.event_type = new_type
    return event


def change_purpose(event: Event, new_purpose: str = "none"):
    logger.info(f"Changing event purpose from {event.purpose} to {new_purpose}")
    event.purpose = new_purpose
    return event


def set_value(event: Event, new_value: str = "none"):
    logger.info(f"Changing event value from {event.value} to {new_value}")
    event.value = new_value
    return event


def save_value(event: Event):
    logger.info(f"Event value {event.value} saved to .old_value")
    event.old_value = str(event.value)
    return event


async def reply(event: Event):
    await event.reply(event.value)
    return event


def json_find(event: Event):
    text = event.value
    try:
        json_data_ = "{" + "{".join(text.split("{")[1:])
        json_data_ = "}".join(json_data_.split("}")[:-1]) + "}"
        event.value = json_data_
        return event
    except:
        return event

# def move_queue(event: Event):
