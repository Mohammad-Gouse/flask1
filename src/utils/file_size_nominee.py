import psycopg2
from src.utils.psqldb import get_connection_from_pool, psql_connect


def tiff_file_size_set(id, nominee_file_size):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        query = """
        UPDATE rta_reverse_feed_details
            SET nom_tiff_size = %s
            WHERE id = %s
        """
        cursor.execute(query, (nominee_file_size, id))
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")


def tiff_file_size_set_aof(id, aof_file_size):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        query = """
        UPDATE rta_reverse_feed_details
            SET aof_tiff_size = %s
            WHERE id = %s
        """
        cursor.execute(query, (aof_file_size, id))
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")

def tiff_file_size_poa(id, poa_file_sizee):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        query = """
        UPDATE poa_rta_list
            SET poa_tiff_size = %s
            WHERE id = %s
        """
        cursor.execute(query, (poa_file_sizee, id))
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")



def download_on_nominee(ids):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        cursor = ps_connection.cursor()

        for id_to_update in ids:
            query = """UPDATE rta_reverse_feed_details
                SET nom_downloaded_on = now()
                WHERE id = %s"""

            cursor.execute(query, (id_to_update,))
            ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")

def download_on_aof(ids):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        cursor = ps_connection.cursor()

        for id_to_update in ids:
            query = """UPDATE rta_reverse_feed_details
                SET aof_downloaded_on = now()
                WHERE id = %s"""

            cursor.execute(query, (id_to_update,))
            ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")

def download_on_poa(ids):
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        cursor = ps_connection.cursor()

        for id_to_update in ids:
            query = """UPDATE poa_rta_list
                SET poa_downloaded_on = now()
                WHERE id = %s"""

            cursor.execute(query, (id_to_update,))
            ps_connection.commit()

        cursor.close()
        ps_connection.close()

    else:
        print("Failed to establish a database connection.")