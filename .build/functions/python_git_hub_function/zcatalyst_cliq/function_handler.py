from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, TypedDict
from ._handler import Handler
from . import _constants as Constants
from ._constants import Handlers
from .handler_response import HandlerResponse
from .response_types import (
    WidgetResponse,
    FormChangeResponse,
    FormDynamicFieldResponse
)
from .request_types import (
    Access,
    ButtonObject,
    Environment,
    User,
    Chat,
    MessageObject,
    Button,
    FormRequestParam,
    FormTarget
)


@dataclass
class FunctionRequest:
    name: str
    user: User
    chat: Chat
    message: MessageObject


@dataclass
class ButtonFunctionRequest(FunctionRequest):
    arguments: Dict[str, Any]
    target: Button


@dataclass
class FormFunctionRequest(FunctionRequest):
    form: FormRequestParam
    target: FormTarget


@dataclass
class WidgetFunctionRequest:
    name: str
    user: User
    target: ButtonObject
    access: Access
    environment: Environment


def button_function_handler(
        func: Callable[
            [ButtonFunctionRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.FUNCTION,
        Handlers.function_handler.BUTTON_HANDLER,
        func,
        HandlerResponse
    )


def form_submit_handler(
        func: Callable[
            [FormFunctionRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.FUNCTION,
        Handlers.function_handler.FORM_HANDLER,
        func,
        HandlerResponse
    )


def form_change_handler(
        func: Callable[
            [FormFunctionRequest, FormChangeResponse, tuple],
            Optional[FormChangeResponse]
        ]
):
    Handler.register_hanlder(
        Constants.FUNCTION,
        Handlers.function_handler.FORM_CHANGE_HANDLER,
        func,
        FormChangeResponse
    )


def form_dynamic_field_handler(
        func: Callable[
            [FormFunctionRequest, FormDynamicFieldResponse, tuple],
            Optional[FormDynamicFieldResponse]
        ]
):
    Handler.register_hanlder(
        Constants.FUNCTION,
        Handlers.function_handler.FORM_VALUES_HANDLER,
        func,
        FormDynamicFieldResponse
    )


def widget_button_handler(
        func: Callable[
            [WidgetFunctionRequest, WidgetResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.FUNCTION,
        Handlers.function_handler.WIDGET_FUNCTION_HANDLER,
        func,
        WidgetResponse
    )


def new_handler_response():
    return HandlerResponse()


def new_form_change_response():
    return FormChangeResponse()


def new_form_dynamic_field_response():
    return FormDynamicFieldResponse()


def new_widget_response():
    return WidgetResponse()
