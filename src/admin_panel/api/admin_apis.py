from src.admin_panel.controller import add_user_controller, delete_user_controller, update_user_controller, get_user_by_id_controller, list_user_controller
from flask import Blueprint, request, jsonify, make_response

admin_handler_bp = Blueprint(
    "admin_handler", __name__, template_folder="templates")


@admin_handler_bp.route("/add-user", methods=["POST"])
def add_user():
    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({"message": "Invalid data"}), 400)

        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        roles = data.get("roles")

        if not username or not password or not confirm_password or not roles:
            return make_response(jsonify({"message": "Username, password, confirm password, and roles are required"}), 400)

        if password != confirm_password:
            return make_response(jsonify({"message": "Password and confirm password do not match"}), 400)

    except Exception as e:
        return make_response(jsonify({"message": "Server error"}), 500)

    return add_user_controller.add_user(username, password, roles)


@admin_handler_bp.route("/update-user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({"message": "Invalid data"}), 400)

        username = data.get("username")
        roles = data.get("roles")

        if not username or not roles:
            return make_response(jsonify({"message": "Username, password, roles, and confirm password are required"}), 400)

    except Exception as e:
        return make_response(jsonify({"message": "Server error"}), 500)
    return update_user_controller.update_user(user_id, username, roles)


@admin_handler_bp.route("/get-user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    return get_user_by_id_controller.get_user_by_id(user_id)


@admin_handler_bp.route("/list-users", methods=["GET"])
def list_users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return list_user_controller.list_users(page, per_page)


@admin_handler_bp.route("/delete-user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    return delete_user_controller.delete_user(user_id)
