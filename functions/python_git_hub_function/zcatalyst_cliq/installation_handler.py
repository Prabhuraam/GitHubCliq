from dataclasses import dataclass
from ._handler import Handler
from typing import Callable, Optional, Tuple
from . import _constants as Constants
from ._constants import Handlers
from .response_types import InstallationResponse
from .request_types import (
    User,
    AppInfo
)


@dataclass
class InstallationRequest:
    user: User
    app_info: AppInfo


def handle_installation(
        func: Callable[
            [InstallationRequest, InstallationResponse, Tuple],
            Optional[InstallationResponse]
        ]
):
    Handler.register_hanlder(
        Constants.INSTALLATION,
        Handlers.installation_handler,
        func,
        InstallationResponse
    )


def new_installation_response():
    return InstallationResponse()
