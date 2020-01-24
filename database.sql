DROP TABLE licenseplate
DROP TABLE public.comment;

CREATE TABLE licenseplate (
	id		SERIAL PRIMARY KEY NOT NULL,
	licenseplate 	text,
	time		date
);

DROP TABLE public.comment;

CREATE TABLE public.comment
(
    id SERIAL PRIMARY KEY NOT NULL,
    grade integer,
    comment text COLLATE pg_catalog."default",
    driver text COLLATE pg_catalog."default",
    carmodel text COLLATE pg_catalog."default",
    license_plate_id integer,
    user_id integer,
    "time" date
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.comment
    OWNER to kgvafgulbaaqbv;