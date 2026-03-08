
-- Verbund Pflegehilfe Data Engineering Task
-- Step 1: Create Leads table
-- Author: Mehak Nigar

-- Ensure correct database
USE lead_management_db;
GO

-- Create Leads table
CREATE TABLE dbo.Leads (
    Id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
    State INT NOT NULL,

    CreatedDateUtc DATETIME2 NULL,
    CancellationRequestDateUtc DATETIME2 NULL,
    CancellationDateUtc DATETIME2 NULL,
    CancellationRejectionDateUtc DATETIME2 NULL,

    SoldEmployee NVARCHAR(255) NULL,
    CancelledEmployee NVARCHAR(255) NULL,

    UpdatedDateUtc DATETIME2 NOT NULL
);
GO

-- Index for incremental pipeline loads
CREATE INDEX idx_leads_updated_date
ON dbo.Leads (UpdatedDateUtc);