create function last_updated() returns trigger
  language plpgsql
as
$$
BEGIN
    NEW.updated_at = now() AT TIME ZONE 'UTC';
    RETURN NEW;
END
$$;

create function texple_audit() returns trigger
  language plpgsql
as
$$
DECLARE
    BEGIN
        IF (TG_OP = 'UPDATE') THEN
            EXECUTE format('INSERT INTO %I.%I SELECT $1,''U'',now() AT TIME ZONE ''UTC'' , $2.*'
                , TG_TABLE_SCHEMA, TG_TABLE_NAME || '_log')
            USING nextval(TG_ARGV[0] :: regclass),  NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            EXECUTE format('INSERT INTO %I.%I SELECT $1,''I'',now() AT TIME ZONE ''UTC'' , $2.*'
                , TG_TABLE_SCHEMA, TG_TABLE_NAME || '_log')
            USING nextval(TG_ARGV[0] :: regclass),  NEW;
        ELSEIF (TG_OP = 'DELETE') THEN
            EXECUTE format('INSERT INTO %I.%I SELECT $1,''D'',now() AT TIME ZONE ''UTC'' , $2.*'
                , TG_TABLE_SCHEMA, TG_TABLE_NAME || '_log')
            USING nextval(TG_ARGV[0] :: regclass),  OLD;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$$;

-- users table

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
  id                 bigint PRIMARY KEY DEFAULT nextval('user_id_seq'::regclass),
  user_name           		  character varying not null UNIQUE,
  password          	  character varying not null,
  is_active				  boolean default true,
  created_at              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
  created_by              integer             default 1,
  updated_at              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
  updated_by              integer             default 1
);


drop table if exists users_log;
CREATE TABLE users_log
(
  log_id        BIGINT PRIMARY KEY,
  dml_action    char(1) NOT NULL CHECK (dml_action IN ('I', 'D', 'U')),
  log_timestamp timestamptz,
  id                          bigint,
  user_name           		  character varying,
  password                    character varying,
  is_active					  boolean,
  created_at                  timestamptz,
  created_by                  integer,
  updated_at                  timestamptz,
  updated_by                  integer
);


CREATE SEQUENCE users_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


CREATE TRIGGER last_updated BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE last_updated();
CREATE TRIGGER texple_audit AFTER INSERT OR UPDATE OR DELETE ON users FOR EACH ROW EXECUTE PROCEDURE texple_audit('users_log_id_seq');

-- roles table

CREATE SEQUENCE roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

DROP TABLE IF EXISTS rbac_roles;
CREATE TABLE rbac_roles
(
  role_id                 bigint PRIMARY KEY DEFAULT nextval('roles_id_seq'::regclass),
  role_name           		  character varying not null UNIQUE,
  is_active				  boolean default true,
  created_at              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
  created_by              integer             default 1,
  updated_at              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
  updated_by              integer             default 1
);


drop table if exists rbac_roles_log;
CREATE TABLE rbac_roles_log
(
  log_id        BIGINT PRIMARY KEY,
  dml_action    char(1) NOT NULL CHECK (dml_action IN ('I', 'D', 'U')),
  log_timestamp timestamptz,
  role_id                          bigint,
  role_name           		  character varying,
  is_active					  boolean,
  created_at                  timestamptz,
  created_by                  integer,
  updated_at                  timestamptz,
  updated_by                  integer
);


CREATE SEQUENCE rbac_roles_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


CREATE TRIGGER last_updated BEFORE UPDATE ON rbac_roles FOR EACH ROW EXECUTE PROCEDURE last_updated();
CREATE TRIGGER texple_audit AFTER INSERT OR UPDATE OR DELETE ON rbac_roles FOR EACH ROW EXECUTE PROCEDURE texple_audit('rbac_roles_log_id_seq');

-- user role mapping table

CREATE SEQUENCE user_role_mapping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

DROP TABLE IF EXISTS user_role_mapping;
CREATE TABLE user_role_mapping
(
    user_role_id                 bigint PRIMARY KEY DEFAULT nextval('user_role_mapping_id_seq'::regclass),
    user_id                   BIGINT NOT NULL REFERENCES users (id),
    role_id                   BIGINT NOT NULL REFERENCES rbac_roles (role_id),  
    is_active				  boolean default true,
    created_at              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
    created_by              integer             default 1,
    updated_at              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_by              integer             default 1
);


drop table if exists user_role_mapping_log;
CREATE TABLE user_role_mapping_log
(
  log_id        BIGINT PRIMARY KEY,
  dml_action    char(1) NOT NULL CHECK (dml_action IN ('I', 'D', 'U')),
  log_timestamp timestamptz,
  user_role_id                          bigint,
  user_id           		  bigint,
  role_id                     bigint,
  is_active					  boolean,
  created_at                  timestamptz,
  created_by                  integer,
  updated_at                  timestamptz,
  updated_by                  integer
);


CREATE SEQUENCE user_role_mapping_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


CREATE TRIGGER last_updated BEFORE UPDATE ON user_role_mapping FOR EACH ROW EXECUTE PROCEDURE last_updated();
CREATE TRIGGER texple_audit AFTER INSERT OR UPDATE OR DELETE ON user_role_mapping FOR EACH ROW EXECUTE PROCEDURE texple_audit('user_role_mapping_log_id_seq');


-- utility table


CREATE SEQUENCE utility_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

DROP TABLE IF EXISTS utility;
CREATE TABLE utility
(
  id                  bigint PRIMARY KEY DEFAULT nextval('utility_id_seq'::regclass),
  client_id           bigint not null,
  client_name         character varying,
  symbol_code         character varying,
  order_date          character varying,
  order_ref           bigint,
  tran_type           character varying,
  quantity            double precision,
  order_amount        double precision,
  bank_account_number bigint,
  ifsc_code           character varying,
  bank_name           character varying,
  dp                  character varying,
  dp_id               character varying,
  demat_ac            bigint,
  custody_code        character varying,
  rta_code            character varying,
  amc_code            character varying,
  nse_symbol          character varying,
  series              character varying,
  isin_code           character varying,
  nse_order_number    character varying,
  nse_error_code      character varying,
  utrn_number         character varying,
  nse_download        integer default 0,
  nse_response        integer default 0,
  custody_buy         integer default 0,
  custody_sell        integer default 0,
  utrn_response       integer default 0,
  utrn_confirmation   integer default 0,
  is_active			  boolean default true,
  created_at          timestamptz DEFAULT (now() AT TIME ZONE 'UTC'),
  created_by          integer     default 1,
  updated_at          timestamptz DEFAULT (now() AT TIME ZONE 'UTC'),
  updated_by          integer     default 1
);


drop table if exists utility_log;
CREATE TABLE utility_log
(
  log_id        BIGINT PRIMARY KEY,
  dml_action    char(1) NOT NULL CHECK (dml_action IN ('I', 'D', 'U')),
  log_timestamp timestamptz,
  id                  bigint,
  client_id           bigint,
  client_name         character varying,
  symbol_code         character varying,
  order_date          character varying,
  order_ref           bigint,
  tran_type           character varying,
  quantity            double precision,
  order_amount        double precision,
  bank_account_number bigint,
  ifsc_code           character varying,
  bank_name           character varying,
  dp                  character varying,
  dp_id               character varying,
  demat_ac            bigint,
  custody_code        character varying,
  rta_code            character varying,
  amc_code            character varying,
  nse_symbol          character varying,
  series              character varying,
  isin_code           character varying,
  nse_order_number    character varying,
  nse_error_code           character varying,
  utrn_number         character varying,
  nse_download        integer,
  nse_response        integer,
  custody_buy         integer,
  custody_sell        integer,
  utrn_response       integer,
  utrn_confirmation   integer,
  is_active	          boolean,
  created_at          timestamptz,
  created_by          integer,
  updated_at          timestamptz,
  updated_by          integer
);


CREATE SEQUENCE utility_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


CREATE TRIGGER last_updated BEFORE UPDATE ON utility FOR EACH ROW EXECUTE PROCEDURE last_updated();
CREATE TRIGGER texple_audit AFTER INSERT OR UPDATE OR DELETE ON utility FOR EACH ROW EXECUTE PROCEDURE texple_audit('utility_log_id_seq');

-- nse script master
CREATE SEQUENCE nse_script_master_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


drop table if exists nse_script_master;
CREATE TABLE nse_script_master
(
    id                                          bigint PRIMARY KEY DEFAULT nextval('nse_script_master_id_seq'::regclass),
    token                                       double precision UNIQUE,
    symbol                                      character varying,
    series                                      character varying,
    instrument_type                             double precision,
    maximum_physical_redemption_quantity_limit  double precision,
    rta_scheme_code                             character varying,
    amc_scheme_code                             character varying,
    schemes_depository_details                  character varying,
    isin                                        character varying,
    folio_length                                double precision,
    security_status_normal_market               double precision,
    eligibility_normal_market                   double precision,
    security_status_odd_lot_market              double precision,
    eligibility_odd_lot__market                 double precision,
    security_status_spot_market                 double precision,
    eligibility_spot_market                     double precision,
    security_status_auction_market              double precision,
    eligibility_auction_market                  double precision,
    amc_code                                    character varying,
    category_code                               character varying,
    scheme_name                                 character varying,
    issue_rate                                  double precision,
    minimum_physical_additional_subscription_value_limit  double precision,
    buy_nav_price                                   double precision,
    sell_nav_price                                  double precision,
    rta_agent_code                                  character varying,
    value_decimal_indicator                         double precision,
    category_start_time                             double precision,
    quantity_decimal_indicator                      double precision,
    category_end_time                               double precision,
    minimum_physical_fresh_subscription_value_limit double precision,
    maximum_physical_redemption_value_limit         double precision,
    nfo_end_date                                    double precision,
    nfo_start_date                                  double precision,
    nav_date                                        double precision,
    nfo_allotment_date                              double precision,
    st_eligible_participate_in_market_index         double precision,
    st_eligible_aon                                 double precision,
    st_eligible_minimum_fill                        double precision,
    security_depository_mandatory                   double precision,
    sec_dividend                                    double precision,
    sec_allow_dep                                   double precision,
    sec_allow_sell                                  double precision,
    sec_mod_cxl                                     double precision,
    sec_allow_buy                                   double precision,
    minimum_physical_redemption_value_limit         double precision,
    minimum_physical_redemption_quantity_limit     double precision,
    dividend                                        double precision,
    rights                                          double precision,
    bonus                                           double precision,
    interest                                        double precision,
    agm                                             double precision,
    egm                                             double precision,
    other                                           double precision,
    local_updated_date_and_time                     double precision,
    delete_flag                                     character varying,
    remark                                          character varying,
    sip_eligibility                                 character varying,
    maximum_physical_fresh_subscription_value_limit         double precision,
    maximum_physical_additional_subscription_value_limit     double precision,
    maximum_depository_fresh_subscription_value_limit       double precision,
    maximum_depository_additional_subscription_value_limit   double precision,
    minimum_depository_fresh_subscription_value_limit        double precision,
    minimum_depository_additional_subscription_value_limit  double precision,
    maximum_depository_redemption_quantity_limit            double precision,
    minimum_depository_redemption_quantity_limit            double precision,
    multiple_for_physical_subscription_limit                 double precision,
    multiple_for_depository_subscription_limit               double precision,
    amc_name                                                character varying,
    direct_plan                                             character varying,
    swp                                                     character varying,
    is_active			                                    boolean default true,
    created_at                                              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
    created_by                                              integer             default 1,
    updated_at                                              timestamptz         DEFAULT (now() AT TIME ZONE 'UTC'),
    updated_by                                              integer             default 1
)


-- Adding a script to add user with password
-- username = texple@texple.com and password = texple123
INSERT INTO users(
	user_name, password)
	VALUES ('texple@texple.com', 'pbkdf2:sha256:260000$N71zQewqP9cTzpq4$70d1accaa6d8b32146ecdba973742dbeab92dffda40a4722c23e99890c3d71c0'),
    ('gouse@texple.com', 'pbkdf2:sha256:600000$441hD7cpYt3ATw50$ba5e57c3908e03026a2b779eb6e12d9e2a63528aa0d4d88402052d4276c025f5'),
    ('zaid@texple.com', 'pbkdf2:sha256:600000$hg38c1QEv4ukANZd$c08d09d3b0afed6f74ff8e6e9f1b22605130cdc8c503dd6f20eec01c7ee2803d');

-- Insert sample data into table: rbac_roles
INSERT INTO rbac_roles (role_name)
VALUES
    ('admin'),
    ('POA'),
    ('Nominee'),
    ('PMS');

-- Insert sample data into table: user_role_mapping
INSERT INTO user_role_mapping (user_id, role_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3);