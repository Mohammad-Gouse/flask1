from audioop import error
from functools import wraps
from flask import make_response, jsonify, request

import jwt

from audioop import error
from functools import wraps
from flask import make_response, jsonify, request

from . import get_user_role

import jwt

from audioop import error
from functools import wraps
from . import get_user_role

import jwt


def token_authorizer(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization').split(' ')[1]
            if not token:
                return make_response(jsonify({"message": "Token is missing"}), 401)
            try:
                alg = jwt.get_unverified_header(token).get("alg")
                payload = jwt.decode(token, "secret", algorithms=[alg])
                user_role = get_user_role.get_user_role_from_database(
                    payload.get('user_name'))
                if user_role != 'admin' and user_role not in roles:
                    return make_response(jsonify({"message": "You do not have the required role"}), 403)
                else:
                    return make_response(jsonify({"message": "Access allowed successfully"}), 200)


            except error:
                return make_response(jsonify({"message": error}), 400)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
