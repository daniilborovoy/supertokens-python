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

import json

from supertokens_python.async_to_sync_wrapper import sync


class Middleware:
    from flask import Flask

    def __init__(self, app: Flask):
        self.app = app
        self.set_before_after_request()
        self.set_error_handler()

    def set_before_after_request(self):
        app = self.app
        from supertokens_python.framework.flask.flask_request import \
            FlaskRequest
        from supertokens_python.framework.flask.flask_response import \
            FlaskResponse
        from supertokens_python.supertokens import manage_cookies_post_response

        from flask.wrappers import Response

        @app.before_request
        def _():
            from supertokens_python import Supertokens

            from flask import request
            from flask.wrappers import Response

            st = Supertokens.get_instance()

            request_ = FlaskRequest(request)
            response_ = FlaskResponse(Response())

            sync(st.middleware(request_, response_))

            # TODO: is this if statement needed?
            # if result is not None:
            #     return result.response

        @app.after_request
        def _(response: Response):
            from flask import g
            response_ = FlaskResponse(response)
            if hasattr(g, 'supertokens'):
                manage_cookies_post_response(g.supertokens, response_)

            return response_.response

    def set_error_handler(self):
        app = self.app
        from supertokens_python.exceptions import SuperTokensError

        from flask import request

        @app.errorhandler(SuperTokensError)
        def error_handler(error):
            from supertokens_python import Supertokens
            from supertokens_python.framework.flask.flask_request import \
                FlaskRequest
            from supertokens_python.framework.flask.flask_response import \
                FlaskResponse
            from werkzeug import Response
            st = Supertokens.get_instance()
            response = Response(json.dumps({}),
                                mimetype='application/json',
                                status=200)
            result = sync(st.handle_supertokens_error(
                FlaskRequest(request), error, FlaskResponse(response)))
            return result.response
