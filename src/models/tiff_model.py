from app import db


class tiff_config_model(db.Model):
    __tablename__ = "tiff_config"
    id = db.Column(db.Integer, primary_key=True)
    poa_tiff_size = db.Column(db.Integer)
    aof_tiff_size = db.Column(db.Integer)
    poa_quality_level = db.Column(db.Integer)
    aof_quality_level = db.Column(db.Integer)

    def __init__(self, data):
        if data[0] != "":
            self.poa_tiff_size = data[0]
        if data[1] != "":
            self.aof_tiff_size = data[1]
        if data[2] != "":
            self.poa_quality_level = data[2]
        if data[3] != "":
            self.aof_quality_level = data[3]

