<p align="center">
  <img src="https://capsule-render.vercel.app/api?text=Lead%20Lifecycle%20Data%20Engineering%20Pipeline&animation=fadeIn&type=waving&color=gradient&height=100"/>
</p>

<h2 align="center">Overview</h2>

<p align="center">
  This project implements an <b>end-to-end Data Engineering pipeline</b> to process lead lifecycle data and generate analytics-ready events.
</p>

<p>
  Lead data is ingested from Excel, stored in <b>Azure Blob Storage</b>, orchestrated through <b>Azure Data Factory</b>,
  transformed using <b>Python via Azure Functions</b>, loaded into <b>Snowflake</b>, and visualized with <b>Power BI</b>.
</p>

<p>
  The Azure infrastructure is managed using <b>Terraform</b> to keep resources version-controlled and reproducible.
</p>

<hr>

<h2 align="center">Technologies Used</h2>

<ul>
  <li>Python</li>
  <li>Azure Data Factory</li>
  <li>Azure Blob Storage</li>
  <li>Azure Functions</li>
  <li>Azure SQL Database</li>
  <li>Snowflake</li>
  <li>Terraform</li>
  <li>GitHub Actions (CI/CD)</li>
  <li>Power BI</li>
  <li>SQL</li>
</ul>

<hr>

<h2 align="center">Architecture</h2>

<pre>
Excel Dataset
      ↓
Azure Blob Storage
      ↓
Azure Data Factory
      ↓
Azure SQL Database
      ↓
Snowflake RAW.LEADS
      ↓
Azure Function (Python Transformation)
      ↓
Snowflake ANALYTICS.LEAD_EVENTS
      ↓
Power BI Dashboard
</pre>

<hr>

<h2 align="center">Infrastructure as Code (Terraform)</h2>

<p>
  This project uses <b>Terraform</b> to manage Azure infrastructure.
</p>

<ul>
  <li>Azure Resource Group</li>
  <li>Azure Storage Account</li>
  <li>Azure Data Factory</li>
</ul>

<p>Example Terraform-managed resource:</p>

<pre>
resource "azurerm_storage_account" "lead_storage" {
  name                     = "leadstorageproject01"
  resource_group_name      = "rg-lead-data-project"
  location                 = "Germany West Central"
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
}
</pre>

<hr>

<h2 align="center">CI/CD Pipeline</h2>

<p>
This project includes a <b>CI/CD pipeline using GitHub Actions</b> to automatically deploy infrastructure and validate Terraform configurations.
</p>

<ul>
<li>Trigger on push to the <code>main</code> branch</li>
<li>Authenticate to Azure using a Service Principal</li>
<li>Initialize Terraform</li>
<li>Run Terraform plan</li>
<li>Deploy infrastructure using Terraform apply</li>
</ul>

<p>Workflow file location:</p>

<pre>
.github/workflows/terraform-deploy.yml
</pre>

<hr>

<h2 align="center">Data Pipeline</h2>

<h3>Data Ingestion</h3>

<ul>
  <li>Excel dataset uploaded to <b>Azure Blob Storage</b></li>
  <li><b>Azure Data Factory</b> loads data into <b>Azure SQL Database</b></li>
</ul>

<p>Pipeline used:</p>

<pre>pl_blob_to_sql_leads</pre>

<h3>Incremental Processing</h3>

<p>
  Incremental loading is implemented using the watermark column:
</p>

<pre>UpdatedDateUtc</pre>

<p>Pipeline used:</p>

<pre>pl_sql_to_snowflake_leads_inc</pre>

<hr>

<h2 align="center">Transformation</h2>

<p>
  Transformation is triggered through an <b>Azure Function (HTTP Trigger)</b>.
</p>

<p>Function name:</p>

<pre>lead-lifecycle-transform-func</pre>

<p>Processing steps:</p>

<ol>
  <li>Read lead data from <b>Snowflake RAW.LEADS</b></li>
  <li>Apply business rules and lifecycle mapping</li>
  <li>Write results into <b>ANALYTICS.LEAD_EVENTS</b></li>
</ol>

<hr>

<h2 align="center">Data Warehouse Model</h2>

<p>The Snowflake analytics layer follows a simple star schema:</p>

<ul>
  <li>FACT_LEAD_EVENTS</li>
  <li>DIM_EMPLOYEE</li>
  <li>DIM_DATE</li>
</ul>

<hr>

<h2 align="center">Power BI Dashboard</h2>

<p>
  The Power BI dashboard provides business insights from the transformed lead lifecycle data.
</p>

<ul>
  <li>Total leads</li>
  <li>Sold leads</li>
  <li>Cancelled leads</li>
  <li>Cancellation requests</li>
  <li>Employee activity</li>
  <li>Lead lifecycle trends</li>
</ul>

<p>Dashboard image:</p>

<pre>docs/images/powerbi_dashboard.png</pre>

<hr>

<h2 align="center">Project Structure</h2>

<pre>
lead-lifecycle-pipeline
│
├── adf/               (ADF pipelines and datasets)
├── app/python/        (Python transformation logic)
├── sql/               (SQL and Snowflake scripts)
├── terraform/         (Terraform infrastructure)
├── docs/images/       (Dashboard screenshots)
├── logs/              (Pipeline logs)
├── requirements.txt
└── README.md
</pre>

<hr>

<h2 align="center">Author</h2>

<p align="center">
  <b>Mehak Nigar Shumaila</b><br>
  Data Engineering Task – Verbund Pflegehilfe
</p>
