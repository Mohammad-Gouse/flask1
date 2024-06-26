from decouple import config

DB_TABLE_UTILITY = config('DB_TABLE_UTILITY')
DB_TABLE_NSE_SCRIPT_MASTER = config('DB_TABLE_NSE_SCRIPT_MASTER')


class Data_Var:
    ws_query = """
            select a.CLIENTID,b.h1name as "Client Name",a.SYMBOLCODE,a.DATEPUR_ACQUI as "Order Date",a.ORDERBLOCKID as "Order Ref",a.TRANTYPE_calc as "Tran Type",a.QUANTITY_CALC as "QTY",a.AMOUNT_CALC as "Order Amount",Bank.dpclientid as "BANK ACCOUNT NUMBER",Bank.bankbranchname as "IFSC CODE",Bank.Depname as "Bank Name",d.DEPBANKCODE as "DP",d.DPBANKID as "DPID",d.dpbankclientid as "DEMAT AC",d.REFCODE1 as "Custody Code",a.ISINCODE as "RTA Code",a.AMCCODE,c.REFSYMBOL2 as "NSESYMBOL",c.Series as "Series",REFSYMBOL5 as "ISIN CODE"  from wpmiiflone.cash_management_t a
left outer join wpmiiflone.client_m b on a.clientid=b.clientid
left outer join wpmiiflone.symbol_m c on a.symbolcode=c.symbolid
left outer join wpmiiflone.custodian_m d on a.clientid=d.clientid
left outer join (select clientid,dpclientid,bankbranchname,depname from wpmiiflone.custodian_m where cashsymbol='CASH') Bank on a.clientid=Bank.clientid
where a.datepur_acqui=to_date(to_char(sysdate,'yyyy-mm-dd'),'yyyy-mm-dd') and d.depbankcode='NSDL'
and a.trantype_calc in('BY-','SL+') and b.h1status not in('NRI/OCB-NRO','NRI/OCB-NRE') and b.schemeid in(86,87,88,89,90,91,92)

            """
    query_transaction = f"""
            SELECT
                util.order_ref AS "Reference_number",
                (CASE WHEN util.tran_type = 'BY-' THEN 1 ELSE 2 END) AS "Transaction_Type",
                nsm.symbol AS "Symbol",
                nsm.series AS "Series",
                (CASE WHEN util.tran_type = 'BY-' THEN 1 ELSE 0 END) AS "Purchase_Type",
                util.client_id AS "First_Client_ID",
                util.dp_id AS "Depository_Participant_ID",
                util.dp AS "Depository_Code",
                util.demat_ac AS "Folio_No_Beneficiary_ID",
                (CASE WHEN util.tran_type = 'BY-' THEN util.order_amount END) AS "Amount",   
                (CASE WHEN util.tran_type = 'SL+' THEN util.quantity END) AS "Quantity",
                (CASE WHEN 1=1 THEN '' END) AS "Order_Number",
                (CASE WHEN 1=1 THEN '' END) AS "Error_Code",
                (CASE WHEN 1=1 THEN 'Y' END) AS "Min_Redemption_Check",
                (CASE WHEN util.tran_type = 'BY-' THEN 'Y' END) AS "DPC",
                (CASE WHEN util.tran_type = 'BY-' THEN 'N' END) AS "Credit confirmation"
            FROM {DB_TABLE_UTILITY} AS util inner JOIN {DB_TABLE_NSE_SCRIPT_MASTER} AS nsm 
                on nsm.isin = util.isin_code and nsm.eligibility_spot_market = 1 and  nsm.category_code = 
                    (CASE
                         WHEN nsm.isin = util.isin_code and nsm.category_code = 'LIQID'
                            THEN nsm.category_code
                         ELSE
                            CASE
                                WHEN nsm.isin = util.isin_code and util.tran_type = 'BY-'
                                            and util.order_amount <= 200000 and nsm.category_code != 'DBTCR' and nsm.category_code != 'HLIQD'
                                    THEN nsm.category_code
                                WHEN nsm.isin = util.isin_code and util.tran_type = 'BY-'
                                            and util.order_amount > 200000
                                    THEN 'DBTCR'
                                WHEN nsm.isin = util.isin_code and util.tran_type = 'SL+'
                                            and nsm.category_code != 'DBTCR' and nsm.category_code != 'HLIQD'
                                    THEN nsm.category_code
                            END
                    END)
            WHERE util.nse_download = 0
        """
    query_custody_buy = """
            SELECT
               util.client_id AS "UCC Code",
               util.isin_code AS "ISIN No",
               nsm.scheme_name AS "Script Name",
               (CASE WHEN 1=1 THEN 'Buy' END) AS "Buy/Sell",
               util.order_amount AS "Amount",
               util.order_ref AS "WS Order ID",
               util.nse_order_number AS "Order Reference Number",	
               util.bank_account_number AS "Strategy Pool Bank Account Number"
            FROM utility AS util INNER JOIN nse_script_master AS nsm 
                ON nsm.isin = util.isin_code AND util.tran_type = 'BY-' and nsm.eligibility_spot_market = 1 and nsm.category_code =
                    (CASE
                        
                            WHEN nsm.isin = util.isin_code and nsm.category_code = 'LIQID'
                                THEN nsm.category_code
                            ELSE 
                                CASE
                                    WHEN nsm.isin = util.isin_code  
                                                AND util.order_amount <= 200000 AND nsm.category_code != 'DBTCR' and nsm.category_code != 'HLIQD'
                                        THEN nsm.category_code
                                    WHEN nsm.isin = util.isin_code  
                                                AND util.order_amount > 200000
                                        THEN 'DBTCR'
                                END
                    END) 
            WHERE util.nse_response = 1 and util.custody_buy = 0
        """
    query_custody_sell = """
            SELECT
               util.custody_code AS "Ofin (Orbis Code)",
               util.client_name AS "Client Name",
               util.isin_code AS "ISIN No",
               nsm.scheme_name AS "ISIN NAME",
               util.quantity AS "QUANTITY",
               util.dp_id AS "DP Id",
               util.client_id AS "Client Id",	
               util.order_ref AS "WS Order ID",
               util.nse_order_number AS "Order Reference Number",
               util.bank_account_number AS "Strategy Pool Bank Account Number"
            FROM utility AS util INNER JOIN nse_script_master AS nsm 
                ON nsm.isin = util.isin_code and util.tran_type = 'SL+' and nsm.eligibility_spot_market = 1 and nsm.category_code =
                     (CASE
                            WHEN nsm.isin = util.isin_code and nsm.category_code = 'LIQID'
                                THEN nsm.category_code
                            ELSE 
                                CASE
                                     WHEN nsm.isin = util.isin_code  
                                                    and nsm.category_code != 'DBTCR' and nsm.category_code != 'HLIQD'
                                        THEN nsm.category_code
                                END
                     END)
            WHERE util.nse_response = 1 and util.custody_sell = 0
        """
    query_utrn_confirmation = """
            SELECT
                util.client_id AS "Client Code",
                util.bank_name AS "Bank Name",
                util.bank_account_number AS "Account Number",
                util.ifsc_code AS "RTGS Code",
                util.utrn_number AS "UTRN Number",
                TO_CHAR(util.order_date::Date, 'dd-Mon-yy') AS "Transfer Date",
                util.nse_order_number AS "Order Number"
            FROM utility AS util  
            WHERE util.utrn_response = 1 and util.utrn_confirmation = 0
        """
    download_summary = """
            SELECT id, client_id, client_name, symbol_code, order_date, order_ref, tran_type, quantity, order_amount, 
            bank_account_number, ifsc_code, bank_name, dp, dp_id, demat_ac, custody_code, rta_code, amc_code, 
            nse_symbol, series, isin_code, nse_order_number, nse_error_code, utrn_number, nse_download, 
            nse_response, custody_buy, custody_sell, utrn_response, utrn_confirmation
            FROM utility WHERE created_at BETWEEN '{0}' and '{1}'
        """
    poa_download_summary = """
            SELECT * FROM poa_rta_list WHERE created_at BETWEEN '{0}' and '{1}'
        """

    rta_download_summary = """
            SELECT * FROM  rta_reverse_feed_details WHERE created_at BETWEEN '{0}' and '{1}'

        """
#     rta_download_summary = """
#     SELECT *
#     FROM rta_reverse_feed_details
#     WHERE created_at >= '{0}' AND created_at <= '{1}'
# """


    transaction_headers = "Reference_number, Transaction_Type, Symbol,Series,Purchase_Type,First_Client_ID,Depository_Participant_ID,Depository_Code,Folio_No_Beneficiary_ID,Amount,Quantity,Order_Number,Error_Code,Min_Redemption_Check,DPC,Credit confirmation"
    query_data_headers = "CLIENTID,CLIENT NAME,SYMBOLCODE,ORDER DATE,ORDER REF,TRAN TYPE,QTY,ORDER AMOUNT,BANK ACCOUNT NUMBER,IFSC CODE,BANK NAME,DP,DPID,DEMAT AC,CUSTODY CODE,RTA CODE,AMCCODE,NSESYMBOL,SERIES,ISIN CODE"
    nse_script_master_headers = ""
    utrn_upload_headers = "Client Code,Bank Name,Account Number,RTGS Code,UTRN Number,Transfer Date,WS order id,Order Number"
    utrn_confirmation_headers = "Client Code,Bank Name,Account Number,RTGS Code,UTRN Number,Transfer Date,Order Number"
    nse_transaction_response_headers = "Reference_number, Transaction_Type, Symbol,Series,Purchase_Type,First_Client_ID,Depository_Participant_ID,Depository_Code,Folio_No_Beneficiary_ID,Amount,Quantity,Order_Number,Error_Code,Min_Redemption_Check,DPC,Credit confirmation"
    nominee_rta_reverse_headers = "REGCODE,CLIENTID,CLIENTNAME,BROKERCODE,AMCCODE,SCHEMECODE,SECURITYNAME,FOLIONO,TRANTYPE,ORDERDATE,QTY,AMOUNT,STATUS,REMARKS,ORDERID,USERTRXNNO"
    nominee_client_master_header = "CLIENTID,CLIENTNAME,CLIENTCODE,CLIENTTYPE,ACCOUNTTYPE,ACCOUNT OPEN DATE,INCEPTIONDATE,PERFORMANCEREPORTINGDATE,CHARGEUPTO,MATURITYDATE,ACCOUNTT CLOSURE DATE,ACCOUNT CLOSING REASON,BIRTHDATE,CONTACTNAME,PHONEHOME,PHONEWORK,MOBILE,EMAIL,FAX,ADDRESS1,ADDRESS2,CITY,PINCODE,STATE,MAIL_ADDRESS1,MAIL_ADDRESS2,MAIL_CITY,MAIL_PINCODE,MAIL_STATE,PANNUMBER,WARD,CIRCLE,TANNUMBER,REFCODE1,REFCODE2,REFCODE3,REFCODE4,DIR1NAME,DIR1MAPIN,DIR2NAME,DIR2MAPIN,DIR3NAME,DIR3MAPIN,OCCUPATION,STATUS,OWNERID,OWNERNAME,GROUPID,GROUPNAME,INTERMEDIARYID,INTERMEDIARYNAME,SCHEMEID,SCHEMENAME,FUNDMGRID,FUNDMGRNAME,BRANCHID,BRANCHNAME,RELMGRID,RELMGRNAME,ADVISORID,ADVISORNAME,USERNAME,BROKERACCOUNTID,TRADING BANK CODE,TRADING BANK ACCOUNT,TRADING CUSTODY CODE,TRADING CUSTODY DP,TRADING CUSTODY ACCOUNTID,CLIENT BANK CODE,CLIENT BANK ACCOUNT,CLIENT CUSTODY CODE,CLIENT CUSTODY DP,CLIENT CUSTODY ACCOUNTID,CLIENT CUSTODY SCHEME CODE,BILLGROUP,TDSONFEES,DAILYEXPENSEACCRUAL,FEEPAYMENTMODE,INCENTIVE,MANDATEBANKNAME,MANDATEBANKBRANCHNAME,MANDATEBANKACCOUNTTYPE,MANDATEBANKACCOUNTNO,MANDATEMICR,MANDATERTGS,MANDATENEFT,MANDATEDEPOSITORY,MANDATEDP,MANDATEDPNAME,MANDATEDPCLIENTID,SALUTATION,FIRSTNAME,MIDDLENAME,LASTNAME,FIRST HOLDER GENDER,FATHER_HUSBAND,JOINT1_NAME,JOINT1_FATHER_HUSBAND,JOINT1_PAN,JOINT2_NAME,JOINT2_FATHER_HUSBAND,JOINT2_PAN,NOMINEENAME,GUARDIANNAME,SECOND HOLDER NAME,SECOND HOLDER PAN,SECOND HOLDER RELATION,SECOND HOLDER DOB,SECOND HOLDER GENDER,SECOND HOLDER FATHER_HUSBAND,SECOND HOLDER STATUS,SECOND HOLDER OCCUPATION,SECOND HOLDER BANK NAME,SECOND HOLDER BRANCH NAME,SECOND HOLDER BANK ACCOUNT NO,SECOND HOLDER BANK ACC.TYPE,SECOND HOLDER MICR NUMBER,SECOND HOLDER NEFT CODE,SECOND HOLDER RTGS CODE,SECOND HOLDER DEPOSITORY,SECOND HOLDER DP ID,SECOND HOLDER DP NAME,SECOND HOLDER DP CLIENT ID,THIRD HOLDER NAME,THIRD HOLDER PAN NO,THIRD HOLDER RELATION,THIRD HOLDER DOB,THIRD HOLDER GENDER,THIRD HOLDER FATHER_HUSBAND,THIRD HOLDER STATUS,THIRD HOLDER OCCUPATION,THIRD HOLDER BANK NAME,THIRD HOLDER BRANCH NAME,THIRD HOLDER BANK ACCOUNT NO,THIRD HOLDER BANK ACC.TYPE,THIRD HOLDER MICR NUMBER ,THIRD HOLDER NEFT CODE,THIRD HOLDER RTGS CODE,THIRD HOLDER DEPOSITORY,THIRD HOLDER DP ID,THIRD HOLDER DP NAME,THIRD HOLDER DP CLIENT ID,ACCOUNTINGTXN,STTTAKEN AS,TRXNTAKEN AS,SKIP FROM MF CORPORATE ACTION,HEAD OF FAMILY,COUNTRY,NATIONALITY,CAPITAL_COMMITTED,MAIL_PHONEHOME,MAIL_PHONEWORK,MAIL_MOBILE,MAIL_FAX,MAIL_EMAILID,SHAREREPORTSFLAG,ARNID,ARN NAME,WEALTHADVISORID,WEALTHADVISOR NAME,FIRST HOLDER KYC,FIRST HOLDER AADHAR,FIRST HOLDER FATCA,FIRST HOLDER UBO,SECOND HOLDER KYC,SECOND HOLDER AADHAR,SECOND HOLDER FATCA,SECOND HOLDER UBO,THIRD HOLDER KYC,THIRD HOLDER AADHAR,THIRD HOLDER FATCA,THIRD HOLDER UBO,MODE OF HOLDING"
    nominee_karvy_reverse_header = "PORTREMARKS,AMC_CODE,BROKE_CD,SBBR_CODE,USER_CODE,USR_TXN_NO,APPL_NO,FOLIO_NO,CK_DIG_NO,TRXN_TYPE,SCH_CODE,FH_NAME,J1_NAME,J2_NAME,ADD1,ADD2,ADD3,CITY,PINCODE,PHONE_OFF,TRXN_DATE,TRXN_TIME,UNITS,AMOUNT,CLOS_AC_CH,FH_DOB,GUARDIAN,TAX_NUMBER,PHONE_RES,FAX_OFF,FAX_RES,EMAIL,ACCT_NO,ACCT_TYPE,BANK_NAME,BR_NAME,BANK_CITY,REINV_TAG,HOLD_NATUR,OCC_CODE,TAX_STATUS,REMARKS,STATE,SUB_TRXN_T,MICR_CD,PAY_MEC,PRICING,PAN_2_HLDR,PAN_3_HLDR,NOM_NAME,NOM_RELA,GUARD_PAN,FH_GNDR,SIP_RGDT,IFSC_CODE,MOBILE_NO,DP_ID,NRI_ADD1,NRI_ADD2,NRI_ADD3,NRI_CITY,NRI_STATE,NRI_CON,NRI_PIN,NOM_PER,NOM2_NAME,NOM2_REL,NOM2_PER,NOM3_NAME,NOM3_REL,NOM3_PER,NRI_ADD_FL,FIRC_STAT,SIP_RFNO,NO_INST,SIP_FQ,SIP_ST_DT,SIP_END_DT,INST_NUM,NOM1_DOB,NOM1_MIN_F,NOM1_GUARD,NOM2_DOB,NOM2_MIN_F,NOM2_GUARD,NOM3_DOB,NOM3_MIN_F,NOM3_GUARD,FH_PAN_EXM,J1_PAN_EXM,J2_PAN_EXM,GD_PAN_EXM,FH_EXM_CAT,J1_EXM_CAT,J2_EXM_CAT,GD_EXM_CAT,FH_KRA_EXM,J1_KRA_EXM,J2_KRA_EXM,GD_KRA_EXM,EUIN_OPT,EUIN,NOM_OPT,SUB_ARN,IIN_NO,FH_CKYC_NO,J1_CKYC_NO,J2_CKYC_NO,GD_CKYC_NO,J1_DOB,J2_DOB,GD_DOB,BROK_TYPE,INV_DP_ID,INV_PIN_CD,CUST_CONST,LOG_WT,AOF_REF,NRI_SOF,FATCA_FLAG,DPC,US_CN_DCL,ISIN,CREDIT_FL,SLF_FAM_FL,STLMNT_NO,PAP_LES_FL,TAC_FLAG,ALTMT_MODE,SIP_NEW,SIP_AMT,FT_ACNO,DEPBANK,DEP_ACNO,DEP_DATE,DEP_RFNO,SUPPL_FLAG,TH_PTY_PAY,LOC_CD,INSTR_NO,KYC_FLG,TRXN_MODE,DUMMY_1,DUMMY_2,DUMMY_3,DUMMY_4,DUMMY_5,DUMMY_6,DUMMY_7,DUMMY_8,DUMMY_9,DUMMY_10,DUMMY_11,DUMMY_12,DUMMY_13,DUMMY_14,DUMMY_15,DUMMY_16,DUMMY_17,DUMMY_18,DUMMY_19,DUMMY_20,DUMMY_21,DUMMY_22,DUMMY_23,DUMMY_24,DUMMY_25,DUMMY_26,DUMMY_27,IHNO,TRANSACTION_DATE"
    poa_headers = "REGCODE,CLIENTID,CLIENTNAME,BROKERCODE,AMCCODE,SCHEMECODE,SECURITYNAME,FOLIONO,TRANTYPE,ORDERDATE,QTY,AMOUNT,STATUS,REMARKS,ORDERID,USERTRXNNO,POA"

    # configuration information
    file_format = 'csv'
    file_delimiter = ','
    data_store_location = 'data'

    # postgresql database variables
    psql_user = config("PSQL_USER")
    psql_pass = config("PSQL_PASS")
    psql_host = config("PSQL_HOST")
    psql_port = config("PSQL_PORT")
    psql_db = config("PSQL_DB")

    # Oracle database variables
    oracle_user = config("ORACLE_USER")
    oracle_pass = config("ORACLE_PASS")
    oracle_host = config("ORACLE_HOST")
    oracle_min = int(config("ORACLE_MIN"))
    oracle_max = int(config("ORACLE_MAX"))
    oracle_increment = int(config("ORACLE_INCREMENT"))
    oracle_encoding = config("ORACLE_ENCODING")

    # updated_by
    updated_by = 1
