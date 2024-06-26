from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from src.api.transactions.transaction_handler import transaction_handler_bp
from src.api.authentications.auth_handler import auth_handler_bp
from src.api.nominee.nominee_handler import nominee_handler_bp
from src.utils.data_variable import Data_Var
from src.admin_panel.api.admin_apis import admin_handler_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(transaction_handler_bp, url_prefix="/")
app.register_blueprint(auth_handler_bp, url_prefix="/")
app.register_blueprint(nominee_handler_bp, url_prefix="/")
app.register_blueprint(admin_handler_bp, url_prefix="/")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{Data_Var.psql_user}:{Data_Var.psql_pass}@{Data_Var.psql_host}:{Data_Var.psql_port}/{Data_Var.psql_db}"
app.config['SECRET_KEY'] = "iifl-secret-key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=False)
