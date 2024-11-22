-- Revert DateDimension:dim_date from pg

BEGIN;

SET search_path TO date_dim;

DROP TABLE dim_date;

COMMIT;
