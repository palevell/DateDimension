-- dim_date_5.sql - Friday, November 22, 2024
/**/


SELECT	TO_CHAR(datum, 'yyyymmdd')::INT AS id,
	datum AS date_id, week_from, week_from_iso,
	TO_CHAR(datum,'TMDay') AS day_name,
	TO_CHAR(datum,'Dy') AS day_abbr,
	TO_CHAR(datum, 'YYYY"W"WW') AS week_id,
	TO_CHAR(datum, 'IYYY"W"IW') AS week_id_iso,
	TO_CHAR(week_from, 'YYYY"W"WW') AS week_id2,
	TO_CHAR(week_from_iso, 'IYYY"W"IW') AS week_id_iso2,
	EXTRACT(ISOYEAR FROM datum) || TO_CHAR(datum, '"W"IW') AS week_id_iso3,
	EXTRACT(YEAR FROM datum) || TO_CHAR(datum, '"-W"WW-') || EXTRACT(DOW FROM datum) AS week_of_year_id,
	EXTRACT(ISOYEAR FROM datum) || TO_CHAR(datum, '"-W"IW-') || EXTRACT(ISODOW FROM datum) AS week_of_year_id_iso,
        datum + (0 - EXTRACT(DOW FROM datum))::INT AS week_from2,
        datum + (1 - EXTRACT(ISODOW FROM datum))::INT AS week_from_iso2,	
	TO_CHAR(datum, 'YYYY"-W"WW-D') AS fafo1,
	TO_CHAR(datum, 'IYYY"-W"IW-ID') AS fafo2,
	TO_CHAR(datum, 'YYYY"-W"WW-') || EXTRACT(DOW FROM datum) AS fafo3,
	datum - DATE_PART('DOW', datum)::INT AS fafo4,
	TO_CHAR(datum, 'YYYY-MM-DD (IYYY-IDDD)') AS fafo
FROM (	SELECT	datum::DATE,
		datum::DATE + (0 - EXTRACT(DOW FROM datum))::INT AS week_from,
		datum::DATE + (1 - EXTRACT(ISODOW FROM datum))::INT AS week_from_iso
	FROM	GENERATE_SERIES (DATE '2023-12-25', DATE '2024-01-15', INTERVAL '1 day') datum);
