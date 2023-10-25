from typing import Any, Callable, Tuple, TypedDict
from .response_types import WidgetEvent, WidgetResponse
from ._handler import Handler
from . import _constants as Constants
from ._constants import Handlers
from .request_types import (
    Access,
    ButtonObject,
    Environment,
    User
)


class WidgetExecutionHandlerRequest(TypedDict):
    user: User
    target: ButtonObject
    event: WidgetEvent
    environment: Environment
    access: Access


def view_handler(
        func: Callable[
            [WidgetExecutionHandlerRequest, WidgetResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.WIDGET,
        Handlers.WidgetHandler.VIEW_HANDLER,
        func,
        WidgetResponse
    )


def new_widget_response():
    return WidgetResponse()
