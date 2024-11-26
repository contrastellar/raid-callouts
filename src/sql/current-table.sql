-- Table: public.callouts

-- DROP TABLE IF EXISTS public.callouts;

CREATE TABLE IF NOT EXISTS public.callouts
(
    user_id bigint NOT NULL,
    date date NOT NULL,
    reason text COLLATE pg_catalog."default",
    nickname text COLLATE pg_catalog."default",
    CONSTRAINT callouts_pkey PRIMARY KEY (user_id, date)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.callouts
    OWNER to opossumbot;