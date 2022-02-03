# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union, List, TYPE_CHECKING
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
if TYPE_CHECKING:
    from supertokens_python.framework import BaseRequest, BaseResponse
    from supertokens_python.recipe.jwt.interfaces import RecipeInterface as JWTRecipeInterface
    from .utils import SessionConfig
    from .session_class import Session


class SessionObj:
    def __init__(self, handle: str, user_id: str, user_data_in_jwt: any):
        self.handle = handle
        self.user_id = user_id
        self.user_data_in_jwt = user_data_in_jwt


class AccessTokenObj:
    def __init__(self, token: str, expiry: int, created_time: int):
        self.token = token
        self.expiry = expiry
        self.created_time = created_time


class RegenerateAccessTokenResult(ABC):
    def __init__(self, status: Literal['OK'], session: SessionObj,
                 access_token: Union[AccessTokenObj, None]):
        self.status = status
        self.session = session
        self.access_token = access_token


class RegenerateAccessTokenOkResult(RegenerateAccessTokenResult):
    def __init__(self, session: SessionObj,
                 access_token: Union[AccessTokenObj, None]):
        super().__init__('OK', session, access_token)


class RecipeInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def create_new_session(self, request: any, user_id: str, user_context: any,
                                 access_token_payload: Union[dict,
                                                             None] = None,
                                 session_data: Union[dict, None] = None) -> Session:
        pass

    @abstractmethod
    async def get_session(self, request: any, user_context: any, anti_csrf_check: Union[bool, None] = None,
                          session_required: bool = True) -> Union[Session, None]:
        pass

    @abstractmethod
    async def refresh_session(self, request: any, user_context: any) -> Session:
        pass

    @abstractmethod
    async def revoke_session(self, session_handle: str, user_context: any) -> bool:
        pass

    @abstractmethod
    async def revoke_all_sessions_for_user(self, user_id: str, user_context: any) -> List[str]:
        pass

    @abstractmethod
    async def get_all_session_handles_for_user(self, user_id: str, user_context: any) -> List[str]:
        pass

    @abstractmethod
    async def revoke_multiple_sessions(self, session_handles: List[str], user_context: any) -> List[str]:
        pass

    @abstractmethod
    async def get_session_information(self, session_handle: str, user_context: any) -> dict:
        pass

    @abstractmethod
    async def update_session_data(self, session_handle: str, new_session_data: dict, user_context: any) -> None:
        pass

    @abstractmethod
    async def update_access_token_payload(self, session_handle: str,
                                          new_access_token_payload: dict, user_context: any) -> None:
        pass

    @abstractmethod
    async def get_access_token_lifetime_ms(self, user_context: any) -> int:
        pass

    @abstractmethod
    async def get_refresh_token_lifetime_ms(self, user_context: any) -> int:
        pass

    @abstractmethod
    async def regenerate_access_token(self,
                                      access_token: str,
                                      user_context: any,
                                      new_access_token_payload: Union[dict, None] = None) -> RegenerateAccessTokenResult:
        pass


class SignOutResponse:
    def __init__(self):
        pass

    @abstractmethod
    def to_json(self):
        pass


class SignOutOkayResponse(SignOutResponse):
    def __init__(self):
        self.status = 'OK'
        super().__init__()
        pass

    def to_json(self):
        return {
            'status': self.status
        }


class APIOptions:
    def __init__(self, request: BaseRequest, response: Union[BaseResponse, None],
                 recipe_id: str, config: SessionConfig, recipe_implementation: RecipeInterface,
                 jwt_recipe_implementation: Union[JWTRecipeInterface, None]):
        self.request = request
        self.response = response
        self.recipe_id = recipe_id
        self.config = config
        self.recipe_implementation = recipe_implementation
        self.jwt_recipe_implementation = jwt_recipe_implementation


class APIInterface(ABC):
    def __init__(self):
        self.disable_refresh_post = False
        self.disable_signout_post = False

    @abstractmethod
    async def refresh_post(self, api_options: APIOptions, user_context: any):
        pass

    @abstractmethod
    async def signout_post(self, api_options: APIOptions, user_context: any) -> SignOutResponse:
        pass

    @abstractmethod
    async def verify_session(self, api_options: APIOptions, user_context: any,
                             anti_csrf_check: Union[bool, None] = None,
                             session_required: bool = True) -> Union[Session, None]:
        pass
