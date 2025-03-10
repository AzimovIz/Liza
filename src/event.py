import asyncio
from dataclasses import dataclass


@dataclass
class EventTypes:
    text = "text"
    user_command = "user_command"
    core_query = "core_query"


class Event:
    """
    Ивент - еденица передачи данных между модулями. Ивент создатся любым модулем и попадает в исходящую очередь этого модуля.
    Ивент содержит свойства по которым происходит маршрутизация иветнов между модулями.
    """

    def __init__(self, event_type: str, value=None, purpose=None, out_queue: asyncio.Queue = None, from_module: str = None, **kwargs):
        """
        При создании ивента обязательным является указать его тип:

        - ``EventTypes.text`` ("text") - Применяются правила маршрутизации
        - ``EventTypes.user_command`` ("user_command") - Обрабатывается с помощью NLU.
        - ``EventTypes.core_query`` ("core_query") - Обращение к ядру для получения данных о ядре/модулях/интентах/итд

        :param event_type:  Тип ивента. От типа зависит то, как он будет обрабатываться.
        :param value: Значение, в большинстве случаев строка, но использование других типов так-же возможно.
        :param purpose: Назначение, нужно для разделения разных ивентов в рамках модуля.
        """
        self.event_type = event_type
        self.value = value
        self.purpose = purpose
        self.out_queue = out_queue
        self.from_module = from_module
        self.context = None
        for key, val in kwargs.items():
            setattr(self, key, val)

    @staticmethod
    def from_dict(data: dict):
        event_type = data.pop("event_type")
        value = data.pop("value")
        event = Event(
            event_type=event_type,
            value=value,
            **data
        )
        return event

    def to_dict(self):
        data = {
            "event_type": self.event_type,
            "value": self.value,
            "purpose": self.purpose,
            "from_module": self.from_module
        }
        return data

    async def reply(self, value, new_purpose=None):
        """
        Создает `Event` и отправляет его в входную очередь модуля отправившего этот ивент

        :param value: Значение ответа, будет использовано в качестве event.value при создании ответного ивента.
        :param new_purpose: Опционально, назначение которое будет присвоено созданному ивенту.
        """
        if self.out_queue:
            await self.out_queue.put(
                Event(
                    event_type=EventTypes.text,
                    value=value,
                    purpose=new_purpose,
                )
            )

    def copy(self):
        data = dict(self.__dict__)
        data.update(
            {
                "event_type": self.event_type,
                "value": self.value,
                "purpose": self.purpose,
                "out_queue": self.out_queue,
                "from_module": self.from_module,
            }
        )
        return Event.from_dict(data)

    # @property
    # def context(self):
    #     raise Exception("Context is not defined, see: https://github.com/AzimovIz/Liza/blob/dev/docs/docs/Контекст.md")

    async def set_context(self, callback: callable, init_context_data: dict = None):
        # See Core.get_context_setter()
        pass

    async def end_context(self):
        # See Core.get_context_deleter()
        pass


class TextEvent(Event):
    def __init__(self, value: str, purpose=None, out_queue: asyncio.Queue = None, from_module: str = None, **kwargs):
        super().__init__(
            EventTypes.text,
            value=value,
            purpose=purpose,
            out_queue=out_queue,
            from_module=from_module,
            **kwargs
        )


class UserCommandEvent(Event):
    def __init__(self, value: str, purpose=None, out_queue: asyncio.Queue = None, from_module: str = None, **kwargs):
        super().__init__(
            EventTypes.user_command,
            value=value,
            purpose=purpose,
            out_queue=out_queue,
            from_module=from_module,
            **kwargs
        )


class CoreCommandEvent(Event):
    def __init__(self, value: str, purpose=None, out_queue: asyncio.Queue = None, from_module: str = None, **kwargs):
        super().__init__(
            EventTypes.core_query,
            value=value,
            purpose=purpose,
            out_queue=out_queue,
            from_module=from_module,
            **kwargs
        )


if __name__ == '__main__':
    event = Event.from_dict({"event_type": "user_command", "value": 1})
    print(event)
    event2 = event.copy()
    print(event2)