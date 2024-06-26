import http

import psycopg2
from src.utils.psqldb import psql_connect, get_connection_from_pool
from flask import make_response, jsonify, request

all_data = []  # Populate this list with your actual data
page_size = 5  # Number of items per page


def get_poa_list_rta(page, per_page):
    try:

        # Calculate the offset based on page and per_page values
        offset = (page - 1) * per_page

        # Establish a connection to the PostgreSQL database
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect to the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cur = ps_connection.cursor()

        # Execute the query with pagination
        count_query = """
            SELECT COUNT(*) FROM poa_rta_list
            WHERE poa = 'E'
        """
        cur.execute(count_query)
        total_rows = cur.fetchone()[0]

        # print("row count", total_rows)

        query = """
            SELECT 
            rta.clientid, rta.clientname, rta.usertrxnno, rta.amccode, rta.brokercode, rta.id,
            rta.updated_at, u.user_name as updated_by, rta.foliono, 
        rta.poa_status,
        rta.poa_tiff_size,
        rta.poa_downloaded_on
            FROM poa_rta_list rta
            JOIN users u ON rta.updated_by = u.id
            WHERE rta.poa = 'E' and rta.poa_downloaded_on is null
            ORDER BY id DESC
            OFFSET %s;

        """
        # cur.execute(query, (offset, per_page))
        cur.execute(query, (offset,))

        # Fetch all the rows returned by the query
        rows = cur.fetchall()

        # Close the cursor and the database connection
        cur.close()
        ps_connection.close()

        # Prepare the payload with key-value pairs
        payload = []
        for row in rows:
            payload.append({
                'clientid': row[0],
                'clientname': row[1],
                'usertrxnno': row[2],
                'amccode': row[3],
                'brokercode': row[4],
                'id': row[5],
                'updated_at': row[6],
                'updated_by': row[7],
                'folio_no': row[8],
                'poa_status': row[9],
                'poa_tiff_size': f'{round(float(row[10])/1000, 2)} MB' if row[10] != 'N/A' else 'N/A',
                'poa_downloaded_on': 'N/A' if row[11] is None else row[11],
                'poa_tiff_kb_size': 'N/A' if row[10] is None else row[10],
                'poa_tiff_file_name': f'{row[3]}$IIFWPMS${row[2]}${row[8]}',
                'poa_dbf': f'{row[3]},IIFWPMS,{row[2]},{row[5]},POA,360 One Portfolio Managers Ltd,{row[3]}$IIFWPMS${row[2]}${row[5]}'

            })

        page = int(request.args.get('page', 1))
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        paginated_data = all_data[start_index:end_index]
        total_row_count = len(all_data)

        return make_response(jsonify({"payload": payload, "row_count": total_rows, "paginated_data": paginated_data}), http.HTTPStatus.OK)

    except psycopg2.Error as e:
        # Handle any errors that occur during the database operations
        return make_response(jsonify({"message": "Internal Server Error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)


def get_poa_list_rta_old(page, per_page):
    try:

        # Calculate the offset based on page and per_page values
        offset = (page - 1) * per_page

        # Establish a connection to the PostgreSQL database
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect to the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cur = ps_connection.cursor()

        # Execute the query with pagination
        count_query = """
            SELECT COUNT(*) FROM poa_rta_list
            WHERE poa = 'E'
        """
        cur.execute(count_query)
        total_rows = cur.fetchone()[0]

        # print("row count", total_rows)

        query = """
            SELECT 
            rta.clientid, rta.clientname, rta.usertrxnno, rta.amccode, rta.brokercode, rta.id,
            rta.updated_at, u.user_name as updated_by, rta.foliono, 
        rta.poa_status,
        rta.poa_tiff_size,
        rta.poa_downloaded_on
            FROM poa_rta_list rta
            JOIN users u ON rta.updated_by = u.id
            WHERE rta.poa = 'E' and rta.poa_downloaded_on is not null
            ORDER BY id DESC
            OFFSET %s;

        """
        # cur.execute(query, (offset, per_page))
        cur.execute(query, (offset,))

        # Fetch all the rows returned by the query
        rows = cur.fetchall()

        # Close the cursor and the database connection
        cur.close()
        ps_connection.close()

        # Prepare the payload with key-value pairs
        payload = []
        for row in rows:
            payload.append({
                'clientid': row[0],
                'clientname': row[1],
                'usertrxnno': row[2],
                'amccode': row[3],
                'brokercode': row[4],
                'id': row[5],
                'updated_at': row[6],
                'updated_by': row[7],
                'folio_no': row[8],
                'poa_status': row[9],
                'poa_tiff_size': f'{round(float(row[10])/1000, 2)} MB' if row[10] != 'N/A' else 'N/A',
                'poa_downloaded_on': 'N/A' if row[11] is None else row[11],
                'poa_tiff_kb_size': 'N/A' if row[10] is None else row[10],
                'poa_tiff_file_name': f'{row[3]}$IIFWPMS${row[2]}${row[8]}',
                'poa_dbf': f'{row[3]},IIFWPMS,{row[2]},{row[5]},POA,360 One Portfolio Managers Ltd,{row[3]}$IIFWPMS${row[2]}${row[5]}'

            })

        page = int(request.args.get('page', 1))
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        paginated_data = all_data[start_index:end_index]
        total_row_count = len(all_data)

        return make_response(jsonify({"payload": payload, "row_count": total_rows, "paginated_data": paginated_data}), http.HTTPStatus.OK)

    except psycopg2.Error as e:
        # Handle any errors that occur during the database operations
        return make_response(jsonify({"message": "Internal Server Error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)
