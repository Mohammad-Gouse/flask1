import psycopg2
from flask import abort
from psycopg2 import pool

from src.utils.data_variable import Data_Var


def psql_connect():
    try:
        psql_pool = \
            psycopg2.pool.SimpleConnectionPool(2,
                                               20,
                                               user=Data_Var.psql_user,
                                               password=Data_Var.psql_pass,
                                               host=Data_Var.psql_host,
                                               port=Data_Var.psql_port,
                                               database=Data_Var.psql_db)

        if psql_pool:
            print("Connection pool created successfully")
            pass
        return psql_pool
    except (Exception, psycopg2.DatabaseError):
        return None


def get_connection_from_pool(psql_pool):
    # Use getconn() to Get Connection from connection pool
    ps_connection = psql_pool.getconn()
    return ps_connection


def psql_release_connection(psql_pool, ps_connection):
    # Use this method to release the connection object and send back to connection pool
    psql_pool.putconn(ps_connection)
    print("Put away a PostgreSQL connection")


def psql_close_connection(psql_pool):
    # closing database connection.
    # use closeall() method to close all the active connection if you want to turn of the application
    if psql_pool:
        psql_pool.closeall()
    print("PostgreSQL connection pool is closed")
