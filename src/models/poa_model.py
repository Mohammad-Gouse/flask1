from app import db


class poa_model(db.Model):
    __tablename__ = "poa_rta_list"

    id = db.Column(db.Integer, primary_key=True)
    regcode = db.Column(db.String(50))
    clientid = db.Column(db.String(50))
    clientname = db.Column(db.String(100))
    brokercode = db.Column(db.String(50))
    amccode = db.Column(db.String(50))
    schemecode = db.Column(db.String(50))
    securityname = db.Column(db.String(100))
    foliono = db.Column(db.String(50))
    trantype = db.Column(db.String(50))
    orderdate = db.Column(db.Date)
    qty = db.Column(db.Integer)
    amount = db.Column(db.Numeric)
    status = db.Column(db.String(50))
    remarks = db.Column(db.String(200))
    orderid = db.Column(db.String(50))
    usertrxnno = db.Column(db.String(50))
    poa = db.Column(db.String(50))

    def __init__(self, data):
        if data[0] != "":
            self.regcode = data[0]
        if data[1] != "":
            self.clientid = data[1]
        if data[2] != "":
            self.clientname = data[2]
        if data[3] != "":
            self.brokercode = data[3]
        if data[4] != "":
            self.amccode = data[4]
        if data[5] != "":
            self.schemecode = data[5]
        if data[6] != "":
            self.securityname = data[6]
        if data[7] != "":
            self.foliono = data[7]
        if data[8] != "":
            self.trantype = data[8]
        if data[9] != "":
            self.orderdate = data[9]
        if data[10] != "":
            self.qty = data[10]
        if data[11] != "":
            self.amount = float(data[11])
        if data[12] != "":
            self.status = data[12]
        if data[13] != "":
            self.remarks = data[13]
        if data[14] != "":
            self.orderid = data[14]
        if data[15] != "":
            self.usertrxnno = data[15]
        if data[16] != "":
            self.poa = data[16]
