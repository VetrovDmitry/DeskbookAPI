--
-- PostgreSQL database dump
--

/restrict EO7QCjCPFgQZYOjXFxEEcF2qAoBza0L6g8Kz4zwSmCcmFIeUrmTtPrGVgIutMrR

-- Dumped from database version 15.8
-- Dumped by pg_dump version 15.14 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO admin;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO admin;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO admin;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin;

--
-- Name: buildings; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.buildings (
    id integer NOT NULL,
    city character varying NOT NULL,
    street character varying NOT NULL,
    number character varying NOT NULL,
    geo_location public.geometry(Point,4326) NOT NULL,
    time_created timestamp without time zone DEFAULT now() NOT NULL,
    time_updated timestamp without time zone NOT NULL
);


ALTER TABLE public.buildings OWNER TO admin;

--
-- Name: buildings_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.buildings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.buildings_id_seq OWNER TO admin;

--
-- Name: buildings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.buildings_id_seq OWNED BY public.buildings.id;


--
-- Name: organization_workings; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.organization_workings (
    working_id character varying NOT NULL,
    organization_id integer NOT NULL
);


ALTER TABLE public.organization_workings OWNER TO admin;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.organizations (
    id integer NOT NULL,
    title character varying NOT NULL,
    building_id integer NOT NULL,
    phones character varying[] NOT NULL,
    time_created timestamp without time zone DEFAULT now() NOT NULL,
    time_updated timestamp without time zone NOT NULL
);


ALTER TABLE public.organizations OWNER TO admin;

--
-- Name: organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.organizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organizations_id_seq OWNER TO admin;

--
-- Name: organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.organizations_id_seq OWNED BY public.organizations.id;


--
-- Name: workings; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.workings (
    id character varying NOT NULL,
    parent_id character varying,
    details character varying NOT NULL,
    time_created timestamp without time zone DEFAULT now() NOT NULL,
    time_updated timestamp without time zone NOT NULL
);


ALTER TABLE public.workings OWNER TO admin;

--
-- Name: buildings id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.buildings ALTER COLUMN id SET DEFAULT nextval('public.buildings_id_seq'::regclass);


--
-- Name: organizations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organizations ALTER COLUMN id SET DEFAULT nextval('public.organizations_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alembic_version (version_num) FROM stdin;
9dedcedc1b6e
\.


--
-- Data for Name: buildings; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.buildings (id, city, street, number, geo_location, time_created, time_updated) FROM stdin;
2	г. Москва	Марксистская улица	24с2	0101000020E61000002975C93846DE4B4082FFAD64C7D44240	2025-10-22 01:58:36.530607	2025-10-22 01:58:36.530615
3	г. Москва	Воронцовская улица	21	0101000020E61000009B3924B550DE4B404E44BFB67ED44240	2025-10-22 01:58:36.552365	2025-10-22 01:58:36.55237
4	г. Москва	улица Гвоздева	7/4с1	0101000020E61000007BA2EBC20FDE4B4059DC7F643AD44240	2025-10-22 01:58:36.552396	2025-10-22 01:58:36.552397
5	г. Москва	улица Малые Каменщики	18к2	0101000020E6100000B438639813DE4B4039D1AE42CAD34240	2025-10-22 01:58:36.552417	2025-10-22 01:58:36.552418
6	г. Москва	улица Ильинка	9с1	0101000020E6100000E065868DB2E04B4039D6C56D34D04240	2025-10-22 01:58:36.552453	2025-10-22 01:58:36.552454
12	﻿г. Тверь	проспект Победы	14	0101000020E6100000E868554B3A6C4C40AE10566309F54140	2025-10-22 03:54:52.176581	2025-10-22 03:54:52.176615
\.


--
-- Data for Name: organization_workings; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.organization_workings (working_id, organization_id) FROM stdin;
Мясная продукция	8
Аксессуары	8
Молочная продукция	2
Запчасти	7
Грузовые	6
Легковые	5
Автомобили	4
Молочная продукция	3
Мясная продукция	2
Еда	1
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.organizations (id, title, building_id, phones, time_created, time_updated) FROM stdin;
1	Kontora	6	{123456}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
2	ОАО "Сплайн"	5	{}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
3	ЗАО "Очки"	4	{1232-23,2223-22}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
4	Тестовая	3	{213-232}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
5	Test 2	2	{222-333-444,222-111-333}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
6	Test	2	{222-333-444,222-111-333}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
7	Firma	5	{}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
8	ООО "Копыта и Рога"	6	{2-222-222,3-333-333,8-923-666-13-13}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
9	ООО “Рога и Копыта”	5	{2-222-222,3-333-333,8-923-666-13-13}	2025-10-01 14:46:03.598701	2025-10-01 14:46:03.598701
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: workings; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.workings (id, parent_id, details, time_created, time_updated) FROM stdin;
Еда	\N	Все о еде	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
Мясная продукция	Еда	Все о мясе	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
Молочная продукция	Еда	Все о молочке	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
Автомобили	\N	Все об авто	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
Грузовые	Автомобили	Все о грузовиках	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
Легковые	Автомобили	Все о легковушках	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
Запчасти	Легковые	Все о запчастях	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
Аксессуары	Легковые	Все о стиле	2025-10-19 09:15:53.1475	2025-10-19 09:15:53.1475
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: buildings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.buildings_id_seq', 12, true);


--
-- Name: organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.organizations_id_seq', 9, true);


--
-- Name: topology_id_seq; Type: SEQUENCE SET; Schema: topology; Owner: admin
--

SELECT pg_catalog.setval('topology.topology_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: buildings buildings_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (id);


--
-- Name: organization_workings organization_workings_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organization_workings
    ADD CONSTRAINT organization_workings_pkey PRIMARY KEY (working_id, organization_id);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: workings workings_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.workings
    ADD CONSTRAINT workings_pkey PRIMARY KEY (id);


--
-- Name: idx_buildings_geo_location; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX idx_buildings_geo_location ON public.buildings USING gist (geo_location);


--
-- Name: organization_workings organization_workings_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organization_workings
    ADD CONSTRAINT organization_workings_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: organization_workings organization_workings_working_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organization_workings
    ADD CONSTRAINT organization_workings_working_id_fkey FOREIGN KEY (working_id) REFERENCES public.workings(id);


--
-- Name: organizations organizations_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.buildings(id);


--
-- Name: workings workings_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.workings
    ADD CONSTRAINT workings_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.workings(id);


--
-- PostgreSQL database dump complete
--

\unrestrict EO7QCjCPFgQZYOjXFxEEcF2qAoBza0L6g8Kz4zwSmCcmFIeUrmTtPrGVgIutMrR

