# import platform

# import oracledb

# from src.utils.data_variable import Data_Var


# def session_pool():
#     global row_data
#     if platform.platform()[:6] == 'Darwin':
#         oracledb.init_oracle_client(
#             lib_dir=r"D:\PMS_Utility\instantclient_21_8")
#     try:
#         # Create the session pool
#         pool = oracledb.SessionPool(
#             Data_Var.oracle_user,
#             Data_Var.oracle_pass,
#             Data_Var.oracle_host,
#             min=Data_Var.oracle_min,
#             max=Data_Var.oracle_max,
#             increment=Data_Var.oracle_increment,
#             encoding=Data_Var.oracle_encoding
#         )
#         if pool:
#             # Acquire a connection from the pool
#             connection = pool.acquire()
#             cursor = connection.cursor()
#             if cursor:
#                 # os.remove('query_data.csv')
#                 # file = open("query_data.csv", 'w')
#                 cursor.execute(Data_Var.ws_query)
#                 row_data = cursor.fetchall()
#             pool.release(connection)
#             pool.close()
#             if row_data:
#                 return row_data
#     except oracledb.DatabaseError as er:
#         return str(er)


import platform

import oracledb

from src.utils.data_variable import Data_Var


def session_pool():
    global row_data
    if platform.platform()[:6] == 'Darwin':
        oracledb.init_oracle_client(
            lib_dir=r"D:\PMS_Utility\instantclient_21_8")
    try:
        # Create the session pool
        pool = oracledb.SessionPool(
            Data_Var.oracle_user,
            Data_Var.oracle_pass,
            Data_Var.oracle_host,
            min=Data_Var.oracle_min,
            max=Data_Var.oracle_max,
            increment=Data_Var.oracle_increment,
            encoding=Data_Var.oracle_encoding
        )
        if pool:
            # Acquire a connection from the pool
            connection = pool.acquire()
            cursor = connection.cursor()
            if cursor:
                # os.remove('query_data.csv')
                # file = open("query_data.csv", 'w')
                cursor.execute(Data_Var.ws_query)
                row_data = cursor.fetchall()
            pool.release(connection)
            pool.close()
            if row_data:
                return row_data
    except oracledb.DatabaseError as er:
        return str(er)
