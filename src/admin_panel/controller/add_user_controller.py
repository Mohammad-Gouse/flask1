import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash


def username_exists(username, cursor):
    """
    Helper function to check if a username already exists in the 'users' table.
    """
    check_username_query = """
        SELECT EXISTS(SELECT 1 FROM users WHERE user_name = %s)
    """
    cursor.execute(check_username_query, (username,))
    return cursor.fetchone()[0]


def add_user(username, password, roles):
    try:
        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            cursor = ps_connection.cursor()

        data = request.get_json()
        if not data:
            return make_response(jsonify({"message": "Invalid data"}), 400)

        hashed_password = generate_password_hash(password)

        if username_exists(username, cursor):
            # print("already exist")
            return make_response(jsonify({"message": "Username already exists"}), 401)

        insert_user_query = """
            INSERT INTO users (user_name, password)
            VALUES (%s, %s)
            RETURNING id
        """

        insert_user_role_mapping_query = """
            INSERT INTO user_role_mapping (user_id, role_id)
            VALUES (%s, %s)
        """

        try:
            # Insert user into users table
            cursor.execute(insert_user_query, (username,
                           hashed_password))
            user_id = cursor.fetchone()[0]

            # Insert user-role mapping into user_role_mapping table for each role in the array
            for role in roles:
                # Get role_id based on role_name
                # get_role_id_query = """
                #     SELECT role_id FROM rbac_roles WHERE role_name = %s
                # """
                # cursor.execute(get_role_id_query, (role,))
                # role_id = cursor.fetchone()[0]

                cursor.execute(insert_user_role_mapping_query,
                               (user_id, role))

            ps_connection.commit()
        except psycopg2.Error as e:
            ps_connection.rollback()
            return make_response(jsonify({"message": "Error adding user"}), 500)

        cursor.close()
        ps_connection.close()

        return make_response(jsonify({"message": "User added successfully"}), 200)

    except Exception as e:
        return make_response(jsonify({"message": "Server error"}), 500)
