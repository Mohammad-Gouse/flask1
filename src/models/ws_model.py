from app import db


class Utility(db.Model):
    __tablename__ = 'utility'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer)
    client_name = db.Column(db.String())
    symbol_code = db.Column(db.String())
    order_date = db.Column(db.String())
    order_ref = db.Column(db.Integer)
    tran_type = db.Column(db.String())
    quantity = db.Column(db.Numeric)
    order_amount = db.Column(db.Numeric)
    bank_account_number = db.Column(db.String())
    ifsc_code = db.Column(db.String())
    bank_name = db.Column(db.String())
    dp = db.Column(db.String())
    dp_id = db.Column(db.String())
    demat_ac = db.Column(db.String())
    custody_code = db.Column(db.String())
    rta_code = db.Column(db.String())
    amc_code = db.Column(db.String())
    nse_symbol = db.Column(db.String())
    series = db.Column(db.String())
    isin_code = db.Column(db.String())
    utrn_number = db.Column(db.String())
    nse_order_number = db.Column(db.String())
    nse_error_code = db.Column(db.String())
    nse_download = db.Column(db.Integer, default=0)
    nse_response = db.Column(db.Integer, default=0)
    custody_buy = db.Column(db.Integer, default=0)
    custody_sell = db.Column(db.Integer, default=0)
    utrn_response = db.Column(db.Integer, default=0)
    utrn_confirmation = db.Column(db.Integer, default=0)

    def __init__(self, data):
        if data[0] != '':
            self.client_id = data[0]
        if data[1] != '':
            self.client_name = data[1]
        if data[2] != '':
            self.symbol_code = data[2]
        if data[3] != '':
            self.order_date = data[3]
        if data[4] != '':
            self.order_ref = data[4]
        if data[5] != '':
            self.tran_type = data[5]
        if data[6] != '':
            self.quantity = round(data[6], 3)
        if data[7] != '':
            self.order_amount = data[7]
        if data[8] != '':
            self.bank_account_number = data[8]
        if data[9] != '':
            self.ifsc_code = data[9]
        if data[10] != '':
            self.bank_name = data[10]
        if data[11] != '':
            self.dp = data[11]
        if data[12] != '':
            self.dp_id = data[12]
        if data[13] != '':
            self.demat_ac = data[13]
        if data[14] != '':
            self.custody_code = data[14]
        if data[15] != '':
            self.rta_code = data[15]
        if data[16] != '':
            self.amc_code = data[16]
        if data[17] != '':
            self.nse_symbol = data[17]
        if data[18] != '':
            self.series = data[18]
        if data[19] != '':
            self.isin_code = data[19]
