import http
import math
import psycopg2
from src.utils.psqldb import psql_connect, get_connection_from_pool
from flask import make_response, jsonify, request


def get_list_rta(page, per_page):
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
            SELECT COUNT(*) FROM rta_reverse_feed_details
            WHERE trant_type = 'P' AND (folio_no IS NULL OR folio_no = '0')
        """
        cur.execute(count_query)
        total_rows = cur.fetchone()[0]

        # query = """
        #     SELECT
        #         rta.client_id,
        #         upper(rta.reg_code) AS reg_code,
        #         rta.client_name,
        #         cm.pan_number,
        #         rta.trant_type AS transaction_type,
        #         rta.user_trxn_no,
        #         rta.amc_code,
        #         rta.broker_code,
        #         rta.id,
        #         rta.updated_at,
        #         u.user_name AS updated_by,
        #         rta.order_date,
        #         rta.amount,
        #         rta.nom_status,
        #         rta.aof_status,
        #         rta.nom_tiff_size,
        #         rta.aof_tiff_size,
        #         rta.downloaded_on
        #     FROM
        #         rta_reverse_feed_details rta
        #     INNER JOIN
        #         client_master cm ON cm.client_id = rta.client_id
        #     INNER JOIN
        #         users u ON u.id = rta.updated_by
        #     WHERE
        #         rta.trant_type = 'P'
        #         AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        #     ORDER BY
        #         rta.id DESC
        #     OFFSET %s;

        # """

        query = """
    SELECT
        rta.client_id,
        upper(rta.reg_code) AS reg_code,
        rta.client_name,
        cm.pan_number,
        rta.trant_type AS transaction_type,
        rta.user_trxn_no,
        rta.amc_code,
        rta.broker_code,
        rta.id,
        rta.updated_at,
        u.user_name AS updated_by,
        rta.order_date,
        rta.amount,
        kr.ih_no,
        rta.nom_status,
        rta.aof_status,
        rta.nom_tiff_size,
        rta.aof_tiff_size,
        rta.nom_downloaded_on,
        rta.aof_downloaded_on
    FROM
        rta_reverse_feed_details rta
    INNER JOIN
        client_master cm ON cm.client_id = rta.client_id
    INNER JOIN
        users u ON u.id = rta.updated_by
    LEFT JOIN 
        karvy_reverse_field kr ON kr.usr_txn_no = rta.user_trxn_no
    WHERE
        rta.trant_type = 'P'
        AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        AND rta.aof_downloaded_on is null
    ORDER BY
        rta.id DESC
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
                'client_id': row[0],
                'reg_code': row[1],
                'client_name': row[2],
                'pan_number': row[3],
                'transaction_type': row[4],
                'user_trxn_no': row[5],
                'amc_code': row[6],
                'broker_code': row[7],
                'id': row[8],
                'updated_at': row[9],
                'updated_by': row[10],
                'order_date': row[11],
                'amount': row[12],
                'ih_no': row[13],
                'nom_status': row[14],
                'aof_status': row[15],
                'nom_tiff_size': f'{round(float(row[16])/1000, 2)} MB' if row[16] != 'N/A' else 'N/A',
                'aof_tiff_size': f'{round(float(row[17])/1000, 2)} MB' if row[17] != 'N/A' else 'N/A',
                'nom_tiff_kb_size': 'N/A' if row[16] is None else row[16],
                'aof_tiff_kb_size': 'N/A' if row[17] is None else row[17],
                'nom_downloaded_on': 'N/A' if row[18] is None else row[18],
                'aof_downloaded_on': 'N/A' if row[19] is None else row[19],
                'AOF_Karvy_TIFF_file_name': f'INP000005874{row[3]}',
                'AOF_cams_TIFF_file_name': f'IFFWPMS${row[3]}$AOF',
                'Nominee_cams_TIFF_file_name': f'FN${row[6]}$IFFWPMS${row[5]}',
                'Nominee_karvy_TIFF_file_name': f'{row[7]}~{row[6]}~{row[5]}',
                'cam_nom_txt': f'{row[6]}|IFFWPMS|{row[5]}|{row[3]}|{row[2]}|FN${row[6]}$IFFWPMS${row[5]}',
                'cams_aof_txt': f'IFFWPMS|{row[3]}|{row[2]}|AOF|IFFWPMS${row[3]}$AOF',
                'karvy_aof_dbf': f'001,{row[5]},{row[3]},{row[6]},{row[7]},{row[7]}, , ,{row[2]},1,N,OF,AOF/POA/BR/ASL/PAN/KYC,{row[3]},{row[13]},Y'
            })

        return make_response(jsonify({"payload": payload, "row_count": total_rows}), http.HTTPStatus.OK)

    except psycopg2.Error as e:
        # Handle any errors that occur during the database operations
        return make_response(jsonify({"message": "Internal Server Error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)


def get_list_rta_old(page, per_page):
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
            SELECT COUNT(*) FROM rta_reverse_feed_details
            WHERE trant_type = 'P' AND (folio_no IS NULL OR folio_no = '0')
        """
        cur.execute(count_query)
        total_rows = cur.fetchone()[0]

        # query = """
        #     SELECT
        #         rta.client_id,
        #         upper(rta.reg_code) AS reg_code,
        #         rta.client_name,
        #         cm.pan_number,
        #         rta.trant_type AS transaction_type,
        #         rta.user_trxn_no,
        #         rta.amc_code,
        #         rta.broker_code,
        #         rta.id,
        #         rta.updated_at,
        #         u.user_name AS updated_by,
        #         rta.order_date,
        #         rta.amount,
        #         rta.nom_status,
        #         rta.aof_status,
        #         rta.nom_tiff_size,
        #         rta.aof_tiff_size,
        #         rta.downloaded_on
        #     FROM
        #         rta_reverse_feed_details rta
        #     INNER JOIN
        #         client_master cm ON cm.client_id = rta.client_id
        #     INNER JOIN
        #         users u ON u.id = rta.updated_by
        #     WHERE
        #         rta.trant_type = 'P'
        #         AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        #     ORDER BY
        #         rta.id DESC
        #     OFFSET %s;

        # """

        query = """
    SELECT
        rta.client_id,
        upper(rta.reg_code) AS reg_code,
        rta.client_name,
        cm.pan_number,
        rta.trant_type AS transaction_type,
        rta.user_trxn_no,
        rta.amc_code,
        rta.broker_code,
        rta.id,
        rta.updated_at,
        u.user_name AS updated_by,
        rta.order_date,
        rta.amount,
        kr.ih_no,
        rta.nom_status,
        rta.aof_status,
        rta.nom_tiff_size,
        rta.aof_tiff_size,
        rta.nom_downloaded_on,
        rta.aof_downloaded_on
    FROM
        rta_reverse_feed_details rta
    INNER JOIN
        client_master cm ON cm.client_id = rta.client_id
    INNER JOIN
        users u ON u.id = rta.updated_by
    LEFT JOIN 
        karvy_reverse_field kr ON kr.usr_txn_no = rta.user_trxn_no
    WHERE
        rta.trant_type = 'P'
        AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        AND rta.aof_downloaded_on is not null
    ORDER BY
        rta.id DESC
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
                'client_id': row[0],
                'reg_code': row[1],
                'client_name': row[2],
                'pan_number': row[3],
                'transaction_type': row[4],
                'user_trxn_no': row[5],
                'amc_code': row[6],
                'broker_code': row[7],
                'id': row[8],
                'updated_at': row[9],
                'updated_by': row[10],
                'order_date': row[11],
                'amount': row[12],
                'ih_no': row[13],
                'nom_status': row[14],
                'aof_status': row[15],
                'nom_tiff_size': f'{round(float(row[16])/1000, 2)} MB' if row[16] != 'N/A' else 'N/A',
                'aof_tiff_size': f'{round(float(row[17])/1000, 2)} MB' if row[17] != 'N/A' else 'N/A',
                'nom_tiff_kb_size': 'N/A' if row[16] is None else row[16],
                'aof_tiff_kb_size': 'N/A' if row[17] is None else row[17],
                'nom_downloaded_on': 'N/A' if row[18] is None else row[18],
                'aof_downloaded_on': 'N/A' if row[19] is None else row[19],
                'AOF_Karvy_TIFF_file_name': f'INP000005874{row[3]}',
                'AOF_cams_TIFF_file_name': f'IFFWPMS${row[3]}$AOF',
                'Nominee_cams_TIFF_file_name': f'FN${row[6]}$IFFWPMS${row[5]}',
                'Nominee_karvy_TIFF_file_name': f'{row[7]}~{row[6]}~{row[5]}',
                'cam_nom_txt': f'{row[6]}|IFFWPMS|{row[5]}|{row[3]}|{row[2]}|FN${row[6]}$IFFWPMS${row[5]}',
                'cams_aof_txt': f'IFFWPMS|{row[3]}|{row[2]}|AOF|IFFWPMS${row[3]}$AOF',
                'karvy_aof_dbf': f'001,{row[5]},{row[3]},{row[6]},{row[7]},{row[7]}, , ,{row[2]},1,N,OF,AOF/POA/BR/ASL/PAN/KYC,{row[3]},{row[13]},Y'
            })

        return make_response(jsonify({"payload": payload, "row_count": total_rows}), http.HTTPStatus.OK)

    except psycopg2.Error as e:
        # Handle any errors that occur during the database operations
        return make_response(jsonify({"message": "Internal Server Error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

# Nomineeeeeeee


def get_list_rta_nom(page, per_page):
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
            SELECT COUNT(*) FROM rta_reverse_feed_details
            WHERE trant_type = 'P' AND (folio_no IS NULL OR folio_no = '0')
        """
        cur.execute(count_query)
        total_rows = cur.fetchone()[0]

        # query = """
        #     SELECT
        #         rta.client_id,
        #         upper(rta.reg_code) AS reg_code,
        #         rta.client_name,
        #         cm.pan_number,
        #         rta.trant_type AS transaction_type,
        #         rta.user_trxn_no,
        #         rta.amc_code,
        #         rta.broker_code,
        #         rta.id,
        #         rta.updated_at,
        #         u.user_name AS updated_by,
        #         rta.order_date,
        #         rta.amount,
        #         rta.nom_status,
        #         rta.aof_status,
        #         rta.nom_tiff_size,
        #         rta.aof_tiff_size,
        #         rta.downloaded_on
        #     FROM
        #         rta_reverse_feed_details rta
        #     INNER JOIN
        #         client_master cm ON cm.client_id = rta.client_id
        #     INNER JOIN
        #         users u ON u.id = rta.updated_by
        #     WHERE
        #         rta.trant_type = 'P'
        #         AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        #     ORDER BY
        #         rta.id DESC
        #     OFFSET %s;

        # """

        query = """
    SELECT
        rta.client_id,
        upper(rta.reg_code) AS reg_code,
        rta.client_name,
        cm.pan_number,
        rta.trant_type AS transaction_type,
        rta.user_trxn_no,
        rta.amc_code,
        rta.broker_code,
        rta.id,
        rta.updated_at,
        u.user_name AS updated_by,
        rta.order_date,
        rta.amount,
        kr.ih_no,
        rta.nom_status,
        rta.aof_status,
        rta.nom_tiff_size,
        rta.aof_tiff_size,
        rta.nom_downloaded_on,
        rta.aof_downloaded_on
    FROM
        rta_reverse_feed_details rta
    INNER JOIN
        client_master cm ON cm.client_id = rta.client_id
    INNER JOIN
        users u ON u.id = rta.updated_by
    LEFT JOIN 
        karvy_reverse_field kr ON kr.usr_txn_no = rta.user_trxn_no
    WHERE
        rta.trant_type = 'P'
        AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        AND rta.nom_downloaded_on is null
    ORDER BY
        rta.id DESC
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
                'client_id': row[0],
                'reg_code': row[1],
                'client_name': row[2],
                'pan_number': row[3],
                'transaction_type': row[4],
                'user_trxn_no': row[5],
                'amc_code': row[6],
                'broker_code': row[7],
                'id': row[8],
                'updated_at': row[9],
                'updated_by': row[10],
                'order_date': row[11],
                'amount': row[12],
                'ih_no': row[13],
                'nom_status': row[14],
                'aof_status': row[15],
                'nom_tiff_size': f'{round(float(row[16])/1000, 2)} MB' if row[16] != 'N/A' else 'N/A',
                'aof_tiff_size': f'{round(float(row[17])/1000, 2)} MB' if row[17] != 'N/A' else 'N/A',
                'nom_tiff_kb_size': 'N/A' if row[16] is None else row[16],
                'aof_tiff_kb_size': 'N/A' if row[17] is None else row[17],
                'nom_downloaded_on': 'N/A' if row[18] is None else row[18],
                'aof_downloaded_on': 'N/A' if row[19] is None else row[19],
                'AOF_Karvy_TIFF_file_name': f'INP000005874{row[3]}',
                'AOF_cams_TIFF_file_name': f'IFFWPMS${row[3]}$AOF',
                'Nominee_cams_TIFF_file_name': f'FN${row[6]}$IFFWPMS${row[5]}',
                'Nominee_karvy_TIFF_file_name': f'{row[7]}~{row[6]}~{row[5]}',
                'cam_nom_txt': f'{row[6]}|IFFWPMS|{row[5]}|{row[3]}|{row[2]}|FN${row[6]}$IFFWPMS${row[5]}',
                'cams_aof_txt': f'IFFWPMS|{row[3]}|{row[2]}|AOF|IFFWPMS${row[3]}$AOF',
                'karvy_aof_dbf': f'001,{row[5]},{row[3]},{row[6]},{row[7]},{row[7]}, , ,{row[2]},1,N,OF,AOF/POA/BR/ASL/PAN/KYC,{row[3]},{row[13]},Y'
            })

        return make_response(jsonify({"payload": payload, "row_count": total_rows}), http.HTTPStatus.OK)

    except psycopg2.Error as e:
        # Handle any errors that occur during the database operations
        return make_response(jsonify({"message": "Internal Server Error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)


def get_list_rta_nom_old(page, per_page):
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
            SELECT COUNT(*) FROM rta_reverse_feed_details
            WHERE trant_type = 'P' AND (folio_no IS NULL OR folio_no = '0')
        """
        cur.execute(count_query)
        total_rows = cur.fetchone()[0]

        # query = """
        #     SELECT
        #         rta.client_id,
        #         upper(rta.reg_code) AS reg_code,
        #         rta.client_name,
        #         cm.pan_number,
        #         rta.trant_type AS transaction_type,
        #         rta.user_trxn_no,
        #         rta.amc_code,
        #         rta.broker_code,
        #         rta.id,
        #         rta.updated_at,
        #         u.user_name AS updated_by,
        #         rta.order_date,
        #         rta.amount,
        #         rta.nom_status,
        #         rta.aof_status,
        #         rta.nom_tiff_size,
        #         rta.aof_tiff_size,
        #         rta.downloaded_on
        #     FROM
        #         rta_reverse_feed_details rta
        #     INNER JOIN
        #         client_master cm ON cm.client_id = rta.client_id
        #     INNER JOIN
        #         users u ON u.id = rta.updated_by
        #     WHERE
        #         rta.trant_type = 'P'
        #         AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        #     ORDER BY
        #         rta.id DESC
        #     OFFSET %s;

        # """

        query = """
    SELECT
        rta.client_id,
        upper(rta.reg_code) AS reg_code,
        rta.client_name,
        cm.pan_number,
        rta.trant_type AS transaction_type,
        rta.user_trxn_no,
        rta.amc_code,
        rta.broker_code,
        rta.id,
        rta.updated_at,
        u.user_name AS updated_by,
        rta.order_date,
        rta.amount,
        kr.ih_no,
        rta.nom_status,
        rta.aof_status,
        rta.nom_tiff_size,
        rta.aof_tiff_size,
        rta.nom_downloaded_on,
        rta.aof_downloaded_on
    FROM
        rta_reverse_feed_details rta
    INNER JOIN
        client_master cm ON cm.client_id = rta.client_id
    INNER JOIN
        users u ON u.id = rta.updated_by
    LEFT JOIN 
        karvy_reverse_field kr ON kr.usr_txn_no = rta.user_trxn_no
    WHERE
        rta.trant_type = 'P'
        AND (rta.folio_no IS NULL OR rta.folio_no = '0')
        AND rta.nom_downloaded_on is not null
    ORDER BY
        rta.id DESC
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
                'client_id': row[0],
                'reg_code': row[1],
                'client_name': row[2],
                'pan_number': row[3],
                'transaction_type': row[4],
                'user_trxn_no': row[5],
                'amc_code': row[6],
                'broker_code': row[7],
                'id': row[8],
                'updated_at': row[9],
                'updated_by': row[10],
                'order_date': row[11],
                'amount': row[12],
                'ih_no': row[13],
                'nom_status': row[14],
                'aof_status': row[15],
                'nom_tiff_size': f'{round(float(row[16])/1000, 2)} MB' if row[16] != 'N/A' else 'N/A',
                'aof_tiff_size': f'{round(float(row[17])/1000, 2)} MB' if row[17] != 'N/A' else 'N/A',
                'nom_tiff_kb_size': 'N/A' if row[16] is None else row[16],
                'aof_tiff_kb_size': 'N/A' if row[17] is None else row[17],
                'nom_downloaded_on': 'N/A' if row[18] is None else row[18],
                'aof_downloaded_on': 'N/A' if row[19] is None else row[19],
                'AOF_Karvy_TIFF_file_name': f'INP000005874{row[3]}',
                'AOF_cams_TIFF_file_name': f'IFFWPMS${row[3]}$AOF',
                'Nominee_cams_TIFF_file_name': f'FN${row[6]}$IFFWPMS${row[5]}',
                'Nominee_karvy_TIFF_file_name': f'{row[7]}~{row[6]}~{row[5]}',
                'cam_nom_txt': f'{row[6]}|IFFWPMS|{row[5]}|{row[3]}|{row[2]}|FN${row[6]}$IFFWPMS${row[5]}',
                'cams_aof_txt': f'IFFWPMS|{row[3]}|{row[2]}|AOF|IFFWPMS${row[3]}$AOF',
                'karvy_aof_dbf': f'001,{row[5]},{row[3]},{row[6]},{row[7]},{row[7]}, , ,{row[2]},1,N,OF,AOF/POA/BR/ASL/PAN/KYC,{row[3]},{row[13]},Y'
            })

        return make_response(jsonify({"payload": payload, "row_count": total_rows}), http.HTTPStatus.OK)

    except psycopg2.Error as e:
        # Handle any errors that occur during the database operations
        return make_response(jsonify({"message": "Internal Server Error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)
