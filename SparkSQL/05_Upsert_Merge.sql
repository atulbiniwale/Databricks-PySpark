-- Databricks notebook source
-- MAGIC %md
-- MAGIC ### Upsert or Merge (means Update plus Insert)
-- MAGIC
-- MAGIC this is Very Very Imp

-- COMMAND ----------

-- MAGIC %python
-- MAGIC df = spark.read.table("sparksql_catelog.sparksql_schema.sales_managedtable")

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC # CREATE A TEMP VIEW
-- MAGIC df.createOrReplaceTempView("sales_temp" )
-- MAGIC
-- MAGIC # or (use any of the methods for creating a temp view)
-- MAGIC
-- MAGIC # CREATE A TEMP VIEW (alternative way to create a temp view)
-- MAGIC spark.sql('''SELECT * FROM {sales_temp}''', sales_temp = df)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### if you have new sales records, then you can Upsert them in other table.

-- COMMAND ----------

MERGE INTO sparksql_catelog.sparksql_schema.sales_managedtable  as target
USING sales_temp as source
ON target.Item_Identifier = source.Item_Identifier
WHEN MATCHED THEN
UPDATE SET *
WHEN NOT MATCHED
THEN INSERT *