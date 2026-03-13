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
<ul>
  <li>Excel Dataset
    <ul>
      <li>Schema</li>
      <li>Lead data collected from marketing sources</li>
    </ul>
  </li>

  <li>Azure Blob Storage
    <ul>
      <li>Raw data landing zone</li>
      <li>Stores uploaded Excel lead files</li>
    </ul>
  </li>

  <li>Azure Data Factory Pipeline
    <ul>
      <li>Trigger
        <ul>
          <li>Schedule/Event trigger to start ingestion pipeline</li>
        </ul>
      </li>

<li>Pipeline Orchestration</li>
        <ul>
          <li>Controls execution of ingestion and transformation steps</li>
          <li>Manages dependencies between activities</li>
        </ul>
      </li>

  <li>ADF Data Flow (df_transform_leads_raw)
        <ul>
          <li>Source
            <ul>
              <li>Read leads from Azure Blob Storage</li>
            </ul>
          </li>

  <li>Schema Mapping
            <ul>
              <li>Map Excel fields to standardized pipeline schema</li>
            </ul>
          </li>

  <li>Validation
            <ul>
              <li>Check required fields</li>
              <li>Separate valid and invalid leads</li>
            </ul>
          </li>

   <li>Transformation
            <ul>
              <li>Deduplicate leads (keep most recent record)</li>
              <li>Clean and standardize required columns</li>
            </ul>
          </li>
    <li>Sink
            <ul>
              <li>Valid leads → Azure SQL Database</li>
              <li>Invalid leads → Rejected leads storage</li>
            </ul>
          </li>

   </ul>
      </li>
    </ul>
  </li>

  <li>Azure SQL Database
    <ul>
      <li>Staging storage for validated leads</li>
    </ul>
  </li>

  <li>Snowflake RAW.LEADS
    <ul>
      <li>Raw data warehouse layer</li>
    </ul>
  </li>

  <li>Azure Function (HTTP Trigger)
    <ul>
      <li>API trigger to start Python transformation pipeline</li>
    </ul>
  </li>

  <li>Python Transformation Pipeline
    <ul>
      <li>Apply business rules and data enrichment</li>
      <li>Generate lead event records</li>
    </ul>
  </li>

  <li>Snowflake ANALYTICS.LEAD_EVENTS
    <ul>
      <li>Store the transformed data in the LeadEvents table in Snowflake.</li>
    </ul>
  </li>

  <li>Power BI Dashboard
    <ul>
      <li>Lead performance analytics and reporting</li>
    </ul>
  </li>
</ul>
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
    └── 04_star_schema.sql
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

<h2>Run the Transformation</h2>

<p>
The Python transformation pipeline is triggered through the Azure Function App.
Once the data is loaded into Snowflake <code>RAW.LEADS</code>, you can start the transformation by calling the Function App endpoint.
</p>

<h3>Trigger the Function</h3>

<ol>
  <li>Deploy the Azure Function App included in this repository.</li>
  <li>Locate the HTTP trigger URL of the function in the Azure Portal.</li>
  <li>Send a request to the endpoint to start the transformation.</li>
</ol>



<p>
This will execute the Python transformation logic and generate lifecycle events
in the <code>ANALYTICS.LEAD_EVENTS</code> table in Snowflake.
</p>

<h3>What Happens After Triggering</h3>

<ul>
<li>The Azure Function starts the Python pipeline.</li>
<li>The script reads lead data from <code>RAW.LEADS</code>.</li>
<li>Lifecycle events are generated.</li>
<li>Results are written to <code>ANALYTICS.LEAD_EVENTS</code>.</li>
</ul>
----
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

<h2>Snowflake Data Warehouse Model</h2>

<p>The analytics schema follows a star schema design:</p>

<ul>
  <li>FACT_LEAD_EVENTS</li>
  <li>DIM_EMPLOYEE</li>
  <li>DIM_DATE</li>
</ul>

<p>
  This structure supports efficient analytical queries and
  Power BI reporting.
</p>

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
