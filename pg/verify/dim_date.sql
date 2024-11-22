-- Verify DateDimension:dim_date on pg

BEGIN;

SET search_path TO date_dim;

SELECT	date_id, epoch, week_id
FROM	dim_date
WHERE	FALSE;

ROLLBACK;
