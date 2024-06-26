from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def to_dict(self):
        return dict(user_name=self.user_name, password=self.password)
