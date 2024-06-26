class UTRN_Model:

    def __init__(self, data):
        self.client_id = data[0]
        self.bank_name = data[1]
        self.account_number = data[2]
        self.ifsc_code = data[3]
        self.utrn_number = data[4]
        self.order_date = data[5]
        self.order_ref = data[6]
        self.nse_order_number = data[7]
