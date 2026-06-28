# Execution Steps

## Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/real-time-stock-market-pipeline.git

cd real-time-stock-market-pipeline
```

---

## Step 2: Create Python Virtual Environment

```bash
python -m venv venv
# or
py -m venv venv

venv\Scripts\activate
```

---

## Step 3: Install Required Libraries

```bash
pip install yfinance pandas boto3 awscli

pip freeze > requirements.txt
```

---

## Step 4: Configure AWS Credentials

Install AWS CLI and configure credentials.

```bash
aws configure
```

Provide:

* AWS Access Key ID
* AWS Secret Access Key
* Region: ap-south-1
* Output Format: json

Verify configuration:

```bash
aws s3 ls
```

---

## Step 5: Create AWS S3 Bucket

Create bucket:

```text
stock-market-data-charan
```

Create folders inside bucket:

```text
raw/
bronze/
silver/
gold/
checkpoints/
```

---

## Step 6: Generate Stock Data

Navigate to producer folder.

```bash
cd producer

python producer.py
```

A CSV file containing stock data will be generated.

Example:

```text
stock_20260628_103000.csv
```

---

## Step 7: Upload Data to S3

Execute:

```bash
python upload_to_s3.py
```

Verify uploaded files in:

```text
s3://stock-market-data-charan/raw/
```

---

## Step 8: Configure AWS IAM, S3 Permissions, and Databricks Compute

### Create IAM Role

1. Go to AWS IAM → Roles → Create Role.
2. Select **AWS Service** → Choose **Databricks (or EC2 if needed)**.
3. Attach required policies such as:

   * AmazonS3FullAccess (or custom policy with limited access)
4. Create the role.

### Edit Trust Policy

Update the trust relationship to allow Databricks to assume the role.

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "<DATABRICKS_ACCOUNT_ID>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

### Update S3 Bucket Policy

Go to S3 → Bucket → Permissions → Bucket Policy.

Add policy to allow IAM role access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "<IAM_ROLE_ARN>"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::stock-market-data-charan",
        "arn:aws:s3:::stock-market-data-charan/*"
      ]
    }
  ]
}
```

---

### Create Databricks Compute

Create a Databricks cluster with:

* Runtime: 15.x LTS
* Worker Nodes: 1
* Node Type: Small

Start the cluster.

---

### Create External Location in Databricks

1. Go to Databricks → Data → External Locations.
2. Create a new external location.
3. Provide:

   * S3 Path: `s3://stock-market-data-charan/`
   * Storage Credential: IAM Role created earlier
4. Validate and create.

---

## Step 9: Execute Bronze Layer Notebook

Run notebook:

```text
01_bronze_ingestion
```

Tasks performed:

* Read CSV files from Raw layer.
* Ingest data using Databricks Auto Loader.
* Store data in Bronze Delta table.

Output location:

```text
s3://stock-market-data-charan/bronze
```

---

## Step 10: Create Bronze Table

Execute SQL:

```sql
CREATE TABLE bronze_stock
USING DELTA
LOCATION 's3://stock-market-data-charan/bronze';
```

---

## Step 11: Execute Silver Layer Notebook

Run notebook:

```text
02_silver_transformation
```

Tasks performed:

* Remove duplicates.
* Convert timestamp datatype.
* Store transformed data into Silver layer.

Output location:

```text
s3://stock-market-data-charan/silver
```

---

## Step 12: Create Silver Table

```sql
CREATE TABLE silver_stock
USING DELTA
LOCATION 's3://stock-market-data-charan/silver';
```

---

## Step 13: Execute Gold Layer Notebook

Run notebook:

```text
03_gold_metrics
```

Tasks performed:

* Generate business KPIs.
* Calculate average price.
* Calculate total volume.
* Calculate highest and lowest prices.

Output location:

```text
s3://stock-market-data-charan/gold
```

---

## Step 14: Create Gold Table

```sql
CREATE TABLE gold_stock_metrics
USING DELTA
LOCATION 's3://stock-market-data-charan/gold';
```

---

## Step 15: Create Dashboard

Create a SQL Warehouse.

Run:

```sql
SELECT * FROM gold_stock_metrics;
```

Create visualizations:

* Average Closing Price by Stock
* Total Volume by Stock
* Highest Price by Stock
* Lowest Price by Stock
* Price Change by Stock

Save dashboard.

---

## Step 16: Create Workflow

Create Databricks Workflow with task sequence:

```text
01_bronze_ingestion
↓
02_silver_transformation
↓
03_gold_metrics
```

Schedule workflow execution.

---

## Step 17: Push Project to GitHub

```bash
git add .

git commit -m "Completed real-time stock market pipeline project"

git branch -M main

git push origin main
```
