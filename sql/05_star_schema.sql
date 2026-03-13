-- =====================================================
-- Set the active database and schema
-- =====================================================
USE DATABASE LEADS_DB;
USE SCHEMA ANALYTICS;


-- =====================================================
-- Dimension Table: Employee
-- Stores unique employees involved in lead events
-- =====================================================
CREATE OR REPLACE TABLE DIM_EMPLOYEE (
    EMPLOYEE_ID INTEGER AUTOINCREMENT, -- surrogate key
    EMPLOYEE_EMAIL STRING              -- employee email identifier
);


-- =====================================================
-- Dimension Table: Date
-- Enables time-based analytics (day, month, year etc.)
-- =====================================================
CREATE OR REPLACE TABLE DIM_DATE (
    DATE_KEY INTEGER,  -- format YYYYMMDD for fast joins
    FULL_DATE DATE,
    DAY INTEGER,
    MONTH INTEGER,
    YEAR INTEGER,
    WEEKDAY STRING
);


-- =====================================================
-- Fact Table: Lead Events
-- Central fact table storing lifecycle event data
-- =====================================================
CREATE OR REPLACE TABLE FACT_LEAD_EVENTS (
    EVENT_ID STRING,        -- unique identifier for event
    LEAD_ID STRING,         -- lead reference
    EVENT_TYPE STRING,      -- event type (LeadSold, Cancelled etc.)
    EMPLOYEE_ID INTEGER,    -- FK -> DIM_EMPLOYEE
    DATE_KEY INTEGER,       -- FK -> DIM_DATE
    EVENT_DATE TIMESTAMP,   -- timestamp of event
    UPDATED_DATE TIMESTAMP  -- last update timestamp
);


-- =====================================================
-- Populate DIM_EMPLOYEE
-- Extract distinct employees from LEAD_EVENTS
-- =====================================================
INSERT INTO DIM_EMPLOYEE (EMPLOYEE_EMAIL)
SELECT DISTINCT EVENT_EMPLOYEE
FROM LEAD_EVENTS
WHERE EVENT_EMPLOYEE IS NOT NULL
AND EVENT_EMPLOYEE != 'Unknown';


-- =====================================================
-- Populate DIM_DATE
-- Extract unique event dates and derive date attributes
-- =====================================================
INSERT INTO DIM_DATE
SELECT DISTINCT
    TO_NUMBER(TO_CHAR(EVENT_DATE,'YYYYMMDD')) AS DATE_KEY,
    EVENT_DATE::DATE AS FULL_DATE,
    DAY(EVENT_DATE),
    MONTH(EVENT_DATE),
    YEAR(EVENT_DATE),
    DAYNAME(EVENT_DATE)
FROM LEAD_EVENTS;


-- =====================================================
-- Populate FACT_LEAD_EVENTS
-- Join events with DIM_EMPLOYEE to resolve surrogate key
-- =====================================================
INSERT INTO FACT_LEAD_EVENTS
SELECT
    ID AS EVENT_ID,
    LEAD_ID,
    EVENT_TYPE,
    E.EMPLOYEE_ID,
    TO_NUMBER(TO_CHAR(EVENT_DATE,'YYYYMMDD')) AS DATE_KEY,
    EVENT_DATE,
    UPDATED_DATE_UTC
FROM LEAD_EVENTS L
LEFT JOIN DIM_EMPLOYEE E
ON L.EVENT_EMPLOYEE = E.EMPLOYEE_EMAIL;


-- =====================================================
-- Validation Query
-- Check distribution of lifecycle events
-- =====================================================
SELECT EVENT_TYPE, COUNT(*)
FROM LEAD_EVENTS
GROUP BY EVENT_TYPE;