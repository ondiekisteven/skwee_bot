import asyncio
import enum
import inspect
import logging

import bot
from bot.schema import IncomingMessageSchema


logger = logging.getLogger(__name__)


class MessageHandler(enum.Enum):
    REGISTRATION = 'registration'
    LYRICS = 'lyrics'


class Whatsapp:
    def __init__(self, message: IncomingMessageSchema, cfg: dict, loop=None):
        self.message: IncomingMessageSchema = message
        self.loop = loop
        self.cfg = cfg

    def _get_handler(self):
        text = self.message.body
        if 'join bot' in text.lower():
            return MessageHandler.REGISTRATION
        elif text.lower().startswith('lyrics'):
            return MessageHandler.LYRICS
        else:
            return None

    def response(self):
        handler = self._get_handler().value.lower() if self._get_handler() is not None else None
        if handler is not None:
            fn = getattr(bot.handlers, handler)
            if inspect.iscoroutinefunction(fn):
                resp = self.loop.run_until_complete(fn)
            else:
                resp = fn(self.message, self.cfg)
            return resp
        logger.info("THIS MESSAGE IS NOT KNOWN")
