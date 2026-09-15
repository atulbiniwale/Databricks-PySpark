-- Databricks notebook source
select * from sparksql_catelog.sparksql_schema.sales_managedtable limit 5

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Creating a Py Dataframe from SQL Select query result set.

-- COMMAND ----------

-- MAGIC %python
-- MAGIC df_test = spark.sql('''SELECT * FROM sparksql_catelog.sparksql_schema.sales_managedtable limit 5;''')
-- MAGIC
-- MAGIC display(df_test)
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC