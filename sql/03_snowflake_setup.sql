-- ======================================================
-- 1. CREATE WAREHOUSE
-- ======================================================

CREATE WAREHOUSE IF NOT EXISTS WH_LEADS_ETL
WITH
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

USE WAREHOUSE WH_LEADS_ETL;


-- ======================================================
-- 2. CREATE DATABASE
-- ======================================================

CREATE DATABASE IF NOT EXISTS LEADS_DB;

USE DATABASE LEADS_DB;


-- ======================================================
-- 3. CREATE SCHEMAS
-- ======================================================

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;


-- ======================================================
-- 4. CREATE LEADS TABLE (RAW LAYER)
-- ======================================================

USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS LEADS (
    Id STRING NOT NULL,
    State INTEGER,
    CreatedDateUtc TIMESTAMP,
    CancellationRequestDateUtc TIMESTAMP,
    CancellationDateUtc TIMESTAMP,
    CancellationRejectionDateUtc TIMESTAMP,
    SoldEmployee STRING,
    CancelledEmployee STRING,
    UpdatedDateUtc TIMESTAMP,

    CONSTRAINT PK_LEADS PRIMARY KEY (Id)
);


-- ======================================================
-- 5. CREATE LEAD_EVENTS TABLE (ANALYTICS LAYER)
-- ======================================================

USE SCHEMA ANALYTICS;

CREATE TABLE IF NOT EXISTS LEAD_EVENTS (
    Id STRING NOT NULL,
    EventType STRING,
    EventEmployee STRING,
    EventDate TIMESTAMP,
    LeadId STRING NOT NULL,
    UpdatedDateUtc TIMESTAMP,

    CONSTRAINT PK_LEAD_EVENTS PRIMARY KEY (Id)
);