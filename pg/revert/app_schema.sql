-- Revert DateDimension:app_schema from pg

BEGIN;

DROP SCHEMA date_dim;

COMMIT;
