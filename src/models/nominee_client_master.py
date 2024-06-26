from app import db


class nominee_client_master_model(db.Model):
    __tablename__ = "client_master"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Numeric())
    client_name = db.Column(db.String())
    client_code = db.Column(db.String())
    client_type = db.Column(db.String())
    account_type = db.Column(db.String())
    account_open_date = db.Column(db.String())
    inception_date = db.Column(db.String())
    performance_reporting_date = db.Column(db.String())
    charge_upto = db.Column(db.String())
    maturity_date = db.Column(db.String())
    account_closure_date = db.Column(db.String())
    account_closing_reason = db.Column(db.String())
    birth_date = db.Column(db.String())
    contact_name = db.Column(db.String())
    phone_home = db.Column(db.Numeric())
    phone_work = db.Column(db.Numeric())
    mobile = db.Column(db.Numeric())
    email = db.Column(db.String())
    fax = db.Column(db.String())
    address_1 = db.Column(db.String())
    address_2 = db.Column(db.String())
    city = db.Column(db.String())
    pin_code = db.Column(db.Numeric())
    state = db.Column(db.String())
    mail_address_1 = db.Column(db.String())
    mail_address_2 = db.Column(db.String())
    mail_city = db.Column(db.String())
    mail_pincode = db.Column(db.Numeric())
    mail_state = db.Column(db.String())
    pan_number = db.Column(db.String())
    ward = db.Column(db.String())
    circle = db.Column(db.String())
    tan_number = db.Column(db.Numeric())
    ref_code_1 = db.Column(db.String())
    ref_code_2 = db.Column(db.String())
    ref_code_3 = db.Column(db.String())
    ref_code_4 = db.Column(db.String())
    dir_1_name = db.Column(db.String())
    dir_1_map_in = db.Column(db.String())
    dir_2_name = db.Column(db.String())
    dir_2_map_in = db.Column(db.String())
    dir_3_name = db.Column(db.String())
    dir_3_map_in = db.Column(db.String())
    occupation = db.Column(db.String())
    status = db.Column(db.String())
    owner_id = db.Column(db.Numeric())
    owner_name = db.Column(db.String())
    group_id = db.Column(db.Numeric())
    group_name = db.Column(db.String())
    intermediary_id = db.Column(db.Numeric())
    intermediary_name = db.Column(db.String())
    scheme_id = db.Column(db.Numeric())
    scheme_name = db.Column(db.String())
    fund_mgr_id = db.Column(db.String())
    fund_mgr_name = db.Column(db.String())
    branch_id = db.Column(db.Numeric())
    branch_name = db.Column(db.String())
    rel_mgr_id = db.Column(db.String())
    rel_mgr_name = db.Column(db.String())
    advisor_id = db.Column(db.String())
    advisor_name = db.Column(db.String())
    user_name = db.Column(db.String())
    broker_account_id = db.Column(db.String())
    trading_bank_code = db.Column(db.String())
    trading_bank_account = db.Column(db.String())
    trading_custody_code = db.Column(db.String())
    trading_custody_dp = db.Column(db.String())
    trading_custody_account_id = db.Column(db.String())
    client_bank_code = db.Column(db.String())
    client_bank_account = db.Column(db.String())
    client_custody_code = db.Column(db.String())
    client_custody_dp = db.Column(db.String())
    client_custody_account_id = db.Column(db.String())
    client_custody_scheme_code = db.Column(db.String())
    bill_group = db.Column(db.String())
    tds_on_fees = db.Column(db.String())
    daily_expense_accrual = db.Column(db.String())
    fee_payment_mode = db.Column(db.String())
    incentive = db.Column(db.String())
    mandate_bank_name = db.Column(db.String())
    mandate_bank_branch_name = db.Column(db.String())
    mandate_bank_account_type = db.Column(db.String())
    mandate_bank_account_no = db.Column(db.String())
    mandate_micr = db.Column(db.String())
    mandate_rtgs = db.Column(db.String())
    mandate_neft = db.Column(db.String())
    mandate_depository = db.Column(db.String())
    mandate_dp = db.Column(db.String())
    mandate_dp_name = db.Column(db.String())
    mandate_dp_client_id = db.Column(db.Numeric())
    salutation = db.Column(db.String())
    first_name = db.Column(db.String())
    middle_name = db.Column(db.String())
    last_name = db.Column(db.String())
    first_holder_gender = db.Column(db.String())
    father_husband = db.Column(db.String())
    joint1_name = db.Column(db.String())
    joint1_father_husband = db.Column(db.String())
    joint1_pan = db.Column(db.String())
    joint2_name = db.Column(db.String())
    joint2_father_husband = db.Column(db.String())
    joint2_pan = db.Column(db.String())
    nominee_name = db.Column(db.String())
    guardian_name = db.Column(db.String())
    second_holder_name = db.Column(db.String())
    second_holder_pan = db.Column(db.String())
    second_holder_relation = db.Column(db.String())
    second_holder_dob = db.Column(db.String())
    second_holder_gender = db.Column(db.String())
    second_holder_father_husband = db.Column(db.String())
    second_holder_status = db.Column(db.String())
    second_holder_occupation = db.Column(db.String())
    second_holder_bank_name = db.Column(db.String())
    second_holder_branch_name = db.Column(db.String())
    second_holder_bank_account_no = db.Column(db.String())
    second_holder_bank_acc_type = db.Column(db.String())
    second_holder_micr_number = db.Column(db.String())
    second_holder_neft_code = db.Column(db.String())
    second_holder_rtgs_code = db.Column(db.String())
    second_holder_depository = db.Column(db.String())
    second_holder_dp_id = db.Column(db.Numeric())
    second_holder_dp_name = db.Column(db.String())
    second_holder_dp_client_id = db.Column(db.Numeric())
    third_holder_name = db.Column(db.String())
    third_holder_pan_no = db.Column(db.String())
    third_holder_relation = db.Column(db.String())
    third_holder_dob = db.Column(db.String())
    third_holder_gender = db.Column(db.String())
    third_holder_father_husband = db.Column(db.String())
    third_holder_status = db.Column(db.String())
    third_holder_occupation = db.Column(db.String())
    third_holder_bank_name = db.Column(db.String())
    third_holder_branch_name = db.Column(db.String())
    third_holder_bank_account_no = db.Column(db.String())
    third_holder_bank_acc_type = db.Column(db.String())
    third_holder_micr_number = db.Column(db.String())
    third_holder_neft_code = db.Column(db.String())
    third_holder_rtgs_code = db.Column(db.String())
    third_holder_depository = db.Column(db.String())
    third_holder_dp_id = db.Column(db.String())
    third_holder_dp_name = db.Column(db.String())
    third_holder_dp_client_id = db.Column(db.Numeric())
    accounting_txn = db.Column(db.Numeric())
    stt_taken_as = db.Column(db.String())
    trxn_taken_as = db.Column(db.String())
    skip_from_mf_corporate_action = db.Column(db.String())
    head_of_family = db.Column(db.String())
    country = db.Column(db.String())
    nationality = db.Column(db.String())
    capital_committed = db.Column(db.String())
    mail_phone_home = db.Column(db.String())
    mail_phone_work = db.Column(db.String())
    mail_mobile = db.Column(db.String())
    mail_fax = db.Column(db.String())
    mail_email_id = db.Column(db.String())
    share_reports_flag = db.Column(db.String())
    arn_id = db.Column(db.String())
    arn_name = db.Column(db.String())
    wealth_advisor_id = db.Column(db.String())
    wealth_advisor_name = db.Column(db.String())
    first_holder_kyc = db.Column(db.String())
    first_holder_aadhar = db.Column(db.Numeric())
    first_holder_fatca = db.Column(db.String())
    first_holder_ubo = db.Column(db.String())
    second_holder_kyc = db.Column(db.String())
    second_holder_aadhar = db.Column(db.Numeric())
    second_holder_fatca = db.Column(db.String())
    second_holder_ubo = db.Column(db.String())
    third_holder_kyc = db.Column(db.String())
    third_holder_aadhar = db.Column(db.Numeric())
    third_holder_fatca = db.Column(db.String())
    third_holder_ubo = db.Column(db.String())
    mode_of_holding = db.Column(db.String())

    def __init__ (self,data):
        attribute_names = [
            "client_id", "client_name", "client_code", "client_type", "account_type", "account_open_date",
            "inception_date", "performance_reporting_date", "charge_upto", "maturity_date", "account_closure_date",
            "account_closing_reason", "birth_date", "contact_name", "phone_home", "phone_work", "mobile", "email",
            "fax", "address_1", "address_2", "city", "pin_code", "state", "mail_address_1", "mail_address_2",
            "mail_city", "mail_pincode", "mail_state", "pan_number", "ward", "circle", "tan_number", "ref_code_1",
            "ref_code_2", "ref_code_3", "ref_code_4", "dir_1_name", "dir_1_map_in", "dir_2_name", "dir_2_map_in",
            "dir_3_name", "dir_3_map_in", "occupation", "status", "owner_id", "owner_name", "group_id", "group_name",
            "intermediary_id", "intermediary_name", "scheme_id", "scheme_name", "fund_mgr_id", "fund_mgr_name",
            "branch_id", "branch_name", "rel_mgr_id", "rel_mgr_name", "advisor_id", "advisor_name", "user_name",
            "broker_account_id", "trading_bank_code", "trading_bank_account", "trading_custody_code",
            "trading_custody_dp", "trading_custody_account_id", "client_bank_code", "client_bank_account",
            "client_custody_code", "client_custody_dp", "client_custody_account_id", "client_custody_scheme_code",
            "bill_group", "tds_on_fees", "daily_expense_accrual", "fee_payment_mode", "incentive", "mandate_bank_name",
            "mandate_bank_branch_name", "mandate_bank_account_type", "mandate_bank_account_no", "mandate_micr",
            "mandate_rtgs", "mandate_neft", "mandate_depository", "mandate_dp", "mandate_dp_name",
            "mandate_dp_client_id",
            "salutation", "first_name", "middle_name", "last_name", "first_holder_gender", "father_husband",
            "joint1_name", "joint1_father_husband", "joint1_pan", "joint2_name", "joint2_father_husband", "joint2_pan",
            "nominee_name", "guardian_name", "second_holder_name", "second_holder_pan", "second_holder_relation",
            "second_holder_dob", "second_holder_gender", "second_holder_father_husband", "second_holder_status",
            "second_holder_occupation", "second_holder_bank_name", "second_holder_branch_name",
            "second_holder_bank_account_no", "second_holder_bank_acc_type", "second_holder_micr_number",
            "second_holder_neft_code", "second_holder_rtgs", "second_holder_depository", "second_holder_dp_id",
            "second_holder_dp_name", "second_holder_dp_client_id", "third_holder_name", "third_holder_pan_no",
            "third_holder_relation", "third_holder_dob", "third_holder_gender",
            "third_holder_father_husband",
            "third_holder_status", "third_holder_occupation", "third_holder_bank_name", "third_holder_branch_name",
            "third_holder_bank_account_no", "third_holder_bank_acc_type", "third_holder_micr_number",
            "third_holder_neft_code", "third_holder_rtgs_code", "third_holder_depository", "third_holder_dp_id",
            "third_holder_dp_name", "third_holder_dp_client_id", "accounting_txn", "stt_taken_as", "trxn_taken_as",
            "skip_from_mf_corporate_action", "head_of_family", "country", "nationality", "capital_committed",
            "mail_phone_home", "mail_phone_work", "mail_mobile", "mail_fax", "mail_email_id", "share_reports_flag",
            "arn_id", "arn_name", "wealth_advisor_id", "wealth_advisor_name", "first_holder_kyc", "first_holder_aadhar",
            "first_holder_fatca", "first_holder_ubo", "second_holder_kyc", "second_holder_aadhar",
            "second_holder_fatca",
            "second_holder_ubo", "third_holder_kyc", "third_holder_aadhar", "third_holder_fatca", "third_holder_ubo",
            "mode_of_holding"
        ]

    # Initialize attributes with data
        for i, attribute_name in enumerate(attribute_names):
            if i < len(data) and data[i] != "":
                setattr(self, attribute_name, data[i])
 