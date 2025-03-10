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

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ..interfaces import (
        APIInterface,
        APIOptions,
    )

from supertokens_python.recipe.session.asyncio import get_session
from supertokens_python.utils import send_200_response


async def handle_resync_session_and_fetch_mfa_info_api(
    _tenant_id: str,
    api_implementation: APIInterface,
    api_options: APIOptions,
    user_context: Dict[str, Any],
):
    if api_implementation.disable_resync_session_and_fetch_mfa_info_put is True:
        return None

    session = await get_session(
        api_options.request,
        override_global_claim_validators=lambda _, __, ___: [],
        user_context=user_context,
    )

    assert session is not None

    response = await api_implementation.resync_session_and_fetch_mfa_info_put(
        api_options,
        session,
        user_context,
    )

    return send_200_response(response.to_json(), api_options.response)
