-- ======================================================
-- Verbund Pflegehilfe Data Engineering Task
-- Step 3: Create RAW.LEADS table
-- Author: Mehak Nigar
--
-- Schema: LEADS_DB.RAW
-- ======================================================


-- Ensure correct database and schema are used
USE DATABASE LEADS_DB;
USE SCHEMA RAW;


-- ======================================================
-- Create Leads table
-- ======================================================

CREATE TABLE IF NOT EXISTS LEADS (

    -- Unique identifier for the lead
    ID STRING NOT NULL,

    -- Lifecycle state of the lead
    STATE INTEGER NOT NULL,

    -- Timestamp when lead was created
    CREATEDDATEUTC TIMESTAMP,

    -- Date when cancellation was requested
    CANCELLATIONREQUESTDATEUTC TIMESTAMP,

    -- Date when cancellation was confirmed
    CANCELLATIONDATEUTC TIMESTAMP,

    -- Date when cancellation request was rejected
    CANCELLATIONREJECTIONDATEUTC TIMESTAMP,

    -- Employee responsible for selling the lead
    SOLDEMPLOYEE STRING,

    -- Employee responsible for cancelling the lead
    CANCELEDEMPLOYEE STRING,

    -- Last update timestamp for the lead record
    UPDATEDDATEUTC TIMESTAMP

);