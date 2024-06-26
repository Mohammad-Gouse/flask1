import http
import json

import bcrypt
from flask import Flask, make_response, jsonify
from werkzeug.security import check_password_hash

# from src.api.authentications.auth_handler import auth_handler_bp
from src.utils.psqldb import get_connection_from_pool, psql_connect, psql_release_connection, psql_close_connection
import psycopg2
import jwt


def login(user_name, pwd):
    global ps_connection, pool_conn
    try:
        pool_conn = psql_connect()
        if not pool_conn:
            return make_response(jsonify({"message": "db error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool_conn)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute("""
                SELECT rbac_roles.role_name 
                FROM user_role_mapping 
                INNER JOIN rbac_roles ON user_role_mapping.role_id = rbac_roles.role_id
                WHERE user_id = (SELECT id FROM users WHERE user_name = %s)
            """, (user_name,))
            roles_data = ps_cursor.fetchall()
            roles_array = [role[0] for role in roles_data]
            encoded_jwt = jwt.encode(
                {"user_name": user_name, "rbac_roles": roles_array}, "secret", algorithm="HS256")
            # decode_data = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
            # payload = decode_data.get('payload')
            ps_cursor.execute(
                "SELECT password FROM users WHERE user_name = %s", (user_name,))
            data = ps_cursor.fetchone()
            ps_cursor.close()
            psql_release_connection(pool_conn, ps_connection)
            psql_close_connection(pool_conn)
            if data:
                if check_password_hash(data[0], pwd):
                    return make_response(jsonify({"token": encoded_jwt, "message": "Logged in Successfully"}), http.HTTPStatus.OK)
                return make_response(jsonify({"message": "Invalid Password"}), http.HTTPStatus.UNAUTHORIZED)
            return make_response(jsonify({"message": "User not found"}), http.HTTPStatus.NOT_FOUND)

    except psycopg2.DatabaseError as error:
        psql_release_connection(pool_conn, ps_connection)
        psql_close_connection(pool_conn)
        return make_response(json.dumps(error), http.HTTPStatus.INTERNAL_SERVER_ERROR)
