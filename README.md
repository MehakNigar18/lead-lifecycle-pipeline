Lead Lifecycle Data Engineering Pipeline
Overview

This project implements a data engineering pipeline that processes lead lifecycle data and generates lifecycle events for analytics.

The pipeline ingests lead data from an Excel source, loads it into a SQL database, transfers it to Snowflake using Azure Data Factory (ADF), and then performs Python-based transformations to compute lead lifecycle events.

The final results are stored in a Snowflake analytics table for further analysis and reporting.

Architecture
Excel Data
     ↓
Azure Blob Storage
     ↓
Azure Data Factory Pipeline
     ↓
SQL Leads Table
     ↓
Snowflake RAW.LEADS
     ↓
Python Transformation Pipeline
     ↓
Snowflake ANALYTICS.LEAD_EVENTS
Technologies Used

Python

Snowflake

Azure Data Factory

Azure Blob Storage

Pandas

GitHub

SQL

Project Structure
lead-lifecycle-pipeline
│
├── adf/                       # Azure Data Factory resources
│   ├── dataset/
│   ├── pipeline/
│   ├── linkedService/
│   └── trigger/
│
├── app/python/                # Python transformation pipeline
│   ├── config/                # Configuration and environment settings
│   ├── connectors/            # External system connections (Snowflake)
│   ├── repositories/          # Data access layer
│   ├── services/              # Business logic and transformations
│   └── pipeline_runner.py     # Pipeline entry point
│
├── sql/                       # Snowflake infrastructure scripts
│   ├── 01_create_database.sql
│   ├── 02_create_schema.sql
│   ├── 03_create_leads_table.sql
│   └── 04_snowflake_setup.sql
│
├── logs/                      # Pipeline execution logs
├── requirements.txt           # Python dependencies
└── README.md
Data Pipeline Steps
1. Extract & Load

The original lead dataset is provided as an Excel file containing 100 leads.

The ingestion process includes:

Upload Excel data to Azure Blob Storage

Use Azure Data Factory pipeline to load data into SQL

Transfer SQL data to Snowflake RAW schema

The ADF pipeline supports:

Incremental loading using a watermark (UpdatedDateUtc)

GitHub integration

Linked services

Scheduled trigger (every 30 minutes)

Snowflake Setup

Snowflake infrastructure is defined using SQL scripts stored in the repository.

Execution order:

01_create_database.sql

02_create_schema.sql

03_create_leads_table.sql

04_snowflake_setup.sql

Schemas used:

LEADS_DB
 ├── RAW
 └── ANALYTICS

RAW schema stores the ingested leads.

ANALYTICS schema stores transformed lifecycle events.

Python Transformation Pipeline

The Python pipeline performs lifecycle event calculations.

Steps:

Read leads from RAW.LEADS

Generate lifecycle events

Write results to ANALYTICS.LEAD_EVENTS

Transformation rules:

State	EventType
0	LeadSold
1	LeadCancellationRequested
2	LeadCancelled
3	LeadCancellationRejected

Event employee logic:

Sold events → SoldEmployee

Cancellation events → CancelledEmployee

Request/Rejected events → "Unknown"

Event date corresponds to the appropriate timestamp column.

Lead Events Table

The transformed table structure:

Column	Description
Id	Unique event identifier
EventType	Lifecycle event type
EventEmployee	Employee responsible for the event
EventDate	Event timestamp
LeadId	Reference to original lead
UpdatedDateUtc	Processing timestamp
Python Design

The Python project follows a modular and maintainable architecture:

config → connectors → repositories → services → pipeline_runner

Key components:

SnowflakeConnection – manages Snowflake connectivity

LeadRepository – retrieves lead records

LeadEventTransformer – calculates lifecycle events

LeadEventRepository – writes transformed data

The design follows object-oriented principles and clean coding practices.

Running the Pipeline

Configure environment variables in .env

Run SQL scripts to create Snowflake resources

Trigger the ADF pipeline for ingestion

Execute Python pipeline:

python pipeline_runner.py
Logging & Error Handling

The pipeline includes:

structured logging

exception handling

modular components for easier debugging and maintenance

Logs are written to:

logs/pipeline.log
Author

Mehak Nigar
Data Engineering Task – Verbund Pflegehilfe
