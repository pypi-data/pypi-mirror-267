# import asyncio
# import sys
# import time

# sys.path.append("../../")
# sys.path.append("../../src")
# from melobot.base import BotAction
# from melobot.context.action import MsgDelActionArgs
# from melobot.models import MessageEvent

# e = MessageEvent(
#     {
#         "message_type": "group",
#         "sub_type": "normal",
#         "message_id": 1745108393,
#         "group_id": 174720233,
#         "user_id": 1574260633,
#         "anonymous": None,
#         "message": [{"type": "text", "data": {"text": "你好"}}],
#         "raw_message": "你好",
#         "font": 0,
#         "sender": {
#             "user_id": 1574260633,
#             "nickname": "Melorenae律回",
#             "card": "律回子",
#             "sex": "unknown",
#             "age": 0,
#             "area": "",
#             "level": "75",
#             "role": "owner",
#             "title": "",
#         },
#         "time": 1712561961,
#         "self_id": 1801297943,
#         "post_type": "message",
#     }
# )
# print(f"{e:hexid}, {e:raw}")
# a = BotAction(MsgDelActionArgs(12312131231233), "13781273712983")
# print(f"{a:hexid}, {a:raw}")

import logging
import sys

import better_exceptions

# 修复在 windows powershell 显示错误的 bug
better_exceptions.encoding.ENCODING = sys.stdout.encoding
better_exceptions.formatter.ENCODING = sys.stdout.encoding
better_exceptions.hook()

# import loguru
# from loguru import logger as logger1

logging.basicConfig(level=logging.DEBUG)
logger1 = logging.getLogger()


def func():
    func2()


def func2():
    func3()


def func3():
    raise Exception("afakjdlfja;lfja")


try:
    func()
except Exception as e:
    # e = Exception("123")
    # print(isinstance(e, BaseException))
    logger1.error("Your error message" + sys.exec)
