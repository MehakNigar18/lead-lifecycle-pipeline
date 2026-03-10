-- ======================================================
-- Create schemas for the lead lifecycle pipeline
-- RAW: landing layer for source data
-- ANALYTICS: transformed data used by reporting
-- ======================================================
CREATE SCHEMA IF NOT EXISTS LEADS_DB.RAW;

CREATE SCHEMA IF NOT EXISTS LEADS_DB.ANALYTICS;