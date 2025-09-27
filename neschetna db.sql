--
-- PostgreSQL database dump
--

\restrict QZtHqfVe8lQuPa25oaHdZnjKncNvuUxf3b3C2JMjJFAsCmqkkELJgiU1HsXJfas

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

-- Started on 2025-09-27 19:38:32

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 218 (class 1259 OID 16551)
-- Name: event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.event (
    id integer NOT NULL,
    title character varying(200),
    date date,
    place character varying(200)
);


ALTER TABLE public.event OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16561)
-- Name: reservation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reservation (
    id integer NOT NULL,
    date date,
    user_id integer NOT NULL,
    ticket_id integer NOT NULL
);


ALTER TABLE public.reservation OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16556)
-- Name: ticket; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ticket (
    id integer NOT NULL,
    price money,
    place integer,
    status boolean,
    event_id integer NOT NULL
);


ALTER TABLE public.ticket OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16546)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    name character varying(50),
    surname character varying(50),
    email character varying(50),
    phone character varying(10)
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 4910 (class 0 OID 16551)
-- Dependencies: 218
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event (id, title, date, place) FROM stdin;
3	Футбольний матч Динамо–Шахтар	2025-11-20	НСК Олімпійський, Київ
2	Театральна вистава "Лісова пісня"	2025-11-02	Театр ім. Франка, Київ
1	Концерт Океан Ельзи	2025-10-15	Палац Спорту, Київ
\.


--
-- TOC entry 4912 (class 0 OID 16561)
-- Dependencies: 220
-- Data for Name: reservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reservation (id, date, user_id, ticket_id) FROM stdin;
3	2025-09-29	3	1
2	2025-09-28	2	3
1	2025-09-27	1	2
\.


--
-- TOC entry 4911 (class 0 OID 16556)
-- Dependencies: 219
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ticket (id, price, place, status, event_id) FROM stdin;
3	400,00 ?	15	t	2
2	750,00 ?	8	t	1
1	500,00 ?	12	t	1
\.


--
-- TOC entry 4909 (class 0 OID 16546)
-- Dependencies: 217
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, name, surname, email, phone) FROM stdin;
1	Іван	Петренко	ivan.petrenko@example.com	0501112233
2	Марія	Ковальчук	maria.kovalchuk@example.com	0671234567
3	Олег	Сидоренко	oleg.sydorenko@example.com	0931234567
\.


--
-- TOC entry 4756 (class 2606 OID 16555)
-- Name: event event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (id);


--
-- TOC entry 4760 (class 2606 OID 16565)
-- Name: reservation reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_pkey PRIMARY KEY (id);


--
-- TOC entry 4758 (class 2606 OID 16560)
-- Name: ticket ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (id);


--
-- TOC entry 4754 (class 2606 OID 16550)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 4762 (class 2606 OID 16576)
-- Name: reservation reservation_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.ticket(id) NOT VALID;


--
-- TOC entry 4763 (class 2606 OID 16571)
-- Name: reservation reservation_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 4761 (class 2606 OID 16566)
-- Name: ticket ticket_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(id) NOT VALID;


-- Completed on 2025-09-27 19:38:33

--
-- PostgreSQL database dump complete
--

\unrestrict QZtHqfVe8lQuPa25oaHdZnjKncNvuUxf3b3C2JMjJFAsCmqkkELJgiU1HsXJfas

