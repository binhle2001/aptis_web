--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 16.4

-- Started on 2025-06-28 09:46:31

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16402)
-- Name: exam_sets; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.exam_sets (
    id integer NOT NULL,
    set_code character varying(50) NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    created_by_user_id integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.exam_sets OWNER TO admin;

--
-- TOC entry 216 (class 1259 OID 16401)
-- Name: exam_sets_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.exam_sets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exam_sets_id_seq OWNER TO admin;

--
-- TOC entry 3531 (class 0 OID 0)
-- Dependencies: 216
-- Name: exam_sets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.exam_sets_id_seq OWNED BY public.exam_sets.id;


--
-- TOC entry 243 (class 1259 OID 16623)
-- Name: exam_submission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.exam_submission (
    id integer NOT NULL,
    user_id integer,
    exam_id integer NOT NULL,
    score double precision,
    answer_string text NOT NULL,
    is_scored boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.exam_submission OWNER TO admin;

--
-- TOC entry 242 (class 1259 OID 16622)
-- Name: exam_submission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.exam_submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exam_submission_id_seq OWNER TO admin;

--
-- TOC entry 3532 (class 0 OID 0)
-- Dependencies: 242
-- Name: exam_submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.exam_submission_id_seq OWNED BY public.exam_submission.id;


--
-- TOC entry 219 (class 1259 OID 16421)
-- Name: exams; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.exams (
    id integer NOT NULL,
    examset_id integer NOT NULL,
    exam_code character varying(50) NOT NULL,
    exam_type character varying(20) NOT NULL,
    description text,
    time_limit integer NOT NULL,
    created_by_user_id integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.exams OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16420)
-- Name: exams_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.exams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exams_id_seq OWNER TO admin;

--
-- TOC entry 3533 (class 0 OID 0)
-- Dependencies: 218
-- Name: exams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.exams_id_seq OWNED BY public.exams.id;


--
-- TOC entry 237 (class 1259 OID 16586)
-- Name: guest; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.guest (
    id integer NOT NULL,
    fullname character varying(255) NOT NULL,
    phone_number character varying(20) NOT NULL,
    is_called boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.guest OWNER TO admin;

--
-- TOC entry 236 (class 1259 OID 16585)
-- Name: guest_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.guest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.guest_id_seq OWNER TO admin;

--
-- TOC entry 3534 (class 0 OID 0)
-- Dependencies: 236
-- Name: guest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.guest_id_seq OWNED BY public.guest.id;


--
-- TOC entry 229 (class 1259 OID 16502)
-- Name: listening_part_1; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.listening_part_1 (
    id integer NOT NULL,
    exam_id integer NOT NULL,
    question text NOT NULL,
    audio_path text NOT NULL,
    correct_answer character varying(10) NOT NULL,
    option1 text NOT NULL,
    option2 text NOT NULL,
    option3 text NOT NULL
);


ALTER TABLE public.listening_part_1 OWNER TO admin;

--
-- TOC entry 228 (class 1259 OID 16501)
-- Name: listening_part_1_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.listening_part_1_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.listening_part_1_id_seq OWNER TO admin;

--
-- TOC entry 3535 (class 0 OID 0)
-- Dependencies: 228
-- Name: listening_part_1_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.listening_part_1_id_seq OWNED BY public.listening_part_1.id;


--
-- TOC entry 231 (class 1259 OID 16516)
-- Name: listening_part_2; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.listening_part_2 (
    id integer NOT NULL,
    exam_id integer NOT NULL,
    topic text,
    audio_path text,
    a integer,
    b integer,
    c integer,
    d integer,
    option1 text NOT NULL,
    option2 text NOT NULL,
    option3 text NOT NULL,
    option4 text NOT NULL,
    option5 text NOT NULL,
    option6 text NOT NULL,
    CONSTRAINT listening_part_2_a_check CHECK (((a >= 1) AND (a <= 6))),
    CONSTRAINT listening_part_2_b_check CHECK (((b >= 1) AND (b <= 6))),
    CONSTRAINT listening_part_2_c_check CHECK (((c >= 1) AND (c <= 6))),
    CONSTRAINT listening_part_2_d_check CHECK (((d >= 1) AND (d <= 6)))
);


ALTER TABLE public.listening_part_2 OWNER TO admin;

--
-- TOC entry 230 (class 1259 OID 16515)
-- Name: listening_part_2_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.listening_part_2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.listening_part_2_id_seq OWNER TO admin;

--
-- TOC entry 3536 (class 0 OID 0)
-- Dependencies: 230
-- Name: listening_part_2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.listening_part_2_id_seq OWNED BY public.listening_part_2.id;


--
-- TOC entry 233 (class 1259 OID 16534)
-- Name: listening_part_3; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.listening_part_3 (
    id integer NOT NULL,
    exam_id integer NOT NULL,
    topic text,
    question text,
    correct_answer character varying(10) NOT NULL,
    audio_path text
);


ALTER TABLE public.listening_part_3 OWNER TO admin;

--
-- TOC entry 232 (class 1259 OID 16533)
-- Name: listening_part_3_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.listening_part_3_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.listening_part_3_id_seq OWNER TO admin;

--
-- TOC entry 3537 (class 0 OID 0)
-- Dependencies: 232
-- Name: listening_part_3_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.listening_part_3_id_seq OWNED BY public.listening_part_3.id;


--
-- TOC entry 235 (class 1259 OID 16548)
-- Name: listening_part_4; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.listening_part_4 (
    id integer NOT NULL,
    exam_id integer NOT NULL,
    topic text,
    question text,
    correct_answer character varying(10) NOT NULL,
    audio_path text,
    option1 text NOT NULL,
    option2 text NOT NULL,
    option3 text NOT NULL
);


ALTER TABLE public.listening_part_4 OWNER TO admin;

--
-- TOC entry 234 (class 1259 OID 16547)
-- Name: listening_part_4_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.listening_part_4_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.listening_part_4_id_seq OWNER TO admin;

--
-- TOC entry 3538 (class 0 OID 0)
-- Dependencies: 234
-- Name: listening_part_4_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.listening_part_4_id_seq OWNED BY public.listening_part_4.id;


--
-- TOC entry 221 (class 1259 OID 16445)
-- Name: reading_part_1; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.reading_part_1 (
    question_id integer NOT NULL,
    exam_id integer NOT NULL,
    group_id integer NOT NULL,
    question text NOT NULL,
    correct_answer character varying(10) NOT NULL,
    option1 text NOT NULL,
    option2 text NOT NULL,
    option3 text NOT NULL
);


ALTER TABLE public.reading_part_1 OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 16444)
-- Name: reading_part_1_question_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.reading_part_1_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reading_part_1_question_id_seq OWNER TO admin;

--
-- TOC entry 3539 (class 0 OID 0)
-- Dependencies: 220
-- Name: reading_part_1_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.reading_part_1_question_id_seq OWNED BY public.reading_part_1.question_id;


--
-- TOC entry 223 (class 1259 OID 16459)
-- Name: reading_part_2; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.reading_part_2 (
    question_id integer NOT NULL,
    exam_id integer NOT NULL,
    group_id integer NOT NULL,
    topic text,
    sentence_text text NOT NULL,
    sentence_key integer NOT NULL,
    is_example_first boolean DEFAULT false
);


ALTER TABLE public.reading_part_2 OWNER TO admin;

--
-- TOC entry 222 (class 1259 OID 16458)
-- Name: reading_part_2_question_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.reading_part_2_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reading_part_2_question_id_seq OWNER TO admin;

--
-- TOC entry 3540 (class 0 OID 0)
-- Dependencies: 222
-- Name: reading_part_2_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.reading_part_2_question_id_seq OWNED BY public.reading_part_2.question_id;


--
-- TOC entry 225 (class 1259 OID 16474)
-- Name: reading_part_3; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.reading_part_3 (
    question_id integer NOT NULL,
    exam_id integer NOT NULL,
    group_id integer NOT NULL,
    topic text,
    question_text text NOT NULL,
    correct_answer character varying(1) NOT NULL,
    person_a text NOT NULL,
    person_b text NOT NULL,
    person_c text NOT NULL,
    person_d text NOT NULL
);


ALTER TABLE public.reading_part_3 OWNER TO admin;

--
-- TOC entry 224 (class 1259 OID 16473)
-- Name: reading_part_3_question_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.reading_part_3_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reading_part_3_question_id_seq OWNER TO admin;

--
-- TOC entry 3541 (class 0 OID 0)
-- Dependencies: 224
-- Name: reading_part_3_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.reading_part_3_question_id_seq OWNED BY public.reading_part_3.question_id;


--
-- TOC entry 227 (class 1259 OID 16488)
-- Name: reading_part_4; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.reading_part_4 (
    question_id integer NOT NULL,
    exam_id integer NOT NULL,
    topic text,
    paragraph text NOT NULL,
    correct_answer character varying(1) NOT NULL,
    option1 text NOT NULL,
    option2 text NOT NULL,
    option3 text NOT NULL,
    option4 text NOT NULL,
    option5 text NOT NULL,
    option6 text NOT NULL,
    option7 text NOT NULL,
    option8 text NOT NULL
);


ALTER TABLE public.reading_part_4 OWNER TO admin;

--
-- TOC entry 226 (class 1259 OID 16487)
-- Name: reading_part_4_question_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.reading_part_4_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reading_part_4_question_id_seq OWNER TO admin;

--
-- TOC entry 3542 (class 0 OID 0)
-- Dependencies: 226
-- Name: reading_part_4_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.reading_part_4_question_id_seq OWNED BY public.reading_part_4.question_id;


--
-- TOC entry 239 (class 1259 OID 16595)
-- Name: speaking; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.speaking (
    id integer NOT NULL,
    exam_id integer NOT NULL,
    part_id integer NOT NULL,
    topic character varying(255),
    instruction text,
    instruction_audio text,
    question text NOT NULL,
    image_path1 character varying(255),
    image_path2 character varying(255)
);


ALTER TABLE public.speaking OWNER TO admin;

--
-- TOC entry 238 (class 1259 OID 16594)
-- Name: speaking_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.speaking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.speaking_id_seq OWNER TO admin;

--
-- TOC entry 3543 (class 0 OID 0)
-- Dependencies: 238
-- Name: speaking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.speaking_id_seq OWNED BY public.speaking.id;


--
-- TOC entry 215 (class 1259 OID 16390)
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    fullname character varying(100) NOT NULL,
    phone_number character varying(20),
    role character varying(20) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO admin;

--
-- TOC entry 214 (class 1259 OID 16389)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO admin;

--
-- TOC entry 3544 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 241 (class 1259 OID 16609)
-- Name: writing; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.writing (
    id integer NOT NULL,
    exam_id integer NOT NULL,
    part_id integer NOT NULL,
    topic character varying(255),
    instruction text,
    questions text NOT NULL
);


ALTER TABLE public.writing OWNER TO admin;

--
-- TOC entry 240 (class 1259 OID 16608)
-- Name: writing_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.writing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.writing_id_seq OWNER TO admin;

--
-- TOC entry 3545 (class 0 OID 0)
-- Dependencies: 240
-- Name: writing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.writing_id_seq OWNED BY public.writing.id;


--
-- TOC entry 3273 (class 2604 OID 16405)
-- Name: exam_sets id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_sets ALTER COLUMN id SET DEFAULT nextval('public.exam_sets_id_seq'::regclass);


--
-- TOC entry 3295 (class 2604 OID 16626)
-- Name: exam_submission id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_submission ALTER COLUMN id SET DEFAULT nextval('public.exam_submission_id_seq'::regclass);


--
-- TOC entry 3277 (class 2604 OID 16424)
-- Name: exams id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exams ALTER COLUMN id SET DEFAULT nextval('public.exams_id_seq'::regclass);


--
-- TOC entry 3290 (class 2604 OID 16589)
-- Name: guest id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.guest ALTER COLUMN id SET DEFAULT nextval('public.guest_id_seq'::regclass);


--
-- TOC entry 3286 (class 2604 OID 16505)
-- Name: listening_part_1 id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_1 ALTER COLUMN id SET DEFAULT nextval('public.listening_part_1_id_seq'::regclass);


--
-- TOC entry 3287 (class 2604 OID 16519)
-- Name: listening_part_2 id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_2 ALTER COLUMN id SET DEFAULT nextval('public.listening_part_2_id_seq'::regclass);


--
-- TOC entry 3288 (class 2604 OID 16537)
-- Name: listening_part_3 id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_3 ALTER COLUMN id SET DEFAULT nextval('public.listening_part_3_id_seq'::regclass);


--
-- TOC entry 3289 (class 2604 OID 16551)
-- Name: listening_part_4 id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_4 ALTER COLUMN id SET DEFAULT nextval('public.listening_part_4_id_seq'::regclass);


--
-- TOC entry 3281 (class 2604 OID 16448)
-- Name: reading_part_1 question_id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_1 ALTER COLUMN question_id SET DEFAULT nextval('public.reading_part_1_question_id_seq'::regclass);


--
-- TOC entry 3282 (class 2604 OID 16462)
-- Name: reading_part_2 question_id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_2 ALTER COLUMN question_id SET DEFAULT nextval('public.reading_part_2_question_id_seq'::regclass);


--
-- TOC entry 3284 (class 2604 OID 16477)
-- Name: reading_part_3 question_id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_3 ALTER COLUMN question_id SET DEFAULT nextval('public.reading_part_3_question_id_seq'::regclass);


--
-- TOC entry 3285 (class 2604 OID 16491)
-- Name: reading_part_4 question_id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_4 ALTER COLUMN question_id SET DEFAULT nextval('public.reading_part_4_question_id_seq'::regclass);


--
-- TOC entry 3293 (class 2604 OID 16598)
-- Name: speaking id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.speaking ALTER COLUMN id SET DEFAULT nextval('public.speaking_id_seq'::regclass);


--
-- TOC entry 3269 (class 2604 OID 16393)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3294 (class 2604 OID 16612)
-- Name: writing id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.writing ALTER COLUMN id SET DEFAULT nextval('public.writing_id_seq'::regclass);


--
-- TOC entry 3499 (class 0 OID 16402)
-- Dependencies: 217
-- Data for Name: exam_sets; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.exam_sets (id, set_code, title, description, created_by_user_id, is_active, created_at, updated_at) FROM stdin;
7	AO1 	Aptis General 001 	\N	1	t	2025-06-25 01:28:34.799904	2025-06-25 01:28:34.799904
8	AO2	Aptis General 002 	\N	1	t	2025-06-25 01:34:19.798169	2025-06-25 01:34:19.798169
9	AO3 	Aptis General 003 	\N	1	t	2025-06-25 01:39:57.915692	2025-06-25 01:39:57.915692
10	AO4 	Aptis General 004 	\N	1	t	2025-06-25 01:56:10.385659	2025-06-25 01:56:10.385659
11	AO5	Aptis General 005 	\N	1	t	2025-06-25 02:29:26.236384	2025-06-25 02:29:26.236384
12	AO6 	Aptis General 006	\N	1	t	2025-06-25 02:56:19.756399	2025-06-25 02:56:19.756399
22	AO7 	Aptis General 007 	\N	1	t	2025-06-25 07:18:34.862847	2025-06-25 07:18:34.862847
23	AO8	Aptis General 008	\N	1	t	2025-06-25 07:19:26.777449	2025-06-25 07:19:26.777449
24	AO9 	Aptis General 009 	\N	1	t	2025-06-25 07:29:05.246027	2025-06-25 07:29:05.246027
25	AO10 	Aptis General 010 	\N	1	t	2025-06-25 07:30:16.30655	2025-06-25 07:30:16.30655
26	AO11	Aptis General 011	\N	1	t	2025-06-25 07:37:50.891345	2025-06-25 07:37:50.891345
27	AO12	Aptis General 012	\N	1	t	2025-06-25 07:45:55.72848	2025-06-25 07:45:55.72848
28	AO13 	Aptis General 013 	\N	1	t	2025-06-25 07:46:58.770185	2025-06-25 07:46:58.770185
30	AO14 	Aptis General 014	\N	1	t	2025-06-25 07:59:22.087462	2025-06-25 07:59:22.087462
31	AO15 	Aptis General 015 	\N	1	t	2025-06-25 08:05:30.544941	2025-06-25 08:05:30.544941
\.


--
-- TOC entry 3525 (class 0 OID 16623)
-- Dependencies: 243
-- Data for Name: exam_submission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.exam_submission (id, user_id, exam_id, score, answer_string, is_scored, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 3501 (class 0 OID 16421)
-- Dependencies: 219
-- Data for Name: exams; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.exams (id, examset_id, exam_code, exam_type, description, time_limit, created_by_user_id, is_active, created_at, updated_at) FROM stdin;
26	8	L002	listening	Listening 2 	40	1	t	2025-06-26 08:16:19.298077	2025-06-26 08:16:19.298077
27	9	L003 	listening	Listening 3 	40	1	t	2025-06-26 08:17:23.305127	2025-06-26 08:17:23.305127
28	10	L004 	listening	Listening 4 	40	1	t	2025-06-26 08:18:21.544011	2025-06-26 08:18:21.544011
29	11	L005	listening	Listening 5 	40	1	t	2025-06-26 08:19:20.283393	2025-06-26 08:19:20.283393
30	12	L006	listening	Listening 6	40	1	t	2025-06-26 08:20:10.083025	2025-06-26 08:20:10.083025
31	22	L007 	listening	Listening 7 	40	1	t	2025-06-26 08:21:00.990269	2025-06-26 08:21:00.990269
32	23	L008	listening	Listening 8	40	1	t	2025-06-26 09:00:06.127647	2025-06-26 09:00:06.127647
33	24	L009	listening	Listening 9 	40	1	t	2025-06-26 09:00:49.1079	2025-06-26 09:00:49.1079
34	25	L010	listening	Listening 10 	40	1	t	2025-06-26 09:01:45.479673	2025-06-26 09:01:45.479673
42	27	L012	listening	Listening 12	40	1	t	2025-06-26 13:16:41.718063	2025-06-26 13:16:41.718063
43	28	L013	listening	Listening 13	40	1	t	2025-06-26 13:17:23.923794	2025-06-26 13:17:23.923794
44	30	L014	listening	Listening 14 	40	1	t	2025-06-26 13:18:22.955778	2025-06-26 13:18:22.955778
45	31	L015	listening	Listening 15	40	1	t	2025-06-26 13:18:46.80435	2025-06-26 13:18:46.80435
46	26	L011	listening	Listening 11	40	1	t	2025-06-27 00:55:19.385103	2025-06-27 00:55:19.385103
25	7	L001	listening	Listening 01	40	1	t	2025-06-26 06:41:54.725245	2025-06-27 03:06:29.789586
9	7	R001 	reading	Reading 1 	35	1	t	2025-06-25 01:29:14.843168	2025-06-27 03:33:48.901832
10	8	R002	reading	Reading 2 	35	1	t	2025-06-25 01:38:01.623595	2025-06-27 07:39:18.795568
11	9	R003	reading	Reading 3 	35	1	t	2025-06-25 01:53:19.274882	2025-06-27 07:47:46.065985
12	10	R004 	reading	Reading 4 	35	1	t	2025-06-25 02:16:48.645036	2025-06-27 07:57:01.449467
13	11	R005 	reading	Reading 5 	35	1	t	2025-06-25 02:29:55.008113	2025-06-27 08:08:09.179515
14	12	R006 	reading	Reading 6 	35	1	t	2025-06-25 02:57:11.313786	2025-06-27 08:16:05.015424
16	22	R007	reading	Reading 7 	35	1	t	2025-06-25 07:19:50.846622	2025-06-27 08:25:16.275091
17	23	R0008	reading	Reading 8 	35	1	t	2025-06-25 07:28:12.793107	2025-06-27 08:30:00.148846
18	24	R009	reading	Reading 9 	35	1	t	2025-06-25 07:31:38.147114	2025-06-27 08:32:11.998598
19	25	R010	reading	Reading 10 	35	1	t	2025-06-25 07:36:49.774268	2025-06-27 08:37:34.093352
20	26	R011	reading	Reading 11 	35	1	t	2025-06-25 07:40:30.386494	2025-06-27 08:40:55.110506
21	27	R012	reading	Reading 12 	35	1	t	2025-06-25 07:46:22.129868	2025-06-27 08:41:09.908157
22	28	R013 	reading	Reading 13 	35	1	t	2025-06-25 07:57:24.995112	2025-06-27 08:47:01.954447
23	30	R014 	reading	Reading 14	35	1	t	2025-06-25 08:00:35.342562	2025-06-27 08:47:23.365037
24	31	R015 	reading	Reading 15 	35	1	t	2025-06-25 08:51:48.879023	2025-06-27 08:47:35.648312
\.


--
-- TOC entry 3519 (class 0 OID 16586)
-- Dependencies: 237
-- Data for Name: guest; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.guest (id, fullname, phone_number, is_called, created_at) FROM stdin;
1	Lê Trần Lâm Bình	0329534237	f	2025-06-26 17:33:51.060265
2	Ngọc Linh	0393365345	f	2025-06-27 01:50:45.952887
\.


--
-- TOC entry 3511 (class 0 OID 16502)
-- Dependencies: 229
-- Data for Name: listening_part_1; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.listening_part_1 (id, exam_id, question, audio_path, correct_answer, option1, option2, option3) FROM stdin;
105	26	1. What do men drink?	/app/raw_file/audio/26_part1_105.mp3	1	Iced tea	Strongbow 	Lemon juice 
106	26	2. What time does she usually write?	/app/raw_file/audio/26_part1_106.mp3	3	In the evenings 	In the mornings 	In the afternoons
107	26	3. What measn of  transport does he use?	/app/raw_file/audio/26_part1_107.mp3	2	By bus 	By train 	By car 
108	26	4. What does she do on Saturday?	/app/raw_file/audio/26_part1_108.mp3	1	Sees her family	Travelling on the beach	Go shopping
109	26	5. What does his wife like to do?	/app/raw_file/audio/26_part1_109.mp3	2	Drawing 	Photography 	Playing sport 
110	26	6. Why did she become a scientist?	/app/raw_file/audio/26_part1_110.mp3	1	A large stone 	A formula 	An exhibition 
111	26	7. When can students play soccer at school?	/app/raw_file/audio/26_part1_111.mp3	1	Wednesday afternoon 	Monday morning 	Sunday afternoon 
112	26	8. How many buildings will the town build?	/app/raw_file/audio/26_part1_112.mp3	1	2000.0	1200.0	2100.0
113	26	9. What did this writer do before?	/app/raw_file/audio/26_part1_113.mp3	2	Office 	Teacher 	Engineer 
114	26	10. How did he request the meeting be adjusted?	/app/raw_file/audio/26_part1_114.mp3	3	Reschedule the meeting	Cancel the meeting	Have the meeting without him
115	26	11. What time is the meeting?	/app/raw_file/audio/26_part1_115.mp3	3	09:45:00	10:00:00	10:15:00
116	26	12. What is he calling for?	/app/raw_file/audio/26_part1_116.mp3	3	To confirm a meeting time	To discuss a project 	To suggest a drink 
117	26	13. What did the mother ask her daughter to buy?	/app/raw_file/audio/26_part1_117.mp3	3	Milk 	Bread	Eggs
118	27	1. What time do we meet?	/app/raw_file/audio/27_part1_118.mp3	2	09:30:00	10:00:00	11:00:00
119	27	2. What is she busy with that she can't pick up the child?	/app/raw_file/audio/27_part1_119.mp3	1	Staying late at the office	Attending a meeting	Shopping for groceries
120	27	3. What movie does she recommend?	/app/raw_file/audio/27_part1_120.mp3	2	Romantic comedy	Action film	Mystery thriller
121	27	4. Where is she?	/app/raw_file/audio/27_part1_121.mp3	2	At the office 	At the town hall 	At a coffee shop 
122	27	5. How does he go to work?	/app/raw_file/audio/27_part1_122.mp3	1	By bus 	By car	By bike 
123	27	6. When should she eat fruit according to the nutritionist?	/app/raw_file/audio/27_part1_123.mp3	1	In the morning 	Before bed 	After lunch 
124	27	7. Why does she wake up so early in the morning?	/app/raw_file/audio/27_part1_124.mp3	2	To have more time	To have some quiet time	Do some workouts
125	27	8. What does he learn to drive a car for?	/app/raw_file/audio/27_part1_125.mp3	3	He plans to take a road trip	He wants to visit friends more easily	He has to drive to work
126	27	9. What did she buy in-store?	/app/raw_file/audio/27_part1_126.mp3	3	Grocceries 	A new phone 	Clothes 
127	27	10. Which place is she talking about?	/app/raw_file/audio/27_part1_127.mp3	2	City center	A university area	Library
128	27	11. What is his biggest problem?	/app/raw_file/audio/27_part1_128.mp3	3	Finances	Finding a new jobs	Persuading his family
129	27	12. How old is the city?	/app/raw_file/audio/27_part1_129.mp3	3	2000 years	500 years	1500 years
130	27	13. Where is the HR office?	/app/raw_file/audio/27_part1_130.mp3	2	On the second floor	On the first floor	On the third floor
131	28	1. How much did he pay for the computer?	/app/raw_file/audio/28_part1_131.mp3	1	250 pounds	300 pounds	350 pounds
132	28	2. Where does he want to go tomorrow?	/app/raw_file/audio/28_part1_132.mp3	1	The town hall 	The city centre	The museum 
133	28	3. What did they bring for the picnic?	/app/raw_file/audio/28_part1_133.mp3	3	Clothes 	Fruit 	Food 
134	28	4. What is the population of this village?	/app/raw_file/audio/28_part1_134.mp3	1	10000.0	2000.0	5000.0
135	28	5. Where will they meet?	/app/raw_file/audio/28_part1_135.mp3	3	At the university	At the station 	At the park 
136	28	6. What color shirt did he buy?	/app/raw_file/audio/28_part1_136.mp3	2	Blue 	Black	Red 
137	28	7. What career did he choose?	/app/raw_file/audio/28_part1_137.mp3	1	To work in business	To be a teacher 	To keep studying
138	28	8. When is the assignment due?	/app/raw_file/audio/28_part1_138.mp3	2	on Friday\n	on Saturday	on Thursday 
139	28	9. What course did he take?	/app/raw_file/audio/28_part1_139.mp3	2	Management  	Computer	Leadership
140	28	10. What did she like the most about the movie?	/app/raw_file/audio/28_part1_140.mp3	3	The car scenes	The fight scenes	The mountain scenes
141	28	11. What did they both like about the movie?	/app/raw_file/audio/28_part1_141.mp3	2	The characters	The ending	The plot 
142	28	12. Why did she become a scientist?	/app/raw_file/audio/28_part1_142.mp3	1	A large stone 	Her dream 	Her favourite collection 
143	28	13. What did he call to say?	/app/raw_file/audio/28_part1_143.mp3	3	To say hello 	To meet Felix 	To say thank you
144	29	1. How many copies did he sell?	/app/raw_file/audio/29_part1_144.mp3	1	Over 300000 copies\n	100.000 copies	30.000 copies
145	29	2. Where did they meet for the bus home?	/app/raw_file/audio/29_part1_145.mp3	3	Hotel entrance	Bus station	Marketplace 
146	29	3. What did he forget?	/app/raw_file/audio/29_part1_146.mp3	3	Money 	Phone 	Glasses 
147	29	4. How many minutes did he have to speak?	/app/raw_file/audio/29_part1_147.mp3	2	10.0	15.0	25.0
148	29	5. Who did she take the picture of?	/app/raw_file/audio/29_part1_148.mp3	1	The girl's team 	The boy's team 	Anna, Sara and the girl's team
149	29	6. What does this family do most weekends?	/app/raw_file/audio/29_part1_149.mp3	3	Goes with their friends	Goes bowling 	Goes for a walk 
150	29	7. A girl is calling her mother. Which dress does she want?	/app/raw_file/audio/29_part1_150.mp3	2	Long and green 	Long and red 	Short and red 
151	29	8. Which room is her favourite?	/app/raw_file/audio/29_part1_151.mp3	1	Bathroom 	Kitchen 	Bedroom 
152	29	9. What does she usually do in her free time?	/app/raw_file/audio/29_part1_152.mp3	3	Go to the theatre and play sports	Play sports and go shopping	Stay at home and shop online
153	29	10. Which room is the largest in her house?	/app/raw_file/audio/29_part1_153.mp3	3	Living room 	Bedroom	Kitchen
154	29	11. What is the weather like today?	/app/raw_file/audio/29_part1_154.mp3	3	Cold and not wet	Hot and wet	Cold and wet
155	29	12. What number do you press to buy a new computer?	/app/raw_file/audio/29_part1_155.mp3	2	2.0	3.0	4.0
156	29	13. How does she go to school?	/app/raw_file/audio/29_part1_156.mp3	1	She walks 	She drives 	She goes by bus 
157	30	1. What time does the train leave?	/app/raw_file/audio/30_part1_157.mp3	3	09:45:00	08:45:00	09:15:00
158	30	2. What does her sister look like?	/app/raw_file/audio/30_part1_158.mp3	1	Short 	Tall 	Thin
159	30	3. What does her sister drink?	/app/raw_file/audio/30_part1_159.mp3	2	Water	Tea	Coffee
160	30	4. A man is calling his wife. Where did they meet?	/app/raw_file/audio/30_part1_160.mp3	3	At the park 	At the station	Outside a shop 
161	30	5. What time does he have dinner these days?	/app/raw_file/audio/30_part1_161.mp3	2	6 o'clock	7 o'clock	8 o'clock
162	30	6. What did the professor want her to do?	/app/raw_file/audio/30_part1_162.mp3	3	Do research	Make a report	Speak at the conference
163	30	7. What does he remember most about his school days?	/app/raw_file/audio/30_part1_163.mp3	2	Homework	History classes	Teachers
164	30	8. Where did she choose to go on holiday?	/app/raw_file/audio/30_part1_164.mp3	1	The south	The park	The mountain
165	30	9. What is special about the new song?	/app/raw_file/audio/30_part1_165.mp3	2	The singer 	The words 	The melody 
166	30	10. What causes air pollution?	/app/raw_file/audio/30_part1_166.mp3	1	Fire from the countryside	Exhaust from private cars	Industrial emissions
167	30	11. How much does the smallest car cost?	/app/raw_file/audio/30_part1_167.mp3	3	1250 pounds	2250 pounds	3250 pounds
168	30	12. Which room will they study in?	/app/raw_file/audio/30_part1_168.mp3	2	Room 201	Room 301 	Room 302 
169	30	13. How old is Stephanie?	/app/raw_file/audio/30_part1_169.mp3	1	21.0	22.0	23.0
170	31	1. How does he feel?	/app/raw_file/audio/31_part1_170.mp3	1	Sick 	Sad	Well 
171	31	2. The train was delayed. What time does the train leave? 	/app/raw_file/audio/31_part1_171.mp3	3	08:45:00	09:15:00	09:30:00
182	31	13. What advice do they need for decorating their living room?	https://drive.google.com/file/d/1WJWNHKUqeCCx90xLHtY-xzGtvl1o55np/view?usp=sharing	3	How to buy a sofa	Where to buy cups	Where to buy a new table
183	32	1. Which area has the best weather?	https://drive.google.com/file/d/1yCZEds-Z5auCITi9S9MEpjfm_UO0sX8K/view?usp=sharing	2	In the south	In the east	In the west
184	32	2. Why was the today’s flight cancelled?	https://drive.google.com/file/d/1qabtVbLe-vx5W6y0-9T4bx4uKeoTmGCn/view?usp=sharing	3	There are no flight staff	Plane maintenance	Poor weather conditions
185	32	3. Which door do they need to take to get to Edinburgh?	https://drive.google.com/file/d/1UEgL7DibUf7fU3XgVLr3Pu64-urss_c6/view?usp=sharing	1	Two 	Three 	Four 
186	32	4. When did they decide to meet?	https://drive.google.com/file/d/1VWs0ZdTKXRVGzbPwpBJm_zlYGTO_Q-l2/view?usp=sharing	2	7 a.m on Friday	9 a.m on Sunday	9 a.m on Saturday
187	32	5. How long does it take to get to the station?	https://drive.google.com/file/d/1An35a1NSkrOlJxnZvnimJfzjTV8yBWta/view?usp=sharing	2	15 minutes	20 minutes	25 minutes 
188	32	6. Why was the museum visit cancelled?	https://drive.google.com/file/d/1eI9dDWzuddtdb7XgGuIA-_SSFfbXHoJR/view?usp=sharing	3	Join other activities	Poor weather conditions	Not enough people
189	32	7. What did he usually do last year?	https://drive.google.com/file/d/1NMx7cTDxlnEEp1ObxxZ_jY12uFzM3VeP/view?usp=sharing	2	Running	Cycling 	Walking 
190	32	8. Where is the office?	https://drive.google.com/file/d/13_NFfTq6a59-SAZUzuV4WTERAQPsqk1J/view?usp=sharing	1	Opposite the hotel	Near the park	Opposite the station
191	32	9. What is his opinion on train travel?	https://drive.google.com/file/d/19VjeidR19qbv2nZn3X_PyeLdsPz4iZhr/view?usp=sharing	3	Convenient	Friendly	Practical
192	32	10. Where is the cafe?	https://drive.google.com/file/d/1rd0x2N9xRJxiThd3275tjhun_DPWEJbs/view?usp=sharing	3	Next to the station 	Near the gift shop 	Opposite the gift shop 
193	32	11. Who is coming to visit him this weekend?	https://drive.google.com/file/d/1BfVr-kScVO_CByJUcVKAhb9LSXKyYB3k/view?usp=sharing	3	His mother	His sister	His sister and her children 
194	32	12. Who does she live with?	https://drive.google.com/file/d/1tLmyjh5-kCBu9Fu_f1aLMd_wBA_s2wBe/view?usp=sharing	3	Her colleague	Her sister	Best friends
195	32	13. Why does she want to be a writer?	https://drive.google.com/file/d/10mAiKfxaVn3hd9R9d9eWzE9_4b1KtxNU/view?usp=sharing	1	Help people	Make money	Her dream
196	33	1. Where is the club near?	https://drive.google.com/file/d/1zdeg1WmgxF0fnpdmR3fZN6D0bV5JySLo/view?usp=sharing	1	A park	A library	A coffee shop
197	33	2. What to feed the cat?	https://drive.google.com/file/d/1zFtewFoM_x3hUEdwkA7XJwbJBYG7MbJw/view?usp=sharing	2	Milk	Fish 	Cat food 
198	33	3. What does he need to buy for his sister?	https://drive.google.com/file/d/1G6pq-KyeFWJzX4CAyyJUO8mY2Zv_ttfo/view?usp=sharing	1	Chocolates	Eggs	Milk
199	33	4. What time is the football match?	https://drive.google.com/file/d/1agQtIx2uZIP5ElJpo5Jjzy0X8wqQ33j9/view?usp=sharing	1	1 pm	7 pm	4 pm
200	33	5. Why does she like the manager?	https://drive.google.com/file/d/15DgBmPQo4BLcKG0nQijPyFEdPnojqjt_/view?usp=sharing	3	He was good at his job	He paid her a lot	He taught her a lot
201	33	6. What does he want to be?	https://drive.google.com/file/d/1NsOze4yv3cykNcDoNltFK4SnaF9Cx9q2/view?usp=sharing	3	Reporter	Chef	Writer
202	33	7. What does he drink?	https://drive.google.com/file/d/1uHV5lt4g4G03TW-s5lW3L_2nyXF6ZwvH/view?usp=sharing	3	Tea	Juice 	Water 
203	33	8. What will he do?	https://drive.google.com/file/d/1RxT839sf-Jh5QI26XGXKvur4Yu073KIV/view?usp=sharing	2	Go to the coffee shop	Go for a drive	Go on a picnic
204	33	9. What does she have in common with her mother?	https://drive.google.com/file/d/1apaI149sZZl2QVmXJkc028nuNXi1z-rG/view?usp=sharing	2	They look like each other	They have similar interests	They have similar characteristics
205	33	10. What does he buy at the shop?	https://drive.google.com/file/d/1mML7Qu2nltfeHHv2kIPu-fB3AOUPfbpb/view?usp=sharing	1	A suit for the office	A dress for his wife	New clothes
206	33	11. What do birds do in winter?	https://drive.google.com/file/d/1uc24FT_fBAwYMxfrmIriNsssDU2pABU-/view?usp=sharing	2	They look for food reserves	They stay in groups for protection	They migrate to other regions
207	33	12. How much are the eggs?	https://drive.google.com/file/d/1UbYLSTURt_GYPQeQBP7EbgkZHW4S4J_j/view?usp=sharing	2	1.25 pound	1.50 pound 	2 pound 
208	33	13. A woman is calling her husband. What time is lunch ready?	https://drive.google.com/file/d/1PcYi4fZ2PU1gyBYN15HZUh1YnHbqQB3V/view?usp=sharing	2	1 pm 	2 pm 	3 pm
209	34	1. What time is the meeting?	https://drive.google.com/file/d/1EuteVi3_UUf4VlGmJkYNQSrLRgnat7qP/view?usp=sharing	1	2 pm 	10 am 	11 am 
210	34	2. What does she usually do in the evening?	https://drive.google.com/file/d/1Td7VhAiChwPNPKlhD9iyBtld-hwvVn3o/view?usp=sharing	2	Listen to music	Go for a walk 	Go to the coffee shop 
211	34	3. What day do they meet?	https://drive.google.com/file/d/1dO_abLzFxiZ4MhbhPvRb5EiWIvv7AcCp/view?usp=sharing	1	Tuesday	Thursday	Friday
173	31	4. Where is she going with her family?	/app/raw_file/audio/31_part1_173.mp3	1	The mountains	The lake 	The park 
174	31	5. Where do they wait for the bus?	/app/raw_file/audio/31_part1_174.mp3	3	Next to the hotel	Near the hotel's main entrance	By the hotel's main entrance
175	31	6. Where is the tea served?	/app/raw_file/audio/31_part1_175.mp3	2	The building	The river boat	The museum
176	31	7. A women is introducing a concert. The concert will end with?	/app/raw_file/audio/31_part1_176.mp3	3	A surprise performance	Some special offers	The city’s favorite group
177	31	8. What is the phone number of the shop?	/app/raw_file/audio/31_part1_177.mp3	1	1930-10-20 00:00:00	10 20 30	2020-10-30 00:00:00
178	31	9. A woman is calling her friend. What did she lose?	/app/raw_file/audio/31_part1_178.mp3	1	Phone	Bag 	Key 
179	31	10. What time will they meet?	/app/raw_file/audio/31_part1_179.mp3	3	Half past eight	Quarter to seven	Quarter to eight
180	31	11. Where did they go last year?	/app/raw_file/audio/31_part1_180.mp3	1	Camping	Cycling 	Bowling
181	31	12. How much do the cleaning products cost?	/app/raw_file/audio/31_part1_181.mp3	1	One pound fifty	Two pounds 	One pence 
212	34	4. A woman is talking about her job. How is being a writer different from other jobs? 	https://drive.google.com/file/d/1AD2S14SJby53-RcL62-4mfV7JPcR-Tud/view?usp=sharing	1	She works irregular time	She does not have a high salary 	She has no fixed workplace 
213	34	5. Where does she buy food?	https://drive.google.com/file/d/108Yoi7H1j1isCsi_1jrmmzvjIJ1tU4hN/view?usp=sharing	3	At a local market	At a convenient store	At a new shopping centre
214	34	6. What does she drink for lunch?	https://drive.google.com/file/d/1jf0ARSCa-rrhnh-znACR_JhqBlUfjBv5/view?usp=sharing	1	Tea	Water	Iced tea
215	34	7. What colour is the teacher's house?	https://drive.google.com/file/d/16X_YZnn-62whtKN-3OqjEDvCcrlXgB62/view?usp=sharing	3	Blue	Red 	White
216	34	8. How much are the eggs?	https://drive.google.com/file/d/1w-NzmDvbBULhVxHtk2yqqztm8pkODSh-/view?usp=sharing	3	1.25 pound	2 pound	2.50 pound
217	34	9. What does she do on her holidays?	https://drive.google.com/file/d/1oUXDaBFPi3w8gx5MVrhJYoDw5hr-rIp-/view?usp=sharing	2	Drawing	Walking	Cooking
218	34	10. What do they both buy?	https://drive.google.com/file/d/1xccxcqTJLjWoY8lTBjeCaC00YlcO1NsJ/view?usp=sharing	3	Books	Trousers	Clothes 
219	34	11. What area is he describing?	https://drive.google.com/file/d/1oIbFxnRPTBnCPDkSA7chlvuJHwNo47-i/view?usp=sharing	1	A university area	A park	A library
220	34	12. What are the similarities between his mom and aunt?	https://drive.google.com/file/d/1NrZPHbMEFgty2xfDleXaGQaXl1A2nwQe/view?usp=sharing	1	They were thin 	They have the same eye color 	They have the same hair color 
221	34	13. How many Americans are there?	https://drive.google.com/file/d/1oqlApN--Io3juwFf109CoDumZNIW9Qg9/view?usp=sharing	1	One 	Two 	Three
306	42	1. What does the actor like to do?	https://drive.google.com/file/d/1xbl2qpHHo0reZNEtW1VMyiBTEYZSS5eD/view?usp=sharing	3	Jogging	Swimming	Drawing
307	42	2. What new thing is being built at the school?	https://drive.google.com/file/d/11HEncciQMTzWV7EjapDn12AznoJOZggu/view?usp=sharing	2	A stadium	A performance space	A school yard
308	42	3. What does he advice young people to do to save money?	https://drive.google.com/file/d/1zhBxtWYCrZ1SuaQAiKsUf-xX1uSVQ6Qe/view?usp=sharing	1	Cook for yourself	Save money	Buy things online
309	42	4. What does he like about Dubai?	https://drive.google.com/file/d/1TEJA7Z0At-L055ACggqzxzb1vT4hjZWd/view?usp=sharing	3	He gets a higher salary	He enjoys the weather here	He enjoys his job here
310	42	5. How much does the small car cost him? 	https://drive.google.com/file/d/1cO8JOWaWUJUkZQmP3_jgmzqlReLoAHmj/view?usp=sharing	1	3250 pounds	3550 pounds	4250 pounds
311	42	6. What time does Ahmed meet Rose?	https://drive.google.com/file/d/1ApNfvrEXsIUWJuIY3uP7jmpPLUn-eJ04/view?usp=sharing	3	Half past seven	Quarter past seven	Quarter to eight
312	42	7. What is the teleshop number? 	https://drive.google.com/file/d/1nZytUK0sOfu19K1OiV2M15bGnaOLPtI2/view?usp=sharing	2	102030.0	201030.0	301020.0
313	42	8. What color top is he going to buy? 	https://drive.google.com/file/d/1OXj_KFSM-cJ0HumJeto0eCx9CfceIAHm/view?usp=sharing	3	Green 	Blue 	Black 
314	42	9. What does Anna do later in the afternoon?	https://drive.google.com/file/d/1m6zvQxLxfEB29ruVKgAF_F6XfI8mWj4z/view?usp=sharing	1	Stay late at the office 	Pick up her kids 	Hang out with friends
315	42	10. Why does Vincent call James?	https://drive.google.com/file/d/1R4liD4RHqJWNeXm04R-d3Ajpq6ri0jiT/view?usp=sharing	2	To say hello 	To suggest a drink 	To arrange meeting
316	42	11. Why did he enjoy last year?	https://drive.google.com/file/d/1kQKhyJsHtGwppg33oiPk-sw536fqM3Dl/view?usp=sharing	3	Go for a walk 	Go picnic 	Go cycling
317	42	12. What encouraged her to become a scientist?	https://drive.google.com/file/d/187rzjGu4_9eZziEPWqQHuufHHMa6MkUZ/view?usp=sharing	2	Her mother 	A large stone 	The computer
318	42	13. How will the concert end?	https://drive.google.com/file/d/1Hu1aEVZfqzPz9ScJrMPZZzsWMnYLJt5B/view?usp=sharing	1	The city's favorite group 	Fireworks performance 	Singing from orchestra 
319	43	1. A man is talking about his family trip. What does the man's wife enjoy?	https://drive.google.com/file/d/1YzgmFmFQeuX53l1-O3We9dYFSQBbIIW8/view?usp=sharing	3	Walking	Shopping	Photography
320	43	2. Jana is talking to her friend. What does Jana's sister look like?	https://drive.google.com/file/d/1bL9Koz7iutNOVUvk6fsb2io6qeywDkxq/view?usp=sharing	1	Short 	Curly hair 	Thin
321	43	3. A man is calling his sister. Where are they going to meet?	https://drive.google.com/file/d/1WtTNDLfwPmIvEz5w5gBewT4u2xTnlSH8/view?usp=sharing	2	At the station 	At the university 	At the park 
322	43	4. A woman is talking about her vacation. What is the relationship between the speaker and Lisa?	https://drive.google.com/file/d/1Qo2Pyz8tIjDSxY-2-5Dw3aWDZGX4UzcH/view?usp=sharing	1	Best friends	Mother and daughter	Teacher and student
323	43	5. A woman is talking about her house. What is she going to change in their house?	https://drive.google.com/file/d/1R-kSv8MowXJ3xDig3w2z9YUhmLvnXwRk/view?usp=sharing	1	The window 	The car 	The computer
324	43	6. Listen to Anna talking about her routine. Where does Anna go for a walk every morning?	https://drive.google.com/file/d/1F77lRSGqD_mgnp-kRNEZGyevPknwgdo3/view?usp=sharing	2	Park 	College 	Neighborhood 
325	43	7. Listen to a girl calling the cafe. What did she forget, and where did she leave it?	https://drive.google.com/file/d/1fSIIiF4kHO3cxFbFupBWKL8eEUb4_zoH/view?usp=sharing	3	On the counter	Near the door	In the corner
326	43	8. Helen is calling a friend about the place her whole family is standing while seeing her off to college. Where are they standing?	https://drive.google.com/file/d/18NXWYrx_IvMoXXWnt9EsQrEo6BwcFkeg/view?usp=sharing	3	Library complex	University area	Residential area
327	43	9. A tour guide is talking about the vacation list of activities. What can people do in the afternoon? 	https://drive.google.com/file/d/15eIglf_v5TIf4OMEc4Lv9mXfsHGE-weR/view?usp=sharing	2	Join a dance class	Play golf	Go shopping
328	43	10. Doctor's office is calling about a change in the appointment. When is the new appointment?	https://drive.google.com/file/d/1RpHrhNjtenne3SKIKHiHlPa_STfTVxa8/view?usp=sharing	1	On Thursday 13th	On Thursday 30th	On Friday 14th
329	43	11. Alice is calling her friend. What did she lose? 	https://drive.google.com/file/d/1SrVHiCBFZNTw_3ftiX-zugpiPHACH5q4/view?usp=sharing	3	A book	A laptop 	A phone 
330	43	12. The woman is calling a friend about meeting for dinner. How long does it take to get to the station?	https://drive.google.com/file/d/1f8m4BkQe6TmO22RRDyWfR682IdXZUY4q/view?usp=sharing	2	30 minutes 	40 minutes 	50 minutes 
331	43	13. Listen to a man talking about their train journey. What time did the train depart? 	https://drive.google.com/file/d/1ZJM89hEtfDkYRHLhyqJxemub41bfXaMc/view?usp=sharing	2	09:00:00	09:30:00	10:00:00
332	44	1. Listen to a woman asking about a flight. How much does the flight in the morning cost?	https://drive.google.com/file/d/13BDH-bSkLKVAmRBl_-4aCvBM0vFtLvEO/view?usp=sharing	2	300 pounds	350 pounds	400 pounds
333	44	2. Listen to a friend talking about selling her music player. How much did she sell it for? 	https://drive.google.com/file/d/1uREv_pczPEbHAaswNor3iHuffgCHV-8t/view?usp=sharing	1	50 dollars	60 dollars	40 dollars
334	44	3. Listen to a woman explaining why he was late. What is the main reason he gets late? 	https://drive.google.com/file/d/1bs6-2LD9p93zL5P9rA8ARKnmh0WO1f1U/view?usp=sharing	3	Overslept 	Forgot something	Missed the train
335	44	4. A mom is calling her son to remind him about picking up groceries. How much is an egg?	https://drive.google.com/file/d/1POqkRaWrYEBR6Kyrhww5iY_T3ylJ1MSS/view?usp=sharing	1	£1.50 (One pounds fifty)	£2.50 (Two pounds fifty)	£3.50 (Three pounds fifty)
336	44	5. An author is talking about her daily routine. When does she usually write? 	https://drive.google.com/file/d/1mzfwOzvnAFs5tgC0nKbcWFvhNMrCEQ7R/view?usp=sharing	2	In the mornings 	In the afternoons 	In the evenings
337	44	6. Jack is calling to invite a friend to his house. What color is Jack's house? 	https://drive.google.com/file/d/1aFmX72Q3Emf0YHBP6KM5DgER7Yu1x7hC/view?usp=sharing	3	Blue	Green 	Red
338	44	7. A man is calling his wife. Where will they meet? 	https://drive.google.com/file/d/1rZKFIRXHNQ7r6OFAgZdXb0rkCSOT_dPI/view?usp=sharing	3	At home 	In the garden 	Outside the shop
339	44	8. A man is talking about his eating habit. What time does he usually eat?	https://drive.google.com/file/d/1oLEJDMnnl8abWAD-Z0l0l4JtfKqVnrwS/view?usp=sharing	2	6 o'clock	7 o'clock 	8 o'clock 
340	44	9. Julie is asking her professor about the assignment. When is the work due? 	https://drive.google.com/file/d/1n5zM8dULz_wFAbQDv7pE8kGLz18ksSWD/view?usp=sharing	3	On Thursday morning	On Friday morning	On Saturday morning
341	44	10. James is talking about his family members. In what way does his mother and his aunt alike? 	https://drive.google.com/file/d/17Ajy0SUezj4y7ttz8xwfjhL45LgwkhaV/view?usp=sharing	1	They were both thin	They both had blue eyes. 	They both had long hair. 
342	44	11. A tour guide is introducing a tourist destination. How many people live in the town?	https://drive.google.com/file/d/15IS5hkKJUl7z-5SALFuJ3Re3nJKZlw1Q/view?usp=sharing	3	8000.0	9000.0	10000.0
343	44	12. A man and a woman are talking about their old school days. What was the man's favorite thing about school? 	https://drive.google.com/file/d/1xodWoki75YjAjTVW8tYLtTUHgGNrxZ4X/view?usp=sharing	3	Math classes \n	Geography classes	History classes
344	44	13. Jorge is calling his friend about their plan for the weekend. What time does the football match start? 	https://drive.google.com/file/d/1kbk-HwXAXq_0giC2xRSvMN_cF5ZMZVSA/view?usp=sharing	2	11 p.m	1 p.m 	6 p.m
345	45	1. A man is talking about his routine after work. What is the man going to do after work?	https://drive.google.com/file/d/1sOHCSAwm8_k83fA5uijAQic5Wffh9HK0/view?usp=sharing	1	Goes running	Cycles home	Meets his client
346	45	2. A professor is talking to his student. What does the professor ask his student to do? 	https://drive.google.com/file/d/1ItHEDSdcgkCeGhzu1Ee8YNICEgyUNcw7/view?usp=sharing	1	Speak at a conference	Write another thesis	Tutor another student
347	45	3. Two friends are talking about their favorite activities. What is the woman's favorite form of entertainment?	https://drive.google.com/file/d/1kf3rQQ-ZMGu1YvF2YTj05wi7X_0aFx28/view?usp=sharing	2	Reading books	Going to the theatre	Playing chess with her cousin
348	45	4. A man is calling his friend, Maria. When will he see her? 	https://drive.google.com/file/d/1IgHzu1VQCb_vuzpSnddfhpo5uEhQjBY8/view?usp=sharing	1	at 9 am on Sunday	at 10 am on Saturday	at 8 am on Sunday
349	45	5. A man is calling his colleague about a meeting with clients. When will the meeting start? 	https://drive.google.com/file/d/19P5YFpi7dOVsbTRCSKoE8qROa4T42Bvk/view?usp=sharing	2	at 9.15 	at 10.15	at 11.15
350	45	6. A customer is calling the hotline of a department store. Which number to press in order to buy a computer? 	https://drive.google.com/file/d/1jlYVUg8KaTVMQkOL03HNVj65_EI2UBMi/view?usp=sharing	3	One 	Two 	Three
351	45	7. An expert is talking about lack of satisfaction at work. What should be the solution? 	https://drive.google.com/file/d/1CGwhyzFlNFhS7dTuotIJ8pTSQ31lAIKR/view?usp=sharing	3	Raise the salary	Seek a new job 	Request a transfer
352	45	8. A man is talking to his friend. Why does he need to learn to drive?	https://drive.google.com/file/d/1Db4za41Y3Di4mL-YmSOPCJ68tS2Q_WxV/view?usp=sharing	2	He lost his driving license. \n	He has to drive to work. 	He bought a new car.\n
353	45	9. A tour guide is talking about birds' behaviors. What do birds do in the winter? 	https://drive.google.com/file/d/17YYnc2eRHAL3UU6x5b7fFOE9KLQ50Rwu/view?usp=sharing	1	Stay together for group protection 	Building nests 	Migrate to a new place
354	45	10. Two friends are talking about their school days. What was the woman good at?	https://drive.google.com/file/d/192VqKaee5VRpVr2CnuL0H3k-6_0JhTon/view?usp=sharing	2	Swimming 	Plays football	Running
355	45	11. Pierre and Emma are talking together about the picnic on the weekend. What will they bring to the picnic? 	https://drive.google.com/file/d/1k9oMOmktfaZYwdVgf8tkudQndppzoSV9/view?usp=sharing	3	Drinks 	Salads	Food
356	45	12. A tour guide is talking about the group's traveling schedule. Where will the group wait for the bus? 	https://drive.google.com/file/d/1BE-S5A9r9T65a7hsTOVQx2w-aXzPQkKk/view?usp=sharing	3	By the hotel's side entrance	Behind the hotel's main entrance 	By the hotel's main entrance
357	45	13. Listen to the announcement from a travel agent representative. Why is the air travel cancelled? 	https://drive.google.com/file/d/1lymJMsGdx-0UwnoI0H_IVpRYMuv59hAS/view?usp=sharing	2	Engine failure 	Poor weather conditions 	Delay at transit spot\n
358	46	1. How many weeks have they been in India?	https://drive.google.com/file/d/1YYtwyF1QpSGirP1Rubdszz0R4327AcKc/view?usp=sharing	2	1 week 	2 weeks	3 weeks
359	46	2. What does she usually do in her free time?	https://drive.google.com/file/d/14UVd9NuD4KFbnSDzGBy3hVscsVI2IQg0/view?usp=sharing	1	Go to the theatre and play sports	Play sports and go shopping	Stay at home and shop online
360	46	3. Where do they go when they travel to India?	https://drive.google.com/file/d/1Zqwhct6EdAuDp-LJL7hNPn1DmaBUMPbM/view?usp=sharing	1	Go to the park	Go to famous places	Go out to eat
361	46	4. What outdoor activities do they do in the afternoon?	https://drive.google.com/file/d/12cNgbiOkpe5NB_krAugfL46cBWD3hl2S/view?usp=sharing	1	Play golf	Go to dance classes	Play bridge
362	46	5. Where does she walk every night?	https://drive.google.com/file/d/1xDbwxdEJc7pgJuCk2ZFgfYAUepSrRZnb/view?usp=sharing	3	The university area	The park 	The college
363	46	6. How many chairs do they need to prepare for a meeting?	https://drive.google.com/file/d/13bzn8JT-VplTnuSS0pensGsedWekrseC/view?usp=sharing	2	10	20	30
364	46	7. Where did she ask the coffee shop to look for her lost item?	https://drive.google.com/file/d/1dPQH--FU2cLxd6PCQ5s1Xvy8rAVn0Rf8/view?usp=sharing	2	On the sofa	In the corner 	On the table 
365	46	8. Where did they meet?	https://drive.google.com/file/d/1-he0w6fZDUTxLuP0u3PDOxm0alIcluOT/view?usp=sharing	2	The parking lot	The front entrance	The school gate
366	46	9. The daughter is calling her father. What did she buy?	https://drive.google.com/file/d/1VaNoSTGwWTHDrC567DwDAZlXwLeC354J/view?usp=sharing	2	Trousers	A dress	Glasses 
367	46	10. There will be a school party soon, what should the teacher prepare?	https://drive.google.com/file/d/1HpBeLZRhITyIuarQKw5DUdOxxHs63J9_/view?usp=sharing	3	Prepare drinks	Arrange the seat	Order the food
368	46	11. When will she need a computer?	https://drive.google.com/file/d/1QVtgngPrxkfoS7kqaN-uqsB0LOhUfErY/view?usp=sharing	1	Friday	Thursday	Monday
369	46	12. What country will they study next semester?	https://drive.google.com/file/d/1nk0G9wYLza48K8p8rljjR6m90Y1TZEM7/view?usp=sharing	1	France	Italy 	Germany
370	46	13. What do they need to repair for the building?	https://drive.google.com/file/d/145jAPPjyFZuhGWgqshBjaOrXVZn76AMx/view?usp=sharing	1	Windows	Doors	Gate
371	25	1. What advice would you give to someone who is incompetent at work?	https://drive.google.com/file/d/1PH-ulmHpLjV6ESKZ0Jqab0N8FrbrV2NI/view?usp=sharing	1	Ask for a transfer	Find a new company	Quit the company
372	25	2. What time do they meet?	https://drive.google.com/file/d/1Nc3e-Q7ruobJ1bQpRax7V347KL4TmSOh/view?usp=sharing	1	6.30 p.m	7.00 a.m	7.30 p.m
373	25	3. Where does she go shopping?	https://drive.google.com/file/d/1JBRgiv8Vu1ebGzxgkulZNlSEQc9gHMK4/view?usp=sharing	2	At a familiar store	At a new shopping mall	Online shopping
374	25	4. What does she like to do most in her free time?	https://drive.google.com/file/d/11Oiw1XbWuwlFJKupJUM_weDx8xfo-IKO/view?usp=sharing	3	Playing sport	Sleeping	Going to the theatre
375	25	5. What is her best sport?	https://drive.google.com/file/d/1HDbojn0JZFOZg--mgxp9bb9CcFlL04zD/view?usp=sharing	3	Pickleball	Volleyball	Football
376	25	6. How long does it take her to ride her bike?	https://drive.google.com/file/d/1_TGejaqVkF3Q5B1MOX9wSMpYDHylUQlL/view?usp=sharing	1	35 minutes	1 hour	15 minutes
377	25	7. When is the meeting?	https://drive.google.com/file/d/1i5rrthcczcRx-iey5wLUKFyZZjS5gxE7/view?usp=sharing	1	On Thursday morning	On Sunday evening	On Tuesday morning
378	25	8. What time do they meet?	https://drive.google.com/file/d/1XYos0LrBtuJdcSixrf3JflEDx1oSOLN0/view?usp=sharing	3	Six o’clock	Five o’clock	Three o'clock
379	25	9. What colour is Jack's house?	https://drive.google.com/file/d/1ahWykH0CtrtZEpvGG8MLnzzCRf5JRM-x/view?usp=sharing	2	Blue 	Red 	Green 
380	25	10. What does he do after work?	https://drive.google.com/file/d/1SrOlbPxvVUa2G7FU6uZG0ks7QE4cQTxR/view?usp=sharing	1	Play football 	Watch film 	Study piano 
381	25	11. What subject does her son like to study?	https://drive.google.com/file/d/1D0KrNYErkZ0K9IAa2BipuNpkCsUyIjcU/view?usp=sharing	2	Match 	Art	English 
382	25	12. How long did he travel to India?	https://drive.google.com/file/d/1lGpPIArWHLddtnQ1jeZ8bdPHu180Y_R4/view?usp=sharing	1	2 weeks	1 month	2 days
383	25	13. What day is the new appointment?	https://drive.google.com/file/d/18LAtwO3hF5TyQe-F7DYUjUOnNMRgiHrS/view?usp=sharing	3	Wednesday 12th	Tuesday 11th	Thursday 13th
172	31	3. What do they plan to do together?	/app/raw_file/audio/31_part1_172.mp3	2	Go to the coffee shop	Make plans later	Have dinner together
\.


--
-- TOC entry 3513 (class 0 OID 16516)
-- Dependencies: 231
-- Data for Name: listening_part_2; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.listening_part_2 (id, exam_id, topic, audio_path, a, b, c, d, option1, option2, option3, option4, option5, option6) FROM stdin;
22	46	14. Listen to the opinions of 4 people, A, B, C, D, about studying habit. Complete the sentences below.	https://drive.google.com/file/d/1N9YkAj1SqQajkkYPd2aK5windtPS4g6h/view?usp=sharing	5	4	1	2	With music 	Late at night 	With friends 	In a quiet place \n	At various places \n	With teachers\n
23	25	14. Four people are talking about their exercise preferences. Complete the sentence below. 	https://drive.google.com/file/d/12AL29-bN4bjC3leD-ABfcId7TcpThBED/view?usp=sharing	4	3	1	5	Walking	Climbing	Going for a run 	Mountain biking 	Horse riding	Swimming
9	26	14. Listen to four people talking about doing exercises and answer the questions below. \n	https://drive.google.com/file/d/1C-xPtjW16bKSJacWwZSIvPCV0JmPJosf/view?usp=sharing	2	6	4	3	Lose weight 	Improve work performance 	Hate exercising 	Have fun exercising with others 	As a hobby 	Find exercise tiring
10	27	14. Four people are talking about protecting the environment. Complete the sentences below. 	https://drive.google.com/file/d/1t5xmMufKVJEeoTf00cxFpmc7ry7Pzqik/view?usp=sharing	3	1	5	2	Protects the environment by not driving to work 	Protects the environment by using less water. 	Protects the environment by using less electricity. 	Protects the environment by using less plastics 	Protects the environment by shopping online.	Protects the environment by using commercial product.
11	28	14. Four people are talking about doing arts. Complete the sentences below. 	https://drive.google.com/file/d/1P87swQGrKGbVd3jjah8HwCkCeWWfodrG/view?usp=sharing	5	4	3	1	Doing arts alone \n	Doing arts to relax 	Doing arts as part of the job 	Doing arts with children 	Doing as a social activity 	Doing as a hobby
12	29	14. Four people are talking about shopping habit. Complete the sentences below.	https://drive.google.com/file/d/1L4ojrL9Dtk1PGAaB2ELheA2N4olhLgI4/view?usp=sharing	4	2	5	3	It reduces waste 	It is cheaper 	There are more choices 	It saves time 	Products are delivered	It is convenient. 
13	30	14. Listen to the opinions of 4 people, A, B, C, and D, about studying habit. Complete the sentences below.	https://drive.google.com/file/d/1NE_7CDB8qU8ALa8oq6Ru5CiSfUxdgP9g/view?usp=sharing	2	1	5	4	Prefer to study at various places	Prefer to study late at night	Prefer to study with friends	Prefer to study in a quiet place	Prefer to study with music	Prefer to study with parents. 
14	31	14. Four people are talking about their journey to work. Complete the sentences below.	https://drive.google.com/file/d/1WQqZuEYqIN0VWWm-VW3zv_XCSodI_N-x/view?usp=sharing	3	1	6	4	Go by bus	Go by foot	Walk with friends	Drive car	Go by train	Walk alone
15	32	14. Four people are talking about shopping online. Complete the sentences below.	https://drive.google.com/file/d/1ORd1r4dOBY-bZ3D23NFWL46G24_R-TIn/view?usp=sharing	2	1	5	3	It is cheaper	Products are delivered	It has more choices	It is convenient	It saves time	It has flexible payment options
16	33	14. Four people are talking about Protecting the environment. Complete the sentences below.	https://drive.google.com/file/d/1yAtvxgJ_ruVyu5olQwFgaA0k7CGIsEzt/view?usp=sharing	1	5	3	2	give away used items	not buy commercial cleaning products	reuse containers for storing food\n	donate old clothes\n	buy environmentally friendly products	support sustainable brands\n
17	34	14. Four people are talking about Running. Complete the sentences below. 	https://drive.google.com/file/d/1NVudsakTjHVxGybIA9RGGsExt0XxcfiP/view?usp=sharing	2	1	3	5	at the seaside	prefer running in the street	on the running track	around a lake	in the fitness center	on forest trails
18	42	14. Listen to the opinions of 4 people talking about their purposes of using the Internet, and answer the questions.	https://drive.google.com/file/d/1DuO4xrioKg6FkfECapcxfUv4mWZ4x3Z7/view?usp=sharing	3	4	1	5	complete school assignments	learn courses	watch film	communicate with friends	find transport information	playing video games
19	43	14. Listen to the opinions of 4 people talking about when they like listening to music. Choose the correct answers.	https://drive.google.com/file/d/1D3Fy970-_GRHM24eCFAuv1Gib42HiNFh/view?usp=sharing	3	5	2	1	After waking up	While singing	To relax	While reading	While studying	While driving 
20	44	14. Listen to the opinions of 4 people talking about their purposes of using the Internet, and answer the questions.	https://drive.google.com/file/d/1Jcd5o29UfUgdqcxp8NYyO2dz6uIj-Cv_/view?usp=sharing	4	5	1	3	complete school assignments	learn courses	find transport information	watch film	communicate with friends	read books
21	45	14. Listen to the opinions of 4 people A, B, C, and D, about when they like listening to music. Choose the correct answers. 	https://drive.google.com/file/d/17QX3KEh2UYPOdEsKcr5H8oINjqSZGg5p/view?usp=sharing	3	5	2	1	After waking up\n	While singing\n	To relax\n	While reading\n	While studying\n	While sleeping\n
\.


--
-- TOC entry 3515 (class 0 OID 16534)
-- Dependencies: 233
-- Data for Name: listening_part_3; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.listening_part_3 (id, exam_id, topic, question, correct_answer, audio_path) FROM stdin;
33	26	15. Listen to two people discussing the subject of beauty. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.\n	People share similar ideas about beauty.	MAN 	https://drive.google.com/file/d/1ETq4rugn1LvZQ2IZTXrWSfVl23q4Wh7m/view?usp=sharing
34	26	15. Listen to two people discussing the subject of beauty. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.\n	Ideas about beauty change over time.	WOMAN 	https://drive.google.com/file/d/1ETq4rugn1LvZQ2IZTXrWSfVl23q4Wh7m/view?usp=sharing
35	26	15. Listen to two people discussing the subject of beauty. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.\n	Beauty can be found in unlikely places.	BOTH 	https://drive.google.com/file/d/1ETq4rugn1LvZQ2IZTXrWSfVl23q4Wh7m/view?usp=sharing
36	26	15. Listen to two people discussing the subject of beauty. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.\n	Traditional ideas about beauty are going to change.	WOMAN 	https://drive.google.com/file/d/1ETq4rugn1LvZQ2IZTXrWSfVl23q4Wh7m/view?usp=sharing
37	27	15. Listen to two people discussing Audition. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice. 	Auditions are most important for an actor's career.\n	MAN	https://drive.google.com/file/d/1CYiGJTrX0c8c5uvRE6HSR4_dWmuPjrtL/view?usp=sharing
38	27	15. Listen to two people discussing Audition. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice. 	Actors tend to respond best to strong and engaging scripts.	WOMAN	https://drive.google.com/file/d/1CYiGJTrX0c8c5uvRE6HSR4_dWmuPjrtL/view?usp=sharing
39	27	15. Listen to two people discussing Audition. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice. 	Theater acting and screen acting are quite different from each other.	BOTH	https://drive.google.com/file/d/1CYiGJTrX0c8c5uvRE6HSR4_dWmuPjrtL/view?usp=sharing
40	27	15. Listen to two people discussing Audition. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice. 	Actors should be praised and recognized as much as possible.\n	BOTH	https://drive.google.com/file/d/1CYiGJTrX0c8c5uvRE6HSR4_dWmuPjrtL/view?usp=sharing
41	28	15. A man and a woman are talking about information technology. Which opinion is expressed by who?	Future generations fail to cope with technology information.	MAN 	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
42	28	15. A man and a woman are talking about information technology. Which opinion is expressed by who?	Technology revolution is good for the economy.	WOMAN	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
43	28	15. A man and a woman are talking about information technology. Which opinion is expressed by who?	No computer is superior to the human brain.	WOMAN	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
44	28	15. A man and a woman are talking about information technology. Which opinion is expressed by who?	More should be done to protect individual privacy.	BOTH 	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
45	29	15. Listen to two people discussing the Internet. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	There is too much information on the Internet. 	MAN 	https://drive.google.com/file/d/1cde94fs5l_uVjb4A9iMmBvEevMWrJRhD/view?usp=sharing
46	29	15. Listen to two people discussing the Internet. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Finding information on the Internet requires skills. 	BOTH 	https://drive.google.com/file/d/1cde94fs5l_uVjb4A9iMmBvEevMWrJRhD/view?usp=sharing
47	29	15. Listen to two people discussing the Internet. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	The use of internet affects the way we think. 	WOMAN 	https://drive.google.com/file/d/1cde94fs5l_uVjb4A9iMmBvEevMWrJRhD/view?usp=sharing
48	29	15. Listen to two people discussing the Internet. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	The internet makes young people less patient. 	BOTH 	https://drive.google.com/file/d/1cde94fs5l_uVjb4A9iMmBvEevMWrJRhD/view?usp=sharing
49	30	15. A man and a woman are talking about the local center that was recently opened. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Exhibitions should be different and diverse.	MAN 	https://drive.google.com/file/d/1ZE2XM_7VOeStWMAzTHoNk80gq5zolGId/view?usp=sharing
50	30	15. A man and a woman are talking about the local center that was recently opened. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Traditional customs are gradually losing their significance.	BOTH 	https://drive.google.com/file/d/1ZE2XM_7VOeStWMAzTHoNk80gq5zolGId/view?usp=sharing
51	30	15. A man and a woman are talking about the local center that was recently opened. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Local festivals will disappear soon in the near future.	WOMAN	https://drive.google.com/file/d/1ZE2XM_7VOeStWMAzTHoNk80gq5zolGId/view?usp=sharing
52	30	15. A man and a woman are talking about the local center that was recently opened. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Schools are important to shaping future generations.	WOMAN	https://drive.google.com/file/d/1ZE2XM_7VOeStWMAzTHoNk80gq5zolGId/view?usp=sharing
53	31	15. Listen to two people discussing singers and music. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Singers can be good models for young people. 	WOMAN	https://drive.google.com/file/d/172cbckVEKaG9sbNichFIdFbdH6iKe5WJ/view?usp=sharing
54	31	15. Listen to two people discussing singers and music. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Taste in music is a highly personal thing. 	BOTH 	https://drive.google.com/file/d/172cbckVEKaG9sbNichFIdFbdH6iKe5WJ/view?usp=sharing
55	31	15. Listen to two people discussing singers and music. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Music is a universal language. 	MAN	https://drive.google.com/file/d/172cbckVEKaG9sbNichFIdFbdH6iKe5WJ/view?usp=sharing
56	31	15. Listen to two people discussing singers and music. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Music can manipulate people's feelings. 	BOTH 	https://drive.google.com/file/d/172cbckVEKaG9sbNichFIdFbdH6iKe5WJ/view?usp=sharing
57	32	15. Two professional educators are talking about university. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	The internet makes education more accessible.	BOTH 	https://drive.google.com/file/d/1qsqHHKt5DdRagRpmwaP8SEIJh-se59pt/view?usp=sharing
58	32	15. Two professional educators are talking about university. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Social interactions are essential to university life. 	MAN 	https://drive.google.com/file/d/1qsqHHKt5DdRagRpmwaP8SEIJh-se59pt/view?usp=sharing
59	32	15. Two professional educators are talking about university. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Diverse curriculum is not always a good thing. 	WOMAN 	https://drive.google.com/file/d/1qsqHHKt5DdRagRpmwaP8SEIJh-se59pt/view?usp=sharing
60	32	15. Two professional educators are talking about university. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Competitions between universities should be encouraged. 	MAN 	https://drive.google.com/file/d/1qsqHHKt5DdRagRpmwaP8SEIJh-se59pt/view?usp=sharing
61	33	15. Listen to two people discussing Politics. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Young people are more into politics. 	BOTH 	https://drive.google.com/file/d/1eK4Wkzs4kbQ18Zf7EKolQc0dbOAcbkxl/view?usp=sharing
62	33	15. Listen to two people discussing Politics. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Social media changes politics.	WOMAN	https://drive.google.com/file/d/1eK4Wkzs4kbQ18Zf7EKolQc0dbOAcbkxl/view?usp=sharing
63	33	15. Listen to two people discussing Politics. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	People are now better informed on politics.	MAN	https://drive.google.com/file/d/1eK4Wkzs4kbQ18Zf7EKolQc0dbOAcbkxl/view?usp=sharing
64	33	15. Listen to two people discussing Politics. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	More women pursue politics. 	BOTH 	https://drive.google.com/file/d/1eK4Wkzs4kbQ18Zf7EKolQc0dbOAcbkxl/view?usp=sharing
65	34	15. A man and a woman are talking about urban farming. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Living space is more important than farming space. 	WOMAN	https://drive.google.com/file/d/1pTRaQXKTwdDKEfHdgzdyNGBRda82atlc/view?usp=sharing
66	34	15. A man and a woman are talking about urban farming. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Farming space is appealing.	MAN	https://drive.google.com/file/d/1pTRaQXKTwdDKEfHdgzdyNGBRda82atlc/view?usp=sharing
67	34	15. A man and a woman are talking about urban farming. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Farming space will benefit the urban economy. 	MAN	https://drive.google.com/file/d/1pTRaQXKTwdDKEfHdgzdyNGBRda82atlc/view?usp=sharing
68	34	15. A man and a woman are talking about urban farming. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Farming space is in need of more food. 	BOTH	https://drive.google.com/file/d/1pTRaQXKTwdDKEfHdgzdyNGBRda82atlc/view?usp=sharing
69	42	15. A man and a woman are talking about information technology. Which opinion is expressed by who? 	Future generations fail to cope with technology information. 	MAN	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
70	42	15. A man and a woman are talking about information technology. Which opinion is expressed by who? 	Technology revolution is good for the economy. 	WOMAN	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
71	42	15. A man and a woman are talking about information technology. Which opinion is expressed by who? 	No computer is superior to the human brain. 	WOMAN	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
72	42	15. A man and a woman are talking about information technology. Which opinion is expressed by who? 	More should be done to protect individual privacy. 	BOTH	https://drive.google.com/file/d/1HyxU-a10VCpad7aLlqYgjEaPMhWc8gSh/view?usp=sharing
73	43	15. You will hear a conversation between a boy, Carl, and a girl, Susanna, about a school concert.	….. feels shy about playing his/her violin in public.	WOMAN	https://drive.google.com/file/d/1-xLEzZSPKN5tpcGngLvWtCbaa_GXFtLH/view?usp=sharing
74	43	15. You will hear a conversation between a boy, Carl, and a girl, Susanna, about a school concert.	….. share the same opinion about practising his/her instruments regularly.	BOTH	https://drive.google.com/file/d/1-xLEzZSPKN5tpcGngLvWtCbaa_GXFtLH/view?usp=sharing
75	43	15. You will hear a conversation between a boy, Carl, and a girl, Susanna, about a school concert.	…... thinks he/she would enjoy working in another country.	WOMAN	https://drive.google.com/file/d/1-xLEzZSPKN5tpcGngLvWtCbaa_GXFtLH/view?usp=sharing
76	43	15. You will hear a conversation between a boy, Carl, and a girl, Susanna, about a school concert.	…… persuades he/she to take part in the concert.	MAN 	https://drive.google.com/file/d/1-xLEzZSPKN5tpcGngLvWtCbaa_GXFtLH/view?usp=sharing
77	44	15. You will hear a conversation between a man, Marco, and his wife, Sarah, about a film they have just seen at the cinema. 	….. was expecting to enjoy the film.	WOMAN 	https://drive.google.com/file/d/1iN3ugxQzUXP8sxXwyJ0PGtJt4RUUx67w/view?usp=sharing
78	44	15. You will hear a conversation between a man, Marco, and his wife, Sarah, about a film they have just seen at the cinema. 	….. agree that the city in the film was London.	BOTH 	https://drive.google.com/file/d/1iN3ugxQzUXP8sxXwyJ0PGtJt4RUUx67w/view?usp=sharing
79	44	15. You will hear a conversation between a man, Marco, and his wife, Sarah, about a film they have just seen at the cinema. 	…... was disappointed with the way the main actor performed.	WOMAN 	https://drive.google.com/file/d/1iN3ugxQzUXP8sxXwyJ0PGtJt4RUUx67w/view?usp=sharing
80	44	15. You will hear a conversation between a man, Marco, and his wife, Sarah, about a film they have just seen at the cinema. 	…… thinks this film is the best the director has made.	MAN	https://drive.google.com/file/d/1iN3ugxQzUXP8sxXwyJ0PGtJt4RUUx67w/view?usp=sharing
81	45	15. You will hear a conversation between a man and a woman about a film they have just seen at the cinema.	….. believes that the series is successful because of the main character.	MAN	https://drive.google.com/file/d/1VZblCQSlMgLqLk1Ut2S0egMy3rx4rlVY/view?usp=sharing
82	45	15. You will hear a conversation between a man and a woman about a film they have just seen at the cinema.	….. admire the main character’s behaviour.	BOTH 	https://drive.google.com/file/d/1VZblCQSlMgLqLk1Ut2S0egMy3rx4rlVY/view?usp=sharing
83	45	15. You will hear a conversation between a man and a woman about a film they have just seen at the cinema.	…... thinks that the main character has similar skills to a detective.	WOMAN	https://drive.google.com/file/d/1VZblCQSlMgLqLk1Ut2S0egMy3rx4rlVY/view?usp=sharing
84	45	15. You will hear a conversation between a man and a woman about a film they have just seen at the cinema.	…… was surprised to find the main character so funny.	MAN	https://drive.google.com/file/d/1VZblCQSlMgLqLk1Ut2S0egMy3rx4rlVY/view?usp=sharing
85	46	15. Listen to two people discussing Community design. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Building design can influence people's behavior.	BOTH 	https://drive.google.com/file/d/1WWAznQEgwKGmpyo3xCyRIR-1NDHrHzd1/view?usp=sharing
86	46	15. Listen to two people discussing Community design. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Creating community can take time.	WOMAN	https://drive.google.com/file/d/1WWAznQEgwKGmpyo3xCyRIR-1NDHrHzd1/view?usp=sharing
87	46	15. Listen to two people discussing Community design. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Work communities and social communities are the same.	MAN 	https://drive.google.com/file/d/1WWAznQEgwKGmpyo3xCyRIR-1NDHrHzd1/view?usp=sharing
88	46	15. Listen to two people discussing Community design. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Technology has changed how community forms. 	MAN 	https://drive.google.com/file/d/1WWAznQEgwKGmpyo3xCyRIR-1NDHrHzd1/view?usp=sharing
89	25	15. Listen to two people discussing changes in the workplace. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Continuity is very important in the workplace.	MAN 	\nhttps://drive.google.com/file/d/1dV3E_Mwi9smX4GTGEgpE52ESQ-PZeAIM/view?usp=sharing
90	25	15. Listen to two people discussing changes in the workplace. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Job security cannot always be guaranteed.	WOMAN 	\nhttps://drive.google.com/file/d/1dV3E_Mwi9smX4GTGEgpE52ESQ-PZeAIM/view?usp=sharing
91	25	15. Listen to two people discussing changes in the workplace. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Job satisfaction is an important motivator.	BOTH 	\nhttps://drive.google.com/file/d/1dV3E_Mwi9smX4GTGEgpE52ESQ-PZeAIM/view?usp=sharing
92	25	15. Listen to two people discussing changes in the workplace. Read the opinions below and decide whose opinion matches the statements, the man, the woman, or both the man and the woman. You can listen to the discussion twice.	Technology is good for the entire economy.	MAN 	\nhttps://drive.google.com/file/d/1dV3E_Mwi9smX4GTGEgpE52ESQ-PZeAIM/view?usp=sharing
\.


--
-- TOC entry 3517 (class 0 OID 16548)
-- Dependencies: 235
-- Data for Name: listening_part_4; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.listening_part_4 (id, exam_id, topic, question, correct_answer, audio_path, option1, option2, option3) FROM stdin;
41	28	16. Listen to an office worker talking about working from home and answer the questions below. 	What does she say about working at home?	2	https://drive.google.com/file/d/1cKyHP6ImrY0XUqMelMuFuVJRlABMqKYS/view?usp=sharing	There are no distractions	Not as good as expected 	Video calls are superior to face-to-face conversation 
42	28	16. Listen to an office worker talking about working from home and answer the questions below. 	According to the author, working from home:	3	https://drive.google.com/file/d/1cKyHP6ImrY0XUqMelMuFuVJRlABMqKYS/view?usp=sharing	Needs a big home office 	Do not require self-motivation 	It depends on your situation and personality
43	28	17. Listen to an expert talking about the importance of sleep and answer the questions below. 	The most important thing(s) to help sleep well is 	1	https://drive.google.com/file/d/1QGQ2quHdPrRDEqEkIMOnWF6tI0NTVteQ/view?usp=sharing	Blocking noise and light is the key	Beds are best for sleeping 	Resting suffieently is necessary 
44	28	17. Listen to an expert talking about the importance of sleep and answer the questions below. 	According to the expert, what is the public attitude towards sleeping? 	1	https://drive.google.com/file/d/1QGQ2quHdPrRDEqEkIMOnWF6tI0NTVteQ/view?usp=sharing	The media overemphasize the subject	The young generation tends to have unhealthy sleeping habits	Sleeping quality has deteriorated over time
33	26	16. Listen to an announcer talking about a newly released novel and answer the questions below. 	What does the announcer say about the new novel? 	1	https://drive.google.com/file/d/1j89wKU1wOLKseLB2B3fmHbhp1z_Y7Xb5/view?usp=sharing	It is different from his earlier works	It is romantic and soft	It is less famous than his earlier works
34	26	16. Listen to an announcer talking about a newly released novel and answer the questions below. 	What does the announcer say the writer should do in the future? 	3	https://drive.google.com/file/d/1j89wKU1wOLKseLB2B3fmHbhp1z_Y7Xb5/view?usp=sharing	The writer should continue to write this genre	The writer should go back to his original genre	He should listen to critics before writing his next work
35	26	17. Listen to an expert talking about professionalism and answer the questions below. 	What does the expert say what being professional is all about?	1	https://drive.google.com/file/d/16GWfHIgl1Xj1Xg8RgP2R-Gk8axQKIO5Z/view?usp=sharing	To maintain positive attitude	To create good working environment	To make good impressions
36	26	17. Listen to an expert talking about professionalism and answer the questions below. 	What does the expert say about the definition of professionalism?	2	https://drive.google.com/file/d/16GWfHIgl1Xj1Xg8RgP2R-Gk8axQKIO5Z/view?usp=sharing	It is the same of 40 years ago	Our definition of it is changing	It will not change anymore
37	27	16. Listen to a writer talking about her experience in writing and choose the correct answer. 	What does the writer believe helps her the most in her writing process? 	2	https://drive.google.com/file/d/1zhaXN63vVWaFw6rW_qgCnOMjFU1vdl-c/view?usp=sharing	Writing every day for 15-20 minutes	Create dedicated periods for writing 	Finding a quiet space to work \n
38	27	16. Listen to a writer talking about her experience in writing and choose the correct answer. 	What does the writer regret doing during her experience with writer's block?	1	https://drive.google.com/file/d/1zhaXN63vVWaFw6rW_qgCnOMjFU1vdl-c/view?usp=sharing	Refuse to seek advice of others 	Ignoring feedback from editors 	Writing without a plan\n
39	27	17. The radio is talking about a musician's career and latest albums. Listen and choose the correct answer. 	What has the musician decided regarding his singing career? 	1	https://drive.google.com/file/d/1-viMn-w4aqqC8BpB7xxl2_zFp--aQNlL/view?usp=sharing	He will retire from singing professionally \n	He will make a comeback after a long break 	He will inform fans about new albums 
40	27	17. The radio is talking about a musician's career and latest albums. Listen and choose the correct answer. 	What could the musician have achieved with his recent albums?	1	https://drive.google.com/file/d/1-viMn-w4aqqC8BpB7xxl2_zFp--aQNlL/view?usp=sharing	He could have been more successful 	He could have inspired future generations in general	He could have gotten a bigger fan base
45	29	16. Listen to a critic talking about a newly broadcast TV series and answer the questions. 	What happened to the TV series?	3	https://drive.google.com/file/d/1yadGJ4TvGsG28as0YDVdt3dAWrtqW0v9/view?usp=sharing	It didn't receive enough investment at the early stage.	It was overlooked by critics.	It caught the audience's attention from the start.
46	29	16. Listen to a critic talking about a newly broadcast TV series and answer the questions. 	According to the expert, what is the series' potential?	3	https://drive.google.com/file/d/1yadGJ4TvGsG28as0YDVdt3dAWrtqW0v9/view?usp=sharing	New seasons will be produced due to great demand. 	It inspires young filmmakers to follow a new movie-making style. 	Series are damaged by overexposure.
47	29	17. Listen to an advertising expert talking about the advertising industry and answer the questions. 	What does the expert say about the negative side of advertising? 	1	https://drive.google.com/file/d/11tVTw06lgrAHLtY7diF1YUJ6Yqe0KL4g/view?usp=sharing	Series are damaged by overexposure.	Advertisements might sometimes be repetitive which is annoying.	Advertising costs the same amount of money to produce a movie.
48	29	17. Listen to an advertising expert talking about the advertising industry and answer the questions. 	In what way can advertising affect sports? 	3	https://drive.google.com/file/d/11tVTw06lgrAHLtY7diF1YUJ6Yqe0KL4g/view?usp=sharing	They help to attract more fans. 	They can boost ticket sales and sales of sports-related items. \n	They can generate negative publicity for the sport. 
49	30	16. An expert is giving comments on a newly released movie and answer the questions. 	What part of the movie is disappointing? 	1	https://drive.google.com/file/d/1PziJgz6I8ZDNeoi52Q1xuaQ-nTWleEH1/view?usp=sharing	The dialogues seem unrealistic	The settings don't make sense	The original cast was replaced
50	30	16. An expert is giving comments on a newly released movie and answer the questions. 	What is the expert's comment on the movie industry? 	2	https://drive.google.com/file/d/1PziJgz6I8ZDNeoi52Q1xuaQ-nTWleEH1/view?usp=sharing	Technology will soon replace human actors	The new industry demand is negatively influencing script production	New story plots should be invented to capture the audience's interest
51	30	17. A critic is giving opinions about a restaurant and answer the questions. 	What are the critics' opinions about the restaurant? 	2	https://drive.google.com/file/d/168Si07aspCPy9BFcjYxfFhNJOWaSJWox/view?usp=sharing	The food is not fresh	The service is not good	The chief lack of experience 
52	30	17. A critic is giving opinions about a restaurant and answer the questions. 	What can compete with online food delivery? 	3	https://drive.google.com/file/d/168Si07aspCPy9BFcjYxfFhNJOWaSJWox/view?usp=sharing	Organic ingredients	Providing ready-made pack for customers	Customers feel valued and welcome
53	31	16. Listen to a lecturer talking about two big writers of history, which are Shakespares William and Louis Michael. 	What was the lecturer's opinion about both authors' past work?	1	https://drive.google.com/file/d/1t86J4C5jZiI4U9uYtz2oo-osO8Gd_n0n/view?usp=sharing	They have both been overlooked by academics.	They make reference to each other's work.	One was less successful than the other.
54	31	16. Listen to a lecturer talking about two big writers of history, which are Shakespares William and Louis Michael. 	What did the lecturer say about both authors?	3	https://drive.google.com/file/d/1t86J4C5jZiI4U9uYtz2oo-osO8Gd_n0n/view?usp=sharing	Their reputation goes beyond their target audience.	They should have been more popular.	It is not always easy for the meanings to be identified.
55	31	17. Listen to an educational expert talking about sport competition in school.  	What is the expert's opinion about sports competitions?	3	https://drive.google.com/file/d/1VeSt2ANsEY2GEo5cFvrxUhv9DACES20H/view?usp=sharing	Provide school with external investments	Nature potential sportsmens for the country	They can cause harmful effects
56	31	17. Listen to an educational expert talking about sport competition in school.  	What is the expert's advice for schools?	2	https://drive.google.com/file/d/1VeSt2ANsEY2GEo5cFvrxUhv9DACES20H/view?usp=sharing	Should consider sports as a mandatory subject 	Provides them with a balance in their lives 	Keep students focus on academic subjects
57	32	16. Listen to a critic talking about a newly broadcast TV series and answer the questions. 	What happened to the TV series? 	3	https://drive.google.com/file/d/1lmYo6vh7z-YBHemXYF8WsfhYv5STeOFy/view?usp=sharing	It didn't receive enough investment at the early stage.	It was overlooked by critics.	It caught the audience's attention from the start.
58	32	16. Listen to a critic talking about a newly broadcast TV series and answer the questions. 	According to the expert, what is the series' potential? 	3	https://drive.google.com/file/d/1lmYo6vh7z-YBHemXYF8WsfhYv5STeOFy/view?usp=sharing	New seasons will be produced due to great demand.	It inspires young filmmakers to follow a new movie-making style.	Series are damaged by overexposure.
59	32	17. Listen to an advertising expert talking about the advertising industry and answer the questions. 	What does the expert say about advertising?	1	https://drive.google.com/file/d/1owbfAJ8ah5piJlBuQdOgkDgPUkMoKefy/view?usp=sharing	It helps to reach new customers.	Advertisements might sometimes be repetitive which is annoying.	Advertising costs the same amount of money to produce a movie.
60	32	17. Listen to an advertising expert talking about the advertising industry and answer the questions. 	In what way can advertising affect sports? 	3	https://drive.google.com/file/d/1owbfAJ8ah5piJlBuQdOgkDgPUkMoKefy/view?usp=sharing	They help to attract more fans.	They can boost ticket sales and sales of sports-related items.	They are not always good for sport fans.
61	33	16. Listen to a city planner talk at a press conference about a Regional Development Planning and answer the questions below. 	What is one of the main criticisms of the Regional Development Plan? 	1	https://drive.google.com/file/d/1CdBx_qtEpy37NOyB73AQWfDodRbMShRs/view?usp=sharing	It doesn't provide enough alternatives to driving.	It places too much emphasis on public transportation.	It is too expensive to implement the plan.
62	33	16. Listen to a city planner talk at a press conference about a Regional Development Planning and answer the questions below. 	What challenge is the Regional Development Plan likely to face? 	3	https://drive.google.com/file/d/1CdBx_qtEpy37NOyB73AQWfDodRbMShRs/view?usp=sharing	It may be delayed due to funding issues.	It could face difficulties in gaining government approval.	It is likely to meet resistance from local communities.
63	33	17. Listen to a critic talk about a New series and answer the questions below. 	What is one criticism mentioned regarding the series' storytelling? 	2	https://drive.google.com/file/d/1l1IbzS6UqQRhnqJHsQ81xA6M2Mb351XV/view?usp=sharing	The plot is overly complicated.	The dialogues seem unrealistic.	The characters' backgrounds are not explored.
64	33	17. Listen to a critic talk about a New series and answer the questions below. 	What issue is highlighted about the series' writing? 	2	https://drive.google.com/file/d/1l1IbzS6UqQRhnqJHsQ81xA6M2Mb351XV/view?usp=sharing	The humor is poorly executed. 	The new industry demand is negatively influencing script production. 	Many scripts are lacking original ideas. 
65	34	16. Listen to a man talk about Life after university and answer the questions below. 	How does life change for graduates after university?	3	https://drive.google.com/file/d/1BC4oj8d87hM0X4fRw0WWQNMMDk-ks5wr/view?usp=sharing	They feel more stressed about job seeking	They are likely to stick to their academic routines	They are likely to be more flexible and open-minded
66	34	16. Listen to a man talk about Life after university and answer the questions below. 	What is a common characteristic of the job market after university?	2	https://drive.google.com/file/d/1BC4oj8d87hM0X4fRw0WWQNMMDk-ks5wr/view?usp=sharing	More opportunities for networking	More competitive	Many jobs offer great benefits
67	34	17. Listen to a man talk about a promotion campaign for a product and answer the questions below. 	What is the main issue with the product's promotion campaign?	2	https://drive.google.com/file/d/17k-cAct84GqOIoxSt0zruWltrLnpwy7i/view?usp=sharing	It is using outdated advertising methods	They use exaggerated claims	It is not targeting the correct market
68	34	17. Listen to a man talk about a promotion campaign for a product and answer the questions below. 	Why is the product struggling to stand out in the market?	2	https://drive.google.com/file/d/17k-cAct84GqOIoxSt0zruWltrLnpwy7i/view?usp=sharing	It is priced too high compared to its competitors	It is too similar to many existing products	It is not available in enough stores
69	42	16. Listen to a professional talk about advertising and sponsoring in sports and answer the questions. 	What is one benefit of advertising and sponsoring in sports?	3	https://drive.google.com/file/d/1FiSZcJAXjH4IN9z-2V_91DafaHk-oc6T/view?usp=sharing	It reduces the cost of sports events by providing additional funding.	It exclusively promotes the sport, without benefiting the sponsoring brand.	It can help reach new customers.
70	42	16. Listen to a professional talk about advertising and sponsoring in sports and answer the questions. 	What is a potential downside of advertising and sponsoring in sports?	1	https://drive.google.com/file/d/1FiSZcJAXjH4IN9z-2V_91DafaHk-oc6T/view?usp=sharing	They can generate negative publicity for the sport.	They lead to the commercialization of sports.	They result in decreased viewership due to overexposure of ads during broadcasts.
71	42	17. Listen to a critic talk about two famous writers, James Joyce and T.S. Eliot, and answer the questions. 	What is a key characteristic of the works of James Joyce and T.S. Eliot?	2	https://drive.google.com/file/d/1iVMb66ICeGcJgr_nDsddbcajJ1uybJRP/view?usp=sharing	They both explore simple, straightforward narratives.	They both make references to each other in their work.	They avoid using historical references in their writing.
72	42	17. Listen to a critic talk about two famous writers, James Joyce and T.S. Eliot, and answer the questions. 	How would you describe the meaning of the works of Joyce and Eliot?	2	https://drive.google.com/file/d/1iVMb66ICeGcJgr_nDsddbcajJ1uybJRP/view?usp=sharing	Their works are straightforward and easily understood on the first reading.	The meaning of their work is not always easily identified.	Their works primarily focus on romance and human connection.
73	43	16. Listen to a speech about research on happiness and answer the questions. 	What is one problem with the way happiness research is shared with the public?	1	https://drive.google.com/file/d/1Asmqdgamezhv6gKwUPRBT4wZjGqW6y--/view?usp=sharing	It has not been accurately reported by the media.	It is only communicated through academic journals.	The media refuses to cover happiness research at all.
74	43	16. Listen to a speech about research on happiness and answer the questions. 	What is true about the happiness research?	3	https://drive.google.com/file/d/1Asmqdgamezhv6gKwUPRBT4wZjGqW6y--/view?usp=sharing	The research lack proper fundings.	The research only studies people from one country.	The research is unlikely to find a conclusive answer.
75	43	17. Listen to a speech about a well-known writer and his novels, both new and previous.	How is the writer’s new novel compared to his previous works?	2	https://drive.google.com/file/d/1PVBXCEGyxyy4IA0HeXtrbr7rcbsAIf-6/view?usp=sharing	It mirrors the exact style and themes of his earlier novels.	It is quite different compared to his previous works.	It abandons all storytelling techniques in favor of randomness.
76	43	17. Listen to a speech about a well-known writer and his novels, both new and previous.	What advice is given to the writer regarding his future novels?	3	https://drive.google.com/file/d/1PVBXCEGyxyy4IA0HeXtrbr7rcbsAIf-6/view?usp=sharing	He should ignore all feedback and keep experimenting recklessly.	He should revert to his original style without trying anything new.	He should listen to the critics before writing the next novel.
77	44	16. Listen to a professional talk about security cameras in the workplace and answer the questions. 	How do employees often feel about security cameras in the workplace?	2	https://drive.google.com/file/d/1qyA8IT8BqyZ3dWwoFIshwBy4uOSTF7zB/view?usp=sharing	They feel they are completely free from surveillance.	Employees probably worry unnecessarily.	They believe cameras are exclusively used to record minor mistakes.
78	44	16. Listen to a professional talk about security cameras in the workplace and answer the questions. 	How should employees feel about security cameras in the workplace?	1	https://drive.google.com/file/d/1qyA8IT8BqyZ3dWwoFIshwBy4uOSTF7zB/view?usp=sharing	People should feel reassured.	Employees should view them as an invasion of privacy.	Workers should feel indifferent to their presence.
79	44	17. Listen to a professor talk about the lives of students after graduating university and answer the questions. 	What is a key strategy for graduates to succeed in life after university?	2	https://drive.google.com/file/d/1aSnY6GC5hJeIKcaZ4L_pGKhUZ-b9dQ7z/view?usp=sharing	Avoiding changes and sticking to rigid plans.	Being flexible and open-minded.	Refusing to work outside their degree field.
80	44	17. Listen to a professor talk about the lives of students after graduating university and answer the questions. 	What is the trend in the job market for university graduates?	1	https://drive.google.com/file/d/1aSnY6GC5hJeIKcaZ4L_pGKhUZ-b9dQ7z/view?usp=sharing	They are becoming more competitive.	Employers are lowering their expectations for candidates.	Jobs are guaranteed for everyone with a degree.
81	45	16. Listen to a professional talk about sleep and tiredness and answer the questions. 	What is one key factor for achieving quality sleep?	1	https://drive.google.com/file/d/1fLOgOteVF1CXIhrC4glktezhdsATK0pO/view?usp=sharing	Blocking out noise and light.	Increasing exposure to natural light at night.	Sleeping in a room with background TV noise.
82	45	16. Listen to a professional talk about sleep and tiredness and answer the questions. 	Why do people often fail to address tiredness?	3	https://drive.google.com/file/d/1fLOgOteVF1CXIhrC4glktezhdsATK0pO/view?usp=sharing	People prioritize diet and exercise over sleep.	People are too busy focusing on their sleep environment.	People can’t always recognize the symptoms of tiredness.
83	45	17. Listen to a financial advisor discussing financial management and answer the questions. 	What is one effective way to manage financial spending?	1	https://drive.google.com/file/d/1iTdWoYxeNEWe0ifycSpVWUCcjTueq4Wp/view?usp=sharing	Monitor your spending for a weekly plan	Save all your income without a spending plan	Ignore small daily expenses to focus on big ones
84	45	17. Listen to a financial advisor discussing financial management and answer the questions. 	What is a helpful strategy for improving financial management?	3	https://drive.google.com/file/d/1iTdWoYxeNEWe0ifycSpVWUCcjTueq4Wp/view?usp=sharing	Rely solely on trial and error for financial decisions	Depend entirely on online budgeting tools	Seek advice from someone who has experience
85	46	16. Listen to a professor talk about how sports participation plays out in students' lives and answer the questions. 	According to the content, what role does sports participation play in students' lives?	1	https://drive.google.com/file/d/1a2JbyfJsUxEh1ISCFbQwr4ilofKlGpVs/view?usp=sharing	It helps balance students' lives	It is solely a leisure activity	It generally distracts students from their studies
86	46	16. Listen to a professor talk about how sports participation plays out in students' lives and answer the questions. 	What possible downside of excessive sports involvement is mentioned in the content?	3	https://drive.google.com/file/d/1a2JbyfJsUxEh1ISCFbQwr4ilofKlGpVs/view?usp=sharing	It primarily results in social isolation	It reduces students’ motivation	It can have a harmful effect
87	46	17. Listen to an MC talk about a successful television series and answer the questions. 	According to the content, what is one characteristic of successful television series?	1	https://drive.google.com/file/d/1TCNQCHE0XSuUJs6gvhFAYQQpb2tL22qU/view?usp=sharing	It has consistent quality throughout.	It relies on frequent plot twists to compensate for uneven quality.	It continually shifts genres to keep the audience interested.
88	46	17. Listen to an MC talk about a successful television series and answer the questions. 	What has made the series changed?	1	https://drive.google.com/file/d/1TCNQCHE0XSuUJs6gvhFAYQQpb2tL22qU/view?usp=sharing	Viewer habits influence the way that series are made.	More money has been invested.	The cast has been changed.
89	25	16. Listen to a student talk about his decision to take a break from studying and answer the question below. 	Why did Jason decide to take a break from studying?	1	https://drive.google.com/file/d/104bearRgHlI0stNRsIaIyEYCeC-ME_TT/view?usp=sharing	He wasn’t ready to start higher education.\n	He wanted to save money.\n	He needed more time to prepare.\n
90	25	16. Listen to a student talk about his decision to take a break from studying and answer the question below. 	What is one of Jason's main goals during his break?	2	https://drive.google.com/file/d/104bearRgHlI0stNRsIaIyEYCeC-ME_TT/view?usp=sharing	To travel more.\n	To become more independent.	To explore different career paths.
91	25	17. Listen to a critic talk about a book about the life of a scientist and answer the questions below.  	What writing style did the critic praise in this book?	3	https://drive.google.com/file/d/1fEklLFRg6rqmzADOxZ9QV8meJMeKd7k1/view?usp=sharing	The use of poetic language to create emotional depth	The use of technical jargon to challenge readers	The use of simple language to describe complex ideas
92	25	17. Listen to a critic talk about a book about the life of a scientist and answer the questions below.  	How does this book compare to the author's previous work?	2	https://drive.google.com/file/d/1fEklLFRg6rqmzADOxZ9QV8meJMeKd7k1/view?usp=sharing	It departs entirely from the themes of the previous book	It is similar to the previous book about a scientist	It focuses on a different subject altogether
\.


--
-- TOC entry 3503 (class 0 OID 16445)
-- Dependencies: 221
-- Data for Name: reading_part_1; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.reading_part_1 (question_id, exam_id, group_id, question, correct_answer, option1, option2, option3) FROM stdin;
234	23	1	My ….. is now far from work. 	Home 	Home 	Near	Toilet
235	23	1	I have to ….. to work.	Drive 	Food 	Drive 	Fly 
236	23	1	I sometimes meet ….. at the coffee shop for lunch.	Friends 	Friends 	Enemies 	Birds
237	23	1	We walk in the …... Sometimes. 	Park 	Moon 	Sun 	Park 
238	23	1	The trees are …... so we like looking at them. 	Pretty 	Quiet	Pretty 	Pray 
189	16	1	I ......  in a flat.\n	live	die	live	say 
190	16	1	I ...... it with my friend.\n	share	share	pull	know
191	16	1	We are in the same .......\n	class	plane	train	class
192	16	1	We ......  to work.\n	drive	drive	destroy	throw
193	16	1	We like to ......  dinner.\n	cook	listen	cook	drink 
209	19	1	The weather is .......	\nGreat	\nGreat	Sad	Tired
210	19	1	We are on the .......	Boat	Boat	Cloud 	Sunny
211	19	1	We eat dinner ......  we go to church.	Then	Do	Then	Make
212	19	1	We are going to ......  around.	Drive	Lie	Drive	Sleep
213	19	1	I hope the weather isn't ...... hot. 	Too	Too	Many	Little
219	21	1	It is ......  what I like.	Just	Do	Just	To
220	21	1	And it is the perfect color, .......	Too	Hard	Last	Too
221	21	1	I am going to wear it ......  my birthday party.	To	To	And	But
222	21	1	I will save you ......  cake. 	Some	Buy	Some	Drop
223	21	1	......  my love to everyone.	Give	Take	Bring	Give
229	22	1	I've just com back from my trip and I really ....... you.	miss	meet 	miss	kick
230	22	1	I ........ you by phone yesterday but coudn't reach you.	called	called	frop	flop 
231	22	1	Are you ...... for the event tomorrow? 	ready 	ready 	weak 	die
232	22	1	I can't wait to ...... you soon and catch up. 	meet	cheat	teach 	meet
233	22	1	Let's go out for ..... tomorrow night when you're free. 	dinner	prefer	butter	dinner
164	12	1	Everyone is ......\n	Friendly 	Hate 	Short	Friendly 
165	12	1	I can ......  to my class.\n	Walk 	Walk 	Fly	Sleep
166	12	1	I met her for the ......  time.\n	First 	Finish 	First 	sad
167	12	1	She can ...... 5 languages.\n	Speak 	Drink 	Lie	Speak 
134	9	1	I am never ........	Late	Meetings	Early 	Late
135	9	1	In the mornings, I attend ........	Meetings	Meetings	Hopital	Cook
136	9	1	I eat lunch in the ........ 	Park	Park 	Boat 	River
137	9	1	I buy food from the ........	Shop	Bus	Shop	Boat 
138	9	1	I always ........ dinner for myself.	Cook	Snap	Take	Cook
139	10	1	My colleague is ......... 	Sick 	Sick	Pink	Better
140	10	1	I need to ........ some reports.	Read	Feel	Read	Meeting
141	10	1	I have an important ........ with a client.	Meeting 	Driving	Sleeping	Meeting
142	10	1	The phone in my office is ........  all the time.	Ringing	Falling	Ringing	Saving
143	10	1	I need to take a break and ........ coffee.	Drink	Drink	Read	See
144	11	1	I start .....\n	Early	Perpectly	Early	Beautifully
145	11	1	I have .....\n	Lunch	Lunch	Tennis 	Ball
146	11	1	I ...... the office.	Leave	Destroy	Leave	Think
147	11	1	I go home in my new ....\n	Car	Sky	Rock	Car
148	11	1	I go to bed when I feel ........	Sleepy	Sleepy	Free	Bad 
168	12	1	We eat dinner .......\n	Together	Alone	Together	Happy
174	13	1	I imagine you don't want to ...... this.\n	Miss	Meet	Miss	Forget
175	13	1	I ......  you earlier but you were not home.\n	Called	Called	Speak 	Tall 
176	13	1	Can you be ...... before 7pm?\n	Ready	Finish 	Ready	Move
177	13	1	I can ......  you at your place then.\n	Meet	Meet	Miss	 Call
178	13	1	Don't have too much ...... because we're going to eat cake.\n	Dinner	Money	Salary	Dinner
184	14	1	The budget doesn't ......\n	Balance	Hard 	Destroy	Balance
185	14	1	Could you get the financial ......?\n	Statement	Statement	Fail	Talk
186	14	1	 I ......  it will help.\n	Think	Hate	Think	Feel
187	14	1	Read the information ...... not quickly.\n	Slowly	Terribly	Fastly	Slowly
188	14	1	Send me the results ...... you go home, not after.\n	Before	Before	After	Faster
194	17	1	The water is ......\n	Clear	Clear	Happy 	Sad
195	17	1	The ......  is out.\n	Sun	Hope	Sun	Tired
196	17	1	I have an ......  holiday.\n	Enjoyable	Acceptable	Label 	Enjoyable
197	17	1	After ......  so hard.\n	Working	Thinking	Working	Listening
198	17	1	I hope to ...... your letter.\n	Read	Read	Help	Hear
204	18	1	I saw some shows in the ......  of one store.\n	Window	Boat	Window	Car
205	18	1	I bought some food at the .......\n	Market	Stadium	Market	Concert
206	18	1	I didn't ......  it.\n	Buy	Buy	Destroy	Sad
207	18	1	I ate .......\n	Cake	Window	Door	Cake
208	18	1	I ......  a program on TV.\n	Watched	Watched	Listened	Heard
214	20	1	I am living with a family ......  the city.\n	Near	Near	Do 	Short 
215	20	1	The children are ...... to me.\n	Friendly	Comfortable	Friendly	Convenient
216	20	1	Seamus and Agnes ......  speaking English with me.\n	Practice	Meet	Practice	Report
217	20	1	Sometimes, I ...... to Seamus and Agnes.\n	Read	Remember	Listen 	Read
218	20	1	I hate the food, ......  yesterday I ate out.\n	So	And	But	So
239	24	1	I love this place because everybody here is … 	Friendly 	Busy	Friendly 	Sad
240	24	1	I live in a flat near the university so I can …. to my class	Walk 	Fly	Drive 	Try 
241	24	1	Yesterday I met Lesly for the … time. She is sharing the flat with me. 	First	First 	Next 	Busy
242	24	1	She is studying French and she can ….. five languages. 	Speak 	Speak 	Call	Buy
243	24	1	Last night we went out for dinner ….. 	Together	Spek 	Try 	Together
\.


--
-- TOC entry 3505 (class 0 OID 16459)
-- Dependencies: 223
-- Data for Name: reading_part_2; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.reading_part_2 (question_id, exam_id, group_id, topic, sentence_text, sentence_key, is_example_first) FROM stdin;
283	9	1	Buying a new house	The first and most important thing is to choose the location.	0	t
284	9	1	Buying a new house	The most important of these to look at is the price of homes.	2	f
285	9	1	Buying a new house	In order to choose the right place, you need to consider several factors.	1	f
286	9	1	Buying a new house	Such requirements of course depend on your personal circumstances. 	4	f
287	9	1	Buying a new house	Other factors to look at are the place of employment, shops and schools.	3	f
288	9	2	Using public cycle	Go to the collection point and click on the screen to choose the bike with your bank card.	0	t
289	9	2	Using public cycle	When you finish your journey, return the bike to any empty collection point.	4	f
290	9	2	Using public cycle	Enter the code on the lock of the bike and wait for the green lights.	2	f
291	9	2	Using public cycle	Choose "hire the cycle" on the screen and then follow the instructions to receive an unlock code.	1	f
292	9	2	Using public cycle	When the light comes, you can unlock your bike and start your journey.	3	f
363	13	1	Printer process	First, you need to find an appropriate place to put your printer.	0	t
364	13	1	Printer process	A light comes on at the front of the printer.	2	f
365	13	1	Printer process	Before using the printer, you need to put papers into it.	4	f
366	13	1	Printer process	If the light is green, your printer is ready to use.	3	f
367	13	1	Printer process	When your printer is in place, turn it on using the switch.	1	f
368	13	2	Traffic lights	You should arrive at the main office by 6.30 a.m and collect your keys.	0	t
369	13	2	Traffic lights	When you have completed all deliveries, return to your office.	3	f
370	13	2	Traffic lights	You must return your keys to the office manager after you get back.	2	f
371	13	2	Traffic lights	In the office, you can also collect a map of your route.	1	f
372	13	2	Traffic lights	You must follow the route on the map to deliver packages.	4	f
443	20	1	Hand in assignment	To successfully finish the assignment, follow these instructions. 	0	t
444	20	2	Fire instructions	The first step is to find out how much know about the problem. 	0	t
485	24	1	A biography	This report gives information regarding public transportation in the city.	0	t
486	24	1	A biography	They all agreed that there is not enough service in morning rush hour.	2	f
487	24	1	A biography	We interviewed 1000 citizens who take the bus at least 5 days a week.	1	f
488	24	1	A biography	This is why we believe we must add more vehicles to busy routes in order to have more satisfied customers.	4	f
489	24	1	A biography	Additionally, they said that the busses are too crowded.	3	f
490	24	2	Visting a new place	If you are visiting our Bed and Breakfast for the first time, please read the instructions carefully.	0	t
491	24	2	Visting a new place	Then, she will give you the key and show you around the apartment.	2	f
492	24	2	Visting a new place	Jessica, our host, will greet you on arrival.	1	f
493	24	2	Visting a new place	At this time, you can also ask her any questions about things to do in the area.	3	f
494	24	2	Visting a new place	During your stay, you can use any of the flat’s amenities at your leisure, and before you check out, please leave the key in the mailbox.	4	f
445	21	1	Gilberto’s Day	The alarm clock was buzzing loudly.	0	t
446	21	1	Gilberto’s Day	As he brushed his teeth, he looked at his phone. It was already 9 am and he was late for school!	4	f
447	21	1	Gilberto’s Day	He was still quite tired and groggy.	2	f
448	21	1	Gilberto’s Day	Grumpily, Gilberto got out of bed.	1	f
449	21	1	Gilberto’s Day	It’s because he had been up late the night before.	3	f
293	10	1	Instructions for new students	When you arrive at the university, go to the help desk.	0	t
294	10	1	Instructions for new students	You can use this card to borrow books from the library and access lesson materials online.	3	f
295	10	1	Instructions for new students	He or she will enter your information into the computer and give you an identification card.	2	f
296	10	1	Instructions for new students	A member of staff will ask for your name and your address.	1	f
297	10	1	Instructions for new students	You will find these in material links on your home page.	4	f
298	10	2	Participate in a race.	On your arrival, please go to the information point at the north gate.	0	t
299	10	2	Participate in a race.	A member of staff will give you a numbered armband to wear.	3	f
300	10	2	Participate in a race.	Runners must register here at least 30 minutes before the race starts at 9am.	1	f
301	10	2	Participate in a race.	Please put this on immediately and join other competitors at the warm-up area.	4	f
450	21	2	Field Trip Instructions 	Please arrive at school at 7 a.m sharp\n	0	t
451	21	2	Field Trip Instructions 	In fact, we will only wait 10 minutes for late arrivals.\n	1	f
452	21	2	Field Trip Instructions 	Once attendance is taken, the busses will be loaded.\n	2	f
453	21	2	Field Trip Instructions 	Please use the bathroom first, as there will be no stops.	4	f
454	21	2	Field Trip Instructions 	However, please check your seat number before this to minimize confusion.\n	3	f
423	18	1	Key card\n	To enter the building and use the lift, you will need your key card.	0	t
424	18	1	Key card\n	He or she will ask for your name and your flat number, and then will write these down.	4	f
425	18	1	Key card\n	If you lose this, you will need to see the staff member at the front desk.	1	f
426	18	1	Key card\n	He or she will make a copy of it and give you a new key card.	2	f
427	18	1	Key card\n	You will also need to show your identification card.	3	f
428	18	2	 Tom Harper\n	When he was young, he began writing short stories for a magazine	0	t
429	18	2	 Tom Harper\n	The characters he imagined were one of the most famous in the world.	3	f
430	18	2	 Tom Harper\n	This popularity made Tome Harper rich and successful.	4	f
431	18	2	 Tom Harper\n	He soon wrote regularly for the magazine, but he was not satisfied.	1	f
432	18	2	 Tom Harper\n	He almost left the magazine, but then he decided to create some unusual new characters.	2	f
302	10	2	Participate in a race.	To do this, you just need to give us your photo card.	2	f
383	14	1	Car park\n	When you arrive, please take a ticket from a machine at the entrance.\n	0	t
384	14	1	Car park\n	Please display the ticket with this information in the window of your car.\n	2	f
385	14	1	Car park\n	The machine will read your information and tell you how much you have to pay.\n	4	f
386	14	1	Car park\n	Before you leave, please put the ticket on the machine by the gate.\n	3	f
387	14	1	Car park\n	This ticket will show the date and the time you arrived.\n	1	f
388	14	2	Paperwork submission process\n	In your account, press "open new window".\n	0	t
389	14	2	Paperwork submission process\n	Once you put the files there, press the "send" button.\n	3	f
390	14	2	Paperwork submission process\n	When you do this, a new window will open.\n	1	f
391	14	2	Paperwork submission process\n	Simply drag and drop your files.\n	2	f
392	14	2	Paperwork submission process\n	After you send your work, you should check your email.\n	4	f
433	19	1	Hand in assignment	First, it is a good idea to check your report and correct mistakes.	0	t
434	19	1	Hand in assignment	The staff member will take your report and confirm that everything is complete.	4	f
435	19	1	Hand in assignment	When you are sure there are no mistakes left, print out your report.	1	f
436	19	1	Hand in assignment	Bring your assignment with the attached cover sheet to the front desk in the main hall.	3	f
437	19	1	Hand in assignment	Next, complete a cover sheet with your name and your student number, and attach it to your printed assignment.	2	f
438	19	2	Fire instructions	When you hear the alarm, leave your bags and belongings at the desk.	0	t
439	19	2	Fire instructions	When you reach the bottom of these stairs, leave the building through the front entrance.	3	f
440	19	2	Fire instructions	Through these doors, there are stairs leading you to the ground floor.	2	f
441	19	2	Fire instructions	Outside, gather on the grass and wait for further instructions.	4	f
442	19	2	Fire instructions	Next, walk calmly to the doors marked Emergency Exit.	1	f
303	11	1	Instructions for new students	The first step is to find out what you know about the problem.	0	t
304	11	1	Instructions for new students	You can also compare your results with experiments in the past.	3	f
305	11	1	Instructions for new students	Then, you need to perform experiments to see if these ideas are true or not.	2	f
306	11	1	Instructions for new students	The next one is to form a hypothesis or an idea based on your information.	1	f
307	11	1	Instructions for new students	In this way, you can add to your knowledge of the subject for future experiments.	4	f
308	11	2	Participate in a race.	Before you start to write your report, you should look at websites for the information you need.	0	t
309	11	2	Participate in a race.	After you make the corrections, send your report by email.	4	f
310	11	2	Participate in a race.	You should also include a list of books that you use for reference.	2	f
311	11	2	Participate in a race.	When you have finished your report, correct all the mistakes	3	f
312	11	2	Participate in a race.	Remember to save links to websites and include them in your report	1	f
343	12	1	Natural history center	The most important of these is the Natural history center.	0	t
344	12	1	Natural history center	The entrance of the center is on the town's main square.	1	f
345	12	1	Natural history center	As well as selling tickets, they can provide maps and useful tour information.	4	f
346	12	1	Natural history center	When you enter the building from the square, you will see a set of stairs to your left.	2	f
347	12	1	Natural history center	The ticket office is on the top of these stairs, the staff there are very helpful.	3	f
348	12	2	Traffic lights	They were out of order and the traffic moved very slowly.	0	t
349	12	2	Traffic lights	Fortunately, in the evening, the traffic lights were working again.	3	f
350	12	2	Traffic lights	As a result of these delays, many people were not able to get to work on time.	2	f
351	12	2	Traffic lights	This created long delays in the roads to the city's business district.	1	f
352	12	2	Traffic lights	Therefore, there were no further delays for people going back home.	4	f
393	16	1	A scientist’s life - Albert\n	As a child, he moved to a special school because he was so clever.\n	0	t
394	16	1	A scientist’s life - Albert\n	These were so advanced that he soon became famous all over the world.\n	2	f
395	16	1	A scientist’s life - Albert\n	Princeton University in the USA offered him a job because he was so famous.\n	4	f
396	16	1	A scientist’s life - Albert\n	His best friend in his new class was a girl named Lavime.\n	3	f
397	16	1	A scientist’s life - Albert\n	She later became his wife and helped him with his earliest scientific discoveries.\n	1	f
398	16	2	Conference hall\n	When you arrive at the conference hall, give your booking number.\n	0	t
399	16	2	Conference hall\n	Inside you will find a schedule of events and the information of the key speaker.\n	3	f
400	16	2	Conference hall\n	After he finishes, there will be time for questions.\n	1	f
401	16	2	Conference hall\n	A staff member will note this down and give you a welcome pack.\n	2	f
402	16	2	Conference hall\n	If you would like to attend his talk, it will take place in the main hall at midday.\n	4	f
465	22	1	Planting potato 	All you need is some earth, a big pot and some old potatoes.	0	t
466	22	1	Planting potato 	That colour means it is perfect for growing, then you pull a hole on earth and put it deep down.	2	f
467	22	1	Planting potato 	When it's done, put it in a sunny place and water it every day.	3	f
468	22	1	Planting potato 	An old potato has a little root, and it is a little green and it is not good for eating.	1	f
469	22	1	Planting potato 	This care will help the potato grow in a couple of weeks.	4	f
470	22	2	Driving process	You should arrive at the main office by 6.30 am and collect your keys.	0	t
471	22	2	Driving process	You must follow the route on the map to deliver the packages.	2	f
472	22	2	Driving process	In the office you can also collect a map of your route.	1	f
473	22	2	Driving process	You must return your keys to the office manager after you get back.	4	f
474	22	2	Driving process	When you have completed all delivery, return to the office.	3	f
403	17	1	Shang Hai	A. As a child, he moved to a special school because he was so clever.\n	0	t
404	17	1	Shang Hai	B. In the 1980s, she finally returned to China and still lives with her Shanghai husband, George Wang. 	4	f
405	17	1	Shang Hai	C. After she finished her school, she went to Wellesley College, a famous university in USA	2	f
406	17	1	Shang Hai	D. At that time, Shanghai is a city filled with many people from different countries	1	f
407	17	1	Shang Hai	E. However, she missed China, and applied for a job in Hong Kong, where she taught from 1959 to 1972, and learnt to speak Cantonese, the local language	3	f
408	17	2	My first car\n\n	A. I have just passed the test, and I am the proud owner of the driving license	0	t
409	17	2	My first car\n\n	B. We agreed on a price and when I handed over the money, he gave me the keys. 	4	f
410	17	2	My first car\n\n	C. However, I did not have a car and my parents would not let me drive theirs.	1	f
411	17	2	My first car\n\n	D. I called the number in that advert and arranged a meeting to meet the owner on the other side of the town.	3	f
412	17	2	My first car\n\n	E. So, when I saw an advertisement in the local newspaper for a cheap second hand car, I did not waste time.	2	f
475	23	1	Zinedine Zidane	As a child, he played for several teams close to his home in Marseille.	0	t
476	23	1	Zinedine Zidane	While he was in the club, he was seen as a talented player.	2	f
477	23	1	Zinedine Zidane	He then left home to join Cannes football Club in the south of France.	1	f
478	23	1	Zinedine Zidane	Since retiring, he has worked as a manager for a football club.	4	f
479	23	1	Zinedine Zidane	Later, he left France to advance his career in Italy and Spain, where he eventually stopped playing.	3	f
480	23	2	Milly Brook	As a child, she spent countless hours practicing her favorite sport every day.	0	t
481	23	2	Milly Brook	Because of this dedication and passion, she quickly improved her skills significantly.	1	f
482	23	2	Milly Brook	They invited her to join their team, recognizing her exceptional talent and commitment.	3	f
483	23	2	Milly Brook	A year later, after extensive training and dedication, she became a key player.	4	f
484	23	2	Milly Brook	The hard work and determination proved to be successful and rewarding.	2	f
\.


--
-- TOC entry 3507 (class 0 OID 16474)
-- Dependencies: 225
-- Data for Name: reading_part_3; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.reading_part_3 (question_id, exam_id, group_id, topic, question_text, correct_answer, person_a, person_b, person_c, person_d) FROM stdin;
316	20	1	TECHNOLOGY	Who uses technology to communicate with family?	?	I moved to a new country and it is challenging to stay in touch with relatives, but thanks to technology, I can now easily contact my family. I rely on technology a lot for this reason, and I believe many people nowadays depend on it too. It makes sense, and I have no issues with that. Technology has made staying connected much more convenient and accessible for all of us.	I work in finance and it is normal for me to use technology to update international banking information and I am an accountant. However, looking at the screen for too long makes my eyes hurt. Also, using my phone for extended periods before bedtime affects my sleep, so I avoid it after 9 jp.m. to ensure a good night's rest.	Our family uses technology a lot. My sister called mom even inside the house! Although my dad told us not to use the phone at night, I use it anyway. I find it convenient to watch movies and listen to music. I also use it to play games with friends. My friends always have the most updated games, which puts pressure on me to buy the latest as soon as I can. I don't want to lag behind them.	I am a professional painter, which is not traditionally connected to technology, but perhaps I will use it more in the future. I have a laptop at home. Whenever I use it, my daughter becomes really interested, so I have to keep it locked away. Although some of my friends are keen on letting children be exposed to technology, I think it would have an effect on their brain development. 
317	20	1	TECHNOLOGY	Who thinks children shouldn't use technology?	?	I moved to a new country and it is challenging to stay in touch with relatives, but thanks to technology, I can now easily contact my family. I rely on technology a lot for this reason, and I believe many people nowadays depend on it too. It makes sense, and I have no issues with that. Technology has made staying connected much more convenient and accessible for all of us.	I work in finance and it is normal for me to use technology to update international banking information and I am an accountant. However, looking at the screen for too long makes my eyes hurt. Also, using my phone for extended periods before bedtime affects my sleep, so I avoid it after 9 jp.m. to ensure a good night's rest.	Our family uses technology a lot. My sister called mom even inside the house! Although my dad told us not to use the phone at night, I use it anyway. I find it convenient to watch movies and listen to music. I also use it to play games with friends. My friends always have the most updated games, which puts pressure on me to buy the latest as soon as I can. I don't want to lag behind them.	I am a professional painter, which is not traditionally connected to technology, but perhaps I will use it more in the future. I have a laptop at home. Whenever I use it, my daughter becomes really interested, so I have to keep it locked away. Although some of my friends are keen on letting children be exposed to technology, I think it would have an effect on their brain development. 
318	20	1	TECHNOLOGY	Who advises against using technology before going to bed? 	?	I moved to a new country and it is challenging to stay in touch with relatives, but thanks to technology, I can now easily contact my family. I rely on technology a lot for this reason, and I believe many people nowadays depend on it too. It makes sense, and I have no issues with that. Technology has made staying connected much more convenient and accessible for all of us.	I work in finance and it is normal for me to use technology to update international banking information and I am an accountant. However, looking at the screen for too long makes my eyes hurt. Also, using my phone for extended periods before bedtime affects my sleep, so I avoid it after 9 jp.m. to ensure a good night's rest.	Our family uses technology a lot. My sister called mom even inside the house! Although my dad told us not to use the phone at night, I use it anyway. I find it convenient to watch movies and listen to music. I also use it to play games with friends. My friends always have the most updated games, which puts pressure on me to buy the latest as soon as I can. I don't want to lag behind them.	I am a professional painter, which is not traditionally connected to technology, but perhaps I will use it more in the future. I have a laptop at home. Whenever I use it, my daughter becomes really interested, so I have to keep it locked away. Although some of my friends are keen on letting children be exposed to technology, I think it would have an effect on their brain development. 
319	20	1	TECHNOLOGY	Who uses technology for entertainment?	?	I moved to a new country and it is challenging to stay in touch with relatives, but thanks to technology, I can now easily contact my family. I rely on technology a lot for this reason, and I believe many people nowadays depend on it too. It makes sense, and I have no issues with that. Technology has made staying connected much more convenient and accessible for all of us.	I work in finance and it is normal for me to use technology to update international banking information and I am an accountant. However, looking at the screen for too long makes my eyes hurt. Also, using my phone for extended periods before bedtime affects my sleep, so I avoid it after 9 jp.m. to ensure a good night's rest.	Our family uses technology a lot. My sister called mom even inside the house! Although my dad told us not to use the phone at night, I use it anyway. I find it convenient to watch movies and listen to music. I also use it to play games with friends. My friends always have the most updated games, which puts pressure on me to buy the latest as soon as I can. I don't want to lag behind them.	I am a professional painter, which is not traditionally connected to technology, but perhaps I will use it more in the future. I have a laptop at home. Whenever I use it, my daughter becomes really interested, so I have to keep it locked away. Although some of my friends are keen on letting children be exposed to technology, I think it would have an effect on their brain development. 
320	20	1	TECHNOLOGY	Who believes that people depend too much on technology?	?	I moved to a new country and it is challenging to stay in touch with relatives, but thanks to technology, I can now easily contact my family. I rely on technology a lot for this reason, and I believe many people nowadays depend on it too. It makes sense, and I have no issues with that. Technology has made staying connected much more convenient and accessible for all of us.	I work in finance and it is normal for me to use technology to update international banking information and I am an accountant. However, looking at the screen for too long makes my eyes hurt. Also, using my phone for extended periods before bedtime affects my sleep, so I avoid it after 9 jp.m. to ensure a good night's rest.	Our family uses technology a lot. My sister called mom even inside the house! Although my dad told us not to use the phone at night, I use it anyway. I find it convenient to watch movies and listen to music. I also use it to play games with friends. My friends always have the most updated games, which puts pressure on me to buy the latest as soon as I can. I don't want to lag behind them.	I am a professional painter, which is not traditionally connected to technology, but perhaps I will use it more in the future. I have a laptop at home. Whenever I use it, my daughter becomes really interested, so I have to keep it locked away. Although some of my friends are keen on letting children be exposed to technology, I think it would have an effect on their brain development. 
321	20	1	TECHNOLOGY	Who uses technology for work purposes?	?	I moved to a new country and it is challenging to stay in touch with relatives, but thanks to technology, I can now easily contact my family. I rely on technology a lot for this reason, and I believe many people nowadays depend on it too. It makes sense, and I have no issues with that. Technology has made staying connected much more convenient and accessible for all of us.	I work in finance and it is normal for me to use technology to update international banking information and I am an accountant. However, looking at the screen for too long makes my eyes hurt. Also, using my phone for extended periods before bedtime affects my sleep, so I avoid it after 9 jp.m. to ensure a good night's rest.	Our family uses technology a lot. My sister called mom even inside the house! Although my dad told us not to use the phone at night, I use it anyway. I find it convenient to watch movies and listen to music. I also use it to play games with friends. My friends always have the most updated games, which puts pressure on me to buy the latest as soon as I can. I don't want to lag behind them.	I am a professional painter, which is not traditionally connected to technology, but perhaps I will use it more in the future. I have a laptop at home. Whenever I use it, my daughter becomes really interested, so I have to keep it locked away. Although some of my friends are keen on letting children be exposed to technology, I think it would have an effect on their brain development. 
322	20	1	TECHNOLOGY	Who buys the latest technology products?	?	I moved to a new country and it is challenging to stay in touch with relatives, but thanks to technology, I can now easily contact my family. I rely on technology a lot for this reason, and I believe many people nowadays depend on it too. It makes sense, and I have no issues with that. Technology has made staying connected much more convenient and accessible for all of us.	I work in finance and it is normal for me to use technology to update international banking information and I am an accountant. However, looking at the screen for too long makes my eyes hurt. Also, using my phone for extended periods before bedtime affects my sleep, so I avoid it after 9 jp.m. to ensure a good night's rest.	Our family uses technology a lot. My sister called mom even inside the house! Although my dad told us not to use the phone at night, I use it anyway. I find it convenient to watch movies and listen to music. I also use it to play games with friends. My friends always have the most updated games, which puts pressure on me to buy the latest as soon as I can. I don't want to lag behind them.	I am a professional painter, which is not traditionally connected to technology, but perhaps I will use it more in the future. I have a laptop at home. Whenever I use it, my daughter becomes really interested, so I have to keep it locked away. Although some of my friends are keen on letting children be exposed to technology, I think it would have an effect on their brain development. 
323	21	1	MONEY	Relations with friends are different if you are wealthy	?	It is important to keep money in perspective: you need some, but don't need too much. Otherwise you'll spend your whole life chasing the Almighty dollar and that's not a healthy relationship to money that you want to have. Some people try to impress with how much money they have, but i see that as a character flaw. If you can help those less fortunate, do it, by all means but realize that just handing out money is usually not an effective way to improve their lives.	I think of money as a tool that helps you build your life. Like a tool you need to know how to use it. One of the problems with money is there are far more people who know how to use a saw or a hammer than there are who know how to use money. For instance most people equate wealth to what you have. If you have a big house and fancy car you feel rich.	Money is something that can buy you everything in the world today. However, easy money makes you lose the opportunity to feel the joy of getting that after you've worked hard enough to earn it. Money is something that everyone needs unanimously. It ironically causes us to be united in our concordant need for it. Money is something that cannot buy you true happiness but not having any of it doesn't give you that happiness either.	Money can buy most of the things but not all the things. When you don't have money, your supposed friends and relatives will not prefer to have you near them. However, if you have money, then they may feel jealous of you and find faults in you without any reason. Besides, having money has its limitations, you can buy expensive treatments, but not life. You can't buy respect, or admiration. However, money can help you to meet your day to day expenses.
324	21	1	MONEY	It is important to learn how you use your money. 	?	It is important to keep money in perspective: you need some, but don't need too much. Otherwise you'll spend your whole life chasing the Almighty dollar and that's not a healthy relationship to money that you want to have. Some people try to impress with how much money they have, but i see that as a character flaw. If you can help those less fortunate, do it, by all means but realize that just handing out money is usually not an effective way to improve their lives.	I think of money as a tool that helps you build your life. Like a tool you need to know how to use it. One of the problems with money is there are far more people who know how to use a saw or a hammer than there are who know how to use money. For instance most people equate wealth to what you have. If you have a big house and fancy car you feel rich.	Money is something that can buy you everything in the world today. However, easy money makes you lose the opportunity to feel the joy of getting that after you've worked hard enough to earn it. Money is something that everyone needs unanimously. It ironically causes us to be united in our concordant need for it. Money is something that cannot buy you true happiness but not having any of it doesn't give you that happiness either.	Money can buy most of the things but not all the things. When you don't have money, your supposed friends and relatives will not prefer to have you near them. However, if you have money, then they may feel jealous of you and find faults in you without any reason. Besides, having money has its limitations, you can buy expensive treatments, but not life. You can't buy respect, or admiration. However, money can help you to meet your day to day expenses.
325	21	1	MONEY	You should help people who need it. 	?	It is important to keep money in perspective: you need some, but don't need too much. Otherwise you'll spend your whole life chasing the Almighty dollar and that's not a healthy relationship to money that you want to have. Some people try to impress with how much money they have, but i see that as a character flaw. If you can help those less fortunate, do it, by all means but realize that just handing out money is usually not an effective way to improve their lives.	I think of money as a tool that helps you build your life. Like a tool you need to know how to use it. One of the problems with money is there are far more people who know how to use a saw or a hammer than there are who know how to use money. For instance most people equate wealth to what you have. If you have a big house and fancy car you feel rich.	Money is something that can buy you everything in the world today. However, easy money makes you lose the opportunity to feel the joy of getting that after you've worked hard enough to earn it. Money is something that everyone needs unanimously. It ironically causes us to be united in our concordant need for it. Money is something that cannot buy you true happiness but not having any of it doesn't give you that happiness either.	Money can buy most of the things but not all the things. When you don't have money, your supposed friends and relatives will not prefer to have you near them. However, if you have money, then they may feel jealous of you and find faults in you without any reason. Besides, having money has its limitations, you can buy expensive treatments, but not life. You can't buy respect, or admiration. However, money can help you to meet your day to day expenses.
326	21	1	MONEY	Money doesn't necessarily make you happy	?	It is important to keep money in perspective: you need some, but don't need too much. Otherwise you'll spend your whole life chasing the Almighty dollar and that's not a healthy relationship to money that you want to have. Some people try to impress with how much money they have, but i see that as a character flaw. If you can help those less fortunate, do it, by all means but realize that just handing out money is usually not an effective way to improve their lives.	I think of money as a tool that helps you build your life. Like a tool you need to know how to use it. One of the problems with money is there are far more people who know how to use a saw or a hammer than there are who know how to use money. For instance most people equate wealth to what you have. If you have a big house and fancy car you feel rich.	Money is something that can buy you everything in the world today. However, easy money makes you lose the opportunity to feel the joy of getting that after you've worked hard enough to earn it. Money is something that everyone needs unanimously. It ironically causes us to be united in our concordant need for it. Money is something that cannot buy you true happiness but not having any of it doesn't give you that happiness either.	Money can buy most of the things but not all the things. When you don't have money, your supposed friends and relatives will not prefer to have you near them. However, if you have money, then they may feel jealous of you and find faults in you without any reason. Besides, having money has its limitations, you can buy expensive treatments, but not life. You can't buy respect, or admiration. However, money can help you to meet your day to day expenses.
327	21	1	MONEY	Some people feel rich just because of their possessions. 	?	It is important to keep money in perspective: you need some, but don't need too much. Otherwise you'll spend your whole life chasing the Almighty dollar and that's not a healthy relationship to money that you want to have. Some people try to impress with how much money they have, but i see that as a character flaw. If you can help those less fortunate, do it, by all means but realize that just handing out money is usually not an effective way to improve their lives.	I think of money as a tool that helps you build your life. Like a tool you need to know how to use it. One of the problems with money is there are far more people who know how to use a saw or a hammer than there are who know how to use money. For instance most people equate wealth to what you have. If you have a big house and fancy car you feel rich.	Money is something that can buy you everything in the world today. However, easy money makes you lose the opportunity to feel the joy of getting that after you've worked hard enough to earn it. Money is something that everyone needs unanimously. It ironically causes us to be united in our concordant need for it. Money is something that cannot buy you true happiness but not having any of it doesn't give you that happiness either.	Money can buy most of the things but not all the things. When you don't have money, your supposed friends and relatives will not prefer to have you near them. However, if you have money, then they may feel jealous of you and find faults in you without any reason. Besides, having money has its limitations, you can buy expensive treatments, but not life. You can't buy respect, or admiration. However, money can help you to meet your day to day expenses.
328	21	1	MONEY	There are things that money can't buy. 	?	It is important to keep money in perspective: you need some, but don't need too much. Otherwise you'll spend your whole life chasing the Almighty dollar and that's not a healthy relationship to money that you want to have. Some people try to impress with how much money they have, but i see that as a character flaw. If you can help those less fortunate, do it, by all means but realize that just handing out money is usually not an effective way to improve their lives.	I think of money as a tool that helps you build your life. Like a tool you need to know how to use it. One of the problems with money is there are far more people who know how to use a saw or a hammer than there are who know how to use money. For instance most people equate wealth to what you have. If you have a big house and fancy car you feel rich.	Money is something that can buy you everything in the world today. However, easy money makes you lose the opportunity to feel the joy of getting that after you've worked hard enough to earn it. Money is something that everyone needs unanimously. It ironically causes us to be united in our concordant need for it. Money is something that cannot buy you true happiness but not having any of it doesn't give you that happiness either.	Money can buy most of the things but not all the things. When you don't have money, your supposed friends and relatives will not prefer to have you near them. However, if you have money, then they may feel jealous of you and find faults in you without any reason. Besides, having money has its limitations, you can buy expensive treatments, but not life. You can't buy respect, or admiration. However, money can help you to meet your day to day expenses.
329	21	1	MONEY	The only objective of some people's lives is money. 	?	It is important to keep money in perspective: you need some, but don't need too much. Otherwise you'll spend your whole life chasing the Almighty dollar and that's not a healthy relationship to money that you want to have. Some people try to impress with how much money they have, but i see that as a character flaw. If you can help those less fortunate, do it, by all means but realize that just handing out money is usually not an effective way to improve their lives.	I think of money as a tool that helps you build your life. Like a tool you need to know how to use it. One of the problems with money is there are far more people who know how to use a saw or a hammer than there are who know how to use money. For instance most people equate wealth to what you have. If you have a big house and fancy car you feel rich.	Money is something that can buy you everything in the world today. However, easy money makes you lose the opportunity to feel the joy of getting that after you've worked hard enough to earn it. Money is something that everyone needs unanimously. It ironically causes us to be united in our concordant need for it. Money is something that cannot buy you true happiness but not having any of it doesn't give you that happiness either.	Money can buy most of the things but not all the things. When you don't have money, your supposed friends and relatives will not prefer to have you near them. However, if you have money, then they may feel jealous of you and find faults in you without any reason. Besides, having money has its limitations, you can buy expensive treatments, but not life. You can't buy respect, or admiration. However, money can help you to meet your day to day expenses.
337	22	1	SPORTS	1. work out with friends is a good idea	?	Exercising with friends is a fantastic idea, don't you think? It adds a fun element to the workout routine. It's important to fuel our bodies properly, though. After a good workout, I always make sure to have a nutritious meal to replenish energy and support muscle recovery. 	Establishing a consistent workout routine has really helped me stay on track with my fitness goals. It's amazing how much more I can accomplish when I have a structured plan in place. Plus, it keeps me accountable and ensures I make time for physical activity every day.	Age is just a number when it comes to exercise. Whether you're young or old, staying active is crucial for maintaining overall health and vitality. While competitions can be motivating for some, they're not necessarily suitable for everyone. It's important to find activities that are enjoyable and sustainable for each individual.	Experiencing pain during exercise isn't necessary and it's a sign that something may be wrong. It's important to listen to our bodies and seek expert advice when needed, whether it's from a trainer, physical therapist, or medical professional. Taking care of ourselves properly ensures we can continue to enjoy physical activity without risking injury.
338	22	1	SPORTS	2. a proper meal is important	?	Exercising with friends is a fantastic idea, don't you think? It adds a fun element to the workout routine. It's important to fuel our bodies properly, though. After a good workout, I always make sure to have a nutritious meal to replenish energy and support muscle recovery. 	Establishing a consistent workout routine has really helped me stay on track with my fitness goals. It's amazing how much more I can accomplish when I have a structured plan in place. Plus, it keeps me accountable and ensures I make time for physical activity every day.	Age is just a number when it comes to exercise. Whether you're young or old, staying active is crucial for maintaining overall health and vitality. While competitions can be motivating for some, they're not necessarily suitable for everyone. It's important to find activities that are enjoyable and sustainable for each individual.	Experiencing pain during exercise isn't necessary and it's a sign that something may be wrong. It's important to listen to our bodies and seek expert advice when needed, whether it's from a trainer, physical therapist, or medical professional. Taking care of ourselves properly ensures we can continue to enjoy physical activity without risking injury.
339	22	1	SPORTS	3. a routine can help us do more sport	?	Exercising with friends is a fantastic idea, don't you think? It adds a fun element to the workout routine. It's important to fuel our bodies properly, though. After a good workout, I always make sure to have a nutritious meal to replenish energy and support muscle recovery. 	Establishing a consistent workout routine has really helped me stay on track with my fitness goals. It's amazing how much more I can accomplish when I have a structured plan in place. Plus, it keeps me accountable and ensures I make time for physical activity every day.	Age is just a number when it comes to exercise. Whether you're young or old, staying active is crucial for maintaining overall health and vitality. While competitions can be motivating for some, they're not necessarily suitable for everyone. It's important to find activities that are enjoyable and sustainable for each individual.	Experiencing pain during exercise isn't necessary and it's a sign that something may be wrong. It's important to listen to our bodies and seek expert advice when needed, whether it's from a trainer, physical therapist, or medical professional. Taking care of ourselves properly ensures we can continue to enjoy physical activity without risking injury.
340	22	1	SPORTS	4. exercise is for both the young and the elderly	?	Exercising with friends is a fantastic idea, don't you think? It adds a fun element to the workout routine. It's important to fuel our bodies properly, though. After a good workout, I always make sure to have a nutritious meal to replenish energy and support muscle recovery. 	Establishing a consistent workout routine has really helped me stay on track with my fitness goals. It's amazing how much more I can accomplish when I have a structured plan in place. Plus, it keeps me accountable and ensures I make time for physical activity every day.	Age is just a number when it comes to exercise. Whether you're young or old, staying active is crucial for maintaining overall health and vitality. While competitions can be motivating for some, they're not necessarily suitable for everyone. It's important to find activities that are enjoyable and sustainable for each individual.	Experiencing pain during exercise isn't necessary and it's a sign that something may be wrong. It's important to listen to our bodies and seek expert advice when needed, whether it's from a trainer, physical therapist, or medical professional. Taking care of ourselves properly ensures we can continue to enjoy physical activity without risking injury.
341	22	1	SPORTS	5. competitions are not useful for everybody	?	Exercising with friends is a fantastic idea, don't you think? It adds a fun element to the workout routine. It's important to fuel our bodies properly, though. After a good workout, I always make sure to have a nutritious meal to replenish energy and support muscle recovery. 	Establishing a consistent workout routine has really helped me stay on track with my fitness goals. It's amazing how much more I can accomplish when I have a structured plan in place. Plus, it keeps me accountable and ensures I make time for physical activity every day.	Age is just a number when it comes to exercise. Whether you're young or old, staying active is crucial for maintaining overall health and vitality. While competitions can be motivating for some, they're not necessarily suitable for everyone. It's important to find activities that are enjoyable and sustainable for each individual.	Experiencing pain during exercise isn't necessary and it's a sign that something may be wrong. It's important to listen to our bodies and seek expert advice when needed, whether it's from a trainer, physical therapist, or medical professional. Taking care of ourselves properly ensures we can continue to enjoy physical activity without risking injury.
342	22	1	SPORTS	6. experience pain is not necessary	?	Exercising with friends is a fantastic idea, don't you think? It adds a fun element to the workout routine. It's important to fuel our bodies properly, though. After a good workout, I always make sure to have a nutritious meal to replenish energy and support muscle recovery. 	Establishing a consistent workout routine has really helped me stay on track with my fitness goals. It's amazing how much more I can accomplish when I have a structured plan in place. Plus, it keeps me accountable and ensures I make time for physical activity every day.	Age is just a number when it comes to exercise. Whether you're young or old, staying active is crucial for maintaining overall health and vitality. While competitions can be motivating for some, they're not necessarily suitable for everyone. It's important to find activities that are enjoyable and sustainable for each individual.	Experiencing pain during exercise isn't necessary and it's a sign that something may be wrong. It's important to listen to our bodies and seek expert advice when needed, whether it's from a trainer, physical therapist, or medical professional. Taking care of ourselves properly ensures we can continue to enjoy physical activity without risking injury.
343	22	1	SPORTS	7. at times we seek expert advice	?	Exercising with friends is a fantastic idea, don't you think? It adds a fun element to the workout routine. It's important to fuel our bodies properly, though. After a good workout, I always make sure to have a nutritious meal to replenish energy and support muscle recovery. 	Establishing a consistent workout routine has really helped me stay on track with my fitness goals. It's amazing how much more I can accomplish when I have a structured plan in place. Plus, it keeps me accountable and ensures I make time for physical activity every day.	Age is just a number when it comes to exercise. Whether you're young or old, staying active is crucial for maintaining overall health and vitality. While competitions can be motivating for some, they're not necessarily suitable for everyone. It's important to find activities that are enjoyable and sustainable for each individual.	Experiencing pain during exercise isn't necessary and it's a sign that something may be wrong. It's important to listen to our bodies and seek expert advice when needed, whether it's from a trainer, physical therapist, or medical professional. Taking care of ourselves properly ensures we can continue to enjoy physical activity without risking injury.
246	12	1	READING BOOKS.	1. plans their reading schedule\n	?	 I have to read a lot for my job, and I find that reading factual books is often boring. The material tends to be dry and lacks excitement. After a long day at work, I usually feel too exhausted to read much, which means I have limited time for reading anything enjoyable.	My wife is always complaining that she can't read many books. I don't have that problem because I plan the reading schedule carefully. I set aside specific times each week for reading, which helps me stay on track. This way, I can enjoy my books while she finds it challenging to keep up.	When I was a child, I struggled to finish one book at a time. It felt overwhelming to stay focused on a single story. However, now that I'm older, I enjoy exploring many genres and even read multiple books at once. I have a long list of books I want to read in the future, which keeps me excited.	I keep a novel on the bedside table because I want to read before sleeping. However, I often find myself getting sleepy as soon as I start reading, which makes it difficult to concentrate. As a result, it has taken me several months to finish this book, and I still haven't completed it.
247	12	1	READING BOOKS.	2. reads more than another family member\n	?	 I have to read a lot for my job, and I find that reading factual books is often boring. The material tends to be dry and lacks excitement. After a long day at work, I usually feel too exhausted to read much, which means I have limited time for reading anything enjoyable.	My wife is always complaining that she can't read many books. I don't have that problem because I plan the reading schedule carefully. I set aside specific times each week for reading, which helps me stay on track. This way, I can enjoy my books while she finds it challenging to keep up.	When I was a child, I struggled to finish one book at a time. It felt overwhelming to stay focused on a single story. However, now that I'm older, I enjoy exploring many genres and even read multiple books at once. I have a long list of books I want to read in the future, which keeps me excited.	I keep a novel on the bedside table because I want to read before sleeping. However, I often find myself getting sleepy as soon as I start reading, which makes it difficult to concentrate. As a result, it has taken me several months to finish this book, and I still haven't completed it.
248	12	1	READING BOOKS.	3. reads many books at once\n	?	 I have to read a lot for my job, and I find that reading factual books is often boring. The material tends to be dry and lacks excitement. After a long day at work, I usually feel too exhausted to read much, which means I have limited time for reading anything enjoyable.	My wife is always complaining that she can't read many books. I don't have that problem because I plan the reading schedule carefully. I set aside specific times each week for reading, which helps me stay on track. This way, I can enjoy my books while she finds it challenging to keep up.	When I was a child, I struggled to finish one book at a time. It felt overwhelming to stay focused on a single story. However, now that I'm older, I enjoy exploring many genres and even read multiple books at once. I have a long list of books I want to read in the future, which keeps me excited.	I keep a novel on the bedside table because I want to read before sleeping. However, I often find myself getting sleepy as soon as I start reading, which makes it difficult to concentrate. As a result, it has taken me several months to finish this book, and I still haven't completed it.
249	12	1	READING BOOKS.	4. wants to read more books\n	?	 I have to read a lot for my job, and I find that reading factual books is often boring. The material tends to be dry and lacks excitement. After a long day at work, I usually feel too exhausted to read much, which means I have limited time for reading anything enjoyable.	My wife is always complaining that she can't read many books. I don't have that problem because I plan the reading schedule carefully. I set aside specific times each week for reading, which helps me stay on track. This way, I can enjoy my books while she finds it challenging to keep up.	When I was a child, I struggled to finish one book at a time. It felt overwhelming to stay focused on a single story. However, now that I'm older, I enjoy exploring many genres and even read multiple books at once. I have a long list of books I want to read in the future, which keeps me excited.	I keep a novel on the bedside table because I want to read before sleeping. However, I often find myself getting sleepy as soon as I start reading, which makes it difficult to concentrate. As a result, it has taken me several months to finish this book, and I still haven't completed it.
250	12	1	READING BOOKS.	5. is having difficulty in fishing a book\n	?	 I have to read a lot for my job, and I find that reading factual books is often boring. The material tends to be dry and lacks excitement. After a long day at work, I usually feel too exhausted to read much, which means I have limited time for reading anything enjoyable.	My wife is always complaining that she can't read many books. I don't have that problem because I plan the reading schedule carefully. I set aside specific times each week for reading, which helps me stay on track. This way, I can enjoy my books while she finds it challenging to keep up.	When I was a child, I struggled to finish one book at a time. It felt overwhelming to stay focused on a single story. However, now that I'm older, I enjoy exploring many genres and even read multiple books at once. I have a long list of books I want to read in the future, which keeps me excited.	I keep a novel on the bedside table because I want to read before sleeping. However, I often find myself getting sleepy as soon as I start reading, which makes it difficult to concentrate. As a result, it has taken me several months to finish this book, and I still haven't completed it.
251	12	1	READING BOOKS.	6. thinks that factual books are boring\n	?	 I have to read a lot for my job, and I find that reading factual books is often boring. The material tends to be dry and lacks excitement. After a long day at work, I usually feel too exhausted to read much, which means I have limited time for reading anything enjoyable.	My wife is always complaining that she can't read many books. I don't have that problem because I plan the reading schedule carefully. I set aside specific times each week for reading, which helps me stay on track. This way, I can enjoy my books while she finds it challenging to keep up.	When I was a child, I struggled to finish one book at a time. It felt overwhelming to stay focused on a single story. However, now that I'm older, I enjoy exploring many genres and even read multiple books at once. I have a long list of books I want to read in the future, which keeps me excited.	I keep a novel on the bedside table because I want to read before sleeping. However, I often find myself getting sleepy as soon as I start reading, which makes it difficult to concentrate. As a result, it has taken me several months to finish this book, and I still haven't completed it.
252	12	1	READING BOOKS.	7. has limited time to read books \n	?	 I have to read a lot for my job, and I find that reading factual books is often boring. The material tends to be dry and lacks excitement. After a long day at work, I usually feel too exhausted to read much, which means I have limited time for reading anything enjoyable.	My wife is always complaining that she can't read many books. I don't have that problem because I plan the reading schedule carefully. I set aside specific times each week for reading, which helps me stay on track. This way, I can enjoy my books while she finds it challenging to keep up.	When I was a child, I struggled to finish one book at a time. It felt overwhelming to stay focused on a single story. However, now that I'm older, I enjoy exploring many genres and even read multiple books at once. I have a long list of books I want to read in the future, which keeps me excited.	I keep a novel on the bedside table because I want to read before sleeping. However, I often find myself getting sleepy as soon as I start reading, which makes it difficult to concentrate. As a result, it has taken me several months to finish this book, and I still haven't completed it.
311	19	1	GOING ON HOLIDAY	3. holiday requires good weather	?	I have a limited budget for holidays because I am a student, so I usually choose to travel nearby or to places within the country. Because of this, I haven't had the opportunity to travel abroad yet. I'm working on earning more, and hopefully, in the future, I'll be able to explore other countries. That will be my first time traveling overseas.	I once went on a hiking holiday, and it was a disaster. The weather was terrible, and I wasn't as prepared as I thought. I used to enjoy walking a lot, going on trails and exploring nature whenever I had the chance. However, now that I'm retired, my preferences have changed. I find more comfort in staying at home, reading, or spending time with family.	Before I go on holiday, I always get a guidebook so I won't miss out on any important places. I find beach trips boring and always avoid them. Instead, I prefer researching tourist attractions ahead of time and visiting those interesting spots. Exploring new places and learning about their history and culture is what makes travel exciting for me.	I want to relax when I'm on holiday, and I disagree with those who say going to the beach is boring. Last year, a friend invited me on a hiking trip, but I declined. However, my perspective has changed, and now I'm planning to go hiking in the near future. This time, I'll closely follow the weather to ensure it doesn't spoil the trip.
312	19	1	GOING ON HOLIDAY	4. want to go mountaineering trip	?	I have a limited budget for holidays because I am a student, so I usually choose to travel nearby or to places within the country. Because of this, I haven't had the opportunity to travel abroad yet. I'm working on earning more, and hopefully, in the future, I'll be able to explore other countries. That will be my first time traveling overseas.	I once went on a hiking holiday, and it was a disaster. The weather was terrible, and I wasn't as prepared as I thought. I used to enjoy walking a lot, going on trails and exploring nature whenever I had the chance. However, now that I'm retired, my preferences have changed. I find more comfort in staying at home, reading, or spending time with family.	Before I go on holiday, I always get a guidebook so I won't miss out on any important places. I find beach trips boring and always avoid them. Instead, I prefer researching tourist attractions ahead of time and visiting those interesting spots. Exploring new places and learning about their history and culture is what makes travel exciting for me.	I want to relax when I'm on holiday, and I disagree with those who say going to the beach is boring. Last year, a friend invited me on a hiking trip, but I declined. However, my perspective has changed, and now I'm planning to go hiking in the near future. This time, I'll closely follow the weather to ensure it doesn't spoil the trip.
344	23	1	WATCHING A MOVIE	1. saw the film previously	?	Person A: A friend recommended the film because she had read the novel. I thought it was excellent, and I was captivated by the plot throughout, even though it was quite lengthy. All of the actors were outstanding, and the scenes where the zombies were finally defeated were amazing. The only thing I didn't like was my choice of viewing location. I should have gone out - it would Kave been much better on the big screen.\n	Person B: This was a sequel, and I hadn't seen the prior film, so I have to admit I felt completely lost. I'm pleased I had company. Luckily, my friend was able to explain who the characters were. There were some aspects I liked - the special effects, for example, were impressive, and the soundtrack was lovely. I would definitely recommend it to people who enjoy feeling scared, but personally, films like this don't frighten me. I think I'll stick to romantic movies in the future.\n	Person C: Unfortunately, it wasn't as good as l expected. The written version was terrifying but also thrilling. However, I ended up feeling bored while watching the film. The acting was rather uninspiring, and two and a half hours was excessive. I reckon the story could have been told in half the time. It was definitely better on the page than on the screen. Furthermore, cinema tickets are so costly these days. To be honest, I wish I hadn't wasted my money!\n	Person D: This was actually my second time watching it, but even though I knew what to expect, I still felt scared whenever a zombie attack happened. The direction really makes it feel like you are right there in the room with the characters. Being familiar with the film didn't make it easier! I was so relieved when my friend called after I got home so that I could chat about ordinary things and forget about it. Otherwise, I might have had nightmares!\n
345	23	1	WATCHING A MOVIE	2. found the film scary	?	Person A: A friend recommended the film because she had read the novel. I thought it was excellent, and I was captivated by the plot throughout, even though it was quite lengthy. All of the actors were outstanding, and the scenes where the zombies were finally defeated were amazing. The only thing I didn't like was my choice of viewing location. I should have gone out - it would Kave been much better on the big screen.\n	Person B: This was a sequel, and I hadn't seen the prior film, so I have to admit I felt completely lost. I'm pleased I had company. Luckily, my friend was able to explain who the characters were. There were some aspects I liked - the special effects, for example, were impressive, and the soundtrack was lovely. I would definitely recommend it to people who enjoy feeling scared, but personally, films like this don't frighten me. I think I'll stick to romantic movies in the future.\n	Person C: Unfortunately, it wasn't as good as l expected. The written version was terrifying but also thrilling. However, I ended up feeling bored while watching the film. The acting was rather uninspiring, and two and a half hours was excessive. I reckon the story could have been told in half the time. It was definitely better on the page than on the screen. Furthermore, cinema tickets are so costly these days. To be honest, I wish I hadn't wasted my money!\n	Person D: This was actually my second time watching it, but even though I knew what to expect, I still felt scared whenever a zombie attack happened. The direction really makes it feel like you are right there in the room with the characters. Being familiar with the film didn't make it easier! I was so relieved when my friend called after I got home so that I could chat about ordinary things and forget about it. Otherwise, I might have had nightmares!\n
346	23	1	WATCHING A MOVIE	3. saw the film at home\n	?	Person A: A friend recommended the film because she had read the novel. I thought it was excellent, and I was captivated by the plot throughout, even though it was quite lengthy. All of the actors were outstanding, and the scenes where the zombies were finally defeated were amazing. The only thing I didn't like was my choice of viewing location. I should have gone out - it would Kave been much better on the big screen.\n	Person B: This was a sequel, and I hadn't seen the prior film, so I have to admit I felt completely lost. I'm pleased I had company. Luckily, my friend was able to explain who the characters were. There were some aspects I liked - the special effects, for example, were impressive, and the soundtrack was lovely. I would definitely recommend it to people who enjoy feeling scared, but personally, films like this don't frighten me. I think I'll stick to romantic movies in the future.\n	Person C: Unfortunately, it wasn't as good as l expected. The written version was terrifying but also thrilling. However, I ended up feeling bored while watching the film. The acting was rather uninspiring, and two and a half hours was excessive. I reckon the story could have been told in half the time. It was definitely better on the page than on the screen. Furthermore, cinema tickets are so costly these days. To be honest, I wish I hadn't wasted my money!\n	Person D: This was actually my second time watching it, but even though I knew what to expect, I still felt scared whenever a zombie attack happened. The direction really makes it feel like you are right there in the room with the characters. Being familiar with the film didn't make it easier! I was so relieved when my friend called after I got home so that I could chat about ordinary things and forget about it. Otherwise, I might have had nightmares!\n
347	23	1	WATCHING A MOVIE	4. enjoyed the story of the film\n	?	Person A: A friend recommended the film because she had read the novel. I thought it was excellent, and I was captivated by the plot throughout, even though it was quite lengthy. All of the actors were outstanding, and the scenes where the zombies were finally defeated were amazing. The only thing I didn't like was my choice of viewing location. I should have gone out - it would Kave been much better on the big screen.\n	Person B: This was a sequel, and I hadn't seen the prior film, so I have to admit I felt completely lost. I'm pleased I had company. Luckily, my friend was able to explain who the characters were. There were some aspects I liked - the special effects, for example, were impressive, and the soundtrack was lovely. I would definitely recommend it to people who enjoy feeling scared, but personally, films like this don't frighten me. I think I'll stick to romantic movies in the future.\n	Person C: Unfortunately, it wasn't as good as l expected. The written version was terrifying but also thrilling. However, I ended up feeling bored while watching the film. The acting was rather uninspiring, and two and a half hours was excessive. I reckon the story could have been told in half the time. It was definitely better on the page than on the screen. Furthermore, cinema tickets are so costly these days. To be honest, I wish I hadn't wasted my money!\n	Person D: This was actually my second time watching it, but even though I knew what to expect, I still felt scared whenever a zombie attack happened. The direction really makes it feel like you are right there in the room with the characters. Being familiar with the film didn't make it easier! I was so relieved when my friend called after I got home so that I could chat about ordinary things and forget about it. Otherwise, I might have had nightmares!\n
348	23	1	WATCHING A MOVIE	5. saw the movies with friends	?	Person A: A friend recommended the film because she had read the novel. I thought it was excellent, and I was captivated by the plot throughout, even though it was quite lengthy. All of the actors were outstanding, and the scenes where the zombies were finally defeated were amazing. The only thing I didn't like was my choice of viewing location. I should have gone out - it would Kave been much better on the big screen.\n	Person B: This was a sequel, and I hadn't seen the prior film, so I have to admit I felt completely lost. I'm pleased I had company. Luckily, my friend was able to explain who the characters were. There were some aspects I liked - the special effects, for example, were impressive, and the soundtrack was lovely. I would definitely recommend it to people who enjoy feeling scared, but personally, films like this don't frighten me. I think I'll stick to romantic movies in the future.\n	Person C: Unfortunately, it wasn't as good as l expected. The written version was terrifying but also thrilling. However, I ended up feeling bored while watching the film. The acting was rather uninspiring, and two and a half hours was excessive. I reckon the story could have been told in half the time. It was definitely better on the page than on the screen. Furthermore, cinema tickets are so costly these days. To be honest, I wish I hadn't wasted my money!\n	Person D: This was actually my second time watching it, but even though I knew what to expect, I still felt scared whenever a zombie attack happened. The direction really makes it feel like you are right there in the room with the characters. Being familiar with the film didn't make it easier! I was so relieved when my friend called after I got home so that I could chat about ordinary things and forget about it. Otherwise, I might have had nightmares!\n
313	19	1	GOING ON HOLIDAY	5. have never been abroad	?	I have a limited budget for holidays because I am a student, so I usually choose to travel nearby or to places within the country. Because of this, I haven't had the opportunity to travel abroad yet. I'm working on earning more, and hopefully, in the future, I'll be able to explore other countries. That will be my first time traveling overseas.	I once went on a hiking holiday, and it was a disaster. The weather was terrible, and I wasn't as prepared as I thought. I used to enjoy walking a lot, going on trails and exploring nature whenever I had the chance. However, now that I'm retired, my preferences have changed. I find more comfort in staying at home, reading, or spending time with family.	Before I go on holiday, I always get a guidebook so I won't miss out on any important places. I find beach trips boring and always avoid them. Instead, I prefer researching tourist attractions ahead of time and visiting those interesting spots. Exploring new places and learning about their history and culture is what makes travel exciting for me.	I want to relax when I'm on holiday, and I disagree with those who say going to the beach is boring. Last year, a friend invited me on a hiking trip, but I declined. However, my perspective has changed, and now I'm planning to go hiking in the near future. This time, I'll closely follow the weather to ensure it doesn't spoil the trip.
314	19	1	GOING ON HOLIDAY	6. prefer to stay at home	?	I have a limited budget for holidays because I am a student, so I usually choose to travel nearby or to places within the country. Because of this, I haven't had the opportunity to travel abroad yet. I'm working on earning more, and hopefully, in the future, I'll be able to explore other countries. That will be my first time traveling overseas.	I once went on a hiking holiday, and it was a disaster. The weather was terrible, and I wasn't as prepared as I thought. I used to enjoy walking a lot, going on trails and exploring nature whenever I had the chance. However, now that I'm retired, my preferences have changed. I find more comfort in staying at home, reading, or spending time with family.	Before I go on holiday, I always get a guidebook so I won't miss out on any important places. I find beach trips boring and always avoid them. Instead, I prefer researching tourist attractions ahead of time and visiting those interesting spots. Exploring new places and learning about their history and culture is what makes travel exciting for me.	I want to relax when I'm on holiday, and I disagree with those who say going to the beach is boring. Last year, a friend invited me on a hiking trip, but I declined. However, my perspective has changed, and now I'm planning to go hiking in the near future. This time, I'll closely follow the weather to ensure it doesn't spoil the trip.
315	19	1	GOING ON HOLIDAY	7. like going walking	?	I have a limited budget for holidays because I am a student, so I usually choose to travel nearby or to places within the country. Because of this, I haven't had the opportunity to travel abroad yet. I'm working on earning more, and hopefully, in the future, I'll be able to explore other countries. That will be my first time traveling overseas.	I once went on a hiking holiday, and it was a disaster. The weather was terrible, and I wasn't as prepared as I thought. I used to enjoy walking a lot, going on trails and exploring nature whenever I had the chance. However, now that I'm retired, my preferences have changed. I find more comfort in staying at home, reading, or spending time with family.	Before I go on holiday, I always get a guidebook so I won't miss out on any important places. I find beach trips boring and always avoid them. Instead, I prefer researching tourist attractions ahead of time and visiting those interesting spots. Exploring new places and learning about their history and culture is what makes travel exciting for me.	I want to relax when I'm on holiday, and I disagree with those who say going to the beach is boring. Last year, a friend invited me on a hiking trip, but I declined. However, my perspective has changed, and now I'm planning to go hiking in the near future. This time, I'll closely follow the weather to ensure it doesn't spoil the trip.
260	13	1	WATCHING TELEVISION.	1. watch TV instead of studying\n	?	A. In my house, the TV is always on, and I watch whatever is playing because it's my way of staying entertained. However, sometimes I come across a really interesting series, and I can't stop constantly keeping up with it. That's how I entertain myself every day. However, I'm also keen on staying updated with the latest news about not only movies but also music.\n	B. I was never good at school because my grades were always low. However, I can remember a lot of practical things from watching TV. For me, it's a great way to expand my understanding of the world, and I believe it will be more useful when I graduate than the dry, theoretical knowledge we learn in school.\n	C. I don't watch television much lately because I find most reality shows to be pretty stupid. I realized they're all scripted, and the actors just follow a set plan. Once I learned that, I stopped watching those kinds of shows altogether. I switched to watching football instead, but my favorite team keeps losing, so I lost interest in that too.\n	D. I probably spend far too long just watching the series "Friends." The characters are so funny, and I find myself laughing out loud in every episode. I've been watching it for three weeks now, and I still can't wait for the next episode. Watching it for so long has actually helped me improve my English speaking skills without having to sit through boring lessons in class.\n
261	13	1	WATCHING TELEVISION.	2. like TV programs which continue over several weeks\n	?	A. In my house, the TV is always on, and I watch whatever is playing because it's my way of staying entertained. However, sometimes I come across a really interesting series, and I can't stop constantly keeping up with it. That's how I entertain myself every day. However, I'm also keen on staying updated with the latest news about not only movies but also music.\n	B. I was never good at school because my grades were always low. However, I can remember a lot of practical things from watching TV. For me, it's a great way to expand my understanding of the world, and I believe it will be more useful when I graduate than the dry, theoretical knowledge we learn in school.\n	C. I don't watch television much lately because I find most reality shows to be pretty stupid. I realized they're all scripted, and the actors just follow a set plan. Once I learned that, I stopped watching those kinds of shows altogether. I switched to watching football instead, but my favorite team keeps losing, so I lost interest in that too.\n	D. I probably spend far too long just watching the series "Friends." The characters are so funny, and I find myself laughing out loud in every episode. I've been watching it for three weeks now, and I still can't wait for the next episode. Watching it for so long has actually helped me improve my English speaking skills without having to sit through boring lessons in class.\n
262	13	1	WATCHING TELEVISION.	3. avoid watching reality TV programs\n	?	A. In my house, the TV is always on, and I watch whatever is playing because it's my way of staying entertained. However, sometimes I come across a really interesting series, and I can't stop constantly keeping up with it. That's how I entertain myself every day. However, I'm also keen on staying updated with the latest news about not only movies but also music.\n	B. I was never good at school because my grades were always low. However, I can remember a lot of practical things from watching TV. For me, it's a great way to expand my understanding of the world, and I believe it will be more useful when I graduate than the dry, theoretical knowledge we learn in school.\n	C. I don't watch television much lately because I find most reality shows to be pretty stupid. I realized they're all scripted, and the actors just follow a set plan. Once I learned that, I stopped watching those kinds of shows altogether. I switched to watching football instead, but my favorite team keeps losing, so I lost interest in that too.\n	D. I probably spend far too long just watching the series "Friends." The characters are so funny, and I find myself laughing out loud in every episode. I've been watching it for three weeks now, and I still can't wait for the next episode. Watching it for so long has actually helped me improve my English speaking skills without having to sit through boring lessons in class.\n
263	13	1	WATCHING TELEVISION.	4. lost interest in watching football on TV\n	?	A. In my house, the TV is always on, and I watch whatever is playing because it's my way of staying entertained. However, sometimes I come across a really interesting series, and I can't stop constantly keeping up with it. That's how I entertain myself every day. However, I'm also keen on staying updated with the latest news about not only movies but also music.\n	B. I was never good at school because my grades were always low. However, I can remember a lot of practical things from watching TV. For me, it's a great way to expand my understanding of the world, and I believe it will be more useful when I graduate than the dry, theoretical knowledge we learn in school.\n	C. I don't watch television much lately because I find most reality shows to be pretty stupid. I realized they're all scripted, and the actors just follow a set plan. Once I learned that, I stopped watching those kinds of shows altogether. I switched to watching football instead, but my favorite team keeps losing, so I lost interest in that too.\n	D. I probably spend far too long just watching the series "Friends." The characters are so funny, and I find myself laughing out loud in every episode. I've been watching it for three weeks now, and I still can't wait for the next episode. Watching it for so long has actually helped me improve my English speaking skills without having to sit through boring lessons in class.\n
264	13	1	WATCHING TELEVISION.	5. get a lot of knowledge by watching TV\n	?	A. In my house, the TV is always on, and I watch whatever is playing because it's my way of staying entertained. However, sometimes I come across a really interesting series, and I can't stop constantly keeping up with it. That's how I entertain myself every day. However, I'm also keen on staying updated with the latest news about not only movies but also music.\n	B. I was never good at school because my grades were always low. However, I can remember a lot of practical things from watching TV. For me, it's a great way to expand my understanding of the world, and I believe it will be more useful when I graduate than the dry, theoretical knowledge we learn in school.\n	C. I don't watch television much lately because I find most reality shows to be pretty stupid. I realized they're all scripted, and the actors just follow a set plan. Once I learned that, I stopped watching those kinds of shows altogether. I switched to watching football instead, but my favorite team keeps losing, so I lost interest in that too.\n	D. I probably spend far too long just watching the series "Friends." The characters are so funny, and I find myself laughing out loud in every episode. I've been watching it for three weeks now, and I still can't wait for the next episode. Watching it for so long has actually helped me improve my English speaking skills without having to sit through boring lessons in class.\n
265	13	1	WATCHING TELEVISION.	6. isn't a very selective viewer\n	?	A. In my house, the TV is always on, and I watch whatever is playing because it's my way of staying entertained. However, sometimes I come across a really interesting series, and I can't stop constantly keeping up with it. That's how I entertain myself every day. However, I'm also keen on staying updated with the latest news about not only movies but also music.\n	B. I was never good at school because my grades were always low. However, I can remember a lot of practical things from watching TV. For me, it's a great way to expand my understanding of the world, and I believe it will be more useful when I graduate than the dry, theoretical knowledge we learn in school.\n	C. I don't watch television much lately because I find most reality shows to be pretty stupid. I realized they're all scripted, and the actors just follow a set plan. Once I learned that, I stopped watching those kinds of shows altogether. I switched to watching football instead, but my favorite team keeps losing, so I lost interest in that too.\n	D. I probably spend far too long just watching the series "Friends." The characters are so funny, and I find myself laughing out loud in every episode. I've been watching it for three weeks now, and I still can't wait for the next episode. Watching it for so long has actually helped me improve my English speaking skills without having to sit through boring lessons in class.\n
266	13	1	WATCHING TELEVISION.	7. keep up to date on cinema and music\n	?	A. In my house, the TV is always on, and I watch whatever is playing because it's my way of staying entertained. However, sometimes I come across a really interesting series, and I can't stop constantly keeping up with it. That's how I entertain myself every day. However, I'm also keen on staying updated with the latest news about not only movies but also music.\n	B. I was never good at school because my grades were always low. However, I can remember a lot of practical things from watching TV. For me, it's a great way to expand my understanding of the world, and I believe it will be more useful when I graduate than the dry, theoretical knowledge we learn in school.\n	C. I don't watch television much lately because I find most reality shows to be pretty stupid. I realized they're all scripted, and the actors just follow a set plan. Once I learned that, I stopped watching those kinds of shows altogether. I switched to watching football instead, but my favorite team keeps losing, so I lost interest in that too.\n	D. I probably spend far too long just watching the series "Friends." The characters are so funny, and I find myself laughing out loud in every episode. I've been watching it for three weeks now, and I still can't wait for the next episode. Watching it for so long has actually helped me improve my English speaking skills without having to sit through boring lessons in class.\n
349	23	1	WATCHING A MOVIE	6. thought the film was too long	?	Person A: A friend recommended the film because she had read the novel. I thought it was excellent, and I was captivated by the plot throughout, even though it was quite lengthy. All of the actors were outstanding, and the scenes where the zombies were finally defeated were amazing. The only thing I didn't like was my choice of viewing location. I should have gone out - it would Kave been much better on the big screen.\n	Person B: This was a sequel, and I hadn't seen the prior film, so I have to admit I felt completely lost. I'm pleased I had company. Luckily, my friend was able to explain who the characters were. There were some aspects I liked - the special effects, for example, were impressive, and the soundtrack was lovely. I would definitely recommend it to people who enjoy feeling scared, but personally, films like this don't frighten me. I think I'll stick to romantic movies in the future.\n	Person C: Unfortunately, it wasn't as good as l expected. The written version was terrifying but also thrilling. However, I ended up feeling bored while watching the film. The acting was rather uninspiring, and two and a half hours was excessive. I reckon the story could have been told in half the time. It was definitely better on the page than on the screen. Furthermore, cinema tickets are so costly these days. To be honest, I wish I hadn't wasted my money!\n	Person D: This was actually my second time watching it, but even though I knew what to expect, I still felt scared whenever a zombie attack happened. The direction really makes it feel like you are right there in the room with the characters. Being familiar with the film didn't make it easier! I was so relieved when my friend called after I got home so that I could chat about ordinary things and forget about it. Otherwise, I might have had nightmares!\n
350	23	1	WATCHING A MOVIE	7. has read the book of the film	?	Person A: A friend recommended the film because she had read the novel. I thought it was excellent, and I was captivated by the plot throughout, even though it was quite lengthy. All of the actors were outstanding, and the scenes where the zombies were finally defeated were amazing. The only thing I didn't like was my choice of viewing location. I should have gone out - it would Kave been much better on the big screen.\n	Person B: This was a sequel, and I hadn't seen the prior film, so I have to admit I felt completely lost. I'm pleased I had company. Luckily, my friend was able to explain who the characters were. There were some aspects I liked - the special effects, for example, were impressive, and the soundtrack was lovely. I would definitely recommend it to people who enjoy feeling scared, but personally, films like this don't frighten me. I think I'll stick to romantic movies in the future.\n	Person C: Unfortunately, it wasn't as good as l expected. The written version was terrifying but also thrilling. However, I ended up feeling bored while watching the film. The acting was rather uninspiring, and two and a half hours was excessive. I reckon the story could have been told in half the time. It was definitely better on the page than on the screen. Furthermore, cinema tickets are so costly these days. To be honest, I wish I hadn't wasted my money!\n	Person D: This was actually my second time watching it, but even though I knew what to expect, I still felt scared whenever a zombie attack happened. The direction really makes it feel like you are right there in the room with the characters. Being familiar with the film didn't make it easier! I was so relieved when my friend called after I got home so that I could chat about ordinary things and forget about it. Otherwise, I might have had nightmares!\n
351	24	1	PLANS FOR A NEW STATION.	1. people should plan their journeys better \n	?	Originally, the city planners promised money for building a hospital initially. I don't understand why they switched to construct a new station then. This new station won't solve the traffic jams, and it will require the city's budget every year. Therefore, we won't have money left to build a hospital while health should be a priority, I believe it's better to invest in health services instead.\n	The new station will be in the residential area, close to the hospital and university. We already have buses for getting around, and even though they might be slow sometimes, that's not a reason for being late. I always go to work on time, and I think everyone should work on their personal schedule. People often blame traffic for being late, but I manage to avoid that.\n	I take the train to work every day, and I am tired of the overcrowded trains. I believe investing in a new station is worthwhile, as it could enhance the transportation system and alleviate congestion at the current station. We should consider placing the new station in densely populated residential areas, as this would improve train travel and help reduce crowding.\n	The city planners say that investing in a new station may not be necessary. Both the current station and the bus services appear to work well. Although I don't use trains regularly, I have found the service to be satisfactory whenever I do. The existing facilities are adequate, and I don't see a pressing need to spend money on a new station at this time.\n
352	24	1	PLANS FOR A NEW STATION.	2. the bus is too busy\n	?	Originally, the city planners promised money for building a hospital initially. I don't understand why they switched to construct a new station then. This new station won't solve the traffic jams, and it will require the city's budget every year. Therefore, we won't have money left to build a hospital while health should be a priority, I believe it's better to invest in health services instead.\n	The new station will be in the residential area, close to the hospital and university. We already have buses for getting around, and even though they might be slow sometimes, that's not a reason for being late. I always go to work on time, and I think everyone should work on their personal schedule. People often blame traffic for being late, but I manage to avoid that.\n	I take the train to work every day, and I am tired of the overcrowded trains. I believe investing in a new station is worthwhile, as it could enhance the transportation system and alleviate congestion at the current station. We should consider placing the new station in densely populated residential areas, as this would improve train travel and help reduce crowding.\n	The city planners say that investing in a new station may not be necessary. Both the current station and the bus services appear to work well. Although I don't use trains regularly, I have found the service to be satisfactory whenever I do. The existing facilities are adequate, and I don't see a pressing need to spend money on a new station at this time.\n
353	24	1	PLANS FOR A NEW STATION.	3. the new station will improve train travel\n	?	Originally, the city planners promised money for building a hospital initially. I don't understand why they switched to construct a new station then. This new station won't solve the traffic jams, and it will require the city's budget every year. Therefore, we won't have money left to build a hospital while health should be a priority, I believe it's better to invest in health services instead.\n	The new station will be in the residential area, close to the hospital and university. We already have buses for getting around, and even though they might be slow sometimes, that's not a reason for being late. I always go to work on time, and I think everyone should work on their personal schedule. People often blame traffic for being late, but I manage to avoid that.\n	I take the train to work every day, and I am tired of the overcrowded trains. I believe investing in a new station is worthwhile, as it could enhance the transportation system and alleviate congestion at the current station. We should consider placing the new station in densely populated residential areas, as this would improve train travel and help reduce crowding.\n	The city planners say that investing in a new station may not be necessary. Both the current station and the bus services appear to work well. Although I don't use trains regularly, I have found the service to be satisfactory whenever I do. The existing facilities are adequate, and I don't see a pressing need to spend money on a new station at this time.\n
354	24	1	PLANS FOR A NEW STATION.	4. the bus service is good\n	?	Originally, the city planners promised money for building a hospital initially. I don't understand why they switched to construct a new station then. This new station won't solve the traffic jams, and it will require the city's budget every year. Therefore, we won't have money left to build a hospital while health should be a priority, I believe it's better to invest in health services instead.\n	The new station will be in the residential area, close to the hospital and university. We already have buses for getting around, and even though they might be slow sometimes, that's not a reason for being late. I always go to work on time, and I think everyone should work on their personal schedule. People often blame traffic for being late, but I manage to avoid that.\n	I take the train to work every day, and I am tired of the overcrowded trains. I believe investing in a new station is worthwhile, as it could enhance the transportation system and alleviate congestion at the current station. We should consider placing the new station in densely populated residential areas, as this would improve train travel and help reduce crowding.\n	The city planners say that investing in a new station may not be necessary. Both the current station and the bus services appear to work well. Although I don't use trains regularly, I have found the service to be satisfactory whenever I do. The existing facilities are adequate, and I don't see a pressing need to spend money on a new station at this time.\n
355	24	1	PLANS FOR A NEW STATION.	5. transport system doesn't need improving\n	?	Originally, the city planners promised money for building a hospital initially. I don't understand why they switched to construct a new station then. This new station won't solve the traffic jams, and it will require the city's budget every year. Therefore, we won't have money left to build a hospital while health should be a priority, I believe it's better to invest in health services instead.\n	The new station will be in the residential area, close to the hospital and university. We already have buses for getting around, and even though they might be slow sometimes, that's not a reason for being late. I always go to work on time, and I think everyone should work on their personal schedule. People often blame traffic for being late, but I manage to avoid that.\n	I take the train to work every day, and I am tired of the overcrowded trains. I believe investing in a new station is worthwhile, as it could enhance the transportation system and alleviate congestion at the current station. We should consider placing the new station in densely populated residential areas, as this would improve train travel and help reduce crowding.\n	The city planners say that investing in a new station may not be necessary. Both the current station and the bus services appear to work well. Although I don't use trains regularly, I have found the service to be satisfactory whenever I do. The existing facilities are adequate, and I don't see a pressing need to spend money on a new station at this time.\n
356	24	1	PLANS FOR A NEW STATION.	6. better medical facilities are needed\n	?	Originally, the city planners promised money for building a hospital initially. I don't understand why they switched to construct a new station then. This new station won't solve the traffic jams, and it will require the city's budget every year. Therefore, we won't have money left to build a hospital while health should be a priority, I believe it's better to invest in health services instead.\n	The new station will be in the residential area, close to the hospital and university. We already have buses for getting around, and even though they might be slow sometimes, that's not a reason for being late. I always go to work on time, and I think everyone should work on their personal schedule. People often blame traffic for being late, but I manage to avoid that.\n	I take the train to work every day, and I am tired of the overcrowded trains. I believe investing in a new station is worthwhile, as it could enhance the transportation system and alleviate congestion at the current station. We should consider placing the new station in densely populated residential areas, as this would improve train travel and help reduce crowding.\n	The city planners say that investing in a new station may not be necessary. Both the current station and the bus services appear to work well. Although I don't use trains regularly, I have found the service to be satisfactory whenever I do. The existing facilities are adequate, and I don't see a pressing need to spend money on a new station at this time.\n
357	24	1	PLANS FOR A NEW STATION.	7. the new station will cost too much to build\n	?	Originally, the city planners promised money for building a hospital initially. I don't understand why they switched to construct a new station then. This new station won't solve the traffic jams, and it will require the city's budget every year. Therefore, we won't have money left to build a hospital while health should be a priority, I believe it's better to invest in health services instead.\n	The new station will be in the residential area, close to the hospital and university. We already have buses for getting around, and even though they might be slow sometimes, that's not a reason for being late. I always go to work on time, and I think everyone should work on their personal schedule. People often blame traffic for being late, but I manage to avoid that.\n	I take the train to work every day, and I am tired of the overcrowded trains. I believe investing in a new station is worthwhile, as it could enhance the transportation system and alleviate congestion at the current station. We should consider placing the new station in densely populated residential areas, as this would improve train travel and help reduce crowding.\n	The city planners say that investing in a new station may not be necessary. Both the current station and the bus services appear to work well. Although I don't use trains regularly, I have found the service to be satisfactory whenever I do. The existing facilities are adequate, and I don't see a pressing need to spend money on a new station at this time.\n
274	14	1	EATING AND COOKING.	Who needs to save money on eating?\n	?	As a child, I always enjoyed eating with friends, whether it was at family gatherings or simple meals after school. Sharing food was a way for me to bond with people, and it still brings back happy memories. I believe that the company makes the meal more enjoyable and turns any ordinary dish into a special occasion.\n	A few years ago, I used to eat out a lot, but I realized I needed to save money on eating. Now, I prefer to eat alone, where I can enjoy my meal in peace without distractions. Eating alone allows me to focus on the taste and quality of the food without the need for conversation.\n	Going to a restaurant is exciting because I like a wide variety of food, and I'm always eager to try new dishes from different cultures. I'm also taking a cookery course to improve my skills, so I can recreate some of my favorite meals at home and expand my culinary knowledge.\n	Fast food is nowhere near as good as home-cooked food because it feels healthier and more comforting than eating out. However, I just eat a few types of food, sticking to simple, familiar dishes that I know I'll enjoy. I'm not very adventurous when it comes to trying new things, but I appreciate the comfort of my favorite meals.\n
275	14	1	EATING AND COOKING.	Who likes a wide variety of food?\n	?	As a child, I always enjoyed eating with friends, whether it was at family gatherings or simple meals after school. Sharing food was a way for me to bond with people, and it still brings back happy memories. I believe that the company makes the meal more enjoyable and turns any ordinary dish into a special occasion.\n	A few years ago, I used to eat out a lot, but I realized I needed to save money on eating. Now, I prefer to eat alone, where I can enjoy my meal in peace without distractions. Eating alone allows me to focus on the taste and quality of the food without the need for conversation.\n	Going to a restaurant is exciting because I like a wide variety of food, and I'm always eager to try new dishes from different cultures. I'm also taking a cookery course to improve my skills, so I can recreate some of my favorite meals at home and expand my culinary knowledge.\n	Fast food is nowhere near as good as home-cooked food because it feels healthier and more comforting than eating out. However, I just eat a few types of food, sticking to simple, familiar dishes that I know I'll enjoy. I'm not very adventurous when it comes to trying new things, but I appreciate the comfort of my favorite meals.\n
276	14	1	EATING AND COOKING.	Who prefers to eat home-cooked food?\n	?	As a child, I always enjoyed eating with friends, whether it was at family gatherings or simple meals after school. Sharing food was a way for me to bond with people, and it still brings back happy memories. I believe that the company makes the meal more enjoyable and turns any ordinary dish into a special occasion.\n	A few years ago, I used to eat out a lot, but I realized I needed to save money on eating. Now, I prefer to eat alone, where I can enjoy my meal in peace without distractions. Eating alone allows me to focus on the taste and quality of the food without the need for conversation.\n	Going to a restaurant is exciting because I like a wide variety of food, and I'm always eager to try new dishes from different cultures. I'm also taking a cookery course to improve my skills, so I can recreate some of my favorite meals at home and expand my culinary knowledge.\n	Fast food is nowhere near as good as home-cooked food because it feels healthier and more comforting than eating out. However, I just eat a few types of food, sticking to simple, familiar dishes that I know I'll enjoy. I'm not very adventurous when it comes to trying new things, but I appreciate the comfort of my favorite meals.\n
277	14	1	EATING AND COOKING.	Who enjoys eating with friends?\n	?	As a child, I always enjoyed eating with friends, whether it was at family gatherings or simple meals after school. Sharing food was a way for me to bond with people, and it still brings back happy memories. I believe that the company makes the meal more enjoyable and turns any ordinary dish into a special occasion.\n	A few years ago, I used to eat out a lot, but I realized I needed to save money on eating. Now, I prefer to eat alone, where I can enjoy my meal in peace without distractions. Eating alone allows me to focus on the taste and quality of the food without the need for conversation.\n	Going to a restaurant is exciting because I like a wide variety of food, and I'm always eager to try new dishes from different cultures. I'm also taking a cookery course to improve my skills, so I can recreate some of my favorite meals at home and expand my culinary knowledge.\n	Fast food is nowhere near as good as home-cooked food because it feels healthier and more comforting than eating out. However, I just eat a few types of food, sticking to simple, familiar dishes that I know I'll enjoy. I'm not very adventurous when it comes to trying new things, but I appreciate the comfort of my favorite meals.\n
278	14	1	EATING AND COOKING.	Who only eats a few types of food?\n	?	As a child, I always enjoyed eating with friends, whether it was at family gatherings or simple meals after school. Sharing food was a way for me to bond with people, and it still brings back happy memories. I believe that the company makes the meal more enjoyable and turns any ordinary dish into a special occasion.\n	A few years ago, I used to eat out a lot, but I realized I needed to save money on eating. Now, I prefer to eat alone, where I can enjoy my meal in peace without distractions. Eating alone allows me to focus on the taste and quality of the food without the need for conversation.\n	Going to a restaurant is exciting because I like a wide variety of food, and I'm always eager to try new dishes from different cultures. I'm also taking a cookery course to improve my skills, so I can recreate some of my favorite meals at home and expand my culinary knowledge.\n	Fast food is nowhere near as good as home-cooked food because it feels healthier and more comforting than eating out. However, I just eat a few types of food, sticking to simple, familiar dishes that I know I'll enjoy. I'm not very adventurous when it comes to trying new things, but I appreciate the comfort of my favorite meals.\n
279	14	1	EATING AND COOKING.	Who is taking a cookery course?\n	?	As a child, I always enjoyed eating with friends, whether it was at family gatherings or simple meals after school. Sharing food was a way for me to bond with people, and it still brings back happy memories. I believe that the company makes the meal more enjoyable and turns any ordinary dish into a special occasion.\n	A few years ago, I used to eat out a lot, but I realized I needed to save money on eating. Now, I prefer to eat alone, where I can enjoy my meal in peace without distractions. Eating alone allows me to focus on the taste and quality of the food without the need for conversation.\n	Going to a restaurant is exciting because I like a wide variety of food, and I'm always eager to try new dishes from different cultures. I'm also taking a cookery course to improve my skills, so I can recreate some of my favorite meals at home and expand my culinary knowledge.\n	Fast food is nowhere near as good as home-cooked food because it feels healthier and more comforting than eating out. However, I just eat a few types of food, sticking to simple, familiar dishes that I know I'll enjoy. I'm not very adventurous when it comes to trying new things, but I appreciate the comfort of my favorite meals.\n
280	14	1	EATING AND COOKING.	Who prefers to eat alone?\n	?	As a child, I always enjoyed eating with friends, whether it was at family gatherings or simple meals after school. Sharing food was a way for me to bond with people, and it still brings back happy memories. I believe that the company makes the meal more enjoyable and turns any ordinary dish into a special occasion.\n	A few years ago, I used to eat out a lot, but I realized I needed to save money on eating. Now, I prefer to eat alone, where I can enjoy my meal in peace without distractions. Eating alone allows me to focus on the taste and quality of the food without the need for conversation.\n	Going to a restaurant is exciting because I like a wide variety of food, and I'm always eager to try new dishes from different cultures. I'm also taking a cookery course to improve my skills, so I can recreate some of my favorite meals at home and expand my culinary knowledge.\n	Fast food is nowhere near as good as home-cooked food because it feels healthier and more comforting than eating out. However, I just eat a few types of food, sticking to simple, familiar dishes that I know I'll enjoy. I'm not very adventurous when it comes to trying new things, but I appreciate the comfort of my favorite meals.\n
281	16	1	VISIT A CITY.	\npublic transport system was good.\n	?	I visited there last summer and I also really enjoy watching the street performances that the city organizes. It adds a vibrant and entertaining element to my travel experience, and I feel immersed in the local atmosphere. I planned to buy some souvenirs but at the end of the trip, I ran out of money, which I deeply regret..	When 1 visit a new place, I tend to spend a bit more on shopping because I believe memorable experiences are worth it. I enjoy treating myself to delicious food, whether trying local specialties or dining at popular restaurants, as it allows me to explore the local cuisine. Buying souvenirs also reminds me of the unique experiences and culture ! encountered during my journey.	Personally, I thought the city's public transport was really good. It was easy to use, efficient, and well-organized. It made getting around and exploring different areas of the city a breeze. It also relieved my worry about walking too much during my trip. I realized the importance of taking care of my feet and not pushing myself too hard. This way, I could enjoy my trip without feeling uncomfortable or tired.	I don't generally go to big cities, asi prefer staying in one area of the city to fully experience the local culture and attractions, I enjoy destinations that feature natural resorts, where I can relax and appreciate the beauty of nature. This way. I can escape the fast pace of city life and truly connect with my surroundings.
282	16	1	VISIT A CITY.	concerned about walking too much causes a problem.\n	?	I visited there last summer and I also really enjoy watching the street performances that the city organizes. It adds a vibrant and entertaining element to my travel experience, and I feel immersed in the local atmosphere. I planned to buy some souvenirs but at the end of the trip, I ran out of money, which I deeply regret..	When 1 visit a new place, I tend to spend a bit more on shopping because I believe memorable experiences are worth it. I enjoy treating myself to delicious food, whether trying local specialties or dining at popular restaurants, as it allows me to explore the local cuisine. Buying souvenirs also reminds me of the unique experiences and culture ! encountered during my journey.	Personally, I thought the city's public transport was really good. It was easy to use, efficient, and well-organized. It made getting around and exploring different areas of the city a breeze. It also relieved my worry about walking too much during my trip. I realized the importance of taking care of my feet and not pushing myself too hard. This way, I could enjoy my trip without feeling uncomfortable or tired.	I don't generally go to big cities, asi prefer staying in one area of the city to fully experience the local culture and attractions, I enjoy destinations that feature natural resorts, where I can relax and appreciate the beauty of nature. This way. I can escape the fast pace of city life and truly connect with my surroundings.
283	16	1	VISIT A CITY.	like the natural resort here.\n	?	I visited there last summer and I also really enjoy watching the street performances that the city organizes. It adds a vibrant and entertaining element to my travel experience, and I feel immersed in the local atmosphere. I planned to buy some souvenirs but at the end of the trip, I ran out of money, which I deeply regret..	When 1 visit a new place, I tend to spend a bit more on shopping because I believe memorable experiences are worth it. I enjoy treating myself to delicious food, whether trying local specialties or dining at popular restaurants, as it allows me to explore the local cuisine. Buying souvenirs also reminds me of the unique experiences and culture ! encountered during my journey.	Personally, I thought the city's public transport was really good. It was easy to use, efficient, and well-organized. It made getting around and exploring different areas of the city a breeze. It also relieved my worry about walking too much during my trip. I realized the importance of taking care of my feet and not pushing myself too hard. This way, I could enjoy my trip without feeling uncomfortable or tired.	I don't generally go to big cities, asi prefer staying in one area of the city to fully experience the local culture and attractions, I enjoy destinations that feature natural resorts, where I can relax and appreciate the beauty of nature. This way. I can escape the fast pace of city life and truly connect with my surroundings.
284	16	1	VISIT A CITY.	spent the holiday in only 1 part of the city.\n	?	I visited there last summer and I also really enjoy watching the street performances that the city organizes. It adds a vibrant and entertaining element to my travel experience, and I feel immersed in the local atmosphere. I planned to buy some souvenirs but at the end of the trip, I ran out of money, which I deeply regret..	When 1 visit a new place, I tend to spend a bit more on shopping because I believe memorable experiences are worth it. I enjoy treating myself to delicious food, whether trying local specialties or dining at popular restaurants, as it allows me to explore the local cuisine. Buying souvenirs also reminds me of the unique experiences and culture ! encountered during my journey.	Personally, I thought the city's public transport was really good. It was easy to use, efficient, and well-organized. It made getting around and exploring different areas of the city a breeze. It also relieved my worry about walking too much during my trip. I realized the importance of taking care of my feet and not pushing myself too hard. This way, I could enjoy my trip without feeling uncomfortable or tired.	I don't generally go to big cities, asi prefer staying in one area of the city to fully experience the local culture and attractions, I enjoy destinations that feature natural resorts, where I can relax and appreciate the beauty of nature. This way. I can escape the fast pace of city life and truly connect with my surroundings.
285	16	1	VISIT A CITY.	like the public theater that the city puts on.\n	?	I visited there last summer and I also really enjoy watching the street performances that the city organizes. It adds a vibrant and entertaining element to my travel experience, and I feel immersed in the local atmosphere. I planned to buy some souvenirs but at the end of the trip, I ran out of money, which I deeply regret..	When 1 visit a new place, I tend to spend a bit more on shopping because I believe memorable experiences are worth it. I enjoy treating myself to delicious food, whether trying local specialties or dining at popular restaurants, as it allows me to explore the local cuisine. Buying souvenirs also reminds me of the unique experiences and culture ! encountered during my journey.	Personally, I thought the city's public transport was really good. It was easy to use, efficient, and well-organized. It made getting around and exploring different areas of the city a breeze. It also relieved my worry about walking too much during my trip. I realized the importance of taking care of my feet and not pushing myself too hard. This way, I could enjoy my trip without feeling uncomfortable or tired.	I don't generally go to big cities, asi prefer staying in one area of the city to fully experience the local culture and attractions, I enjoy destinations that feature natural resorts, where I can relax and appreciate the beauty of nature. This way. I can escape the fast pace of city life and truly connect with my surroundings.
286	16	1	VISIT A CITY.	usually spend a lot of money on shopping.\n	?	I visited there last summer and I also really enjoy watching the street performances that the city organizes. It adds a vibrant and entertaining element to my travel experience, and I feel immersed in the local atmosphere. I planned to buy some souvenirs but at the end of the trip, I ran out of money, which I deeply regret..	When 1 visit a new place, I tend to spend a bit more on shopping because I believe memorable experiences are worth it. I enjoy treating myself to delicious food, whether trying local specialties or dining at popular restaurants, as it allows me to explore the local cuisine. Buying souvenirs also reminds me of the unique experiences and culture ! encountered during my journey.	Personally, I thought the city's public transport was really good. It was easy to use, efficient, and well-organized. It made getting around and exploring different areas of the city a breeze. It also relieved my worry about walking too much during my trip. I realized the importance of taking care of my feet and not pushing myself too hard. This way, I could enjoy my trip without feeling uncomfortable or tired.	I don't generally go to big cities, asi prefer staying in one area of the city to fully experience the local culture and attractions, I enjoy destinations that feature natural resorts, where I can relax and appreciate the beauty of nature. This way. I can escape the fast pace of city life and truly connect with my surroundings.
287	16	1	VISIT A CITY.	pay a lot for their meal.\n	?	I visited there last summer and I also really enjoy watching the street performances that the city organizes. It adds a vibrant and entertaining element to my travel experience, and I feel immersed in the local atmosphere. I planned to buy some souvenirs but at the end of the trip, I ran out of money, which I deeply regret..	When 1 visit a new place, I tend to spend a bit more on shopping because I believe memorable experiences are worth it. I enjoy treating myself to delicious food, whether trying local specialties or dining at popular restaurants, as it allows me to explore the local cuisine. Buying souvenirs also reminds me of the unique experiences and culture ! encountered during my journey.	Personally, I thought the city's public transport was really good. It was easy to use, efficient, and well-organized. It made getting around and exploring different areas of the city a breeze. It also relieved my worry about walking too much during my trip. I realized the importance of taking care of my feet and not pushing myself too hard. This way, I could enjoy my trip without feeling uncomfortable or tired.	I don't generally go to big cities, asi prefer staying in one area of the city to fully experience the local culture and attractions, I enjoy destinations that feature natural resorts, where I can relax and appreciate the beauty of nature. This way. I can escape the fast pace of city life and truly connect with my surroundings.
288	17	1	THE QUALITY OF A RESTAURANT	1. was impressed by the range of appetizers.\n	?	Person A: The Menu I read has a lot of good reviews online and decided to try it out. The prices are reasonable, and the food is good and varied. My favorite part is the starters - there are so many things that I don't know what to choose from. My only criticism is the noise level. The live show was excellent, but the volume was a bit low; they should turn it up next time. Despite that, I enjoyed the food and the show overall.	Person B: I'm not sure if i'll return to it. The staff seemed like they just had an argument, making the atmosphere unpleasant. Maybe they had a rough day. I ordered fish and chips. It is not bad but not good either. People said this restaurant was excellent, but my experience might be an exception.	Person C: I was looking forward to visiting this restaurant, but my first visit left me certain that I won't come back. The staff wasn't friendly at all, and while the meal was huge, it made me question whether that was a good sign. The traditional style of the food didn't match the modern décor, creating an odd experience that I don't want to repeat. Additionally, the food was too expensive.	Person D: The newspaper I saw has lots of appetizing food. Unfortunately, on the day I arrived, I came late, so I couldn't order dinner. However, the drinks here were great. I tried a mango drink and it was delicious. The background music was just right, and the decor matched the atmosphere perfectly. Overall, it was great, I'll definitely come back on time next time to try their food.
289	17	1	THE QUALITY OF A RESTAURANT	2. thought the music was too quiet.	?	Person A: The Menu I read has a lot of good reviews online and decided to try it out. The prices are reasonable, and the food is good and varied. My favorite part is the starters - there are so many things that I don't know what to choose from. My only criticism is the noise level. The live show was excellent, but the volume was a bit low; they should turn it up next time. Despite that, I enjoyed the food and the show overall.	Person B: I'm not sure if i'll return to it. The staff seemed like they just had an argument, making the atmosphere unpleasant. Maybe they had a rough day. I ordered fish and chips. It is not bad but not good either. People said this restaurant was excellent, but my experience might be an exception.	Person C: I was looking forward to visiting this restaurant, but my first visit left me certain that I won't come back. The staff wasn't friendly at all, and while the meal was huge, it made me question whether that was a good sign. The traditional style of the food didn't match the modern décor, creating an odd experience that I don't want to repeat. Additionally, the food was too expensive.	Person D: The newspaper I saw has lots of appetizing food. Unfortunately, on the day I arrived, I came late, so I couldn't order dinner. However, the drinks here were great. I tried a mango drink and it was delicious. The background music was just right, and the decor matched the atmosphere perfectly. Overall, it was great, I'll definitely come back on time next time to try their food.
290	17	1	THE QUALITY OF A RESTAURANT	3. didn't eat anything at the restaurant.	?	Person A: The Menu I read has a lot of good reviews online and decided to try it out. The prices are reasonable, and the food is good and varied. My favorite part is the starters - there are so many things that I don't know what to choose from. My only criticism is the noise level. The live show was excellent, but the volume was a bit low; they should turn it up next time. Despite that, I enjoyed the food and the show overall.	Person B: I'm not sure if i'll return to it. The staff seemed like they just had an argument, making the atmosphere unpleasant. Maybe they had a rough day. I ordered fish and chips. It is not bad but not good either. People said this restaurant was excellent, but my experience might be an exception.	Person C: I was looking forward to visiting this restaurant, but my first visit left me certain that I won't come back. The staff wasn't friendly at all, and while the meal was huge, it made me question whether that was a good sign. The traditional style of the food didn't match the modern décor, creating an odd experience that I don't want to repeat. Additionally, the food was too expensive.	Person D: The newspaper I saw has lots of appetizing food. Unfortunately, on the day I arrived, I came late, so I couldn't order dinner. However, the drinks here were great. I tried a mango drink and it was delicious. The background music was just right, and the decor matched the atmosphere perfectly. Overall, it was great, I'll definitely come back on time next time to try their food.
291	17	1	THE QUALITY OF A RESTAURANT	4. enjoyed the atmosphere of the restaurant.	?	Person A: The Menu I read has a lot of good reviews online and decided to try it out. The prices are reasonable, and the food is good and varied. My favorite part is the starters - there are so many things that I don't know what to choose from. My only criticism is the noise level. The live show was excellent, but the volume was a bit low; they should turn it up next time. Despite that, I enjoyed the food and the show overall.	Person B: I'm not sure if i'll return to it. The staff seemed like they just had an argument, making the atmosphere unpleasant. Maybe they had a rough day. I ordered fish and chips. It is not bad but not good either. People said this restaurant was excellent, but my experience might be an exception.	Person C: I was looking forward to visiting this restaurant, but my first visit left me certain that I won't come back. The staff wasn't friendly at all, and while the meal was huge, it made me question whether that was a good sign. The traditional style of the food didn't match the modern décor, creating an odd experience that I don't want to repeat. Additionally, the food was too expensive.	Person D: The newspaper I saw has lots of appetizing food. Unfortunately, on the day I arrived, I came late, so I couldn't order dinner. However, the drinks here were great. I tried a mango drink and it was delicious. The background music was just right, and the decor matched the atmosphere perfectly. Overall, it was great, I'll definitely come back on time next time to try their food.
292	17	1	THE QUALITY OF A RESTAURANT	5. thought his experience was probably unusual.\n	?	Person A: The Menu I read has a lot of good reviews online and decided to try it out. The prices are reasonable, and the food is good and varied. My favorite part is the starters - there are so many things that I don't know what to choose from. My only criticism is the noise level. The live show was excellent, but the volume was a bit low; they should turn it up next time. Despite that, I enjoyed the food and the show overall.	Person B: I'm not sure if i'll return to it. The staff seemed like they just had an argument, making the atmosphere unpleasant. Maybe they had a rough day. I ordered fish and chips. It is not bad but not good either. People said this restaurant was excellent, but my experience might be an exception.	Person C: I was looking forward to visiting this restaurant, but my first visit left me certain that I won't come back. The staff wasn't friendly at all, and while the meal was huge, it made me question whether that was a good sign. The traditional style of the food didn't match the modern décor, creating an odd experience that I don't want to repeat. Additionally, the food was too expensive.	Person D: The newspaper I saw has lots of appetizing food. Unfortunately, on the day I arrived, I came late, so I couldn't order dinner. However, the drinks here were great. I tried a mango drink and it was delicious. The background music was just right, and the decor matched the atmosphere perfectly. Overall, it was great, I'll definitely come back on time next time to try their food.
293	17	1	THE QUALITY OF A RESTAURANT	6. the food was of average quality.\n	?	Person A: The Menu I read has a lot of good reviews online and decided to try it out. The prices are reasonable, and the food is good and varied. My favorite part is the starters - there are so many things that I don't know what to choose from. My only criticism is the noise level. The live show was excellent, but the volume was a bit low; they should turn it up next time. Despite that, I enjoyed the food and the show overall.	Person B: I'm not sure if i'll return to it. The staff seemed like they just had an argument, making the atmosphere unpleasant. Maybe they had a rough day. I ordered fish and chips. It is not bad but not good either. People said this restaurant was excellent, but my experience might be an exception.	Person C: I was looking forward to visiting this restaurant, but my first visit left me certain that I won't come back. The staff wasn't friendly at all, and while the meal was huge, it made me question whether that was a good sign. The traditional style of the food didn't match the modern décor, creating an odd experience that I don't want to repeat. Additionally, the food was too expensive.	Person D: The newspaper I saw has lots of appetizing food. Unfortunately, on the day I arrived, I came late, so I couldn't order dinner. However, the drinks here were great. I tried a mango drink and it was delicious. The background music was just right, and the decor matched the atmosphere perfectly. Overall, it was great, I'll definitely come back on time next time to try their food.
294	17	1	THE QUALITY OF A RESTAURANT	7. will definitely not return to the restaurant.\n	?	Person A: The Menu I read has a lot of good reviews online and decided to try it out. The prices are reasonable, and the food is good and varied. My favorite part is the starters - there are so many things that I don't know what to choose from. My only criticism is the noise level. The live show was excellent, but the volume was a bit low; they should turn it up next time. Despite that, I enjoyed the food and the show overall.	Person B: I'm not sure if i'll return to it. The staff seemed like they just had an argument, making the atmosphere unpleasant. Maybe they had a rough day. I ordered fish and chips. It is not bad but not good either. People said this restaurant was excellent, but my experience might be an exception.	Person C: I was looking forward to visiting this restaurant, but my first visit left me certain that I won't come back. The staff wasn't friendly at all, and while the meal was huge, it made me question whether that was a good sign. The traditional style of the food didn't match the modern décor, creating an odd experience that I don't want to repeat. Additionally, the food was too expensive.	Person D: The newspaper I saw has lots of appetizing food. Unfortunately, on the day I arrived, I came late, so I couldn't order dinner. However, the drinks here were great. I tried a mango drink and it was delicious. The background music was just right, and the decor matched the atmosphere perfectly. Overall, it was great, I'll definitely come back on time next time to try their food.
302	18	1	OPINIONS ON FLYING.	\n1. suggest making flights more expensive\n	?	I used to fly to Italy every summer for my wine trade, where I enjoyed relaxing while traveling and tasting some of the finest wines. For me, visiting vineyards and connecting with local producers was not just about business; it was a chance to unwind and appreciate the beautiful landscapes. My travels allowed me to immerse myself in different cultures, making my work even more fulfilling.	People find it strange that I dislike flying, especially as a travel blogger who frequently needs to fly for my work. Despite the excitement of discovering new destinations, I think that flying is a bad experience overall, with long security lines and cramped seats. I often share tips with my followers about finding alternative travel options, like road trips, that allow for more enjoyable and flexible adventures.	Personally, I have mixed feelings about flying. While I want to work as a tour guide in other countries to share my love for travel with others, I also dread the uncomfortable experience of air travel. I even suggest increasing the flight ticket price to reduce the number of flights, making travel a more thoughtful experience that allows people to appreciate their journeys.	My son and his family live far from me, so I visit relatives regularly by plane. I know this is harmful for the environment but there are other things that I do in order to protect our nature. I usually walk or cycle to local grocery stores instead of driving, and I limit my use of plastic as much as possible. I believe that small actions, like these, contribute to a healthier planet and set a good example for my family.
303	18	1	OPINIONS ON FLYING.	2. want to work in other countries\n	?	I used to fly to Italy every summer for my wine trade, where I enjoyed relaxing while traveling and tasting some of the finest wines. For me, visiting vineyards and connecting with local producers was not just about business; it was a chance to unwind and appreciate the beautiful landscapes. My travels allowed me to immerse myself in different cultures, making my work even more fulfilling.	People find it strange that I dislike flying, especially as a travel blogger who frequently needs to fly for my work. Despite the excitement of discovering new destinations, I think that flying is a bad experience overall, with long security lines and cramped seats. I often share tips with my followers about finding alternative travel options, like road trips, that allow for more enjoyable and flexible adventures.	Personally, I have mixed feelings about flying. While I want to work as a tour guide in other countries to share my love for travel with others, I also dread the uncomfortable experience of air travel. I even suggest increasing the flight ticket price to reduce the number of flights, making travel a more thoughtful experience that allows people to appreciate their journeys.	My son and his family live far from me, so I visit relatives regularly by plane. I know this is harmful for the environment but there are other things that I do in order to protect our nature. I usually walk or cycle to local grocery stores instead of driving, and I limit my use of plastic as much as possible. I believe that small actions, like these, contribute to a healthier planet and set a good example for my family.
304	18	1	OPINIONS ON FLYING.	3. visit relatives regularly\n	?	I used to fly to Italy every summer for my wine trade, where I enjoyed relaxing while traveling and tasting some of the finest wines. For me, visiting vineyards and connecting with local producers was not just about business; it was a chance to unwind and appreciate the beautiful landscapes. My travels allowed me to immerse myself in different cultures, making my work even more fulfilling.	People find it strange that I dislike flying, especially as a travel blogger who frequently needs to fly for my work. Despite the excitement of discovering new destinations, I think that flying is a bad experience overall, with long security lines and cramped seats. I often share tips with my followers about finding alternative travel options, like road trips, that allow for more enjoyable and flexible adventures.	Personally, I have mixed feelings about flying. While I want to work as a tour guide in other countries to share my love for travel with others, I also dread the uncomfortable experience of air travel. I even suggest increasing the flight ticket price to reduce the number of flights, making travel a more thoughtful experience that allows people to appreciate their journeys.	My son and his family live far from me, so I visit relatives regularly by plane. I know this is harmful for the environment but there are other things that I do in order to protect our nature. I usually walk or cycle to local grocery stores instead of driving, and I limit my use of plastic as much as possible. I believe that small actions, like these, contribute to a healthier planet and set a good example for my family.
204	9	1	VOLUNTEERING TO CLEAN A LOCAL PARK	Who thinks the park is a beautiful place to relax?	B	I just have too much work that I don't have much free time for myself. This tight schedule makes it impossible for me to join in the park cleaning. I work all week, and the only time I go out is on weekends with my family. We usually visit the park to play games and take a walk. I am relieved to hear that the park will be cleaned by the children volunteering from the school nearby. I believe these experiences will benefit them in the future, helping them sharpen skills needed for their future careers.	I adore the gorgeous scenery and fresh air at the park. Therefore, I always bring my family to the park to relax. My husband and I are always willing to do some volunteer work, so I will ask my husband to help out since he usually doesn't do much anyway. I will make specific plans for everyone in the neighborhood to follow so the park could be cleaned in no time.	The park plays an important role in teaching children about responsibility through volunteering. Cleaning the local park not only helps keep the environment clean but also teaches kids the value of teamwork and dedication. We admire their efforts to protect nature, whether it's picking up trash or planting flowers. Volunteering is a great way for children to improve their skills and mindset while making a positive impact on our community.	This is a reminder that not just the park, but other areas in our town also need regular cleaning. Keeping our neighborhoods clean is important for a healthy environment. The community should work together to organize cleaning events more often, as ignoring trash can harm wildlife and make the area unpleasant. By joining these efforts, residents can take pride in their surroundings and make sure everyone has a nice place to enjoy.
205	9	1	VOLUNTEERING TO CLEAN A LOCAL PARK	Who can't help because of busy life?	A	I just have too much work that I don't have much free time for myself. This tight schedule makes it impossible for me to join in the park cleaning. I work all week, and the only time I go out is on weekends with my family. We usually visit the park to play games and take a walk. I am relieved to hear that the park will be cleaned by the children volunteering from the school nearby. I believe these experiences will benefit them in the future, helping them sharpen skills needed for their future careers.	I adore the gorgeous scenery and fresh air at the park. Therefore, I always bring my family to the park to relax. My husband and I are always willing to do some volunteer work, so I will ask my husband to help out since he usually doesn't do much anyway. I will make specific plans for everyone in the neighborhood to follow so the park could be cleaned in no time.	The park plays an important role in teaching children about responsibility through volunteering. Cleaning the local park not only helps keep the environment clean but also teaches kids the value of teamwork and dedication. We admire their efforts to protect nature, whether it's picking up trash or planting flowers. Volunteering is a great way for children to improve their skills and mindset while making a positive impact on our community.	This is a reminder that not just the park, but other areas in our town also need regular cleaning. Keeping our neighborhoods clean is important for a healthy environment. The community should work together to organize cleaning events more often, as ignoring trash can harm wildlife and make the area unpleasant. By joining these efforts, residents can take pride in their surroundings and make sure everyone has a nice place to enjoy.
206	9	1	VOLUNTEERING TO CLEAN A LOCAL PARK	Who will ask other people to help?	B	I just have too much work that I don't have much free time for myself. This tight schedule makes it impossible for me to join in the park cleaning. I work all week, and the only time I go out is on weekends with my family. We usually visit the park to play games and take a walk. I am relieved to hear that the park will be cleaned by the children volunteering from the school nearby. I believe these experiences will benefit them in the future, helping them sharpen skills needed for their future careers.	I adore the gorgeous scenery and fresh air at the park. Therefore, I always bring my family to the park to relax. My husband and I are always willing to do some volunteer work, so I will ask my husband to help out since he usually doesn't do much anyway. I will make specific plans for everyone in the neighborhood to follow so the park could be cleaned in no time.	The park plays an important role in teaching children about responsibility through volunteering. Cleaning the local park not only helps keep the environment clean but also teaches kids the value of teamwork and dedication. We admire their efforts to protect nature, whether it's picking up trash or planting flowers. Volunteering is a great way for children to improve their skills and mindset while making a positive impact on our community.	This is a reminder that not just the park, but other areas in our town also need regular cleaning. Keeping our neighborhoods clean is important for a healthy environment. The community should work together to organize cleaning events more often, as ignoring trash can harm wildlife and make the area unpleasant. By joining these efforts, residents can take pride in their surroundings and make sure everyone has a nice place to enjoy.
207	9	1	VOLUNTEERING TO CLEAN A LOCAL PARK	Who thinks cleaning should happen regularly?	D	I just have too much work that I don't have much free time for myself. This tight schedule makes it impossible for me to join in the park cleaning. I work all week, and the only time I go out is on weekends with my family. We usually visit the park to play games and take a walk. I am relieved to hear that the park will be cleaned by the children volunteering from the school nearby. I believe these experiences will benefit them in the future, helping them sharpen skills needed for their future careers.	I adore the gorgeous scenery and fresh air at the park. Therefore, I always bring my family to the park to relax. My husband and I are always willing to do some volunteer work, so I will ask my husband to help out since he usually doesn't do much anyway. I will make specific plans for everyone in the neighborhood to follow so the park could be cleaned in no time.	The park plays an important role in teaching children about responsibility through volunteering. Cleaning the local park not only helps keep the environment clean but also teaches kids the value of teamwork and dedication. We admire their efforts to protect nature, whether it's picking up trash or planting flowers. Volunteering is a great way for children to improve their skills and mindset while making a positive impact on our community.	This is a reminder that not just the park, but other areas in our town also need regular cleaning. Keeping our neighborhoods clean is important for a healthy environment. The community should work together to organize cleaning events more often, as ignoring trash can harm wildlife and make the area unpleasant. By joining these efforts, residents can take pride in their surroundings and make sure everyone has a nice place to enjoy.
208	9	1	VOLUNTEERING TO CLEAN A LOCAL PARK	Who thinks volunteering is important for children?	C	I just have too much work that I don't have much free time for myself. This tight schedule makes it impossible for me to join in the park cleaning. I work all week, and the only time I go out is on weekends with my family. We usually visit the park to play games and take a walk. I am relieved to hear that the park will be cleaned by the children volunteering from the school nearby. I believe these experiences will benefit them in the future, helping them sharpen skills needed for their future careers.	I adore the gorgeous scenery and fresh air at the park. Therefore, I always bring my family to the park to relax. My husband and I are always willing to do some volunteer work, so I will ask my husband to help out since he usually doesn't do much anyway. I will make specific plans for everyone in the neighborhood to follow so the park could be cleaned in no time.	The park plays an important role in teaching children about responsibility through volunteering. Cleaning the local park not only helps keep the environment clean but also teaches kids the value of teamwork and dedication. We admire their efforts to protect nature, whether it's picking up trash or planting flowers. Volunteering is a great way for children to improve their skills and mindset while making a positive impact on our community.	This is a reminder that not just the park, but other areas in our town also need regular cleaning. Keeping our neighborhoods clean is important for a healthy environment. The community should work together to organize cleaning events more often, as ignoring trash can harm wildlife and make the area unpleasant. By joining these efforts, residents can take pride in their surroundings and make sure everyone has a nice place to enjoy.
209	9	1	VOLUNTEERING TO CLEAN A LOCAL PARK	Who thinks other local areas need cleaning?	D	I just have too much work that I don't have much free time for myself. This tight schedule makes it impossible for me to join in the park cleaning. I work all week, and the only time I go out is on weekends with my family. We usually visit the park to play games and take a walk. I am relieved to hear that the park will be cleaned by the children volunteering from the school nearby. I believe these experiences will benefit them in the future, helping them sharpen skills needed for their future careers.	I adore the gorgeous scenery and fresh air at the park. Therefore, I always bring my family to the park to relax. My husband and I are always willing to do some volunteer work, so I will ask my husband to help out since he usually doesn't do much anyway. I will make specific plans for everyone in the neighborhood to follow so the park could be cleaned in no time.	The park plays an important role in teaching children about responsibility through volunteering. Cleaning the local park not only helps keep the environment clean but also teaches kids the value of teamwork and dedication. We admire their efforts to protect nature, whether it's picking up trash or planting flowers. Volunteering is a great way for children to improve their skills and mindset while making a positive impact on our community.	This is a reminder that not just the park, but other areas in our town also need regular cleaning. Keeping our neighborhoods clean is important for a healthy environment. The community should work together to organize cleaning events more often, as ignoring trash can harm wildlife and make the area unpleasant. By joining these efforts, residents can take pride in their surroundings and make sure everyone has a nice place to enjoy.
210	9	1	VOLUNTEERING TO CLEAN A LOCAL PARK	Volunteering will help with future employment/job?	A	I just have too much work that I don't have much free time for myself. This tight schedule makes it impossible for me to join in the park cleaning. I work all week, and the only time I go out is on weekends with my family. We usually visit the park to play games and take a walk. I am relieved to hear that the park will be cleaned by the children volunteering from the school nearby. I believe these experiences will benefit them in the future, helping them sharpen skills needed for their future careers.	I adore the gorgeous scenery and fresh air at the park. Therefore, I always bring my family to the park to relax. My husband and I are always willing to do some volunteer work, so I will ask my husband to help out since he usually doesn't do much anyway. I will make specific plans for everyone in the neighborhood to follow so the park could be cleaned in no time.	The park plays an important role in teaching children about responsibility through volunteering. Cleaning the local park not only helps keep the environment clean but also teaches kids the value of teamwork and dedication. We admire their efforts to protect nature, whether it's picking up trash or planting flowers. Volunteering is a great way for children to improve their skills and mindset while making a positive impact on our community.	This is a reminder that not just the park, but other areas in our town also need regular cleaning. Keeping our neighborhoods clean is important for a healthy environment. The community should work together to organize cleaning events more often, as ignoring trash can harm wildlife and make the area unpleasant. By joining these efforts, residents can take pride in their surroundings and make sure everyone has a nice place to enjoy.
211	10	1	VISIT AN ISLAND.	forgot something to bring.	A	I went to this island to visit some remote beaches. I thought walking shoes would be helpful. However, when I arrived, I realized that I had forgotten to bring them. The remoteness means there are no other visitors. It is good, but it has its downside. There is nowhere to buy food and drink, so I have to bring my own.	Being an architect, when I go abroad, I am very curious about the construction of local buildings. I often lay down at the beach and buy some souvenirs at the local shop. This time, I traveled by taxi to go around. There is no one to share so the cost is high. However, it's worth it because I could see some beautiful traditional houses.	The sharp bends of the island look dangerous and that put me off hiring a car, especially when it is costly. Therefore, I chose to travel by bus. However, the bus service is not very frequent. If they improve it, it would be perfect. I visit some famous places near my hotel on foot. I love it because I can see many beautiful locations.	I stayed in a village and ate at various local restaurants. I cannot recommend a specific dish because everything was amazing. However, if you want to cook by yourself, you would need to take a bus to the town. There is a street market where you can buy some local products. I had some real bargains there.
212	10	1	VISIT AN ISLAND.	liked buying things on the island. (souvenir)	B	I went to this island to visit some remote beaches. I thought walking shoes would be helpful. However, when I arrived, I realized that I had forgotten to bring them. The remoteness means there are no other visitors. It is good, but it has its downside. There is nowhere to buy food and drink, so I have to bring my own.	Being an architect, when I go abroad, I am very curious about the construction of local buildings. I often lay down at the beach and buy some souvenirs at the local shop. This time, I traveled by taxi to go around. There is no one to share so the cost is high. However, it's worth it because I could see some beautiful traditional houses.	The sharp bends of the island look dangerous and that put me off hiring a car, especially when it is costly. Therefore, I chose to travel by bus. However, the bus service is not very frequent. If they improve it, it would be perfect. I visit some famous places near my hotel on foot. I love it because I can see many beautiful locations.	I stayed in a village and ate at various local restaurants. I cannot recommend a specific dish because everything was amazing. However, if you want to cook by yourself, you would need to take a bus to the town. There is a street market where you can buy some local products. I had some real bargains there.
213	10	1	VISIT AN ISLAND.	spent a lot of money on transport.	B	I went to this island to visit some remote beaches. I thought walking shoes would be helpful. However, when I arrived, I realized that I had forgotten to bring them. The remoteness means there are no other visitors. It is good, but it has its downside. There is nowhere to buy food and drink, so I have to bring my own.	Being an architect, when I go abroad, I am very curious about the construction of local buildings. I often lay down at the beach and buy some souvenirs at the local shop. This time, I traveled by taxi to go around. There is no one to share so the cost is high. However, it's worth it because I could see some beautiful traditional houses.	The sharp bends of the island look dangerous and that put me off hiring a car, especially when it is costly. Therefore, I chose to travel by bus. However, the bus service is not very frequent. If they improve it, it would be perfect. I visit some famous places near my hotel on foot. I love it because I can see many beautiful locations.	I stayed in a village and ate at various local restaurants. I cannot recommend a specific dish because everything was amazing. However, if you want to cook by yourself, you would need to take a bus to the town. There is a street market where you can buy some local products. I had some real bargains there.
214	10	1	VISIT AN ISLAND.	loved eating food here.	D	I went to this island to visit some remote beaches. I thought walking shoes would be helpful. However, when I arrived, I realized that I had forgotten to bring them. The remoteness means there are no other visitors. It is good, but it has its downside. There is nowhere to buy food and drink, so I have to bring my own.	Being an architect, when I go abroad, I am very curious about the construction of local buildings. I often lay down at the beach and buy some souvenirs at the local shop. This time, I traveled by taxi to go around. There is no one to share so the cost is high. However, it's worth it because I could see some beautiful traditional houses.	The sharp bends of the island look dangerous and that put me off hiring a car, especially when it is costly. Therefore, I chose to travel by bus. However, the bus service is not very frequent. If they improve it, it would be perfect. I visit some famous places near my hotel on foot. I love it because I can see many beautiful locations.	I stayed in a village and ate at various local restaurants. I cannot recommend a specific dish because everything was amazing. However, if you want to cook by yourself, you would need to take a bus to the town. There is a street market where you can buy some local products. I had some real bargains there.
215	10	1	VISIT AN ISLAND.	liked to walk.	C	I went to this island to visit some remote beaches. I thought walking shoes would be helpful. However, when I arrived, I realized that I had forgotten to bring them. The remoteness means there are no other visitors. It is good, but it has its downside. There is nowhere to buy food and drink, so I have to bring my own.	Being an architect, when I go abroad, I am very curious about the construction of local buildings. I often lay down at the beach and buy some souvenirs at the local shop. This time, I traveled by taxi to go around. There is no one to share so the cost is high. However, it's worth it because I could see some beautiful traditional houses.	The sharp bends of the island look dangerous and that put me off hiring a car, especially when it is costly. Therefore, I chose to travel by bus. However, the bus service is not very frequent. If they improve it, it would be perfect. I visit some famous places near my hotel on foot. I love it because I can see many beautiful locations.	I stayed in a village and ate at various local restaurants. I cannot recommend a specific dish because everything was amazing. However, if you want to cook by yourself, you would need to take a bus to the town. There is a street market where you can buy some local products. I had some real bargains there.
216	10	1	VISIT AN ISLAND.	thought public transport could be improved.	C	I went to this island to visit some remote beaches. I thought walking shoes would be helpful. However, when I arrived, I realized that I had forgotten to bring them. The remoteness means there are no other visitors. It is good, but it has its downside. There is nowhere to buy food and drink, so I have to bring my own.	Being an architect, when I go abroad, I am very curious about the construction of local buildings. I often lay down at the beach and buy some souvenirs at the local shop. This time, I traveled by taxi to go around. There is no one to share so the cost is high. However, it's worth it because I could see some beautiful traditional houses.	The sharp bends of the island look dangerous and that put me off hiring a car, especially when it is costly. Therefore, I chose to travel by bus. However, the bus service is not very frequent. If they improve it, it would be perfect. I visit some famous places near my hotel on foot. I love it because I can see many beautiful locations.	I stayed in a village and ate at various local restaurants. I cannot recommend a specific dish because everything was amazing. However, if you want to cook by yourself, you would need to take a bus to the town. There is a street market where you can buy some local products. I had some real bargains there.
217	10	1	VISIT AN ISLAND.	liked being alone.	A	I went to this island to visit some remote beaches. I thought walking shoes would be helpful. However, when I arrived, I realized that I had forgotten to bring them. The remoteness means there are no other visitors. It is good, but it has its downside. There is nowhere to buy food and drink, so I have to bring my own.	Being an architect, when I go abroad, I am very curious about the construction of local buildings. I often lay down at the beach and buy some souvenirs at the local shop. This time, I traveled by taxi to go around. There is no one to share so the cost is high. However, it's worth it because I could see some beautiful traditional houses.	The sharp bends of the island look dangerous and that put me off hiring a car, especially when it is costly. Therefore, I chose to travel by bus. However, the bus service is not very frequent. If they improve it, it would be perfect. I visit some famous places near my hotel on foot. I love it because I can see many beautiful locations.	I stayed in a village and ate at various local restaurants. I cannot recommend a specific dish because everything was amazing. However, if you want to cook by yourself, you would need to take a bus to the town. There is a street market where you can buy some local products. I had some real bargains there.
218	11	1	ART	Who has some artistic skills?	?	I know the names of some famous artists, and I recognize some paintings. However, I only go to exhibitions when my friends want to. I find that seeing exhibitions is often boring, and while I appreciate the skill it takes to create art. I can't help but feel that many galleries lack excitement. Despite this, I do have some artistic techniques myself; I enjoy painting in my free time, but I prefer to create rather than just observe.\n	I think that looking at art is a personal experience. I much prefer to see art on my own, where I can take my time to appreciate each piece without distractions. I think visitors to galleries should focus more on the art itself rather than chatting or using their phones. When I'm alone with a painting, I can truly connect with it and reflect on what the artist intended.	I find art fascinating. I have developed a good knowledge about various art movements and techniques over the years. Each piece tells a story, and I love discovering the history behind them. The colors, forms, and emotions captured in art pieces captivate my imagination. I could spend hours discussing and analyzing art, and I always look forward to learning more.	I have great memories associated with art, as I have been going to numerous art exhibitions in my whole life. I cherish the moments spent with friends and family, exploring galleries together. Seeing art with people close to me adds a special dimension to the experience; we share our thoughts and feelings about the pieces we encounter. These shared experiences have created lasting bonds and wonderful memories.
219	11	1	ART	Who prefers seeing art by themselves?	?	I know the names of some famous artists, and I recognize some paintings. However, I only go to exhibitions when my friends want to. I find that seeing exhibitions is often boring, and while I appreciate the skill it takes to create art. I can't help but feel that many galleries lack excitement. Despite this, I do have some artistic techniques myself; I enjoy painting in my free time, but I prefer to create rather than just observe.\n	I think that looking at art is a personal experience. I much prefer to see art on my own, where I can take my time to appreciate each piece without distractions. I think visitors to galleries should focus more on the art itself rather than chatting or using their phones. When I'm alone with a painting, I can truly connect with it and reflect on what the artist intended.	I find art fascinating. I have developed a good knowledge about various art movements and techniques over the years. Each piece tells a story, and I love discovering the history behind them. The colors, forms, and emotions captured in art pieces captivate my imagination. I could spend hours discussing and analyzing art, and I always look forward to learning more.	I have great memories associated with art, as I have been going to numerous art exhibitions in my whole life. I cherish the moments spent with friends and family, exploring galleries together. Seeing art with people close to me adds a special dimension to the experience; we share our thoughts and feelings about the pieces we encounter. These shared experiences have created lasting bonds and wonderful memories.
220	11	1	ART	Who has a good knowledge about art?	?	I know the names of some famous artists, and I recognize some paintings. However, I only go to exhibitions when my friends want to. I find that seeing exhibitions is often boring, and while I appreciate the skill it takes to create art. I can't help but feel that many galleries lack excitement. Despite this, I do have some artistic techniques myself; I enjoy painting in my free time, but I prefer to create rather than just observe.\n	I think that looking at art is a personal experience. I much prefer to see art on my own, where I can take my time to appreciate each piece without distractions. I think visitors to galleries should focus more on the art itself rather than chatting or using their phones. When I'm alone with a painting, I can truly connect with it and reflect on what the artist intended.	I find art fascinating. I have developed a good knowledge about various art movements and techniques over the years. Each piece tells a story, and I love discovering the history behind them. The colors, forms, and emotions captured in art pieces captivate my imagination. I could spend hours discussing and analyzing art, and I always look forward to learning more.	I have great memories associated with art, as I have been going to numerous art exhibitions in my whole life. I cherish the moments spent with friends and family, exploring galleries together. Seeing art with people close to me adds a special dimension to the experience; we share our thoughts and feelings about the pieces we encounter. These shared experiences have created lasting bonds and wonderful memories.
221	11	1	ART	Who thinks visitors to the galleries should focus more on the art?	?	I know the names of some famous artists, and I recognize some paintings. However, I only go to exhibitions when my friends want to. I find that seeing exhibitions is often boring, and while I appreciate the skill it takes to create art. I can't help but feel that many galleries lack excitement. Despite this, I do have some artistic techniques myself; I enjoy painting in my free time, but I prefer to create rather than just observe.\n	I think that looking at art is a personal experience. I much prefer to see art on my own, where I can take my time to appreciate each piece without distractions. I think visitors to galleries should focus more on the art itself rather than chatting or using their phones. When I'm alone with a painting, I can truly connect with it and reflect on what the artist intended.	I find art fascinating. I have developed a good knowledge about various art movements and techniques over the years. Each piece tells a story, and I love discovering the history behind them. The colors, forms, and emotions captured in art pieces captivate my imagination. I could spend hours discussing and analyzing art, and I always look forward to learning more.	I have great memories associated with art, as I have been going to numerous art exhibitions in my whole life. I cherish the moments spent with friends and family, exploring galleries together. Seeing art with people close to me adds a special dimension to the experience; we share our thoughts and feelings about the pieces we encounter. These shared experiences have created lasting bonds and wonderful memories.
222	11	1	ART	Who likes seeing art with others?\n	?	I know the names of some famous artists, and I recognize some paintings. However, I only go to exhibitions when my friends want to. I find that seeing exhibitions is often boring, and while I appreciate the skill it takes to create art. I can't help but feel that many galleries lack excitement. Despite this, I do have some artistic techniques myself; I enjoy painting in my free time, but I prefer to create rather than just observe.\n	I think that looking at art is a personal experience. I much prefer to see art on my own, where I can take my time to appreciate each piece without distractions. I think visitors to galleries should focus more on the art itself rather than chatting or using their phones. When I'm alone with a painting, I can truly connect with it and reflect on what the artist intended.	I find art fascinating. I have developed a good knowledge about various art movements and techniques over the years. Each piece tells a story, and I love discovering the history behind them. The colors, forms, and emotions captured in art pieces captivate my imagination. I could spend hours discussing and analyzing art, and I always look forward to learning more.	I have great memories associated with art, as I have been going to numerous art exhibitions in my whole life. I cherish the moments spent with friends and family, exploring galleries together. Seeing art with people close to me adds a special dimension to the experience; we share our thoughts and feelings about the pieces we encounter. These shared experiences have created lasting bonds and wonderful memories.
223	11	1	ART	Who has been going to art exhibitions all their life?\n	?	I know the names of some famous artists, and I recognize some paintings. However, I only go to exhibitions when my friends want to. I find that seeing exhibitions is often boring, and while I appreciate the skill it takes to create art. I can't help but feel that many galleries lack excitement. Despite this, I do have some artistic techniques myself; I enjoy painting in my free time, but I prefer to create rather than just observe.\n	I think that looking at art is a personal experience. I much prefer to see art on my own, where I can take my time to appreciate each piece without distractions. I think visitors to galleries should focus more on the art itself rather than chatting or using their phones. When I'm alone with a painting, I can truly connect with it and reflect on what the artist intended.	I find art fascinating. I have developed a good knowledge about various art movements and techniques over the years. Each piece tells a story, and I love discovering the history behind them. The colors, forms, and emotions captured in art pieces captivate my imagination. I could spend hours discussing and analyzing art, and I always look forward to learning more.	I have great memories associated with art, as I have been going to numerous art exhibitions in my whole life. I cherish the moments spent with friends and family, exploring galleries together. Seeing art with people close to me adds a special dimension to the experience; we share our thoughts and feelings about the pieces we encounter. These shared experiences have created lasting bonds and wonderful memories.
224	11	1	ART	Who thinks seeing an exhibition is boring?	?	I know the names of some famous artists, and I recognize some paintings. However, I only go to exhibitions when my friends want to. I find that seeing exhibitions is often boring, and while I appreciate the skill it takes to create art. I can't help but feel that many galleries lack excitement. Despite this, I do have some artistic techniques myself; I enjoy painting in my free time, but I prefer to create rather than just observe.\n	I think that looking at art is a personal experience. I much prefer to see art on my own, where I can take my time to appreciate each piece without distractions. I think visitors to galleries should focus more on the art itself rather than chatting or using their phones. When I'm alone with a painting, I can truly connect with it and reflect on what the artist intended.	I find art fascinating. I have developed a good knowledge about various art movements and techniques over the years. Each piece tells a story, and I love discovering the history behind them. The colors, forms, and emotions captured in art pieces captivate my imagination. I could spend hours discussing and analyzing art, and I always look forward to learning more.	I have great memories associated with art, as I have been going to numerous art exhibitions in my whole life. I cherish the moments spent with friends and family, exploring galleries together. Seeing art with people close to me adds a special dimension to the experience; we share our thoughts and feelings about the pieces we encounter. These shared experiences have created lasting bonds and wonderful memories.
305	18	1	OPINIONS ON FLYING.	4. try to protect the environment\n	?	I used to fly to Italy every summer for my wine trade, where I enjoyed relaxing while traveling and tasting some of the finest wines. For me, visiting vineyards and connecting with local producers was not just about business; it was a chance to unwind and appreciate the beautiful landscapes. My travels allowed me to immerse myself in different cultures, making my work even more fulfilling.	People find it strange that I dislike flying, especially as a travel blogger who frequently needs to fly for my work. Despite the excitement of discovering new destinations, I think that flying is a bad experience overall, with long security lines and cramped seats. I often share tips with my followers about finding alternative travel options, like road trips, that allow for more enjoyable and flexible adventures.	Personally, I have mixed feelings about flying. While I want to work as a tour guide in other countries to share my love for travel with others, I also dread the uncomfortable experience of air travel. I even suggest increasing the flight ticket price to reduce the number of flights, making travel a more thoughtful experience that allows people to appreciate their journeys.	My son and his family live far from me, so I visit relatives regularly by plane. I know this is harmful for the environment but there are other things that I do in order to protect our nature. I usually walk or cycle to local grocery stores instead of driving, and I limit my use of plastic as much as possible. I believe that small actions, like these, contribute to a healthier planet and set a good example for my family.
306	18	1	OPINIONS ON FLYING.	5. like relaxing while they travel\n	?	I used to fly to Italy every summer for my wine trade, where I enjoyed relaxing while traveling and tasting some of the finest wines. For me, visiting vineyards and connecting with local producers was not just about business; it was a chance to unwind and appreciate the beautiful landscapes. My travels allowed me to immerse myself in different cultures, making my work even more fulfilling.	People find it strange that I dislike flying, especially as a travel blogger who frequently needs to fly for my work. Despite the excitement of discovering new destinations, I think that flying is a bad experience overall, with long security lines and cramped seats. I often share tips with my followers about finding alternative travel options, like road trips, that allow for more enjoyable and flexible adventures.	Personally, I have mixed feelings about flying. While I want to work as a tour guide in other countries to share my love for travel with others, I also dread the uncomfortable experience of air travel. I even suggest increasing the flight ticket price to reduce the number of flights, making travel a more thoughtful experience that allows people to appreciate their journeys.	My son and his family live far from me, so I visit relatives regularly by plane. I know this is harmful for the environment but there are other things that I do in order to protect our nature. I usually walk or cycle to local grocery stores instead of driving, and I limit my use of plastic as much as possible. I believe that small actions, like these, contribute to a healthier planet and set a good example for my family.
307	18	1	OPINIONS ON FLYING.	6. need to fly for their work\n	?	I used to fly to Italy every summer for my wine trade, where I enjoyed relaxing while traveling and tasting some of the finest wines. For me, visiting vineyards and connecting with local producers was not just about business; it was a chance to unwind and appreciate the beautiful landscapes. My travels allowed me to immerse myself in different cultures, making my work even more fulfilling.	People find it strange that I dislike flying, especially as a travel blogger who frequently needs to fly for my work. Despite the excitement of discovering new destinations, I think that flying is a bad experience overall, with long security lines and cramped seats. I often share tips with my followers about finding alternative travel options, like road trips, that allow for more enjoyable and flexible adventures.	Personally, I have mixed feelings about flying. While I want to work as a tour guide in other countries to share my love for travel with others, I also dread the uncomfortable experience of air travel. I even suggest increasing the flight ticket price to reduce the number of flights, making travel a more thoughtful experience that allows people to appreciate their journeys.	My son and his family live far from me, so I visit relatives regularly by plane. I know this is harmful for the environment but there are other things that I do in order to protect our nature. I usually walk or cycle to local grocery stores instead of driving, and I limit my use of plastic as much as possible. I believe that small actions, like these, contribute to a healthier planet and set a good example for my family.
308	18	1	OPINIONS ON FLYING.	7. find flying tiring\n	?	I used to fly to Italy every summer for my wine trade, where I enjoyed relaxing while traveling and tasting some of the finest wines. For me, visiting vineyards and connecting with local producers was not just about business; it was a chance to unwind and appreciate the beautiful landscapes. My travels allowed me to immerse myself in different cultures, making my work even more fulfilling.	People find it strange that I dislike flying, especially as a travel blogger who frequently needs to fly for my work. Despite the excitement of discovering new destinations, I think that flying is a bad experience overall, with long security lines and cramped seats. I often share tips with my followers about finding alternative travel options, like road trips, that allow for more enjoyable and flexible adventures.	Personally, I have mixed feelings about flying. While I want to work as a tour guide in other countries to share my love for travel with others, I also dread the uncomfortable experience of air travel. I even suggest increasing the flight ticket price to reduce the number of flights, making travel a more thoughtful experience that allows people to appreciate their journeys.	My son and his family live far from me, so I visit relatives regularly by plane. I know this is harmful for the environment but there are other things that I do in order to protect our nature. I usually walk or cycle to local grocery stores instead of driving, and I limit my use of plastic as much as possible. I believe that small actions, like these, contribute to a healthier planet and set a good example for my family.
309	19	1	GOING ON HOLIDAY	1. like seeing tourist attractions	?	I have a limited budget for holidays because I am a student, so I usually choose to travel nearby or to places within the country. Because of this, I haven't had the opportunity to travel abroad yet. I'm working on earning more, and hopefully, in the future, I'll be able to explore other countries. That will be my first time traveling overseas.	I once went on a hiking holiday, and it was a disaster. The weather was terrible, and I wasn't as prepared as I thought. I used to enjoy walking a lot, going on trails and exploring nature whenever I had the chance. However, now that I'm retired, my preferences have changed. I find more comfort in staying at home, reading, or spending time with family.	Before I go on holiday, I always get a guidebook so I won't miss out on any important places. I find beach trips boring and always avoid them. Instead, I prefer researching tourist attractions ahead of time and visiting those interesting spots. Exploring new places and learning about their history and culture is what makes travel exciting for me.	I want to relax when I'm on holiday, and I disagree with those who say going to the beach is boring. Last year, a friend invited me on a hiking trip, but I declined. However, my perspective has changed, and now I'm planning to go hiking in the near future. This time, I'll closely follow the weather to ensure it doesn't spoil the trip.
310	19	1	GOING ON HOLIDAY	2. going to the beach is boring	?	I have a limited budget for holidays because I am a student, so I usually choose to travel nearby or to places within the country. Because of this, I haven't had the opportunity to travel abroad yet. I'm working on earning more, and hopefully, in the future, I'll be able to explore other countries. That will be my first time traveling overseas.	I once went on a hiking holiday, and it was a disaster. The weather was terrible, and I wasn't as prepared as I thought. I used to enjoy walking a lot, going on trails and exploring nature whenever I had the chance. However, now that I'm retired, my preferences have changed. I find more comfort in staying at home, reading, or spending time with family.	Before I go on holiday, I always get a guidebook so I won't miss out on any important places. I find beach trips boring and always avoid them. Instead, I prefer researching tourist attractions ahead of time and visiting those interesting spots. Exploring new places and learning about their history and culture is what makes travel exciting for me.	I want to relax when I'm on holiday, and I disagree with those who say going to the beach is boring. Last year, a friend invited me on a hiking trip, but I declined. However, my perspective has changed, and now I'm planning to go hiking in the near future. This time, I'll closely follow the weather to ensure it doesn't spoil the trip.
\.


--
-- TOC entry 3509 (class 0 OID 16488)
-- Dependencies: 227
-- Data for Name: reading_part_4; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.reading_part_4 (question_id, exam_id, topic, paragraph, correct_answer, option1, option2, option3, option4, option5, option6, option7, option8) FROM stdin;
330	23	HOTEL	There are several types of vegetarian diets. Some people avoid all animal products, like vegans, while others, like lacto-vegetarians, eat dairy. Others, like ovo-vegetarians, include eggs. Many people also follow a pescatarian diet, which includes fish but no other meat. Each of these diets offers a variety of meals rich in fruits, vegetables, grains, and plant-based proteins.\n	C	The price of convenience may be high.	The benefits of living with less.	A sensible financial choice.	The importance of planning in advance.	The advantages of having your own space.	A competitive business.	The impact of lack of freedom.	A creative outlet of expressing emotions
331	23	HOTEL	The reasons behind dietary choices can be as diverse as the individuals making them. Many people opt for a vegetarian lifestyle due to ethical concerns, environmental awareness, or health considerations. Some may be motivated by cultural traditions or personal beliefs, while others seek new culinary experiences. Understanding these motivations fosters respectful discussions about food choices and their implications, promoting a more inclusive dialogue around dietary preferences.\n	A	The price of convenience may be high.	The benefits of living with less.	A sensible financial choice.	The importance of planning in advance.	The advantages of having your own space.	A competitive business.	The impact of lack of freedom.	A creative outlet of expressing emotions
332	23	HOTEL	As the global population continues to grow, concerns about food security and sustainability intensify. The increasing demand for resources puts immense pressure on agricultural systems, leading to potential shortages and rising prices. Without significant changes in our consumption patterns and food production methods, we may face a considerable crisis soon. This reality underscores the need for diverse dietary choices including vegetarian options, which can alleviate some of the pressure on our food systems.\n	D	The price of convenience may be high.	The benefits of living with less.	A sensible financial choice.	The importance of planning in advance.	The advantages of having your own space.	A competitive business.	The impact of lack of freedom.	A creative outlet of expressing emotions
333	23	HOTEL	The industrial approach to livestock production raises numerous ethical and environmental questions. Large-scale operations often prioritize efficiency over animal welfare, resulting in cramped living conditions and the overuse of antibiotics. This practice not only impacts the lives of animals but contributes to pollution and greenhouse gas emissions. As awareness of these issues grows, many advocates push for more humane and sustainable farming practices, which align better with the ethical motivations of those choosing plant-based diets.\n	G	The price of convenience may be high.	The benefits of living with less.	A sensible financial choice.	The importance of planning in advance.	The advantages of having your own space.	A competitive business.	The impact of lack of freedom.	A creative outlet of expressing emotions
334	23	HOTEL	In an interconnected world, our food consumption choices carry significant weight. Each individual's decisions can influence broader societal impacts, affecting everything from environmental sustainability to animal welfare. Embracing a sense of stewardship encourages us to consider how our eating habits impact not just our health, but also the health of the planet. By making conscious choices, such as incorporating more plant-based meals, we can collectively work towards a more equitable and sustainable future for all.\n	B	The price of convenience may be high.	The benefits of living with less.	A sensible financial choice.	The importance of planning in advance.	The advantages of having your own space.	A competitive business.	The impact of lack of freedom.	A creative outlet of expressing emotions
335	23	HOTEL	Opting for a diet rich in plant-based foods offers numerous advantages for overall well-being. Research suggests that a variety of fruits, vegetables, whole grains, and legumes can lower the risk of chronic diseases such as heart disease and diabetes. These foods are often high in essential nutrients and low in unhealthy fats. Embracing a more plant-centered way of eating not only supports personal health but also aligns with global sustainability efforts, enhancing vitality and energy levels for everyone.\n	E	The price of convenience may be high.	The benefits of living with less.	A sensible financial choice.	The importance of planning in advance.	The advantages of having your own space.	A competitive business.	The impact of lack of freedom.	A creative outlet of expressing emotions
336	23	HOTEL	Recognizing the intrinsic value of all living beings is essential for fostering a compassionate world. This perspective encourages reflection on our interactions with nature and other creatures, promoting empathy and kindness. By cultivating a mindset of respect, we can appreciate the interconnectedness of life and acknowledge the importance of coexisting harmoniously with all beings. Such an approach inspires actions that contribute to a more peaceful and sustainable planet, ultimately benefiting both individuals and society as a whole.\n	F	The price of convenience may be high.	The benefits of living with less.	A sensible financial choice.	The importance of planning in advance.	The advantages of having your own space.	A competitive business.	The impact of lack of freedom.	A creative outlet of expressing emotions
309	21	MEATLESS DIET	1. Nowadays, there are many delicious options for those who choose not to eat meat. From vibrant salads loaded with fresh vegetables to hearty grain bowls filled with quinoa and beans, the possibilities are endless. Creative recipes often incorporate a variety of fruits, nuts, and plant-based proteins, providing a satisfying array of flavors and textures. International cuisines, such as Indian curries or Mediterranean mezze, showcase the versatility of meat-free dining and highlight the diverse ways people can enjoy plant-based meals.	D	Respect to life	Various explanations behind dietary and preferences	Numerous health benefits of plant-based diets	Types of vegetarian meals	Our global responsibilities	The ethical and environmental implications of factory farming	Understanding the Possible global food crisis and it causes	 A sensible financial choice.
310	21	MEATLESS DIET	2. The reasons behind dietary choices can be as diverse as the individuals making them. Many people opt for a vegetarian lifestyle due to ethical concerns, environmental awareness, or health considerations. Some may be motivated by cultural traditions or personal beliefs, while others seek new culinary experiences. Understanding these motivations fosters respectful discussions about food choices and their implications, promoting a more inclusive dialogue around dietary preferences.	B	Respect to life	Various explanations behind dietary and preferences	Numerous health benefits of plant-based diets	Types of vegetarian meals	Our global responsibilities	The ethical and environmental implications of factory farming	Understanding the Possible global food crisis and it causes	 A sensible financial choice.
311	21	MEATLESS DIET	3. As the global population continues to grow, concerns about food security and sustainability intensify. The increasing demand for resources puts immense pressure on agricultural systems, leading to potential shortages and rising prices. Without significant changes in our consumption patterns and food production methods, we may face a considerable crisis soon. This reality underscores the need for diverse dietary choices including vegetarian options, which can alleviate some of the pressure on our food systems.	G	Respect to life	Various explanations behind dietary and preferences	Numerous health benefits of plant-based diets	Types of vegetarian meals	Our global responsibilities	The ethical and environmental implications of factory farming	Understanding the Possible global food crisis and it causes	 A sensible financial choice.
312	21	MEATLESS DIET	4. The industrial approach to livestock production raises numerous ethical and environmental questions. Large-scale operations often prioritize efficiency over animal welfare, resulting in cramped living conditions and the overuse of antibiotics. This practice not only impacts the lives of animals but contributes to pollution and greenhouse gas emissions. As awareness of these issues grows, many advocates push for more humane and sustainable farming practices, which align better with the ethical motivations of those choosing plant-based diets.	F	Respect to life	Various explanations behind dietary and preferences	Numerous health benefits of plant-based diets	Types of vegetarian meals	Our global responsibilities	The ethical and environmental implications of factory farming	Understanding the Possible global food crisis and it causes	 A sensible financial choice.
313	21	MEATLESS DIET	5. In an interconnected world, our food consumption choices carry significant weight. Each individual's decisions can influence broader societal impacts, affecting everything from environmental sustainability to animal welfare. Embracing a sense of stewardship encourages us to consider how our eating habits impact not just our health, but also the health of the planet. By making conscious choices, such as incorporating more plant-based meals, we can collectively work towards a more equitable and sustainable future for all.	E	Respect to life	Various explanations behind dietary and preferences	Numerous health benefits of plant-based diets	Types of vegetarian meals	Our global responsibilities	The ethical and environmental implications of factory farming	Understanding the Possible global food crisis and it causes	 A sensible financial choice.
260	14	BIBLIOGRAPHY OF CHARLES DICKENS	1. Charles Dickens's work remains remarkably popular today, much as it was in his own time. His captivating tales of wealth and poverty endure as timeless classics, brimming with characters who are both amusing and grotesque. These stories are often transformed into television series and films. Iconic figures like Oliver Twist, Scrooge, and Mrs. Gamp are so well-known that even those who haven't read his books can easily recognize them.\n	G	Keeping the readers guessing.	Dickens's early success.	The influence of the media.	Trying to protect his property.	Bring the books to life.	Difficulties for modern readers.	Dickens for our time.	Lack both knowledge and skills.\n
261	14	BIBLIOGRAPHY OF CHARLES DICKENS	2. One reason fewer people read Dickens's novels today is their considerable length. Books like Bleak House and Little Dorrit, each spanning roughly 900 pages, can feel intimidating. Additionally, Dickens's distinct writing style and the more complex language of his time, coupled with his detailed descriptions of characters and settings, make his works challenging for modern readers. As a result, many are discouraged from exploring his stories.\n	F	Keeping the readers guessing.	Dickens's early success.	The influence of the media.	Trying to protect his property.	Bring the books to life.	Difficulties for modern readers.	Dickens for our time.	Lack both knowledge and skills.\n
262	14	BIBLIOGRAPHY OF CHARLES DICKENS	3. The challenges that the average modern reader encounters with the novels Dickens wrote were not evident to the readers of his era. To start with, the books were published in serial form and appeared in easily digestible parts every month. Dickens was careful to conclude each installment with a dramatic moment and, like the writer of a modern-day soap opera, left his audience wondering what would happen next. His American readers were so eager to discover the fate of their favorite characters that they waited at New York harbor for the arrival of the latest chapters coming over from England by ship.\n	A	Keeping the readers guessing.	Dickens's early success.	The influence of the media.	Trying to protect his property.	Bring the books to life.	Difficulties for modern readers.	Dickens for our time.	Lack both knowledge and skills.\n
263	14	BIBLIOGRAPHY OF CHARLES DICKENS	4. Beyond writing novels, Dickens also worked as a reporter and editor, contributing to magazines and newspapers. The 19th century saw significant advancements in education, leading to a surge in literacy and a growing demand for printed material. Trained as a newspaper reporter, Dickens became proficient in shorthand and could write at an impressive pace, churning out pages on demand. With the public's endless appetite for sentiment and drama, Dickens had the energy and skill to deliver exactly what they craved.\n	C	Keeping the readers guessing.	Dickens's early success.	The influence of the media.	Trying to protect his property.	Bring the books to life.	Difficulties for modern readers.	Dickens for our time.	Lack both knowledge and skills.\n
264	14	BIBLIOGRAPHY OF CHARLES DICKENS	5. Dickens made his mark with his debut novel. The Pickwick Papers, published in book form when he was only 24 years old. Initially intended as a narrative to complement illustrations by the renowned artist Robert Seymour, the work quickly exceeded its original purpose. Its immense popularity turned it into an instant success, firmly establishing Dickens's reputation as a prominent writer.\n	B	Keeping the readers guessing.	Dickens's early success.	The influence of the media.	Trying to protect his property.	Bring the books to life.	Difficulties for modern readers.	Dickens for our time.	Lack both knowledge and skills.\n
265	14	BIBLIOGRAPHY OF CHARLES DICKENS	6. Despite his literary success, Charles Dickens faced challenges in safeguarding his intellectual property. During the Victorian era, copyright laws were weak allowing unauthorized adaptations of his work. Dickens was proactive in this regard, advocating for stronger copyright protections for authors. He believed writers deserved the same rights as inventors, emphasizing the need for legislative changes. His efforts not only aimed to protect his legacy but also sought to benefit future writers in an era of growing literary output.\n	D	Keeping the readers guessing.	Dickens's early success.	The influence of the media.	Trying to protect his property.	Bring the books to life.	Difficulties for modern readers.	Dickens for our time.	Lack both knowledge and skills.\n
266	14	BIBLIOGRAPHY OF CHARLES DICKENS	7. The lasting appeal of Dickens's novels lies in their adaptability across various media. Filmmakers and theater directors have embraced his rich narratives and complex characters, leading to numerous adaptations. His engaging plots and vivid descriptions make them ideal for visual storytelling. From plays to films, Dickens's themes of social justice and resilience resonate with contemporary audiences, ensuring his works remain relevant and vibrant in today's cultural landscape.\n	E	Keeping the readers guessing.	Dickens's early success.	The influence of the media.	Trying to protect his property.	Bring the books to life.	Difficulties for modern readers.	Dickens for our time.	Lack both knowledge and skills.\n
314	21	MEATLESS DIET	6. Opting for a diet rich in plant-based foods offers numerous advantages for overall well-being. Research suggests that a variety of fruits, vegetables, whole grains, and legumes can lower the risk of chronic diseases such as heart disease and diabetes. These foods are often high in essential nutrients and low in unhealthy fats. Embracing a more plant-centered way of eating not only supports personal health but also aligns with global sustainability efforts, enhancing vitality and energy levels for everyone.	C	Respect to life	Various explanations behind dietary and preferences	Numerous health benefits of plant-based diets	Types of vegetarian meals	Our global responsibilities	The ethical and environmental implications of factory farming	Understanding the Possible global food crisis and it causes	 A sensible financial choice.
315	21	MEATLESS DIET	7. Recognizing the intrinsic value of all living beings is essential for fostering a compassionate world. This perspective encourages reflection on our interactions with nature and other creatures, promoting empathy and kindness. By cultivating a mindset of respect, we can appreciate the interconnectedness of life and acknowledge the importance of coexisting harmoniously with all beings. Such an approach inspires actions that contribute to a more peaceful and sustainable planet, ultimately benefiting both individuals and society as a whole.	A	Respect to life	Various explanations behind dietary and preferences	Numerous health benefits of plant-based diets	Types of vegetarian meals	Our global responsibilities	The ethical and environmental implications of factory farming	Understanding the Possible global food crisis and it causes	 A sensible financial choice.
267	16	THE GOLDEN AGE OF TULIPS	During the period of the Dutch Golden Age, the port of Manchester was one of the wealthiest in all of Europe. This prosperity was in part due to the trade connections established by the Dutch East India Company, which transported luxury and exotic goods to Europe from Asia and beyond. Among the imported items, tulip bulbs made their way to Europe and quickly captured public attention, especially after their arrival in the bustling ports of the Netherlands. Tulips, with their striking colors and exotic appeal, soon became a symbol of status and luxury in Europe, especially as they gained popularity through trade at the prominent Manchester port.	C	 Coming into fashion.	Different types of tulip.	The economy during the golden age.	Trade across Europe.	An object of trade.	Trade mechanics.	An unexpected turn of events	The influence of the media.
268	16	THE GOLDEN AGE OF TULIPS	In 1593, studies conducted at Dutch universities revealed that tulips could survive the cold European climate, an insight that fueled the flower's popularity. Their vibrant and diverse colors stood out against the more subdued tones of European flora, making tulips a unique spectacle. As they gained popularity, tulips became a symbol of wealth and status, particularly in the Netherlands. This popularity spread quickly across Europe, establishing tulips as a highly desirable commodity and solidifying their reputation as a status symbol among the European elite.	A	 Coming into fashion.	Different types of tulip.	The economy during the golden age.	Trade across Europe.	An object of trade.	Trade mechanics.	An unexpected turn of events	The influence of the media.
269	16	THE GOLDEN AGE OF TULIPS	The demand for tulips surged, with collectors and merchants eagerly seeking the most colorful and unique blooms. Because tulips only bloomed during a limited season, from September to November, those who wanted tulips outside this window had to place orders in advance. This created a system of advance sales and pre-purchases, giving rise to a speculative market. This practice of pre-ordering tulips and trading contracts for their future delivery resembled modern-day options and futures trading in the financial markets, laying the groundwork for a complex market around these rare and exotic flowers.	E	 Coming into fashion.	Different types of tulip.	The economy during the golden age.	Trade across Europe.	An object of trade.	Trade mechanics.	An unexpected turn of events	The influence of the media.
270	16	THE GOLDEN AGE OF TULIPS	Tulip values varied greatly, depending on their rarity and color. Multi-colored tulips, especially those with striking patterns, commanded higher prices than solid-colored varieties. Of particular interest were tulips affected by a viral infection that caused beautiful flame-like patterns on the petals, known as "broken" tulips. These rare blooms were highly valued for their unique appearance and sold for premium prices. Since tulips were also susceptible to disease, their fragility and exclusivity made them a prized commodity, as any remaining tulips became even more desirable. 	B	 Coming into fashion.	Different types of tulip.	The economy during the golden age.	Trade across Europe.	An object of trade.	Trade mechanics.	An unexpected turn of events	The influence of the media.
271	16	THE GOLDEN AGE OF TULIPS	As the tulip market grew, prices skyrocketed. Merchants often held onto their bulbs, waiting to sell at inflated prices. Between 1634 and 1637, the value of certain tulips rose by up to sixty times their original price. Speculators poured increasing amounts of money into tulips, driven by the hope of reselling them at even higher prices. The speculative nature of the market led to an economic bubble, where the price of tulips continued to rise without any intrinsic reason beyond collective belief in their value.\n	F	 Coming into fashion.	Different types of tulip.	The economy during the golden age.	Trade across Europe.	An object of trade.	Trade mechanics.	An unexpected turn of events	The influence of the media.
272	16	THE GOLDEN AGE OF TULIPS	Tulip prices reached such extreme heights that they began to be traded on exchanges and even listed on stock markets. The general public, hoping to partake in the lucrative trade, flocked to purchase tulip bulbs. This speculative frenzy drew in a wide range of people, from merchants to commoners, all vying for a piece of what seemed like a guaranteed profitable investment. The tulip market became a cultural and economic phenomenon, with people from all backgrounds willing to invest their savings into tulips, expecting substantial returns.	D	 Coming into fashion.	Different types of tulip.	The economy during the golden age.	Trade across Europe.	An object of trade.	Trade mechanics.	An unexpected turn of events	The influence of the media.
273	16	THE GOLDEN AGE OF TULIPS	However, this bustling tulip market eventually reached its breaking point. As with many speculative bubbles, the tulip craze was unsustainable, and prices eventually began to plummet. Once people realized that tulip prices had risen far beyond reasonable levels, panic selling ensued, and the market collapsed. The dramatic fall in prices left many investors in financial ruin, as the value of tulips dwindled to a fraction of their peak. The tulip mania became one of history's most famous economic bubbles, offering a cautionary tale about the dangers of speculation and the risks inherent in market bubbles.	G	 Coming into fashion.	Different types of tulip.	The economy during the golden age.	Trade across Europe.	An object of trade.	Trade mechanics.	An unexpected turn of events	The influence of the media.
337	24	THE BENEFITS OF LEARNING INSTRUMENTS	Research indicates that children who play an instrument experience various positive effects. They become more engaged in school, leading to improved academic performance, especially in comprehension and math. Learning to play music also enhances their fine and gross motor skills and coordination. It can positively impact mental health and well-being and help with memory and social interactions. Moreover, playing an instrument fosters a sense of accomplishment, boosts confidence, and allows for self-expression in children. These benefits make learning music a wonderful experience for your child.\n	G	A great sense of well-being	Enhance sensitivity to others' feelings	A creative outlet of expressing emotions	A way to learn discipline and importance of routine	A great opportunity to broaden social circle	A good way to boost memory	A physically demanding activity	
338	24	THE BENEFITS OF LEARNING INSTRUMENTS	Learning and playing music has been linked to enhanced memory function. Memorizing sheet music, chords, and melodies exercises the brain, improving memory and cognitive abilities. The process of learning new pieces and practicing them regularly helps strengthen neural connections, leading to improved memory retention and recall in other areas of life as well.\n	F	A great sense of well-being	Enhance sensitivity to others' feelings	A creative outlet of expressing emotions	A way to learn discipline and importance of routine	A great opportunity to broaden social circle	A good way to boost memory	A physically demanding activity	
274	17	EATING IN CHINA (CHINESE FOOD)	The story of this cuisine stretches back thousands of years, shaped by local farming and customs. Early diets were simple, relying on grains and ingredients from nearby sources. Over time, different areas began to create their own flavors influenced by unique resources and historical events. Key foods, such as rice and noodles. became staples, adding depth to a rich culinary history that continues to evolve.\n	A	The origins of Chinese food.\n	Regional variations.\n	The influence of philosophy.\n	Cooking methods.\n	The style of eating.\n	Effects of a changing diet.\n	Changes in the Chinese diet.	The success of a simple idea
275	17	EATING IN CHINA (CHINESE FOOD)	Ancient ideas play a significant role in shaping attitudes toward food and meals. Concepts like balance and harmony are often reflected in how dishes are prepared and enjoyed, guiding choices in cooking. This backdrop helps create an environment where meals are not just about sustenance but also about connection and community, enriching the overall dining experience.\n	C	The origins of Chinese food.\n	Regional variations.\n	The influence of philosophy.\n	Cooking methods.\n	The style of eating.\n	Effects of a changing diet.\n	Changes in the Chinese diet.	The success of a simple idea
276	17	EATING IN CHINA (CHINESE FOOD)	The diverse geography of the country results in a wide range of culinary styles. Each area showcases distinct flavors based on local ingredients and traditions. For instance, the bold tastes found in one region can be quite different from the lighter fare in another. These variations highlight the richness of the culinary landscape. influenced by both local practices and cultural exchanges.\n	B	The origins of Chinese food.\n	Regional variations.\n	The influence of philosophy.\n	Cooking methods.\n	The style of eating.\n	Effects of a changing diet.\n	Changes in the Chinese diet.	The success of a simple idea
277	17	EATING IN CHINA (CHINESE FOOD)	A variety of cooking techniques are used that enhance the flavors of the ingredients. Quick methods, like stir-frying, keep vegetables crisp and fresh, while steaming helps maintain the natural taste and nutrients of food. Each technique serves to improve the overall eating experience, showing how versatile and innovative cooking can be.\n	D	The origins of Chinese food.\n	Regional variations.\n	The influence of philosophy.\n	Cooking methods.\n	The style of eating.\n	Effects of a changing diet.\n	Changes in the Chinese diet.	The success of a simple idea
278	17	EATING IN CHINA (CHINESE FOOD)	Dining is often approached as a communal experience, emphasizing sharing and togetherness. Meals are usually served in a way that allows everyone to sample different dishes, fostering conversation and connection among diners. The use of chopsticks adds an element of culture, making the act of eating feel more intentional and connected to tradition.\n	E	The origins of Chinese food.\n	Regional variations.\n	The influence of philosophy.\n	Cooking methods.\n	The style of eating.\n	Effects of a changing diet.\n	Changes in the Chinese diet.	The success of a simple idea
279	17	EATING IN CHINA (CHINESE FOOD)	Recent years have seen shifts in eating habits, influenced by modern lifestyles and global trends. While traditional foods remain important there's a growing interest in fast food and snacks, reflecting a blend of old and new practices. This evolution illustrates how culinary choices can change while still holding onto some aspects of the past.\n	G	The origins of Chinese food.\n	Regional variations.\n	The influence of philosophy.\n	Cooking methods.\n	The style of eating.\n	Effects of a changing diet.\n	Changes in the Chinese diet.	The success of a simple idea
280	17	EATING IN CHINA (CHINESE FOOD)	The shift in dietary habits carries various implications for health and cultural practices. Increased consumption of processed foods and sugary drinks has raised concerns, challenging long-held eating traditions. As younger generations lean towards convenience, there's a risk of losing valuable culinary knowledge. Balancing contemporary choices with traditional practices is essential for maintaining cultural integrity and promoting healthier lifestyles.\n	F	The origins of Chinese food.\n	Regional variations.\n	The influence of philosophy.\n	Cooking methods.\n	The style of eating.\n	Effects of a changing diet.\n	Changes in the Chinese diet.	The success of a simple idea
339	24	THE BENEFITS OF LEARNING INSTRUMENTS	Playing an instrument isn't only good for your brain, it's also a fantastic opportunity to connect with other like minded individuals. Joining a band, orchestra, or music group allows musicians to collaborate, share experiences, and develop friendships. Music also has a universal language, making it easier to communicate and connect with people from diverse backgrounds and cultures.\n	E	A great sense of well-being	Enhance sensitivity to others' feelings	A creative outlet of expressing emotions	A way to learn discipline and importance of routine	A great opportunity to broaden social circle	A good way to boost memory	A physically demanding activity	
340	24	THE BENEFITS OF LEARNING INSTRUMENTS	Unless you're an out-of-this-world child prodigy, learning to play an instrument isn't a skill you can master overnight. Learning music takes time and effort, and helps children understand that if they want to be good at something, they'll need to put in the hours and organize their time effectively. This disciplined approach fosters a strong work ethic patience, and perseverance that can be applied to other areas of life.\n	D	A great sense of well-being	Enhance sensitivity to others' feelings	A creative outlet of expressing emotions	A way to learn discipline and importance of routine	A great opportunity to broaden social circle	A good way to boost memory	A physically demanding activity	
341	24	THE BENEFITS OF LEARNING INSTRUMENTS	Music serves as a channel for individuals to express themselves and communicate in special ways. When kids learn to play an instrument, they can explore their inner world and share thoughts uniquely, even when they struggle to do so verbally. Additionally, playing music can be a form of stress relief. The act of playing an instrument requires concentration and focus, which can help children relax and unwind. It can also provide a healthy way to channel their emotions and energy.\n	C	A great sense of well-being	Enhance sensitivity to others' feelings	A creative outlet of expressing emotions	A way to learn discipline and importance of routine	A great opportunity to broaden social circle	A good way to boost memory	A physically demanding activity	
342	24	THE BENEFITS OF LEARNING INSTRUMENTS	Being a musician in a five-minute song requires physical and mental involvement, but emotional connection is even more crucial. It's not just about the music's mood but also our own feelings. Music develops focus, which helps in life. Research shows that music education improves emotional intelligence, understanding our emotions and others. Musicians learn to listen and cooperate with others, being attentive and adaptable. This fosters better appreciation of others' emotions and viewpoints.\n	B	A great sense of well-being	Enhance sensitivity to others' feelings	A creative outlet of expressing emotions	A way to learn discipline and importance of routine	A great opportunity to broaden social circle	A good way to boost memory	A physically demanding activity	
343	24	THE BENEFITS OF LEARNING INSTRUMENTS	Playing a musical instrument has been shown to help mental health by reducing stress, anxiety and depression. It requires all of your attention allowing you an escape from day-to-day stresses and creates a feeling of mindfulness and calm. Music releases dopamine, the feel-good chemical in the brain, so playing an instrument makes people happy! Factor in the sense of achievement you'll feel when you learn a new note or master a piece and you'll never have felt better.\n	A	A great sense of well-being	Enhance sensitivity to others' feelings	A creative outlet of expressing emotions	A way to learn discipline and importance of routine	A great opportunity to broaden social circle	A good way to boost memory	A physically demanding activity	
288	18	CHILDREN AND EXERCISE	1. In recent years, children have become increasingly inactive. While technology often receives blame for this trend, it is not the only factor at play. Urbanization has led to a lack of safe play spaces for kids. Many neighborhoods no longer have parks or playgrounds, forcing children to stay indoors. This combination of screen time and limited physical activity opportunities is contributing to a decline in children's overall fitness and health.	F	A design for exercise and for study\n	The success of a simple idea\n	Ways in which environment can influence behavior\n	Achieving the right balance	The situation has the potential of being worse	Factors contributing to inactivity	The wider effects of regular activity	Regional variations.\n
289	18	CHILDREN AND EXERCISE	2. Currently, the issue of children not getting enough exercise is worsening, largely due to the time they spend staring at screens. The allure of laptops and smartphones is hard to resist, making it difficult for both parents and children to limit their use. As awareness grows about the importance of physical activity, it is essential for everyone to recognize the seriousness of this problem and work together to find effective solutions that encourage a more active lifestyle.	E	A design for exercise and for study\n	The success of a simple idea\n	Ways in which environment can influence behavior\n	Achieving the right balance	The situation has the potential of being worse	Factors contributing to inactivity	The wider effects of regular activity	Regional variations.\n
190	9	TINY HOUSE	Choosing to live in a tiny house is a conscious decision to reduce your living space and simplify your life. By scaling down, people are often able to focus on what truly matters, eliminating unnecessary clutter and distractions. Living on a smaller scale also means fewer household responsibilities, allowing more time for personal interests and hobbies.	F	Homes are too big with few people.	Making a small impact.	Motivated to adapt to the situation.	Sharing skills with other people.	The lasting change.	Live on a small scale.	Advantages of Living in a Small House.	Disadvantages of small house. 
191	9	TINY HOUSE	One of the biggest challenges of moving into a tiny house is adapting to the limited space. This often requires a shift in mindset, learning to prioritize essentials and making creative use of every square inch. Those who successfully adapt often find that the constraints lead to a more intentional and mindful lifestyle, where each possession(quyền quyết định) and decision holds greater significance(ý nghĩa lớn hơn).	C	Homes are too big with few people.	Making a small impact.	Motivated to adapt to the situation.	Sharing skills with other people.	The lasting change.	Live on a small scale.	Advantages of Living in a Small House.	Disadvantages of small house. 
192	9	TINY HOUSE	There are numerous benefits to living in a tiny house, including reduced living costs, lower energy consumption, and a smaller environmental footprint. The simplicity(sự đơn giản) of a small home can lead to a more sustainable and financially secure lifestyle. Additionally, tiny houses often foster a sense of freedom, as they require less maintenance and offer more flexibility in terms of mobility and location.	G	Homes are too big with few people.	Making a small impact.	Motivated to adapt to the situation.	Sharing skills with other people.	The lasting change.	Live on a small scale.	Advantages of Living in a Small House.	Disadvantages of small house. 
193	9	TINY HOUSE	In contrast to tiny homes, many traditional houses are designed with far more space than is necessary, often leaving rooms unused and leading to waste. For small families or individuals, these large homes can feel empty and difficult to maintain, creating a disconnect between the amount of space available and the actual needs of the occupants.	A	Homes are too big with few people.	Making a small impact.	Motivated to adapt to the situation.	Sharing skills with other people.	The lasting change.	Live on a small scale.	Advantages of Living in a Small House.	Disadvantages of small house. 
194	9	TINY HOUSE	The tiny house community is known for its strong culture of collaboration and sharing. From building techniques to design tips, people often exchange knowledge and resources to help each other succeed in their small-space living endeavors. This sense of community is one of the most rewarding aspects of the tiny house lifestyle, fostering connections and mutual support among those who have chosen to downsize.	D	Homes are too big with few people.	Making a small impact.	Motivated to adapt to the situation.	Sharing skills with other people.	The lasting change.	Live on a small scale.	Advantages of Living in a Small House.	Disadvantages of small house. 
195	9	TINY HOUSE	Living in a tiny house might seem like a small, personal choice, but it can have a wider impact. By reducing their consumption and living more sustainably, tiny house residents contribute to larger environmental goals. Their commitment to minimalism and sustainability can inspire others to consider how their own living habits affect the planet.	B	Homes are too big with few people.	Making a small impact.	Motivated to adapt to the situation.	Sharing skills with other people.	The lasting change.	Live on a small scale.	Advantages of Living in a Small House.	Disadvantages of small house. 
196	9	TINY HOUSE	For many, the decision to move into a tiny house represents a profound and lasting change in their lives. It often goes beyond just the physical space, influencing how they spend their time, money, and energy. This shift in lifestyle can lead to more meaningful and fulfilling experiences, as people become more focused on what truly matters and less on material possessions.	E	Homes are too big with few people.	Making a small impact.	Motivated to adapt to the situation.	Sharing skills with other people.	The lasting change.	Live on a small scale.	Advantages of Living in a Small House.	Disadvantages of small house. 
290	18	CHILDREN AND EXERCISE	3. One inspiring example comes from a teacher who implemented a program called the Daily Mile. Each day, students are encouraged to run at least one mile, and this simple idea quickly gained popularity. It has won awards for its effectiveness and has spread to over 3,500 schools in more than 30 countries, thanks to media coverage and positive testimonials. This initiative highlights how even small changes can have a significant impact on promoting physical activity among children.	B	A design for exercise and for study\n	The success of a simple idea\n	Ways in which environment can influence behavior\n	Achieving the right balance	The situation has the potential of being worse	Factors contributing to inactivity	The wider effects of regular activity	Regional variations.\n
323	22	VEGETARIANS AND THEIR IMPACT ON THE WORLD	There are several types of vegetarian diets. Some people avoid all animal products, like vegans, while others, like lacto-vegetarians, eat dairy. Others, like ovo-vegetarians, include eggs. Many people also follow a pescatarian diet, which includes fish but no other meat. Each of these diets offers a variety of meals rich in fruits, vegetables, grains, and plant-based proteins.\n	A	Types of vegetarians.	Various explanations.	Factory farming - it is a harmful thing.	Respect to life.	Health gets better with diet.	Our global responsibilities 	Possible global food crisis	Result of a lucky escape.
324	22	VEGETARIANS AND THEIR IMPACT ON THE WORLD	The reasons behind dietary choices can be as diverse as the individuals making them. Many people opt for a vegetarian lifestyle due to ethical concerns, environmental awareness, or health considerations. Some may be motivated by cultural traditions or personal beliefs, while others seek new culinary experiences. Understanding these motivations fosters respectful discussions about food choices and their implications, promoting a more inclusive dialogue around dietary preferences.\n	B	Types of vegetarians.	Various explanations.	Factory farming - it is a harmful thing.	Respect to life.	Health gets better with diet.	Our global responsibilities 	Possible global food crisis	Result of a lucky escape.
325	22	VEGETARIANS AND THEIR IMPACT ON THE WORLD	As the global population continues to grow, concerns about food security and sustainability intensify. The increasing demand for resources puts immense pressure on agricultural systems, leading to potential shortages and rising prices. Without significant changes in our consumption patterns and food production methods, we may face a considerable crisis soon. This reality underscores the need for diverse dietary choices including vegetarian options, which can alleviate some of the pressure on our food systems.\n	G	Types of vegetarians.	Various explanations.	Factory farming - it is a harmful thing.	Respect to life.	Health gets better with diet.	Our global responsibilities 	Possible global food crisis	Result of a lucky escape.
197	10	ZOO	A long time ago, zoos were reserved exclusively for monarchs and aristocrats, showcasing a grand collection of rare and exotic animals as symbols of their richness and social status. These animals served not only as a display of wealth but also as diplomatic tools, where animals were exchanged as prestigious gifts among the wealthy elite. Kings and emperors delighted in possessing the most diverse and extraordinary creatures from faraway lands, reflecting their dominion over nature and their realm.\n	B	Opening the door for everyone\n	Symbol of privilege and wealth\n	Away from enclosure towards greater freedom\n	Away from amusement towards instruction\n	A modern-day alternative\n	A new mission of conservation\n	A different set of values\n	A different way to search 
198	10	ZOO	It wasn't until the reign of England's King John, in the early 13th century, that the concept of the zoo shifted dramatically. King John, a progressive ruler, opened the royal animal exhibit at the Tower of London to the public. This groundbreaking decision marked a turning point, as zoos gradually transitioned from being exclusive enclaves of royalty to inclusive spaces accessible to people from all walks of life. Zoos transformed into places where the general public could enjoy leisure and explore the wonders of the animal kingdom.\n	A	Opening the door for everyone\n	Symbol of privilege and wealth\n	Away from enclosure towards greater freedom\n	Away from amusement towards instruction\n	A modern-day alternative\n	A new mission of conservation\n	A different set of values\n	A different way to search 
199	10	ZOO	As societal beliefs progressed, zoos took on a more educational role. Conservation efforts gained strength, and zoos began to focus on raising awareness about endangered species and the importance of preserving biodiversity. The purpose of zoos extended beyond entertainment to provide valuable learning experiences. Modern zoos now prioritize animal welfare, creating environments that mimic natural habitats to ensure the well-being of their residents. Educational programs are designed to inform visitors about wildlife conservation, fostering a deeper appreciation for the natural world. \n	D	Opening the door for everyone\n	Symbol of privilege and wealth\n	Away from enclosure towards greater freedom\n	Away from amusement towards instruction\n	A modern-day alternative\n	A new mission of conservation\n	A different set of values\n	A different way to search 
200	10	ZOO	In the 19th century, there was a significant change in how zoos treated animals, thanks to the pioneering work of Carl Hagenbeck, a renowned German animal dealer and zoo founder. Hagenbeck completely transformed the way zoos were designed. Instead of confining animals in small cages and enclosures, he introduced the concept of open enclosures In these more naturalistic environments, animals had greater freedom to move around and express their natural behaviors. The shift from confinement to freedom not only improved the animals quality of life but also allowed visitors to observe animals in a more authentic setting.\n	C	Opening the door for everyone\n	Symbol of privilege and wealth\n	Away from enclosure towards greater freedom\n	Away from amusement towards instruction\n	A modern-day alternative\n	A new mission of conservation\n	A different set of values\n	A different way to search 
201	10	ZOO	As culture and ethics evolve, zoos are reevaluating their beliefs. Instead of solely showcasing rare and exotic animals, modern zoos are now stressing the significance of protecting biodiversity and the environment. Their goal is to encourage visitors to appreciate and care for all forms of life on Earth. Zoos are now working towards practices that prioritize animal welfare and conservation, encouraging a stronger sense of responsibility towards our planet.\n	G	Opening the door for everyone\n	Symbol of privilege and wealth\n	Away from enclosure towards greater freedom\n	Away from amusement towards instruction\n	A modern-day alternative\n	A new mission of conservation\n	A different set of values\n	A different way to search 
202	10	ZOO	As climate change and habitat destruction pose significant threats to wildlife, zoos have embraced a new mission - protecting animals on the brink of extinction. They play a crucial role in species recovery and act as sanctuaries for critically endangered creatures. Through dedicated conservation programs, zoos work tirelessly to ensure the survival and well-being of these vulnerable species. By taking a lead in conservation efforts, zoos aim to inspire visitors and the wider community to recognize the urgency of protecting our fragile ecosystems and the species that inhabit them.\n	F	Opening the door for everyone\n	Symbol of privilege and wealth\n	Away from enclosure towards greater freedom\n	Away from amusement towards instruction\n	A modern-day alternative\n	A new mission of conservation\n	A different set of values\n	A different way to search 
203	10	ZOO	While zoos have evolved to prioritize conservation and education, the question arises: Do modern humans still need zoos to learn about animals? Zoos aim to strike a delicate balance, simultaneously educating people. protecting animals, and ensuring their well-being. To achieve this, some zoos are exploring innovative approaches, such as virtual reality experiences and augmented reality exhibits, to offer visitors an immersive and educational experience without physical enclosure. By embracing these modern-life alternatives, zoos can effectively fulfill their educational objectives while also emphasizing the importance of animal welfare and freedom in their mission to protect and preserve wildlife.\n	E	Opening the door for everyone\n	Symbol of privilege and wealth\n	Away from enclosure towards greater freedom\n	Away from amusement towards instruction\n	A modern-day alternative\n	A new mission of conservation\n	A different set of values\n	A different way to search 
291	18	CHILDREN AND EXERCISE	4. The Daily Mile program not only enhances fitness levels among students but also has surprising benefits for their academic performance. Teachers have reported that students participating in this program are more focused and alert during lessons. Psychologists support this observation, suggesting that a healthy body leads to a healthy mind. The saying "a strong body, a strong mind" appears to hold true, as regular physical activity positively influences students' ability to learn and retain information.	G	A design for exercise and for study\n	The success of a simple idea\n	Ways in which environment can influence behavior\n	Achieving the right balance	The situation has the potential of being worse	Factors contributing to inactivity	The wider effects of regular activity	Regional variations.\n
292	18	CHILDREN AND EXERCISE	5. The design of our environments can significantly impact how we behave. For instance, workplaces are often designed to enhance productivity, and homes are structured to encourage communication. Similarly, schools can be designed to promote physical activity. By creating spaces that encourage movement, such as open areas for play and exercise, educators can foster a more active lifestyle among students, helping to counteract the trend of inactivity.	C	A design for exercise and for study\n	The success of a simple idea\n	Ways in which environment can influence behavior\n	Achieving the right balance	The situation has the potential of being worse	Factors contributing to inactivity	The wider effects of regular activity	Regional variations.\n
232	12	CONSUMER AGE OF THE 20TH CENTURY	In today's consumer-driven society, the focus is often on acquiring new products. However, adopting a more sustainable approach to consumption can have positive effects on the environment and our wallets.By ensuring proper maintenance and repair, we can extend the lifespan of things, leading to reduced waste and conserved resources. Companies can also play a crucial role by designing products with durability in mind, encouraging a shift towards a more eco-friendly and responsible consumer culture.\n	G	A temporary experiment.	The reason for secrecy.	Reason to reach a compromise.	The difficulty of being generous.	Important lessons for all of us.	Still relevant to our times.	Making things last longer.	A modern-day alternative
233	12	CONSUMER AGE OF THE 20TH CENTURY	Temporary consumption trends, like fad diets or fast fashion, are common in the modern world. While they might seem harmless, they can contribute to overconsumption and unnecessary waste. Being mindful of our consumption habits and avoiding temporary fads can help us make more sustainable choices. Opting for long-lasting, classic styles and sustainable products can reduce the negative impact of these fleeting trends on the environment.\n	A	A temporary experiment.	The reason for secrecy.	Reason to reach a compromise.	The difficulty of being generous.	Important lessons for all of us.	Still relevant to our times.	Making things last longer.	A modern-day alternative
234	12	CONSUMER AGE OF THE 20TH CENTURY	In some instances, luxurious consumption has become a social status symbol. People may feel pressured to show off their wealth by purchasing luxury items, even if they don't really need them. This behavior can be harmful to the environment and lead to financial strain. Encouraging a culture of modesty and frugality can counteract the negative effects of conspicuous consumption, promoting a more sustainable and equitable society.\n	B	A temporary experiment.	The reason for secrecy.	Reason to reach a compromise.	The difficulty of being generous.	Important lessons for all of us.	Still relevant to our times.	Making things last longer.	A modern-day alternative
204	11	COFFEE	The custom of drinking coffee started in the 1500s. Around that time, cafés began to open in places like Egypt and Ethiopia, though coffee was banned before that. Later, coffee made its way to Italy and spread throughout Europe. The Dutch even introduced coffee to Asia. Over time, drinking coffee became a common habit in many parts of the world, bringing people together in new ways.	C	The ancient origin of coffee.	Coffee encourages.	The custom of coffee drinking begins to spread.	A habit that has become a big economy.	The Health risks versus health benefits debate.	Problems of the coffee economy.	A remedy of unjust revenue distribution.	A modern-day alternative
205	11	COFFEE	Europe is known as the biggest coffee-drinking region. In the 18th century, writers, philosophers, and politicians used coffee as a way to stay alert during intense discussions or meetings. Coffeehouses became popular meeting spots where people shared ideas and debated important topics. These places helped encourage the exchange of intellectual thoughts and played a key role in business and social life at the time.	B	The ancient origin of coffee.	Coffee encourages.	The custom of coffee drinking begins to spread.	A habit that has become a big economy.	The Health risks versus health benefits debate.	Problems of the coffee economy.	A remedy of unjust revenue distribution.	A modern-day alternative
206	11	COFFEE	Today, many people drink coffee in the morning to wake up, or in the evening to socialize after work. Coffeehouses are everywhere, offering places to chat and relax. Coffee has grown into a global business, with coffee machines even sold for private homes. Famous global brands have become well-known for their coffee, using strong branding and marketing strategies to attract millions of coffee lovers worldwide.	D	The ancient origin of coffee.	Coffee encourages.	The custom of coffee drinking begins to spread.	A habit that has become a big economy.	The Health risks versus health benefits debate.	Problems of the coffee economy.	A remedy of unjust revenue distribution.	A modern-day alternative
207	11	COFFEE	Europe consumes 90% of the world's coffee production, making it the largest market. Countries like Egypt and Ethiopia rely heavily on exporting coffee to support their economies. However, there is an issue of inequality: workers in coffee-producing countries often face poor working and living conditions. While coffee brings in money for these nations, the people producing it don't always receive fair pay for their hard work.	F	The ancient origin of coffee.	Coffee encourages.	The custom of coffee drinking begins to spread.	A habit that has become a big economy.	The Health risks versus health benefits debate.	Problems of the coffee economy.	A remedy of unjust revenue distribution.	A modern-day alternative
208	11	COFFEE	To address these inequalities, certification programs for agricultural products were introduced. If coffee meets certain certification standards, it can be sold at a fair price, preventing it from being sold too cheaply. However, critics argue that only about 5% of coffee gets certified. Many small coffee producers are too poor to afford the certification fees, which keeps them even further behind in the global market.	G	The ancient origin of coffee.	Coffee encourages.	The custom of coffee drinking begins to spread.	A habit that has become a big economy.	The Health risks versus health benefits debate.	Problems of the coffee economy.	A remedy of unjust revenue distribution.	A modern-day alternative
209	11	COFFEE	Coffee has several benefits. It contains antioxidants, which can help prevent diseases. However, there are also some risks. It is not recommended to drink coffee with added flavors or sweeteners because these can be harmful to your health. If you drink pure black coffee, it's usually fine. Just remember to avoid adding too many unhealthy ingredients to your cup of coffee to stay on the safe side.	E	The ancient origin of coffee.	Coffee encourages.	The custom of coffee drinking begins to spread.	A habit that has become a big economy.	The Health risks versus health benefits debate.	Problems of the coffee economy.	A remedy of unjust revenue distribution.	A modern-day alternative
210	11	COFFEE	According to legend, a man in an old country once visited another land where he saw a bird eating coffee beans. The bird became much more active than usual. Curious, the man decided to try the beans himself. After eating them, he felt more energetic and awake. This was how he discovered the amazing effects of coffee, which eventually became known to the rest of the world. 	A	The ancient origin of coffee.	Coffee encourages.	The custom of coffee drinking begins to spread.	A habit that has become a big economy.	The Health risks versus health benefits debate.	Problems of the coffee economy.	A remedy of unjust revenue distribution.	A modern-day alternative
293	18	CHILDREN AND EXERCISE	6. One innovative architect from Japan has designed a kindergarten with a unique approach. The playground is structured like a running track, allowing children to run and play freely. This creative design has proven successful and has even received awards for its impact on children's activity levels. Such thoughtful architectural designs can inspire other schools to rethink how they create environments that promote both learning and physical activity.	A	A design for exercise and for study\n	The success of a simple idea\n	Ways in which environment can influence behavior\n	Achieving the right balance	The situation has the potential of being worse	Factors contributing to inactivity	The wider effects of regular activity	Regional variations.\n
294	18	CHILDREN AND EXERCISE	7. The Daily Mile initiative and the Japanese architect's playground represent two ends of the economic spectrum. The Daily Mile is a cost-effective program that requires minimal investment, while the architect's design involves significant funding. Local authorities must consider various factors when striving for a balance between promoting physical activity and managing budgets. By exploring both affordable and innovative solutions, communities can create environments that support children's health and well-being.	D	A design for exercise and for study\n	The success of a simple idea\n	Ways in which environment can influence behavior\n	Achieving the right balance	The situation has the potential of being worse	Factors contributing to inactivity	The wider effects of regular activity	Regional variations.\n
326	22	VEGETARIANS AND THEIR IMPACT ON THE WORLD	The industrial approach to livestock production raises numerous ethical and environmental questions. Large-scale operations often prioritize efficiency over animal welfare, resulting in cramped living conditions and the overuse of antibiotics. This practice not only impacts the lives of animals but contributes to pollution and greenhouse gas emissions. As awareness of these issues grows, many advocates push for more humane and sustainable farming practices, which align better with the ethical motivations of those choosing plant-based diets.\n	C	Types of vegetarians.	Various explanations.	Factory farming - it is a harmful thing.	Respect to life.	Health gets better with diet.	Our global responsibilities 	Possible global food crisis	Result of a lucky escape.
295	19	ANTARCTICA - FROZEN LAND	This continent is governed by an international agreement known as the Antarctic Treaty System, established in 1961. This treaty ensures that the region is utilized for peaceful purposes and encourages global scientific collaboration. While no nation officially owns this land, several countries-Argentina, Australia, Chile, France, New Zealand, Norway, and the United Kingdom-assert territorial claims. The treaty forbids military activity, resource extraction, and nuclear tests, designating the area for research and conservation efforts. As a result, scientists from various countries gather to study this unique environment, sharing their discoveries for the benefit of humanity.\n	D	Where is the end of the Earth?	Why is it so cold?	First step on the ice.	Who is in charge?	Race to the Pole.	Less effort needed.	Hidden geography.	Achieving the right balance
296	19	ANTARCTICA - FROZEN LAND	Setting foot on Antarctica is a significant event for any explorer or scientist. The journey typically begins in South America, where travelers board a ship or a plane to cross the Drake Passage. Once they arrive, the first step on the ice is both exhilarating and daunting. Visitors are immediately struck by the vast expanse of white. the crisp, cold air, and the breathtaking scenery. The sound of crunching ice underfoot serves as a reminder of the remote and untouched nature of this continent, a place where human footprints are few and far between.\n	C	Where is the end of the Earth?	Why is it so cold?	First step on the ice.	Who is in charge?	Race to the Pole.	Less effort needed.	Hidden geography.	Achieving the right balance
235	12	CONSUMER AGE OF THE 20TH CENTURY	Despite the rise of digital media and online streaming, physical books, vinyl records, and other tangible goods still hold value to many. Some people find joy in collecting items that have sentimental significance or represent their interests. Balancing these interests with mindful consumption can lead to a more meaningful and less wasteful lifestyle, as appreciating and caring for possessions can extend their lifespan and reduce the need for frequent replacements.\n	F	A temporary experiment.	The reason for secrecy.	Reason to reach a compromise.	The difficulty of being generous.	Important lessons for all of us.	Still relevant to our times.	Making things last longer.	A modern-day alternative
236	12	CONSUMER AGE OF THE 20TH CENTURY	In a world driven by consumerism, practicing generosity can be challenging. We may feel compelled to constantly acquire more for ourselves, making it hard to prioritize giving to others or supporting charitable causes. However, embracing a more generous mindset can bring about a sense of fulfillment and happiness. By focusing on giving rather than accumulating, we can contribute positively to society and make a difference in the lives of others.\n	D	A temporary experiment.	The reason for secrecy.	Reason to reach a compromise.	The difficulty of being generous.	Important lessons for all of us.	Still relevant to our times.	Making things last longer.	A modern-day alternative
237	12	CONSUMER AGE OF THE 20TH CENTURY	As consumers, we often face choices that involve making compromises. Balancing our desires for convenience and luxury with the need for sustainability and responsible consumption can be tough. However, making thoughtful compromises can help us strike a balance between personal enjoyment and environmental impact. Opting for eco-friendly alternatives, even if they require some adjustments, can lead to a more sustainable lifestyle that benefits both ourselves and the planet.\n	C	A temporary experiment.	The reason for secrecy.	Reason to reach a compromise.	The difficulty of being generous.	Important lessons for all of us.	Still relevant to our times.	Making things last longer.	A modern-day alternative
238	12	CONSUMER AGE OF THE 20TH CENTURY	Consumption has a profound impact on our lives and the environment. By making conscious choices, such as making things last longer, resisting temporary trends, and being mindful of the true value of possessions, we can promote sustainability and reduce waste. Additionally, learning to be generous and making thoughtful compromises can lead to a more fulfilling and responsible consumer culture. As consumers, each one of us has the power to shape the future and create a more sustainable world for generations to come.\n	E	A temporary experiment.	The reason for secrecy.	Reason to reach a compromise.	The difficulty of being generous.	Important lessons for all of us.	Still relevant to our times.	Making things last longer.	A modern-day alternative
297	19	ANTARCTICA - FROZEN LAND	Positioned around the South Pole, Antarctica represents the southernmost point on the planet. The continent's remoteness contributes to its mystique, drawing adventurers and researchers alike. The harsh conditions, including bitter cold and relentless winds, create a sense of otherworldliness. In many ways, it feels like the last frontier on Earth, where the landscape remains largely unspoiled and the natural world thrives in its purest form. \n	A	Where is the end of the Earth?	Why is it so cold?	First step on the ice.	Who is in charge?	Race to the Pole.	Less effort needed.	Hidden geography.	Achieving the right balance
298	19	ANTARCTICA - FROZEN LAND	Beneath the massive ice sheets lies a concealed landscape that reveals much about the planet's geological history. This region hosts the largest ice mass globally, covering approximately 98 percent of its area. The ice conceals a variety of geological features, including mountains and valleys. Researchers analyze ice cores extracted from deep within the layers to uncover details about past climates and atmospheric conditions. These investigations provide vital information for understanding global climate change and its potential implications for our world.\n	G	Where is the end of the Earth?	Why is it so cold?	First step on the ice.	Who is in charge?	Race to the Pole.	Less effort needed.	Hidden geography.	Achieving the right balance
299	19	ANTARCTICA - FROZEN LAND	The pursuit of the southernmost point in the early 20th century captivated many. Adventurers such as Robert Falcon Scott and Roald Amundsen undertook perilous journeys to achieve this milestone. Amundsen's successful expedition in 1911 marked a significant achievement in exploration, while Scott's tragic story underscored the risks associated with such endeavors. These tales of courage and ambition continue to inspire modern explorers, highlighting the fascination that this harsh terrain holds.\n	E	Where is the end of the Earth?	Why is it so cold?	First step on the ice.	Who is in charge?	Race to the Pole.	Less effort needed.	Hidden geography.	Achieving the right balance
300	19	ANTARCTICA - FROZEN LAND	Recent advancements in technology have made reaching this icy expanse easier than in the past. Modern icebreakers and advanced aircraft enable safer and more efficient travel. This accessibility has led to a rise in interest for tourism, allowing more people to experience the breathtaking beauty of the landscape. However, the increase in visitors raises concerns about the potential environmental impact, emphasizing the necessity for sustainable practices to safeguard this delicate ecosystem.\n	F	Where is the end of the Earth?	Why is it so cold?	First step on the ice.	Who is in charge?	Race to the Pole.	Less effort needed.	Hidden geography.	Achieving the right balance
301	19	ANTARCTICA - FROZEN LAND	The extreme low temperatures in this region result mainly from its high elevation and geographic positioning. Being located over the South Pole means it receives minimal direct sunlight, especially during the prolonged winter months of darkness. Average temperatures can plummet below -60°C (-76°F), with summer still remaining quite frigid. The reflective nature of ice further contributes to the chilling climate. Understanding these climatic influences is crucial for scientists studying global weather systems and shifts in climate patterns.\n	B	Where is the end of the Earth?	Why is it so cold?	First step on the ice.	Who is in charge?	Race to the Pole.	Less effort needed.	Hidden geography.	Achieving the right balance
327	22	VEGETARIANS AND THEIR IMPACT ON THE WORLD	In an interconnected world, our food consumption choices carry significant weight. Each individual's decisions can influence broader societal impacts, affecting everything from environmental sustainability to animal welfare. Embracing a sense of stewardship encourages us to consider how our eating habits impact not just our health, but also the health of the planet. By making conscious choices, such as incorporating more plant-based meals, we can collectively work towards a more equitable and sustainable future for all.\n	F	Types of vegetarians.	Various explanations.	Factory farming - it is a harmful thing.	Respect to life.	Health gets better with diet.	Our global responsibilities 	Possible global food crisis	Result of a lucky escape.
302	20	DOGGETT'S COAT AND BADGE	A. Doggett's Coat and Badge, an annual rowing race held on the River Thames, offers an interesting insight into traditional British sporting events. The race is known for being one of the oldest surviving rowing contests in the world, dating back to 1715. Since the race is held on the Thames itself, the most convenient ways to get to the event are by riverboat or on foot. Spectators can enjoy the event from various points along the river, making it accessible to many who wish to witness this historic competition.\n	G	Origins of what the winner receives.	Generations of champions.	Earning a reputation.	A need for change.	Not in it for the money.	Result of a lucky escape.	The easiest way to travel	The success of a simple idea
303	20	DOGGETT'S COAT AND BADGE	B. Because the circumstances on the River Thames can be unexpected, the fate of the race can occasionally depend on a fortunate survival. Weather, river currents, and other factors can all influence the performance of the rowers. Competitors often have to navigate these challenges skillfully, and those who manage to adapt and overcome difficult circumstances can gain an advantage in the race.\n	F	Origins of what the winner receives.	Generations of champions.	Earning a reputation.	A need for change.	Not in it for the money.	Result of a lucky escape.	The easiest way to travel	The success of a simple idea
246	13	THE EARLY AUSTRALIA	1. The history of early Australians stretches back much further than previously believed, with evidence suggesting human presence on the Australian continent dating back approximately 65,00 years. This timeline challenges traditional views held by historians regarding the first human settlers in Australia. Carbon analysis of archaeological sites has provided different results, leading to alternative hypotheses about the early inhabitants of the land Down Under. The findings shed new light on the ancient origins and rich cultural heritage of the Indigenous people who have inhabited the continent for millennia. \n	F	No precise figures available.\n	The determination of the explorers in ages.\n	Natural barrier to resettlement.\n	Lack both knowledge and skills.\n	A Journey made in stages\n	New evidence to speculation.\n	Technology helps uncover the sea's secrets.\n	Important lessons for all of us.
247	13	THE EARLY AUSTRALIA	2. Recent discoveries have revealed that the settlement of Australia was not a singular event. In addition to the early settlers, scientists have uncovered traces of two other human groups that migrated to the continent. The presence of multiple groups suggests a complex history of human migration and interaction. However, reaching the isolated continent would have posed significant challenges for ancient humans, as they would have needed to traverse vast stretches of open sea, a feat seemingly impossible with the technology available to them at the time.\n	C	No precise figures available.\n	The determination of the explorers in ages.\n	Natural barrier to resettlement.\n	Lack both knowledge and skills.\n	A Journey made in stages\n	New evidence to speculation.\n	Technology helps uncover the sea's secrets.\n	Important lessons for all of us.
248	13	THE EARLY AUSTRALIA	3. The aid of advanced equipment and techniques has allowed scientists to identify a series of small islands closely connected, forming a continuous pathway leading to Australia. Remote sensing technology has helped researchers identify and map small islands and potential migration routes. Geographic Information Systems (GIS) have integrated various data sets, to discover about the past migration corridors. This discovery provides insight into the probable routes taken by ancient migrants as they ventured across the vast expanse of the sea, providing a deeper understanding of the complex migration patterns that shaped the early history of the continent.\n	G	No precise figures available.\n	The determination of the explorers in ages.\n	Natural barrier to resettlement.\n	Lack both knowledge and skills.\n	A Journey made in stages\n	New evidence to speculation.\n	Technology helps uncover the sea's secrets.\n	Important lessons for all of us.
249	13	THE EARLY AUSTRALIA	4. The migration patterns of early Australians reveal a gradual journey to the continent. Archaeological evidence points to the likelihood of different tribes arriving in Australia through a series of island-hopping journeys. Each island served as a resting point and a source of food, allowing them to continue their voyage. This gradual movement indicates an adaptive and resourceful approach taken by these ancient tribes, who navigated the challenges of the terrain to ultimately settle in Australia.\n	E	No precise figures available.\n	The determination of the explorers in ages.\n	Natural barrier to resettlement.\n	Lack both knowledge and skills.\n	A Journey made in stages\n	New evidence to speculation.\n	Technology helps uncover the sea's secrets.\n	Important lessons for all of us.
250	13	THE EARLY AUSTRALIA	5. Scientists can only speculate about the exact number of individuals required to undertake such a migration, which could have ranged from a small group to several thousand people. The uncertainty stems from various factors, including the limitations of available archaeological evidence and the complexities of ancient human migration. The lack of exact statistics makes it challenging to determine the scale and composition of these early human journeys accurately. However, ongoing research and technological advancements may offer more insights in the future.	A	No precise figures available.\n	The determination of the explorers in ages.\n	Natural barrier to resettlement.\n	Lack both knowledge and skills.\n	A Journey made in stages\n	New evidence to speculation.\n	Technology helps uncover the sea's secrets.\n	Important lessons for all of us.
251	13	THE EARLY AUSTRALIA	6. Some skeptics argue that ancient humans didn't have enough the intellectual capacity, knowledge, and skills needed to undertake such journeys. They question whether early humans possessed the navigational and maritime expertise to traverse vast stretches of ocean. Critics contend that without advanced tools or navigational aids, navigating through open seas would have been beyond the capabilities of ancient civilizations, However, it is crucial to acknowledge that human ingenuity and adaptability have proven remarkable throughout history, enabling our ancestors to overcome various challenges and achieve extraordinary feats.\n	D	No precise figures available.\n	The determination of the explorers in ages.\n	Natural barrier to resettlement.\n	Lack both knowledge and skills.\n	A Journey made in stages\n	New evidence to speculation.\n	Technology helps uncover the sea's secrets.\n	Important lessons for all of us.
304	20	DOGGETT'S COAT AND BADGE	C. There is a longstanding custom that informs what the champion of Doggett's Coat and Badge obtains. The race was originally established to commemorate the 18th-century waterman and lighterman Thomas Doggett. The prize, which includes a distinctive coat and badge, symbolizes the legacy of Doggett and his contribution to the river trade. The coat and badge have become iconic symbols of the race, representing the honor and tradition of winning this prestigious event.\n	A	Origins of what the winner receives.	Generations of champions.	Earning a reputation.	A need for change.	Not in it for the money.	Result of a lucky escape.	The easiest way to travel	The success of a simple idea
252	13	THE EARLY AUSTRALIA	7. History has demonstrated the unwavering determination and resilience of human explorers in the past. From deep-sea expeditions in ancient times to modern space travel, humans have showcased their resolve to explore and conquer the unknown. The same determination might have driven the early Australians to embark on perilous journeys across treacherous waters. While the challenges they faced were undoubtedly immense, the spirit of human curiosity and the desire to discover new lands and opportunities likely motivated these ancient explorers, leaving a remarkable legacy in the annals of history.\n	B	No precise figures available.\n	The determination of the explorers in ages.\n	Natural barrier to resettlement.\n	Lack both knowledge and skills.\n	A Journey made in stages\n	New evidence to speculation.\n	Technology helps uncover the sea's secrets.\n	Important lessons for all of us.
305	20	DOGGETT'S COAT AND BADGE	D. As the tournament developed over time, it became apparent that the event's framework was required to adapt. Originally open only to watermen and lightermen, the race eventually became more inclusive, allowing a broader range of competitors. This change was driven by the desire to keep the race relevant and engaging, ensuring that it continued to attract skilled rowers and maintain its historical significance in a modern context.\n	D	Origins of what the winner receives.	Generations of champions.	Earning a reputation.	A need for change.	Not in it for the money.	Result of a lucky escape.	The easiest way to travel	The success of a simple idea
306	20	DOGGETT'S COAT AND BADGE	E. Gaining recognition in Doggett's Coat and Badge requires not only winning the race but also demonstrating exceptional skill and sportsmanship. The event is highly regarded in the rowing community, and participants who perform well in the race build a reputation for excellence. The challenge of competing in such a historic event adds to the prestige of the race and the honor associated with succeeding in it.\n	C	Origins of what the winner receives.	Generations of champions.	Earning a reputation.	A need for change.	Not in it for the money.	Result of a lucky escape.	The easiest way to travel	The success of a simple idea
307	20	DOGGETT'S COAT AND BADGE	F. Doggett's Coat and Badge has been a part of centuries of champions; many families have had multiple members who have competed and won the race over the years. This tradition of passing down the competitive spirit highlights the enduring appeal of the event and the commitment of those involved. Each new champion adds to the rich history of the race, continuing the legacy established by previous winners.	B	Origins of what the winner receives.	Generations of champions.	Earning a reputation.	A need for change.	Not in it for the money.	Result of a lucky escape.	The easiest way to travel	The success of a simple idea
308	20	DOGGETT'S COAT AND BADGE	G. The fact that many competitors have no interest in it for their financial gain contributes to the race's appeal. While there are prizes, the primary motivation for many rowers is the honor of competing in such a historic event and the challenge it presents. The emphasis on tradition, skill, and personal achievement over financial reward underscores the cultural significance of Doggett's Coat and Badge.\n	E	Origins of what the winner receives.	Generations of champions.	Earning a reputation.	A need for change.	Not in it for the money.	Result of a lucky escape.	The easiest way to travel	The success of a simple idea
328	22	VEGETARIANS AND THEIR IMPACT ON THE WORLD	Opting for a diet rich in plant-based foods offers numerous advantages for overall well-being. Research suggests that a variety of fruits, vegetables, whole grains, and legumes can lower the risk of chronic diseases such as heart disease and diabetes. These foods are often high in essential nutrients and low in unhealthy fats. Embracing a more plant-centered way of eating not only supports personal health but also aligns with global sustainability efforts, enhancing vitality and energy levels for everyone.\n	E	Types of vegetarians.	Various explanations.	Factory farming - it is a harmful thing.	Respect to life.	Health gets better with diet.	Our global responsibilities 	Possible global food crisis	Result of a lucky escape.
329	22	VEGETARIANS AND THEIR IMPACT ON THE WORLD	Recognizing the intrinsic value of all living beings is essential for fostering a compassionate world. This perspective encourages reflection on our interactions with nature and other creatures, promoting empathy and kindness. By cultivating a mindset of respect, we can appreciate the interconnectedness of life and acknowledge the importance of coexisting harmoniously with all beings. Such an approach inspires actions that contribute to a more peaceful and sustainable planet, ultimately benefiting both individuals and society as a whole.\n	D	Types of vegetarians.	Various explanations.	Factory farming - it is a harmful thing.	Respect to life.	Health gets better with diet.	Our global responsibilities 	Possible global food crisis	Result of a lucky escape.
\.


--
-- TOC entry 3521 (class 0 OID 16595)
-- Dependencies: 239
-- Data for Name: speaking; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.speaking (id, exam_id, part_id, topic, instruction, instruction_audio, question, image_path1, image_path2) FROM stdin;
\.


--
-- TOC entry 3497 (class 0 OID 16390)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, username, password_hash, fullname, phone_number, role, is_active, created_at, updated_at) FROM stdin;
1	admin	$2b$12$iKvSqbG/Mg.9I/VrVSBfM.fUWTvb/Oj7WJe1PCZC0kGCDB7bROE6e	Administrator	\N	admin	t	2025-06-24 14:46:29.331682	2025-06-24 14:46:29.331682
2	Phuc32	$2b$12$5gKOfZEd4jyYHxlGxrIXJuYx8dCxfIBayGct/tOCxG7QMyrywEf2G	Nguyen Hoang Phuc 	0337772756	member	t	2025-06-24 15:15:15.317489	2025-06-24 15:15:15.317489
6	Lanhuong	$2b$12$cQ4emu.0ZGBdh28lDIaAKuioyXjw/QN/9OUQWzOP8xlkSdgJNpHWi	Lan Hương 	033551111344	member	t	2025-06-28 01:42:20.837041	2025-06-28 01:43:45.29265
7	thanhtuyen	$2b$12$oEzF9wYReL77wfO/HG63bOAFKNUfXh.wJurFHOr4p1PTuvqYR4m4O	Thanh Tuyền 	033124225512	member	t	2025-06-28 01:44:40.670201	2025-06-28 01:44:40.670201
8	nguyenthithitho	$2b$12$S4UvyxkwPPmDEGMa8caNDO4pWIGwf.L/I9BTORoGyGs5vC7eNqsOG	Nguyễn Thị Thi Thơ 	03333222564	member	t	2025-06-28 01:50:17.190811	2025-06-28 01:50:17.190811
\.


--
-- TOC entry 3523 (class 0 OID 16609)
-- Dependencies: 241
-- Data for Name: writing; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.writing (id, exam_id, part_id, topic, instruction, questions) FROM stdin;
\.


--
-- TOC entry 3546 (class 0 OID 0)
-- Dependencies: 216
-- Name: exam_sets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.exam_sets_id_seq', 31, true);


--
-- TOC entry 3547 (class 0 OID 0)
-- Dependencies: 242
-- Name: exam_submission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.exam_submission_id_seq', 1, false);


--
-- TOC entry 3548 (class 0 OID 0)
-- Dependencies: 218
-- Name: exams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.exams_id_seq', 46, true);


--
-- TOC entry 3549 (class 0 OID 0)
-- Dependencies: 236
-- Name: guest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.guest_id_seq', 2, true);


--
-- TOC entry 3550 (class 0 OID 0)
-- Dependencies: 228
-- Name: listening_part_1_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.listening_part_1_id_seq', 383, true);


--
-- TOC entry 3551 (class 0 OID 0)
-- Dependencies: 230
-- Name: listening_part_2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.listening_part_2_id_seq', 23, true);


--
-- TOC entry 3552 (class 0 OID 0)
-- Dependencies: 232
-- Name: listening_part_3_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.listening_part_3_id_seq', 92, true);


--
-- TOC entry 3553 (class 0 OID 0)
-- Dependencies: 234
-- Name: listening_part_4_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.listening_part_4_id_seq', 92, true);


--
-- TOC entry 3554 (class 0 OID 0)
-- Dependencies: 220
-- Name: reading_part_1_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.reading_part_1_question_id_seq', 243, true);


--
-- TOC entry 3555 (class 0 OID 0)
-- Dependencies: 222
-- Name: reading_part_2_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.reading_part_2_question_id_seq', 494, true);


--
-- TOC entry 3556 (class 0 OID 0)
-- Dependencies: 224
-- Name: reading_part_3_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.reading_part_3_question_id_seq', 357, true);


--
-- TOC entry 3557 (class 0 OID 0)
-- Dependencies: 226
-- Name: reading_part_4_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.reading_part_4_question_id_seq', 343, true);


--
-- TOC entry 3558 (class 0 OID 0)
-- Dependencies: 238
-- Name: speaking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.speaking_id_seq', 1, false);


--
-- TOC entry 3559 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- TOC entry 3560 (class 0 OID 0)
-- Dependencies: 240
-- Name: writing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.writing_id_seq', 1, false);


--
-- TOC entry 3308 (class 2606 OID 16412)
-- Name: exam_sets exam_sets_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_sets
    ADD CONSTRAINT exam_sets_pkey PRIMARY KEY (id);


--
-- TOC entry 3310 (class 2606 OID 16414)
-- Name: exam_sets exam_sets_set_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_sets
    ADD CONSTRAINT exam_sets_set_code_key UNIQUE (set_code);


--
-- TOC entry 3338 (class 2606 OID 16633)
-- Name: exam_submission exam_submission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_submission
    ADD CONSTRAINT exam_submission_pkey PRIMARY KEY (id);


--
-- TOC entry 3312 (class 2606 OID 16433)
-- Name: exams exams_exam_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_exam_code_key UNIQUE (exam_code);


--
-- TOC entry 3314 (class 2606 OID 16431)
-- Name: exams exams_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_pkey PRIMARY KEY (id);


--
-- TOC entry 3332 (class 2606 OID 16593)
-- Name: guest guest_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.guest
    ADD CONSTRAINT guest_pkey PRIMARY KEY (id);


--
-- TOC entry 3324 (class 2606 OID 16509)
-- Name: listening_part_1 listening_part_1_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_1
    ADD CONSTRAINT listening_part_1_pkey PRIMARY KEY (id);


--
-- TOC entry 3326 (class 2606 OID 16527)
-- Name: listening_part_2 listening_part_2_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_2
    ADD CONSTRAINT listening_part_2_pkey PRIMARY KEY (id);


--
-- TOC entry 3328 (class 2606 OID 16541)
-- Name: listening_part_3 listening_part_3_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_3
    ADD CONSTRAINT listening_part_3_pkey PRIMARY KEY (id);


--
-- TOC entry 3330 (class 2606 OID 16555)
-- Name: listening_part_4 listening_part_4_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_4
    ADD CONSTRAINT listening_part_4_pkey PRIMARY KEY (id);


--
-- TOC entry 3316 (class 2606 OID 16452)
-- Name: reading_part_1 reading_part_1_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_1
    ADD CONSTRAINT reading_part_1_pkey PRIMARY KEY (question_id);


--
-- TOC entry 3318 (class 2606 OID 16467)
-- Name: reading_part_2 reading_part_2_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_2
    ADD CONSTRAINT reading_part_2_pkey PRIMARY KEY (question_id);


--
-- TOC entry 3320 (class 2606 OID 16481)
-- Name: reading_part_3 reading_part_3_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_3
    ADD CONSTRAINT reading_part_3_pkey PRIMARY KEY (question_id);


--
-- TOC entry 3322 (class 2606 OID 16495)
-- Name: reading_part_4 reading_part_4_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_4
    ADD CONSTRAINT reading_part_4_pkey PRIMARY KEY (question_id);


--
-- TOC entry 3334 (class 2606 OID 16602)
-- Name: speaking speaking_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.speaking
    ADD CONSTRAINT speaking_pkey PRIMARY KEY (id);


--
-- TOC entry 3304 (class 2606 OID 16398)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3306 (class 2606 OID 16400)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 3336 (class 2606 OID 16616)
-- Name: writing writing_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.writing
    ADD CONSTRAINT writing_pkey PRIMARY KEY (id);


--
-- TOC entry 3339 (class 2606 OID 16415)
-- Name: exam_sets exam_sets_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_sets
    ADD CONSTRAINT exam_sets_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id);


--
-- TOC entry 3352 (class 2606 OID 16639)
-- Name: exam_submission exam_submission_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_submission
    ADD CONSTRAINT exam_submission_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id) ON DELETE CASCADE;


--
-- TOC entry 3353 (class 2606 OID 16634)
-- Name: exam_submission exam_submission_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exam_submission
    ADD CONSTRAINT exam_submission_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 3340 (class 2606 OID 16439)
-- Name: exams exams_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public.users(id);


--
-- TOC entry 3341 (class 2606 OID 16434)
-- Name: exams exams_examset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_examset_id_fkey FOREIGN KEY (examset_id) REFERENCES public.exam_sets(id);


--
-- TOC entry 3346 (class 2606 OID 16510)
-- Name: listening_part_1 listening_part_1_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_1
    ADD CONSTRAINT listening_part_1_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3347 (class 2606 OID 16528)
-- Name: listening_part_2 listening_part_2_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_2
    ADD CONSTRAINT listening_part_2_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3348 (class 2606 OID 16542)
-- Name: listening_part_3 listening_part_3_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_3
    ADD CONSTRAINT listening_part_3_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3349 (class 2606 OID 16556)
-- Name: listening_part_4 listening_part_4_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.listening_part_4
    ADD CONSTRAINT listening_part_4_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3342 (class 2606 OID 16453)
-- Name: reading_part_1 reading_part_1_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_1
    ADD CONSTRAINT reading_part_1_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3343 (class 2606 OID 16468)
-- Name: reading_part_2 reading_part_2_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_2
    ADD CONSTRAINT reading_part_2_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3344 (class 2606 OID 16482)
-- Name: reading_part_3 reading_part_3_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_3
    ADD CONSTRAINT reading_part_3_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3345 (class 2606 OID 16496)
-- Name: reading_part_4 reading_part_4_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.reading_part_4
    ADD CONSTRAINT reading_part_4_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id);


--
-- TOC entry 3350 (class 2606 OID 16603)
-- Name: speaking speaking_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.speaking
    ADD CONSTRAINT speaking_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id) ON DELETE CASCADE;


--
-- TOC entry 3351 (class 2606 OID 16617)
-- Name: writing writing_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.writing
    ADD CONSTRAINT writing_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id) ON DELETE CASCADE;


-- Completed on 2025-06-28 09:46:32

--
-- PostgreSQL database dump complete
--

