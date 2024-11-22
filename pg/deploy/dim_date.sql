-- Deploy DateDimension:dim_date to pg
-- requires: app_schema

BEGIN;

SET search_path TO date_dim;

CREATE TABLE dim_date (
	id			INT NOT NULL PRIMARY KEY,
	date_id			DATE NOT NULL UNIQUE,
	epoch			BIGINT NOT NULL,
	day_suffix		VARCHAR(4) NOT NULL,
	day_name		VARCHAR(9) NOT NULL,
	day_abbr		CHAR(3) NOT NULL,
	day_of_week		INT NOT NULL,
	day_of_week_iso		INT NOT NULL,
	day_of_month		INT NOT NULL,
	day_of_quarter		INT NOT NULL,
	day_of_year		INT NOT NULL,
	week_id			VARCHAR(7) NOT NULL,
	week_id_iso		VARCHAR(7) NOT NULL,
	week_name		VARCHAR(3) NOT NULL,
	week_name_iso		VARCHAR(3) NOT NULL,
	week_of_month		INT NOT NULL,
	week_of_year		INT NOT NULL,
	week_of_year_iso	INT NOT NULL,
	week_of_year_id		CHAR(10) NOT NULL,
	week_of_year_id_iso	CHAR(10) NOT NULL,
	month_of_year		INT NOT NULL,
	month_name		VARCHAR(9) NOT NULL,
	month_abbr		CHAR(3) NOT NULL,
	quarter_of_year		INT NOT NULL,
	quarter_name		VARCHAR(9) NOT NULL,
	quarter_id		CHAR(6) NOT NULL,
	yyyy			INT NOT NULL,
	week_from		DATE NOT NULL,
	week_thru		DATE NOT NULL,
	week_from_iso		DATE NOT NULL,
	week_thru_iso		DATE NOT NULL,
	month_from		DATE NOT NULL,
	month_thru		DATE NOT NULL,
	quarter_from		DATE NOT NULL,
	quarter_thru		DATE NOT NULL,
	year_from		DATE NOT NULL,
	year_thru		DATE NOT NULL,
	mmyyyy			CHAR(6) NOT NULL,
	mmddyyyy		CHAR(10) NOT NULL,
	is_weekend		BOOLEAN NOT NULL
);

CREATE INDEX idx_dim_date_week_thru ON dim_date(week_thru);
CREATE INDEX idx_dim_date_month_thru ON dim_date(month_thru);
CREATE INDEX idx_dim_date_year ON dim_date(yyyy);

COMMIT;
