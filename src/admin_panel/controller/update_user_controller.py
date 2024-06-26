import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash


def update_user(user_id, username, roles):
    try:
        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            cursor = ps_connection.cursor()

        data = request.get_json()
        if not data:
            return make_response(jsonify({"message": "Invalid data"}), 400)

        update_user_query = """
            UPDATE users
            SET user_name = %s
            WHERE id = %s
        """

        delete_user_roles_query = """
            DELETE FROM user_role_mapping
            WHERE user_id = %s
        """

        insert_query = """
            INSERT INTO user_role_mapping (user_id, role_id)
            VALUES (%s, %s);
        """

        try:
            # Update user information in users table
            cursor.execute(update_user_query, (username, user_id))

            cursor.execute(delete_user_roles_query, (user_id,))

            # Update user roles in user_role_mapping table
            for role in roles:
                cursor.execute(insert_query,
                               (user_id, role))

            ps_connection.commit()
        except psycopg2.Error as e:
            ps_connection.rollback()
            return make_response(jsonify({"message": "Error updating user"}), 500)

        cursor.close()
        ps_connection.close()

        return make_response(jsonify({"message": "User updated successfully"}), 200)

    except Exception as e:
        return make_response(jsonify({"message": "Server error"}), 500)
