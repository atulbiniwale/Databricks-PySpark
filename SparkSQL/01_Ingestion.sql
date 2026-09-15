-- Databricks notebook source
-- MAGIC %md
-- MAGIC **_source data filepath_**
-- MAGIC
-- MAGIC _/Volumes/ab-test-catelog/ab-test-schema/ab-test-volume/ecommerce_orders_large.csv_

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Ingest csv in a DF

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC df = spark.read.format("csv")\
-- MAGIC     .option("header", "true")\
-- MAGIC     .option("inferSchema", "true")\
-- MAGIC     .load("/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/BigMart Sales.csv")
-- MAGIC
-- MAGIC df1 = df.limit(5)
-- MAGIC display(df1)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Temp views?

-- COMMAND ----------

-- MAGIC %md
-- MAGIC - temp views are temporary. 
-- MAGIC - They are deleted after the cluster is stopped/terminated/ after the session is over. 
-- MAGIC - temp view is only available for that 1 session. 
-- MAGIC
-- MAGIC now you can play around (temporarily) using the temp view created.
-- MAGIC
-- MAGIC To make the temp view available to other sessions, create a Global Temp view.

-- COMMAND ----------

-- MAGIC %python
-- MAGIC #creates a temp view "orders_temp"
-- MAGIC
-- MAGIC df.createOrReplaceTempView("sales_temp")

-- COMMAND ----------

select * from sales_temp limit 4

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Global temp View
-- MAGIC
-- MAGIC - temp views which are available in all sessions till the cluster is on/working.
-- MAGIC - they are only available in all purpose compute and other computes (but not serverless compute)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### External Vs Managed Tables

-- COMMAND ----------

-- create a catelog

CREATE CATALOG sparkSQL_catelog;

-- COMMAND ----------

-- create Schema

CREATE SCHEMA sparkSQL_catelog.sparkSQL_schema;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### 1. Create Managed tables.
-- MAGIC

-- COMMAND ----------

CREATE TABLE sparksql_catelog.sparksql_schema.sales_managedtable
AS
SELECT * from sales_temp;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### 2. Create External tables.

-- COMMAND ----------

/*
CREATE  TABLE sparksql_catelog.sparksql_schema.sales_exttable \
LOCATION 's3://<your-bucket>/<your-directory>/sales_exttable' \
AS \
SELECT * from sales_temp;
*/

-- COMMAND ----------

