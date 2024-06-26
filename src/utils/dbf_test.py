# import dbf
# from src.utils.psqldb import get_connection_from_pool, psql_connect
# from flask import Blueprint, request, jsonify, make_response, send_file, Response

# def fetch_data_from_database():
#     pool = psql_connect()
#     ps_connection = get_connection_from_pool(pool)

#     if ps_connection:
#         # Create a cursor object to interact with the database
#         cursor = ps_connection.cursor()

#         # Execute a SELECT query to retrieve the quality level
#         select_query = "SELECT regcode, clientname,  brokercode, amccode, schemecode, securityname, foliono, trantype, status, remarks, orderid, usertrxnno, poa, poa_status FROM poa_rta_list"
#         cursor.execute(select_query)
#         # data = cursor.fetchall()

#         field_names = [f'FIELD{i}' for i in range(1, 27)]


#         # field_names = ['FIELD1', 'FIELD2', 'FIELD3', 'FIELD4', 'FIELD5', 'FIELD6', 'FIELD7', 'FIELD8', 'FIELD9', 'FIELD10', 'FIELD11', 'FIELD12', 'FIELD13', 'FIELD14', 'FIELD15', 'FIELD16']

#         # Create a new DBF file to store the data
#         dbf_filename = 'poa_rta_list.dbf'
#         dbf_table = dbf.Table(
#             filename=dbf_filename,
#             field_specs=[f"{field_name} C(255)" for field_name in field_names],  # Assuming character fields of length 255
#             on_disk=True,  # Save to disk
#         )
#         dbf_table.open(dbf.READ_WRITE)

#         for row in cursor:
#             print("row: ", row)
#             dbf_table.append(row)

#         # Fetch the quality level from the result
        

#         dbf_table.close()


#             # Close the cursor and the connection
#         cursor.close()
#         ps_connection.close()


import dbf
from src.utils.psqldb import get_connection_from_pool, psql_connect
from flask import Blueprint, request, jsonify, make_response, send_file, Response

def fetch_data_from_database():
    pool = psql_connect()
    ps_connection = get_connection_from_pool(pool)

    if ps_connection:
        # Create a cursor object to interact with the database
        cursor = ps_connection.cursor()

        # Execute a SELECT query to retrieve the quality level
        select_query = "SELECT regcode, clientname,  brokercode, amccode, schemecode, securityname, foliono, trantype, status, remarks, orderid, usertrxnno, poa, poa_status FROM poa_rta_list"
        cursor.execute(select_query)

        # Define the DBF field names to match the database field names
        dbf_field_names = [
            'regcode', 'clientname', 'brokercode', 'amccode', 'schemecode',
            'security', 'foliono', 'trantype', 'status', 'remarks',
            'orderid', 'usrtrxno', 'poa', 'poastatus'
        ]

        # Create a new DBF file to store the data
        dbf_filename = 'poa_rta_list.dbf'
        dbf_table = dbf.Table(
            filename=dbf_filename,
            field_specs=[f"{field_name} C(50)" for field_name in dbf_field_names],
            on_disk=True,
        )
        dbf_table.open(dbf.READ_WRITE)

        data = cursor.fetchall()

        print("data: ", data)

        for row in data:
            dbf_table.append(row)

        dbf_table.close()

        # Close the cursor and the connection
        cursor.close()
        ps_connection.close()

