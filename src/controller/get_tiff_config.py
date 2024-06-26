from src.utils.psqldb import get_connection_from_pool, psql_connect
from flask import Blueprint, request, jsonify, make_response, send_file, Response


def get_poa_quality():
    # Create a connection pool and get a connection
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        # Execute a SELECT query to retrieve the quality level
        select_query = "SELECT poa_quality_level FROM tiff_config;"
        cursor.execute(select_query)

        # Fetch the quality level from the result
        quality_level = cursor.fetchone()

        if quality_level:
            # quality_level will be a tuple; extract the value
            quality_level = quality_level[0]

            # Close the cursor and the connection
            cursor.close()
            ps_connection.close()

            # Return the quality level in the response
            response = quality_level
            return response


def get_aof_quality():
    # Create a connection pool and get a connection
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        # Execute a SELECT query to retrieve the quality level
        select_query = "SELECT aof_quality_level FROM tiff_config;"
        cursor.execute(select_query)

        # Fetch the quality level from the result
        quality_level = cursor.fetchone()

        if quality_level:
            # quality_level will be a tuple; extract the value
            quality_level = quality_level[0]

            # Close the cursor and the connection
            cursor.close()
            ps_connection.close()

            # Return the quality level in the response
            response = quality_level
            return response
