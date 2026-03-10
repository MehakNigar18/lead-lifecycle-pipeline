Lead Lifecycle Data Engineering Pipeline Overview

This project implements a complete data engineering pipeline for processing lead lifecycle data and generating lifecycle events for analytics.

The pipeline ingests lead data from an Excel source, loads it into Azure Blob Storage, processes it through Azure Data Factory pipelines, stores raw data in Snowflake, and performs Python-based transformations triggered through an Azure Function App.

The final transformed data is stored in Snowflake ANALYTICS tables for reporting and analysis.

