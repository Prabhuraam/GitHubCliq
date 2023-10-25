from typing import List, Literal, Union
from .types import (
    Component,
    ICatalystSignupConfig,
    ICatalystUserDetails,
    ICatalystUser
)
from .exceptions import CatalystAuthenticationError
from . import validator
from ._http_client import AuthorizedHttpClient
from ._constants import RequestMethod, CredentialUser, Components


class ICatalystNewUser(ICatalystSignupConfig):
    user_details: ICatalystUser


UserStatus = Literal['enable', 'disable']


class Authentication(Component):
    def __init__(self, app) -> None:
        self._app = app
        self._requester = AuthorizedHttpClient(self._app)

    def get_component_name(self):
        return Components.AUTHENTICATION

    def get_current_user(self) -> ICatalystUser:
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/project-user/current',
            user=CredentialUser.USER
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def get_all_users(self, org_id: str = None) -> List[ICatalystUser]:
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/project-user',
            user=CredentialUser.ADMIN,
            params={
                'org_id': org_id
            } if org_id else None
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def get_user_details(self, user_id: Union[int, str]) -> ICatalystUser:
        validator.is_non_empty_string_or_number(user_id, 'user_id', CatalystAuthenticationError)
        resp = self._requester.request(
            method=RequestMethod.GET,
            path=f'/project-user/{user_id}',
            user=CredentialUser.ADMIN
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def delete_user(self, user_id: Union[int, str]) -> bool:
        validator.is_non_empty_string_or_number(user_id, 'user_id', CatalystAuthenticationError)
        resp = self._requester.request(
            method=RequestMethod.DELETE,
            path=f'/project-user/{user_id}',
            user=CredentialUser.ADMIN
        )
        resp_json = resp.response_json
        return bool(resp_json.get('data'))

    def register_user(
        self,
        signup_config: ICatalystSignupConfig,
        user_details: ICatalystUserDetails
    ) -> ICatalystNewUser:
        self._validate_signup_config(signup_config, {'platform_type', 'zaid'})
        self._validate_user_details(user_details, {'last_name', 'email_id'})
        signup_config['user_details'] = user_details
        resp = self._requester.request(
            method=RequestMethod.POST,
            path='/project-user/signup',
            json=signup_config,
            user=CredentialUser.ADMIN
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def add_user_to_org(
        self,
        signup_config: ICatalystSignupConfig,
        user_details: ICatalystUserDetails
    ) -> ICatalystNewUser:
        self._validate_signup_config(signup_config, {'platform_type'})
        self._validate_user_details(user_details, {'last_name', 'email_id', 'zaaid'})
        signup_config['user_details'] = user_details
        resp = self._requester.request(
            method=RequestMethod.POST,
            path='/project-user',
            json=signup_config,
            user=CredentialUser.ADMIN
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def get_all_orgs(self):
        resp = self._requester.request(
            method=RequestMethod.GET,
            path='/project-user/orgs',
            user=CredentialUser.ADMIN
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def update_user_status(
        self,
        user_id: Union[str, int],
        status: UserStatus
    ):
        validator.is_non_empty_string_or_number(user_id, 'user_id', CatalystAuthenticationError)
        validator.is_non_empty_string(status, 'status', CatalystAuthenticationError)
        if status not in ['enable', 'disable']:
            raise CatalystAuthenticationError(
                'INVALID_USER_STATUS',
                "Status must be either 'enable' or 'disable'."
            )
        resp = self._requester.request(
            method=RequestMethod.POST,
            path=f'/project-user/{user_id}/{status}',
            user=CredentialUser.ADMIN
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def update_user_details(
        self,
        user_id: str,
        user_details: ICatalystUserDetails
    ):
        validator.is_non_empty_string(user_id, 'user_id', CatalystAuthenticationError)
        self._validate_user_details(user_details, {'email_id'})
        resp = self._requester.request(
            method=RequestMethod.POST,
            path=f'/project-user/{user_id}',
            json=user_details,
            user=CredentialUser.ADMIN
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    def reset_password(
        self,
        signup_config: ICatalystSignupConfig,
        user_details: ICatalystUserDetails
    ) -> str:
        self._validate_signup_config(signup_config, {'platform_type', 'zaid'})
        self._validate_user_details(user_details, {'email_id'})
        signup_config['user_details'] = user_details
        resp = self._requester.request(
            method=RequestMethod.POST,
            path='/project-user/forgotpassword',
            json=signup_config,
            user=CredentialUser.USER,
            headers={
                'project_id': signup_config['zaid']
            }
        )
        resp_json = resp.response_json
        return resp_json.get('data')

    @staticmethod
    def _validate_signup_config(signup_config, mandatories):
        if not signup_config or not isinstance(signup_config, dict):
            raise CatalystAuthenticationError(
                'INVALID_SIGNUP_CONFIG',
                'signup config must be a non empty dict'
            )
        for mand in mandatories:
            if mand not in signup_config or not signup_config[mand]:
                raise CatalystAuthenticationError(
                    'INVALID_SIGNUP_CONFIG',
                    (f"Either the key '{mand}' is missing or "
                     f"value provided for the {mand} is None in user details")
                )

    @staticmethod
    def _validate_user_details(user_details, mandatories):
        if not user_details or not isinstance(user_details, dict):
            raise CatalystAuthenticationError(
                'INVALID_USER_DETAILS',
                'User details must be a non empty dict'
            )

        for mand in mandatories:
            if mand not in user_details or not user_details[mand]:
                raise CatalystAuthenticationError(
                    'INVALID_USER_DETAILS',
                    (f"Either the key '{mand}' is missing or "
                     f"value provided for the {mand} is None in user details")
                )
