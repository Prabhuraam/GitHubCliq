from dataclasses import dataclass
from requests import Response
from typing import Any, Callable, Dict, List, Optional, Tuple
from ._handler import Handler
from .error import CatalystError
from ._constants import Handlers
from ._utils import send_request
from .request_types import (
    User,
    Environment,
    Access,
    Attachment,
    MessageDetails,
    Location,
    Mention,
    Chat
)
from . import _constants as Constants
from .handler_response import HandlerResponse
import json


@dataclass
class BotHandlerRequest:
    user: User
    name: str
    unique_name: str
    environment: Optional[Environment]
    access: Optional[Access]


@dataclass
class BotWelcomeHandlerRequest(BotHandlerRequest):
    newuser: bool


@dataclass
class BotMessageHandlerRequest(BotHandlerRequest):
    attachments: List[Attachment]
    links: List[str]
    message_details: MessageDetails
    location: Location
    raw_message: str
    message: str
    mentions: List[Mention]
    chat: Chat

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


@dataclass
class BotContextHandlerRequest:
    user: User
    name: str
    unique_name: str
    chat: Chat
    context_id: str
    answers: Any


@dataclass
class BotMentionHandlerRequest(BotHandlerRequest):
    location: Location
    chat: Chat


@dataclass
class BotMenuActionHandlerRequest(BotHandlerRequest):
    action_name: str
    location: Location
    chat: Chat


@dataclass
class BotWebHookHandlerRequest(BotHandlerRequest):
    headers: Dict[str, str]
    param: Dict[str, str]
    body: Dict[str, Any]
    http_method: str


@dataclass
class BotParticipationHandlerRequest(BotHandlerRequest):
    operation: str
    data: Dict[str, Any]
    chat: Chat


def welcome_handler(
        func: Callable[
            [BotWelcomeHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.BOT,
        Handlers.BotHandler.WELCOME_HANDLER,
        func,
        HandlerResponse
    )


def message_handler(
        func: Callable[
            [BotMessageHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.BOT,
        Handlers.BotHandler.MESSAGE_HANDLER,
        func,
        HandlerResponse
    )


def context_handler(
        func: Callable[
            [BotContextHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.BOT,
        Handlers.BotHandler.CONTEXT_HANDLER,
        func,
        HandlerResponse
    )


def mention_handler(
        func: Callable[
            [BotMentionHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.BOT,
        Handlers.BotHandler.MENTION_HANDLER,
        func,
        HandlerResponse
    )


def menu_action_handler(
        func: Callable[
            [BotMenuActionHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.BOT,
        Handlers.BotHandler.ACTION_HANDLER,
        func,
        HandlerResponse
    )


def webhook_handler(
        func: Callable[
            [BotWebHookHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.BOT,
        Handlers.BotHandler.INCOMING_WEBHOOK_HANDLER,
        func,
        HandlerResponse
    )


def participation_handler(
        func: Callable[
            [BotParticipationHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.BOT,
        Handlers.BotHandler.PARTICIPATION_HANDLER,
        func,
        HandlerResponse
    )


def new_handler_response():
    return HandlerResponse()

class Util:
    @staticmethod
    def get_attached_file(attachments: List[Attachment]):
        result: list[bytes] = []
        try:
            for attachment in attachments:
                resp: Response = send_request('GET', attachment.url, stream=True)
                result.append(resp.content)
        except Exception as e:
            raise CatalystError('Error when getting the attached file', 0, e)
        return result
