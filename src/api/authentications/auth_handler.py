import http

from flask import Blueprint, jsonify, make_response, request
from src.controller.auth_controller import login
from audioop import error
auth_handler_bp = Blueprint("auth_handler_bp", __name__, template_folder="templates")


@auth_handler_bp.route("/login", methods=["POST"])
def user_login():
    try:
        data = request.get_json()
        user_name = data.get("username")
        password = data.get("password")
        response = login(user_name, password)
        return response
    except error:
        return make_response(jsonify({"message": "Internal Server Error"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)