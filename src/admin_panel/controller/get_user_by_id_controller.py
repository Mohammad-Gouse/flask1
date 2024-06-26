import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect
from flask import jsonify, make_response


def get_user_by_id(user_id):
    try:
        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            cursor = ps_connection.cursor()

        # get_user_query = """
        #     SELECT u.id, u.user_name, array_agg(r.role_name) as roles, u.updated_at as last_updated
        #     FROM users u
        #     LEFT JOIN user_role_mapping urm ON u.id = urm.user_id
        #     LEFT JOIN rbac_roles r ON urm.role_id = r.role_id
        #     WHERE u.id = %s
        #     GROUP BY u.id;
        # """

        get_user_query = """
        SELECT
            u.id,
            u.user_name,
            array_agg(r.role_id) as role_ids,
            u.updated_at as last_updated
        FROM
            users u
            LEFT JOIN user_role_mapping urm ON u.id = urm.user_id
            LEFT JOIN rbac_roles r ON urm.role_id = r.role_id
        WHERE
            u.id = %s
        GROUP BY
            u.id;
        """

        try:
            cursor.execute(get_user_query, (user_id,))
            user_data = cursor.fetchone()

            if not user_data:
                return make_response(jsonify({"message": "User not found"}), 404)

            user_info = {
                "id": user_data[0],
                "username": user_data[1],
                "roles": user_data[2] or [],
                "last_updated": user_data[3]
            }

            cursor.close()
            ps_connection.close()

            return jsonify(user_info)

        except psycopg2.Error as e:
            cursor.close()
            ps_connection.close()
            return make_response(jsonify({"message": "Error retrieving user data"}), 500)

    except Exception as e:
        return make_response(jsonify({"message": "Server error"}), 500)
