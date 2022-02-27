import enum
import logging

import bot
from bot.schema import IncomingMessageSchema


logger = logging.getLogger(__name__)


class MessageCategory(enum.Enum):
    REGISTRATION = 'registration'


class Whatsapp:
    def __init__(self, message: IncomingMessageSchema):
        self.message: IncomingMessageSchema = message

    def _category(self):
        text = self.message.body
        if text.lower().startswith('join bot'):
            return MessageCategory.REGISTRATION
        else:
            return None

    def response(self):
        cat = self._category().value.lower() if self._category() is not None else None
        if cat is not None:
            fn = getattr(bot.handlers, cat)
            resp = fn(self.message)
            return resp
        logger.info("THIS MESSAGE IS NOT KNOWN")
