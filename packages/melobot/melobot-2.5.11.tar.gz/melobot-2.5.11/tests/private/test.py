import asyncio
import sys
import time

sys.path.append("../../")
sys.path.append("../../src")
from melobot.base import BotAction
from melobot.context.action import MsgDelActionArgs
from melobot.models import MessageEvent

e = MessageEvent(
    {
        "message_type": "group",
        "sub_type": "normal",
        "message_id": 1745108393,
        "group_id": 174720233,
        "user_id": 1574260633,
        "anonymous": None,
        "message": [{"type": "text", "data": {"text": "你好"}}],
        "raw_message": "你好",
        "font": 0,
        "sender": {
            "user_id": 1574260633,
            "nickname": "Melorenae律回",
            "card": "律回子",
            "sex": "unknown",
            "age": 0,
            "area": "",
            "level": "75",
            "role": "owner",
            "title": "",
        },
        "time": 1712561961,
        "self_id": 1801297943,
        "post_type": "message",
    }
)
print(f"{e:hexid}, {e:raw}")
a = BotAction(MsgDelActionArgs(12312131231233), "13781273712983")
print(f"{a:hexid}, {a:raw}")
