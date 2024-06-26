from app import db


class nominee_rta_reverse_model(db.Model):
    __tablename__ = "rta_reverse_feed_details"

    id = db.Column(db.Integer, primary_key=True)
    reg_code = db.Column(db.String())
    client_id = db.Column(db.Numeric())
    client_name = db.Column(db.String())
    broker_code = db.Column(db.String())
    amc_code = db.Column(db.String())
    scheme_code = db.Column(db.String())
    security_name = db.Column(db.String())
    folio_no = db.Column(db.String())
    trant_type = db.Column(db.String())
    order_date = db.Column(db.String())
    qty = db.Column(db.Numeric())
    amount = db.Column(db.Numeric())
    status = db.Column(db.String())
    remarks = db.Column(db.String())
    order_id = db.Column(db.Numeric())
    user_trxn_no = db.Column(db.Numeric())
    created_by = db.Column(db.Numeric())
    updated_by = db.Column(db.Numeric())

    def __init__(self, data):
        if data[0] != "":
            self.reg_code = data[0]
        if data[1] != "":
            self.client_id = data[1]
        if data[2] != "":
            self.client_name = data[2]
        if data[3] != "":
            self.broker_code = data[3]
        if data[4] != "":
            self.amc_code = data[4]
        if data[5] != "":
            self.scheme_code = data[5]
        if data[6] != "":
            self.security_name = data[6]
        if data[7] != "":
            self.folin_no = data[7]
        if data[8] != "":
            self.trant_type = data[8]
        if data[9] != "":
            self.order_date = data[9]
        if data[10] != "":
            self.qty = data[10]
        if data[11] != "":
            self.amount = float(data[11])
        if data[12] != "":
            self.status = data[12]
        if data[13] != "":
            self.remarks = data[13]
        if data[14] != "":
            self.order_id = data[14]
        if data[15] != "":
            self.user_trxn_no = data[15]
        # if data[16] != "":
        #     self.created_by = data[16]
