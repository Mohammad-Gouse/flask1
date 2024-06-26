class NSE_Transaction_Model:
    def __init__(self, data):
        self.order_ref = data[0]
        self.nse_symbol_code = data[2]
        self.nse_order_number = data[11]
        if data[11] == '':
            self.nse_order_number = None

    def to_dict(self):
        return dict(
            order_ref=self.order_ref,
            nse_symbol=self.nse_symbol_code,
            nse_order_number=self.nse_order_number,
            nse_response=1
        )
