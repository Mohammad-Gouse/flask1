import http
import os
import dbf
import time
import csv
import zipfile
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var

TRANSACTION_FILE_NAME = Data_Var.data_store_location
nominee_karvy_reverse_header = "PORTREMARKS,AMC_CODE,BROKE_CD,SBBR_CODE,USER_CODE,USR_TXN_NO,APPL_NO,FOLIO_NO,CK_DIG_NO,TRXN_TYPE,SCH_CODE,FH_NAME,J1_NAME,J2_NAME,ADD1,ADD2,ADD3,CITY,PINCODE,PHONE_OFF,TRXN_DATE,TRXN_TIME,UNITS,AMOUNT,CLOS_AC_CH,FH_DOB,GUARDIAN,TAX_NUMBER,PHONE_RES,FAX_OFF,FAX_RES,EMAIL,ACCT_NO,ACCT_TYPE,BANK_NAME,BR_NAME,BANK_CITY,REINV_TAG,HOLD_NATUR,OCC_CODE,TAX_STATUS,REMARKS,STATE,SUB_TRXN_T,MICR_CD,PAY_MEC,PRICING,PAN_2_HLDR,PAN_3_HLDR,NOM_NAME,NOM_RELA,GUARD_PAN,FH_GNDR,SIP_RGDT,IFSC_CODE,MOBILE_NO,DP_ID,NRI_ADD1,NRI_ADD2,NRI_ADD3,NRI_CITY,NRI_STATE,NRI_CON,NRI_PIN,NOM_PER,NOM2_NAME,NOM2_REL,NOM2_PER,NOM3_NAME,NOM3_REL,NOM3_PER,NRI_ADD_FL,FIRC_STAT,SIP_RFNO,NO_INST,SIP_FQ,SIP_ST_DT,SIP_END_DT,INST_NUM,NOM1_DOB,NOM1_MIN_F,NOM1_GUARD,NOM2_DOB,NOM2_MIN_F,NOM2_GUARD,NOM3_DOB,NOM3_MIN_F,NOM3_GUARD,FH_PAN_EXM,J1_PAN_EXM,J2_PAN_EXM,GD_PAN_EXM,FH_EXM_CAT,J1_EXM_CAT,J2_EXM_CAT,GD_EXM_CAT,FH_KRA_EXM,J1_KRA_EXM,J2_KRA_EXM,GD_KRA_EXM,EUIN_OPT,EUIN,NOM_OPT,SUB_ARN,IIN_NO,FH_CKYC_NO,J1_CKYC_NO,J2_CKYC_NO,GD_CKYC_NO,J1_DOB,J2_DOB,GD_DOB,BROK_TYPE,INV_DP_ID,INV_PIN_CD,CUST_CONST,LOG_WT,AOF_REF,NRI_SOF,FATCA_FLAG,DPC,US_CN_DCL,ISIN,CREDIT_FL,SLF_FAM_FL,STLMNT_NO,PAP_LES_FL,TAC_FLAG,ALTMT_MODE,SIP_NEW,SIP_AMT,FT_ACNO,DEPBANK,DEP_ACNO,DEP_DATE,DEP_RFNO,SUPPL_FLAG,TH_PTY_PAY,LOC_CD,INSTR_NO,KYC_FLG,TRXN_MODE,DUMMY_1,DUMMY_2,DUMMY_3,DUMMY_4,DUMMY_5,DUMMY_6,DUMMY_7,DUMMY_8,DUMMY_9,DUMMY_10,DUMMY_11,DUMMY_12,DUMMY_13,DUMMY_14,DUMMY_15,DUMMY_16,DUMMY_17,DUMMY_18,DUMMY_19,DUMMY_20,DUMMY_21,DUMMY_22,DUMMY_23,DUMMY_24,DUMMY_25,DUMMY_26,DUMMY_27,IHNO,TRANSACTION_DATE"
fields_list = nominee_karvy_reverse_header.split(',')


def upload_karvy_reverse(data):
    from app import db
    from src.models.nominee_karvy_reverse_feed import nominee_karvy_reverse_field
    from src.models.nominee_client_master import nominee_client_master_model
    from src.models.nominee_rta_reverse import nominee_rta_reverse_model

    try:
        csv_fields = data[0].split(",")
        # print(csv_fields)

        fields_of_db_table = Data_Var.nominee_karvy_reverse_header.split(",")
        # print(fields_of_db_table)

        if len(csv_fields) != len(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload valid file."}), 401)

        data.pop(0)
        count = 0
        matching_records = []
        for row in data:
            single_record = nominee_karvy_reverse_field(row.split(","))
            query_to_check_record_exist = db.session.query(nominee_karvy_reverse_field.id).filter(
                nominee_karvy_reverse_field.ih_no == single_record.ih_no
            )
            filter_matching_records = (
                db.session.query(
                    nominee_rta_reverse_model, nominee_client_master_model, nominee_karvy_reverse_field)
                .join(nominee_client_master_model,
                      nominee_client_master_model.client_id == nominee_rta_reverse_model.client_id)
                .join(nominee_karvy_reverse_field,
                      nominee_karvy_reverse_field.usr_txn_no == nominee_rta_reverse_model.user_trxn_no)
                .filter(
                    nominee_rta_reverse_model.trant_type == 'P',
                    db.or_(nominee_rta_reverse_model.folio_no.is_(
                        None), nominee_rta_reverse_model.folio_no == 0)
                )
            )
            if db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            if filter_matching_records:
                matching_records.append(row)
            db.session.add(single_record)
            count += 1
        db.session.commit()
        if matching_records:
            csv_file_path, csv_file_name = save_matching_records_to_csv(
                matching_records)
            dbf_file_path, dbf_file_name = csv_to_dbf(
                csv_file_path, csv_file_name)
            zip_folder_name = f'{csv_file_name}'
            zip_folder = f'{TRANSACTION_FILE_NAME}/nominee/karvy/{zip_folder_name}'
            os.mkdir(zip_folder)

            # Add the CSV and DBF files to the zip archive
            dbt_new_path = os.path.join(zip_folder, f"{csv_file_name}.dbt")
            dbf_file_path = os.path.join(zip_folder, f"{dbf_file_name}")

            os.rename(
                f'{TRANSACTION_FILE_NAME}/nominee/karvy/{csv_file_name}.dbt', dbt_new_path)
            os.rename(
                f'{TRANSACTION_FILE_NAME}/nominee/karvy/{dbf_file_name}', dbf_file_path)
            zip_file_name = f'{TRANSACTION_FILE_NAME}/nominee/karvy/{csv_file_name}.zip'

            # with zipfile.ZipFile(zip_file_name, "w") as zipf:
            #     zipf.write(dbt_new_path, arcname=f'{zip_folder_name}/{csv_file_name}.dbt')
            #     zipf.write(dbf_file_path, arcname=f'{zip_folder_name}/{dbf_file_name}')
            with zipfile.ZipFile(zip_file_name, "w") as zipf:
                # Add the CSV and DBF files to the zip archive
                for root, _, files in os.walk(zip_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, zip_folder)
                        zipf.write(file_path, arcname=arcname)

            return zip_file_name, csv_file_name
        else:
            return make_response(jsonify({"message": "No new records found."}), 400)

        #    return  str(count) + " records added successfully"
    except sqlalchemy.exc.DatabaseError as e:
        print(e)
        db.session.rollback()
        return make_response("Please check the database connection", 500)


# zip_folder_counter = 1


def save_matching_records_to_csv(records):
    # global zip_folder_counter
    csv_file_name = generate_file_name_with_epoch()
    zip_file_path = f'{TRANSACTION_FILE_NAME}/nominee/karvy'
    os.makedirs(zip_file_path, exist_ok=True)
    csv_file_path = f'{TRANSACTION_FILE_NAME}/nominee/karvy/{csv_file_name}.csv'
    # zip_folder_counter = zip_folder_counter+1
    # print(zip_folder_counter)
    with open(csv_file_path, 'w',newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # csv_writer.writerow(fields)
        for record in records:
            csv_writer.writerow(record.split(','))

    return csv_file_path, csv_file_name


def csv_to_dbf(csv_file_path, csv_file_name):
    dbf_file_name = f'{csv_file_name}.dbf'
    dbf_file_path = os.path.join(
        f'{TRANSACTION_FILE_NAME}/nominee/karvy/', dbf_file_name)
    # dbf_file_path = os.path.join(
    #     f'{TRANSACTION_FILE_NAME}/nominee/poa/{csv_file_name}', dbf_file_name)
    # folder_path = os.path.join(f'{TRANSACTION_FILE_NAME}/nominee/poa/', f'{csv_file_name}')
    # os.makedirs(folder_path, exist_ok=True)
    tables = dbf.from_csv(csvfile=f'{csv_file_path}', filename=dbf_file_path,
                          #   field_names='REGCODE CLIENTID CLIENTNAME BROKERCODE AMCCODE SCHEMECODE SECURINAME FOLIONO TRANTYPE ORDERDATE QTY AMOUNT STATUS REMARKS ORDERID USERTRXNNO POA'.split())
                          field_names='PORTREM AMCCODE BROKECD SBBRCODE USERCODE USRTXNNO APPLNO FOLIONO CKDIGNO TRXNTYPE SCHCODE FHNAME J1NAME J2NAME ADD1 ADD2 ADD3 CITY PINCODE PHNOFF TRXNDT TRXNTIME UNITS AMOUNT CLOSCCH FHD_OB GUARDIAN TAXNO PHNORE FAXOFF FAXRES EMAIL ACCNO ACCTTYPE BKNAM BRNAM BNKCITY REINVTAG HOLDNATU OCCCODE TAXSTAT REMARKS STATE SUBTRXN MICRCODE PAYMEC PRICING PAN2HLDR PAN3HLDR NOMNAME NOMRELA GURDPAN FHGNDR SIPRGDT IFSCCOD MOBNODP NRIAD1 NRIAD2 NRIAD3 NRICITY NRISTATE NRICON NRIPIN NOMPPER NOM2NAM NOM2RELA NOM2PER NOM3NAM NOM3RELA NOM3PER NRIADFL FIRCSTAT SIPRFNO NOINST SIPFQ SIPSTDT SIPEDT INSTMUM N1DOB N1MINF N1GUARD N2DOB N2MINF N2GUARD N3DOB N3MINF N3GUARD FHPANEX J1PANEX J2PANEX GDPANEX FHEXCAT J1EXCAT J2EXCAT GDEXCAT FHKRAEX J1KRAEX J2KRAEX GDKRAEX EUINOPT EUIN NOMOPT SUBARN IINNO FHCYNO J1CYNO J2CYNO GDCYNO J1DOB J2DOB GDDOB BROKTYPE INVDID INVPIN CUSTCONS LOGWGT AOFREF NRSOF FATCAFL DPC USCNDCL ISIN CDTFL SFLFAMFL STLMNTNO PAPLFL TACFLG ALTMTMOD SIPNW SIPAMT FTACNO DPBANK DPNACNO DPDEDT DPRFNO SPLFLG TPTYPAY LOCCD INSNO KYCFLG TRXNMDE D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22 D23 D24 D25 D26 D27 IHNO TRXNDATE'.split())

    return dbf_file_path, dbf_file_name


def generate_file_name_with_epoch():

    current_time = int(time.time())  # Get current epoch time

    # Create a file name using epoch time
    file_name = f"KARVY_MATCHING_FILE_{current_time}"

    return file_name