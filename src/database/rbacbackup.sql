

CREATE SEQUENCE poa_rta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.poa_rta_id_seq OWNER TO postgres;

-- SET default_tablespace = '';

-- SET default_table_access_method = heap;

--
-- Name: poa_rta_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE poa_rta_list (
    id bigint DEFAULT nextval('poa_rta_id_seq'::regclass) NOT NULL,
    regcode character varying(50),
    clientid character varying(50),
    clientname character varying(100),
    brokercode character varying(50),
    amccode character varying(50),
    schemecode character varying(50),
    securityname character varying(100),
    foliono character varying(50),
    trantype character varying(50),
    orderdate date,
    qty integer,
    amount numeric,
    status character varying(50),
    remarks character varying(200),
    orderid character varying(50),
    usertrxnno character varying(50),
    poa character varying(50),
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer DEFAULT 1 NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_by integer DEFAULT 1 NOT NULL
);


-- ALTER TABLE public.poa_rta_list OWNER TO postgres;

--
-- Name: rbac_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rbac_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rbac_role_id_seq OWNER TO postgres;

--
-- Name: rbac_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rbac_roles (
    role_id bigint DEFAULT nextval('public.rbac_role_id_seq'::regclass) NOT NULL,
    role_name character varying(100) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer DEFAULT 1 NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_by integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.rbac_roles OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_role_map_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_role_map_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_role_map_id_seq OWNER TO postgres;

--
-- Name: user_role_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_role_mapping (
    user_role_id bigint DEFAULT nextval('public.user_role_map_id_seq'::regclass) NOT NULL,
    user_id integer NOT NULL,
    role_id integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer DEFAULT 1 NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_by integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.user_role_mapping OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint DEFAULT nextval('public.user_id_seq'::regclass) NOT NULL,
    user_name character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer DEFAULT 1 NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_by integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_log (
    log_id bigint NOT NULL,
    dml_action character(1) NOT NULL,
    log_timestamp timestamp with time zone,
    id bigint,
    user_name character varying,
    password character varying,
    is_active boolean,
    created_at timestamp with time zone,
    created_by integer,
    updated_at timestamp with time zone,
    updated_by integer,
    CONSTRAINT users_log_dml_action_check CHECK ((dml_action = ANY (ARRAY['I'::bpchar, 'D'::bpchar, 'U'::bpchar])))
);


ALTER TABLE public.users_log OWNER TO postgres;

--
-- Name: users_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_log_id_seq OWNER TO postgres;

--
-- Data for Name: poa_rta_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.poa_rta_list (id, regcode, clientid, clientname, brokercode, amccode, schemecode, securityname, foliono, trantype, orderdate, qty, amount, status, remarks, orderid, usertrxnno, poa, is_active, created_at, created_by, updated_at, updated_by) FROM stdin;
1	CAMS	103357	VENKATRAMAN SRINIVASAN	INP000005874	L	D72SG	SBI Liquid Direct-G	31558152	R	2023-07-03	0	0.0000	VALID	00-Transaction Processed Successfully	137346	77998	E	t	2023-07-31 14:57:22.083125	1	2023-07-31 14:57:22.083125	1
2	CAMS	103357	VENKATRAMAN SRINIVASAN	INP000005874	MAF	CFD1	Mirae Asset Cash Management Direct-G	79961586752	R	2023-07-03	46	0.0000	VALID	Successfully uploaded	137347	77993	P	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
3	CAMS	103357	VENKATRAMAN SRINIVASAN	INP000005874	K	470D	Kotak Liquid Direct-G	11307230	R	2023-07-03	0	0.0000	VALID	00-Transaction Processed Successfully	137349	77999	E	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
4	CAMS	103357	VENKATRAMAN SRINIVASAN	INP000005874	P	8096	ICICI Pru Liquid Direct-G	23856412	R	2023-07-03	0	0.0000	VALID	00-Transaction Processed Successfully	137350	78000	E	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
5	CAMS	103357	VENKATRAMAN SRINIVASAN	INP000005874	H	LFGTN	HDFC Liquid Direct-G	20344121	R	2023-07-03	0	0.0000	VALID	00-Transaction Processed Successfully	137352	77995	P	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
6	CAMS	103357	VENKATRAMAN SRINIVASAN	INP000005874	H	LFGTN	HDFC Liquid Direct-G	20344120	R	2023-07-03	0	0.0000	VALID	00-Transaction Processed Successfully	137353	77994	E	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
7	CAMS	103357	VENKATRAMAN SRINIVASAN	INP000005874	B	153GZ	Aditya Birla Sun Life Liquid Fund GrowthDirect Plan	1043667460	R	2023-07-03	0	0.0000	VALID	00-Transaction Processed Successfully	137354	78002	E	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
8	KARVY	103357	VENKATRAMAN SRINIVASAN	INP000005874	UTI	SFD2	UTI Arbitrage Direct-G	599352300955	R	2023-07-03	657695	0.0000	VALID	Successfully uploaded	137355	77997	P	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
9	CAMS	102087	SANJAY MEDIRATTA	INP000005874	L	D57G	SBI Overnight Direct-G	33674637	SO	2023-07-03	0	108000.0000	VALID	00-Transaction Processed Successfully	137359	77978	E	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
10	CAMS	103489	PARUCHURI VENKATA MADHURI	INP000005874	Y	LGD	WhiteOak Capital Liquid Fund Direct-G	1000179152	SO	2023-07-03	0	52000.0000	VALID	00-Transaction Processed Successfully	137361	77979	P	t	2023-07-31 14:59:51.951016	1	2023-07-31 14:59:51.951016	1
\.


--
-- Data for Name: rbac_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rbac_roles (role_id, role_name, is_active, created_at, created_by, updated_at, updated_by) FROM stdin;
1	admin	t	2023-07-31 14:37:59.63385	1	2023-07-31 14:37:59.63385	1
2	POA	t	2023-07-31 14:37:59.63385	1	2023-07-31 14:37:59.63385	1
3	Nominee	t	2023-07-31 14:37:59.63385	1	2023-07-31 14:37:59.63385	1
4	PMS	t	2023-07-31 14:37:59.63385	1	2023-07-31 14:37:59.63385	1
\.


--
-- Data for Name: user_role_mapping; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_role_mapping (user_role_id, user_id, role_id, is_active, created_at, created_by, updated_at, updated_by) FROM stdin;
1	1	1	t	2023-07-31 14:40:31.169899	1	2023-07-31 14:40:31.169899	1
2	2	2	t	2023-07-31 14:40:31.169899	1	2023-07-31 14:40:31.169899	1
3	3	1	t	2023-07-31 14:40:31.169899	1	2023-07-31 19:03:02.512484	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, user_name, password, is_active, created_at, created_by, updated_at, updated_by) FROM stdin;
1	texple@texple.com	pbkdf2:sha256:260000$N71zQewqP9cTzpq4$70d1accaa6d8b32146ecdba973742dbeab92dffda40a4722c23e99890c3d71c0	t	2023-07-31 14:39:38.509207	1	2023-07-31 14:39:38.509207	1
2	gouse	pbkdf2:sha256:600000$441hD7cpYt3ATw50$ba5e57c3908e03026a2b779eb6e12d9e2a63528aa0d4d88402052d4276c025f5	t	2023-07-31 14:39:38.509207	1	2023-07-31 14:39:38.509207	1
3	zaid	pbkdf2:sha256:600000$hg38c1QEv4ukANZd$c08d09d3b0afed6f74ff8e6e9f1b22605130cdc8c503dd6f20eec01c7ee2803d	t	2023-07-31 14:39:38.509207	1	2023-07-31 14:39:38.509207	1
\.


--
-- Data for Name: users_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_log (log_id, dml_action, log_timestamp, id, user_name, password, is_active, created_at, created_by, updated_at, updated_by) FROM stdin;
1	I	2023-07-31 09:09:38.509207+05:30	1	texple@texple.com	pbkdf2:sha256:260000$N71zQewqP9cTzpq4$70d1accaa6d8b32146ecdba973742dbeab92dffda40a4722c23e99890c3d71c0	t	2023-07-31 14:39:38.509207+05:30	1	2023-07-31 14:39:38.509207+05:30	1
2	I	2023-07-31 09:09:38.509207+05:30	2	gouse	pbkdf2:sha256:600000$441hD7cpYt3ATw50$ba5e57c3908e03026a2b779eb6e12d9e2a63528aa0d4d88402052d4276c025f5	t	2023-07-31 14:39:38.509207+05:30	1	2023-07-31 14:39:38.509207+05:30	1
3	I	2023-07-31 09:09:38.509207+05:30	3	zaid	pbkdf2:sha256:600000$hg38c1QEv4ukANZd$c08d09d3b0afed6f74ff8e6e9f1b22605130cdc8c503dd6f20eec01c7ee2803d	t	2023-07-31 14:39:38.509207+05:30	1	2023-07-31 14:39:38.509207+05:30	1
\.


--
-- Name: poa_rta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.poa_rta_id_seq', 10, true);


--
-- Name: rbac_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rbac_role_id_seq', 4, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 3, true);


--
-- Name: user_role_map_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_role_map_id_seq', 3, true);


--
-- Name: users_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_log_id_seq', 3, true);


--
-- Name: poa_rta_list poa_rta_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poa_rta_list
    ADD CONSTRAINT poa_rta_list_pkey PRIMARY KEY (id);


--
-- Name: rbac_roles rbac_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rbac_roles
    ADD CONSTRAINT rbac_roles_pkey PRIMARY KEY (role_id);


--
-- Name: rbac_roles rbac_roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rbac_roles
    ADD CONSTRAINT rbac_roles_role_name_key UNIQUE (role_name);


--
-- Name: user_role_mapping user_role_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_role_mapping
    ADD CONSTRAINT user_role_mapping_pkey PRIMARY KEY (user_role_id);


--
-- Name: users_log users_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_log
    ADD CONSTRAINT users_log_pkey PRIMARY KEY (log_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_user_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);


--
-- Name: poa_rta_list last_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER last_updated BEFORE UPDATE ON public.poa_rta_list FOR EACH ROW EXECUTE FUNCTION public.last_updated();


--
-- Name: rbac_roles last_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER last_updated BEFORE UPDATE ON public.rbac_roles FOR EACH ROW EXECUTE FUNCTION public.last_updated();


--
-- Name: user_role_mapping last_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER last_updated BEFORE UPDATE ON public.user_role_mapping FOR EACH ROW EXECUTE FUNCTION public.last_updated();


--
-- Name: users last_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER last_updated BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.last_updated();


--
-- Name: users texple_audit; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER texple_audit AFTER INSERT OR DELETE OR UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.texple_audit('users_log_id_seq');


--
-- Name: user_role_mapping user_role_mapping_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_role_mapping
    ADD CONSTRAINT user_role_mapping_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.rbac_roles(role_id);


--
-- Name: user_role_mapping user_role_mapping_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_role_mapping
    ADD CONSTRAINT user_role_mapping_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

