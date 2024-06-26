# import psycopg2
# from src.utils.psqldb import get_connection_from_pool, psql_connect
# from flask import jsonify, make_response


# def list_users():
#     try:
#         pool = psql_connect()
#         ps_connection = get_connection_from_pool(pool)

#         if ps_connection:
#             cursor = ps_connection.cursor()
#         list_users_query = """
#             SELECT u.id, u.user_name, array_agg(r.role_name) as roles, u.updated_at as last_updated
#             FROM users u
#             LEFT JOIN user_role_mapping urm ON u.id = urm.user_id
#             LEFT JOIN rbac_roles r ON urm.role_id = r.role_id
#             WHERE u.is_active = true
#             GROUP BY u.id order by u.id desc;
#         """

#         try:
#             cursor.execute(list_users_query)
#             users_data = cursor.fetchall()

#             user_list = []
#             for user_data in users_data:
#                 user_info = {
#                     "id": user_data[0],
#                     "username": user_data[1],
#                     # Convert roles to list or empty list if None
#                     "roles": user_data[2] or [],
#                     "last_updated": user_data[3]
#                 }
#                 user_list.append(user_info)

#             cursor.close()
#             ps_connection.close()

#             return jsonify(user_list)

#         except psycopg2.Error as e:
#             cursor.close()
#             ps_connection.close()
#             return make_response(jsonify({"message": "Error retrieving user data"}), 500)

#     except Exception as e:
#         return make_response(jsonify({"message": "Server error"}), 500)

import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect
from flask import jsonify, make_response, request
import http


def list_users(page, per_page):
    try:
        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            cursor = ps_connection.cursor()

        # Get pagination parameters from the request
        page = int(request.args.get('page', 1))
        # Default to 10 records per page
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page

        list_users_query = """
            SELECT u.id, u.user_name, array_agg(r.role_name) as roles, u.updated_at as last_updated, uu.user_name as updated_by
            FROM users u
            LEFT JOIN user_role_mapping urm ON u.id = urm.user_id
            LEFT JOIN rbac_roles r ON urm.role_id = r.role_id
            LEFT JOIN users uu on u.updated_by = uu.id
            WHERE u.is_active = true
            GROUP BY u.id, uu.user_name
            ORDER BY u.id DESC
            OFFSET %s
            LIMIT %s;
        """

        try:
            cursor.execute(list_users_query, (offset, per_page))
            users_data = cursor.fetchall()

            # Get the total count of users for pagination
            total_count_query = """
                SELECT COUNT(*) FROM users WHERE is_active = true
            """
            cursor.execute(total_count_query)
            total_count = cursor.fetchone()[0]

            payload = []
            for user_data in users_data:
                user_info = {
                    "id": user_data[0],
                    "username": user_data[1],
                    # Convert roles to list or empty list if None
                    "roles": user_data[2] or [],
                    "last_updated": user_data[3],
                    "updated_by": user_data[4]
                }
                payload.append(user_info)

            cursor.close()
            ps_connection.close()

            # return jsonify({"total_count": total_count, "users": payload})
            return make_response(jsonify({"payload": payload, "row_count": total_count}), http.HTTPStatus.OK)
        except psycopg2.Error as e:
            cursor.close()
            ps_connection.close()
            return make_response(jsonify({"message": "Error retrieving user data"}), 500)

    except Exception as e:
        return make_response(jsonify({"message": "Server error"}), 500)
