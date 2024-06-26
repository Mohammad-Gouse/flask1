import pandas as pd
from io import BytesIO
from flask import Flask, send_file, make_response, jsonify
import psycopg2
from src.utils.psqldb import psql_connect, get_connection_from_pool
from openpyxl.styles import NamedStyle
from openpyxl import Workbook
from openpyxl.styles import numbers
import warnings


# def download_excel():
#     # Fetch data from the database

#     data = fetch_data_from_database()

#     print("data: ", data)

#     # Create a Pandas DataFrame
#     df = pd.DataFrame(data)

#     excel_buffer = BytesIO()

#     df.to_excel(excel_buffer, index=False)

#     excel_buffer.seek(0)

#     # Define the filename for the Excel file
#     excel_filename = 'database_data.xlsx'

#     # Return the Excel file as a downloadable attachment
#     return send_file(excel_buffer, download_name=excel_filename, as_attachment=True)

def download_excel():
    # Fetch data from the database
    data = fetch_data_from_database()

    print("data: ", data)

    # Create a Pandas DataFrame
    df = pd.DataFrame(data)

    df[3] = df[3].dt.strftime('%m/%d/%Y')

    # Create an Excel writer
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlwt') as excel_writer:
        df.to_excel(excel_writer, sheet_name='Sheet1', index=False)

        # Get the openpyxl workbook and sheet objects
        # workbook = excel_writer.book
        # sheet = workbook['Sheet1']

        # # Set the date format for column '2' (assuming '2' corresponds to column 'B' in Excel)
        # date_format = NamedStyle(name='date_style', number_format='MM/DD/YYYY')
        # date_time_format = NamedStyle(
        #     name='date_style2', number_format='MM/DD/YYYY HH:MM:SS')
        # # sheet.column_dimensions['C'].style = date_format
        # for cell in sheet['C'][1:]:
        #     cell.style = date_format

        # for cell in sheet['D'][1:]:
        #     cell.style = date_time_format

    excel_buffer.seek(0)

    # Define the filename for the Excel file
    excel_filename = 'database_data.xls'

    # Return the Excel file as a downloadable attachment
    return send_file(excel_buffer, download_name=excel_filename, as_attachment=True)


def fetch_data_from_database():
    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect to the database."}), 501)

        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cur = ps_connection.cursor()

        # Execute the query with pagination
        query = """
            SELECT * FROM table1
        """
        cur.execute(query)
        total_rows = cur.fetchall()
        return total_rows
    except psycopg2.DatabaseError as error:
        return make_response(jsonify({"message": "Please check database connection details"}), 500)
