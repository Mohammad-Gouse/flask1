import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect


def get_user_role_from_database(username):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

    query = """
        SELECT r.role_name
        FROM users u
        JOIN user_role_mapping m ON u.id = m.user_id
        JOIN rbac_roles r ON m.role_id = r.role_id
        WHERE u.user_name = %s;
    """
    cursor.execute(query, (username,))
    role = cursor.fetchone()

    cursor.close()
    ps_connection.close()

    if role:
        return role[0]  # Extract the role from the result
    else:
        return None  # Return None if the user or role is not found
