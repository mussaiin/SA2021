-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.client (
	id int8 NOT NULL,
	"name" varchar NULL,
	CONSTRAINT client_pkey PRIMARY KEY (id)
);