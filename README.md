<p align="center">
  <img src="https://capsule-render.vercel.app/api?text=Lead%20Lifecycle%20Data%20Engineering%20Pipeline&animation=fadeIn&type=waving&color=gradient&height=100"/>
</p>

<h2 align="center">Overview</h2>

<p align="center">
This project implements a complete <b>Data Engineering Pipeline</b> to process lead lifecycle data and generate lifecycle events for analytics.
</p>

<p>
The system ingests lead data from an Excel dataset, stores it in <b>Azure Blob Storage</b>, processes it through <b>Azure Data Factory pipelines</b>, loads the data into <b>Snowflake</b>, and performs <b>Python-based transformations</b> triggered through an <b>Azure Function App</b>.
</p>

<p>
The final transformed data is stored in <b>Snowflake Lead_Events tables</b> and visualized through a <b>Power BI dashboard</b>.
</p>

---

<h2 align="center">Architecture</h2>

<pre>
Excel Dataset
      │
      ▼
Azure Blob Storage
      │
      ▼
Azure Data Factory Pipeline
      │
      ▼
Azure SQL Database
      │
      ▼
Snowflake RAW.LEADS
      │
      ▼
Azure Function (HTTP Trigger)
      │
      ▼
Python Transformation Pipeline
      │
      ▼
Snowflake ANALYTICS.LEAD_EVENTS
      │
      ▼
Power BI Dashboard
</pre>

---

<h2 align="center">Technologies Used</h2>

<ul>
<li>Python</li>
<li>Azure Data Factory</li>
<li>Azure Blob Storage</li>
<li>Azure Function App</li>
<li>Snowflake</li>
<li>Azure SQL Database</li>
<li>Pandas</li>
<li>Power BI</li>
<li>GitHub</li>
<li>SQL</li>
</ul>

---

<h2 align="center">Project Structure</h2>

<pre>
lead-lifecycle-pipeline
│
├── adf/
│   ├── dataset/
│   ├── pipeline/
│   ├── linkedService/
│   └── trigger/
│
├── app/python/
│   ├── config/
│   ├── connectors/
│   ├── repositories/
│   ├── services/
│   └── pipeline_runner.py
│
├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_schema.sql
│   ├── 03_create_leads_table.sql
│   └── 04_snowflake_setup.sql
│
├── docs/
│   └── images/
│       └── powerbi_dashboard.png
│
├── logs/
├── requirements.txt
└── README.md
</pre>

---

<h2 align="center">Data Ingestion</h2>

<p>
The original dataset contains <b>100 lead records</b> provided in Excel format.
</p>

<p>Data ingestion process:</p>

<ul>
<li>Upload dataset to <b>Azure Blob Storage</b></li>
<li>Azure Data Factory reads the dataset</li>
<li>Data is loaded into <b>Azure SQL Database</b></li>
</ul>

<p>ADF pipeline used:</p>

<pre>
pl_blob_to_sql_leads
</pre>

---

<h2 align="center">Incremental Data Processing</h2>

<p>
The system supports <b>incremental loading</b> using a watermark column:
</p>

<pre>
UpdatedDateUtc
</pre>

<p>
This ensures that only new or updated records are processed.
</p>

<p>ADF pipeline used:</p>

<pre>
pl_sql_to_snowflake_leads_inc
</pre>

---

<h2 align="center">Azure Data Factory Features</h2>

<ul>
<li>Incremental loads using watermark column</li>
<li>GitHub integration for version control</li>
<li>Extensible and maintainable pipeline design</li>
<li>Email alerts for pipeline failures</li>
<li>Usage of linked services for connectivity</li>
<li>Pipeline trigger scheduled every 30 minutes</li>
</ul>

---

<h2 align="center">Snowflake Data Warehouse</h2>

<p>Snowflake is used as the central analytics data warehouse.</p>

<pre>
LEADS_DB
│
├── RAW
│   └── LEADS
│
└── ANALYTICS
    └── LEAD_EVENTS
</pre>

<p>SQL scripts used for Snowflake setup:</p>

<pre>
01_create_database.sql
02_create_schema.sql
03_create_leads_table.sql
04_snowflake_setup.sql
</pre>

---

<h2 align="center">Azure Function Trigger</h2>

<p>
The Python transformation pipeline is triggered using an Azure Function.
</p>

<p>Function type:</p>

<pre>
HTTP Trigger
</pre>

<p>Function name:</p>

<pre>
lead-lifecycle-transform-func
</pre>

---

<h2 align="center">Python Transformation Pipeline</h2>

<p>The Python pipeline performs lifecycle event calculations.</p>

<p>Processing steps:</p>

<ol>
<li>Read leads from <b>Snowflake RAW.LEADS</b></li>
<li>Generate lifecycle events</li>
<li>Insert results into <b>Snowflake ANALYTICS.LEAD_EVENTS</b></li>
</ol>

<p>Lifecycle event mapping:</p>

<table>
<tr>
<th>State</th>
<th>EventType</th>
</tr>
<tr>
<td>0</td>
<td>LeadSold</td>
</tr>
<tr>
<td>1</td>
<td>LeadCancellationRequested</td>
</tr>
<tr>
<td>2</td>
<td>LeadCancelled</td>
</tr>
<tr>
<td>3</td>
<td>LeadCancellationRejected</td>
</tr>
</table>

---

<h2 align="center">Lead Events Table</h2>

<table>
<tr>
<th>Column</th>
<th>Description</th>
</tr>
<tr>
<td>Id</td>
<td>Unique event identifier</td>
</tr>
<tr>
<td>EventType</td>
<td>Lifecycle event type</td>
</tr>
<tr>
<td>EventEmployee</td>
<td>Responsible employee</td>
</tr>
<tr>
<td>EventDate</td>
<td>Event timestamp</td>
</tr>
<tr>
<td>LeadId</td>
<td>Reference to original lead</td>
</tr>
<tr>
<td>UpdatedDateUtc</td>
<td>Processing timestamp</td>
</tr>
</table>

---

<h2 align="center">Power BI Dashboard</h2>

<p align="center">
This dashboard was created as an additional analytics layer to visualize lead lifecycle events.
</p>



<p>Dashboard insights include:</p>

<ul>
<li>Total leads</li>
<li>Sold leads</li>
<li>Cancelled leads</li>
<li>Cancellation requests</li>
<li>Lead lifecycle distribution</li>
<li>Employee activity</li>
<li>Lead trends over time</li>
</ul>

---

<h2 align="center">Logging</h2>

<p>Pipeline logs are stored in:</p>

<pre>
logs/pipeline.log
</pre>

---

<h2 align="center">Author</h2>

<p align="center">
<b>Mehak Nigar Shumaila</b><br>
Data Engineering Task – Verbund Pflegehilfe
</p>
