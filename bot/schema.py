from typing import Optional

from pydantic import BaseModel


class IncomingMessageSchema(BaseModel):
    id: str
    body: str
    fromMe: Optional[bool] = False
    self: Optional[int] = 0
    isForwarded: bool
    author: str
    time: int
    chatId: str
    type: str
    senderName: str
    caption: Optional[str] = None
    quotedMsgId: Optional[str] = None
