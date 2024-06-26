import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect
from flask import jsonify, make_response
import http


def delete_user(user_id):
    try:
        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            cursor = ps_connection.cursor()

        soft_delete_user_query = """
            UPDATE users
            SET is_active = false
            WHERE id = %s
        """

        try:
            cursor.execute(soft_delete_user_query, (user_id,))

            ps_connection.commit()

            cursor.close()
            ps_connection.close()

            return make_response(jsonify({"message": "User deleted successfully"}), http.HTTPStatus.OK)

        except psycopg2.Error as e:
            ps_connection.rollback()
            cursor.close()
            ps_connection.close()
            return make_response(jsonify({"message": "Error while deleting user"}), http.HTTPStatus.BAD_REQUEST)

    except Exception as e:
        return make_response(jsonify({"message": "Server error"}), 500)
