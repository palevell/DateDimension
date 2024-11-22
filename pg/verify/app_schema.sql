-- Verify DateDimension:app_schema on pg

BEGIN;

SELECT pg_catalog.has_schema_privilege('date_dim', 'usage');

ROLLBACK;
