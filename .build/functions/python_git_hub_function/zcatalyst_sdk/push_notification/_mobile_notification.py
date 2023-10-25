from typing import List
from ..exceptions import CatalystPushNotificationError
from ..types import (
    ICatalystPushDetails,
    ICatalystMobileNotification
)
from .._constants import (
    RequestMethod,
    CredentialUser
)
from .. import validator
from .._http_client import AuthorizedHttpClient


class MobileNotification:
    def __init__(self, notification_instance, app_id):
        self._app_id = app_id
        self._app = notification_instance._app
        self._requester: AuthorizedHttpClient = notification_instance._requester

    def send_notification(
        self,
        notify_obj: ICatalystPushDetails,
        recipients: List[str]
    ) -> ICatalystMobileNotification:
        if not isinstance(notify_obj, dict) or not notify_obj.get('message'):
            raise CatalystPushNotificationError(
                'Invalid Argument',
                ("Notify object should be a instance of dict and "
                 "must contain non empty value for 'message' key"),
                notify_obj
            )
        validator.is_non_empty_list(recipients, 'recipients', CatalystPushNotificationError)
        resp = self._requester.request(
            method=RequestMethod.POST,
            path=f'/push-notification/{self._app_id}/project-user/notify',
            json={
                'push_details': notify_obj,
                'recipients': recipients
            },
            user=CredentialUser.ADMIN
        )
        return resp.response_json.get('data')
