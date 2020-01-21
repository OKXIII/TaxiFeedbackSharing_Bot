DROP TABLE licenseplate

CREATE TABLE licenseplate (
	id		SERIAL PRIMARY KEY NOT NULL,
	licenseplate 	text,
	time		date
);