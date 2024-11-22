-- dim_date_2.sql - Tuesday, November 19, 2024

SELECT	datum AS date_id,
	TO_CHAR(datum, 'TMDay') AS day_name,
	EXTRACT(DOW FROM datum) AS day_of_week,
	EXTRACT(ISODOW FROM datum) AS day_of_week_iso,
	EXTRACT(YEAR FROM datum + INTERVAL '1 day') || TO_CHAR(datum + INTERVAL '1 day', '"W"IW') AS week_id,
	EXTRACT(YEAR FROM datum) || TO_CHAR(datum, '"W"WW') AS week_id_iso,
	TO_CHAR(datum + INTERVAL '1 day', '"W"WW') AS week_name,
	TO_CHAR(datum, '"W"WW') AS week_name_iso,
	-- TO_CHAR(datum, 'W')::INT AS week_of_month,
	-- EXTRACT(WEEK FROM datum + INTERVAL '1 day') AS week_of_year,
	EXTRACT(WEEK FROM datum) AS week_of_year,
	EXTRACT(YEAR FROM datum + INTERVAL '1 day') || TO_CHAR(datum + INTERVAL '1 day', '"-W"WW-') || EXTRACT(DOW FROM datum) AS week_of_year_id,
	EXTRACT(WEEK FROM datum) AS week_of_year_iso,
	EXTRACT(ISOYEAR FROM datum) || TO_CHAR(datum, '"-W"IW-') || EXTRACT(ISODOW FROM datum) AS week_of_year_iso_id
	FROM (	SELECT	'2024-11-09'::DATE + SEQUENCE.DAY AS datum
	FROM	GENERATE_SERIES(0, 21) AS SEQUENCE (DAY)
	GROUP BY SEQUENCE.DAY) DQ
ORDER BY 1;
