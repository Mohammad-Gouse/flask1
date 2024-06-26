import http
from src.utils.auth import token_authorizer

from src.controller import transaction_controller
import logging
from logging.config import dictConfig
from flask import Blueprint, request, make_response, jsonify

record = {}
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "transactions.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
)

logger = logging.getLogger("transaction_logger")

transaction_handler_bp = Blueprint(
    "transaction_handler_bp", __name__, template_folder="templates")


#   Method : POST
# @transaction_handler_bp.route("/query-data", methods=["POST"])
# def ws_query_data_to_utility():
#     global record
#     try:
#         # this will extract csv data
#         csvFile = request.files.get('file').stream.read()
#         data = csvFile.decode(errors='ignore')
#         response = transaction_controller.insert_query_data_to_utility(data.splitlines())
#         return response
#     except error:
#         return make_response(jsonify({"message": "Internal Server Error"}), 500)


# Method : GET the collection
@transaction_handler_bp.route("/transactions", methods=["GET"])
@token_authorizer(['POA'])
def download_transactions_data():
    file_name = request.args.get('filename')
    return transaction_controller.get_transactions(file_name)


@transaction_handler_bp.route("/upload-nse-response", methods=["POST"])
@token_authorizer(['POA'])
def upload_nse_response():
    # this will extract csv data
    csvFile = request.files.get('file').stream.read()
    data = csvFile.decode(errors='ignore')
    return transaction_controller.upload_nse_transaction_response(data.splitlines())


@transaction_handler_bp.route("/upload-utrn", methods=["POST"])
@token_authorizer(['Nominee'])
def upload_utrn():
    # this will extract csv data
    csvFile = request.files.get('file').stream.read()
    data = csvFile.decode(errors='ignore')
    return transaction_controller.upload_utrn(data.splitlines())


@transaction_handler_bp.route("/custody-buy", methods=["GET"])
def download_custody_buy_data():
    file_name = request.args.get('filename')
    return transaction_controller.get_custody_buy(file_name)


@transaction_handler_bp.route("/custody-sell", methods=["GET"])
def download_custody_sell_data():
    file_name = request.args.get('filename')
    return transaction_controller.get_custody_sell(file_name)


@transaction_handler_bp.route("/utrn-confirmation", methods=["GET"])
def download_utrn_confirmation_data():
    file_name = request.args.get('filename')
    return transaction_controller.get_utrn_confirmation(file_name)


#  Method : GET
@transaction_handler_bp.route("/summary", methods=["GET"])
def get_summary():
    from audioop import error
    try:
        data = request.args.to_dict()
        return transaction_controller.get_summary(data)
    except error:
        print(error)
        return make_response(jsonify({"message": error}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


@transaction_handler_bp.route("/nse-script-master", methods=["POST"])
def add_nse_script_master():
    global record
    # this will extract csv data
    csvFile = request.files.get('file').stream.read()
    data = csvFile.decode(errors='ignore')
    return transaction_controller.add_nse_script_master(data.splitlines())
