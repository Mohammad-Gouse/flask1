import csv
import datetime
import http
import os

import pandas.errors
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var
from src.utils.oracledb import session_pool
from src.utils.psqldb import get_connection_from_pool, psql_connect

TRANSACTION_FILE_NAME = Data_Var.data_store_location


def script_master_exist():
    from app import db
    from src.models.nse_script_master_model import NSE_Script_Master
    try:
        result = db.session.query(NSE_Script_Master).first()
        return result
    except sqlalchemy.exc.DatabaseError:
        return None


def get_transactions(file_name):
    import pandas as pd
    from app import db
    from src.models.ws_model import Utility
    # file_name = "transaction_" + str(datetime.datetime.now()).replace(" ", "T").replace(":", "-")
    sub_folder_name = "transaction"
    try:
        is_script_master_exist = script_master_exist()
        if not is_script_master_exist:
            return make_response(jsonify({"message": "Please upload NSE scheme master and then try again."}),
                                 http.HTTPStatus.NOT_FOUND)

        result = session_pool()
        if not result:
            return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
        if type(result) == str:
            return make_response(jsonify({"message": "Error while connecting WS database."}), http.HTTPStatus.CONFLICT)
        count = insert_query_data_to_utility(result)
        if count == 0:
            return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            output_query = f"COPY ({Data_Var.query_transaction}) TO STDOUT WITH (FORMAT CSV, DELIMITER '{Data_Var.file_delimiter}');"
            # output_query = f"COPY ({Data_Var.query_transaction}) TO STDOUT WITH (FORMAT CSV, DELIMITER '{Data_Var.file_delimiter}', HEADER);"
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            isTransactionDirExist = os.path.exists(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            if not isTransactionDirExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)
                f.close()
            ps_cursor.close()
            if len(pd.read_csv(
                    f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', header=None)) < 1:
                os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)

            db.session.query(Utility).filter(Utility.nse_download == 0).update(
                {Utility.nse_download: 1},
                synchronize_session="fetch"
            )
            db.session.commit()
            return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', as_attachment=True)
    except psycopg2.DatabaseError as error:
        db.session.rollback()
        os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def get_custody_buy(file_name):
    import pandas as pd
    from app import db
    from src.models.ws_model import Utility
    # file_name = "custody-buy_" + str(datetime.datetime.now()).replace(" ", "T").replace(":", "-")
    sub_folder_name = "custody-buy"
    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Please check database connection details"}),
                                 http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            output_query = f"COPY ({Data_Var.query_custody_buy}) TO STDOUT WITH (FORMAT CSV, DELIMITER '{Data_Var.file_delimiter}', HEADER);"
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            isTransactionDirExist = os.path.exists(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            if not isTransactionDirExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')

            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)
                f.close()
            ps_cursor.close()
            db_response = pd.read_csv(
                f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
            if len(db_response) < 1:
                os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}') as file_obj:
                next(file_obj)
                reader_obj = csv.reader(file_obj)
                for row in reader_obj:
                    db.session.query(Utility).filter(Utility.custody_buy == 0, Utility.order_ref == row[5]).update(
                        {Utility.custody_buy: 1},
                        synchronize_session="fetch"
                    )
            db.session.commit()
            return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', as_attachment=True)

    except psycopg2.DatabaseError as error:
        os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}), 400)


def get_custody_sell(file_name):
    import pandas as pd
    from app import db
    from src.models.ws_model import Utility
    # file_name = "custody-sell_" + str(datetime.datetime.now()).replace(" ", "T").replace(":", "-")
    sub_folder_name = "custody-sell"
    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            output_query = f"COPY ({Data_Var.query_custody_sell}) TO STDOUT WITH (FORMAT CSV, DELIMITER '{Data_Var.file_delimiter}', HEADER);"
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            isTransactionDirExist = os.path.exists(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            if not isTransactionDirExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')

            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)
                f.close()
            ps_cursor.close()
            db_response = pd.read_csv(
                f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
            if len(db_response) < 1:
                os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}') as file_obj:
                next(file_obj)
                reader_obj = csv.reader(file_obj)
                for row in reader_obj:
                    db.session.query(Utility).filter(Utility.custody_sell == 0, Utility.order_ref == row[7]).update(
                        {Utility.custody_sell: 1},
                        synchronize_session="fetch"
                    )
            db.session.commit()
            return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', as_attachment=True)

    except psycopg2.DatabaseError as error:
        os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def get_utrn_confirmation(file_name):
    import pandas as pd
    from app import db
    from src.models.ws_model import Utility
    # file_name = "utrn-confirmation_" + str(datetime.datetime.now()).replace(" ", "T").replace(":", "-")
    sub_folder_name = "utrn-confirmation"
    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            output_query = f"COPY ({Data_Var.query_utrn_confirmation}) TO STDOUT WITH (FORMAT CSV, DELIMITER '|' );"
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            isTransactionDirExist = os.path.exists(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            if not isTransactionDirExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')

            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)
                f.close()
            ps_cursor.close()
            try:
                if len(pd.read_csv(
                        f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')) < 1:
                    os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                    return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
            except pandas.errors.EmptyDataError:
                os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
            db.session.query(Utility).filter(Utility.utrn_confirmation == 0, Utility.custody_buy == 1).update(
                {Utility.utrn_confirmation: 1},
                synchronize_session="fetch"
            )
            db.session.commit()
            return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', as_attachment=True)

    except psycopg2.DatabaseError as error:
        os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
        return make_response(
            jsonify({"message": "We are unable to connect to database at this time. Please try again."}),
            http.HTTPStatus.INTERNAL_SERVER_ERROR)


def get_summary(data):
    import pandas as pd
    file_name = data.get('filename')
    sub_folder_name = "summary"
    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            if start_date == end_date:
                date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()
                date = date + datetime.timedelta(days=1)
                end_date = date.strftime("%m-%d-%Y")
            else:
                end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date().strftime("%m-%d-%Y")
            start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').date().strftime("%m-%d-%Y")
            output_query = f"COPY ({Data_Var.download_summary}) TO STDOUT WITH (FORMAT CSV, DELIMITER ',', HEADER);".format(
                start_date, end_date)
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            isTransactionDirExist = os.path.exists(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            if not isTransactionDirExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')

            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)
                f.close()
            ps_cursor.close()
            if len(pd.read_csv(
                    f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')) < 1:
                os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
            return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}',
                             as_attachment=True)

    except psycopg2.DatabaseError as error:
        print(error)
        os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)



def insert_query_data_to_utility(data):
    from app import db
    from src.models.ws_model import Utility
    try:
        count = 0
        for row in data:
            single_record = Utility(row)
            query_to_check_record_exist = db.session.query(Utility.id).filter(
                Utility.order_ref == single_record.order_ref)
            if db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            db.session.add(single_record)
            count += 1
        db.session.commit()
        return count
    except sqlalchemy.exc.DatabaseError:
        db.session.rollback()
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def upload_nse_transaction_response(data):
    from app import db
    from src.models.nse_transaction_model import NSE_Transaction_Model
    from src.models.ws_model import Utility
    try:
        list_of_csv_fields = data[0].lower().split(',')
        # for item in list_of_csv_fields:
        #     if item == '':
        #         list_of_csv_fields.remove(item)
        fields_of_db_table = Data_Var.nse_transaction_response_headers.lower().split(",")
        if len(list_of_csv_fields) != len(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload valid csv file"}), http.HTTPStatus.NOT_FOUND)

        # data.pop(0)
        count = 0
        for row in data:
            single_record = NSE_Transaction_Model(row.split(','))
            query_to_check_record_exist = db.session.query(Utility.id).filter(
                Utility.order_ref == single_record.order_ref, Utility.nse_download == 1)
            if not db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            db.session.query(Utility).filter(Utility.order_ref == single_record.order_ref).update(
                single_record.to_dict(), synchronize_session="fetch"
            )
            count += 1
        db.session.commit()
        if count < 1:
            return make_response(jsonify({"message": "No records updated"}),
                                 http.HTTPStatus.NOT_FOUND)

        if count == 1:
            return make_response(jsonify({"message": str(count) + " record updated."}),
                                 http.HTTPStatus.OK)
        return make_response(jsonify({"message": str(count) + " records updated."}),
                             http.HTTPStatus.OK)
    except sqlalchemy.exc.DatabaseError as error:
        db.session.rollback()
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def upload_utrn(data):
    from app import db
    from src.models.utrn_model import UTRN_Model
    from src.models.ws_model import Utility
    try:
        list_of_csv_fields = data[0].lower().split(',')
        for item in list_of_csv_fields:
            if item == '':
                list_of_csv_fields.remove(item)
        fields_of_db_table = Data_Var.utrn_upload_headers.lower().split(",")
        if set(list_of_csv_fields) != set(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload valid csv file"}), http.HTTPStatus.NOT_FOUND)
        data.pop(0)
        count = 0
        for row in data:
            single_record = UTRN_Model(row.split(','))
            query_to_check_record_exist = db.session.query(Utility.id).filter(
                Utility.custody_buy == 1, Utility.order_ref == single_record.order_ref)
            if not db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            db.session.query(Utility).filter(Utility.order_ref == single_record.order_ref).update(
                {Utility.utrn_number: str(single_record.utrn_number), Utility.utrn_response: 1},
                synchronize_session="fetch"
            )
            count += 1
        db.session.commit()
        if count < 1:
            return make_response(jsonify({"message": "No records updated"}), http.HTTPStatus.NOT_FOUND)
        if count == 1:
            return make_response(jsonify({"message": str(count) + " record updated."}), http.HTTPStatus.OK)
        return make_response(jsonify({"message": str(count) + " records updated."}), http.HTTPStatus.OK)
    except sqlalchemy.exc.DatabaseError as error:
        db.session.rollback()
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def add_nse_script_master(data):
    from app import db
    try:
        from src.models.nse_script_master_model import NSE_Script_Master
        # list_of_csv_fields = data[0].split(',')
        # for item in list_of_csv_fields:
        #     if item == '':
        #         list_of_csv_fields.remove(item)
        # fields_of_db_table = Data_Var.nse_script_master_headers.split(",")
        # if set(list_of_csv_fields) != set(fields_of_db_table):
        #     return make_response(jsonify({"message": "Please upload valid csv file"}), http.HTTPStatus.BAD_REQUEST)

        data.pop(0)
        bulk_insert_data = []
        count = 0
        for row in data:
            count += 1
            single_record = NSE_Script_Master(row.split(','))
            bulk_insert_data.append(single_record)
        db.session.query(NSE_Script_Master).delete()
        db.session.add_all(bulk_insert_data)
        db.session.commit()
        return {"message": str(count) + " records added successfully"}
    except sqlalchemy.exc.DatabaseError:
        db.session.rollback()
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)
