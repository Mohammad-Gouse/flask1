import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect


def nominee_status_set(id):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        query = """
        UPDATE rta_reverse_feed_details
            SET nom_status = %s
            WHERE id = %s
        """
        cursor.execute(query, ('generated',id))
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")


def aof_status_set(id):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        query = """
        UPDATE rta_reverse_feed_details
            SET aof_status = %s
            WHERE id = %s
        """
        cursor.execute(query, ('generated',id))
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")


def poa_status_set(id):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        query = """
        UPDATE poa_rta_list
            SET poa_status = %s
            WHERE id = %s
        """
        cursor.execute(query, ('generated',id))
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")


