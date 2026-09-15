-- Databricks notebook source
-- MAGIC %md
-- MAGIC
-- MAGIC ### Delta Lake with SparkSQL

-- COMMAND ----------

select * from sparksql_catelog.sparksql_schema.sales_managedtable limit 5

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC #### DESCRIBE EXTENDED command to get info about the catelog (datasets)

-- COMMAND ----------

DESCRIBE  EXTENDED sparksql_catelog.sparksql_schema.sales_managedtable


-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### DATA VERSIONING + Time Travel

-- COMMAND ----------

-- lets imagine we delete some records accidently, but later realized the mistake.
-- In that case, we can go back to previous version and retrieve the original data. 

delete from sparksql_catelog.sparksql_schema.sales_managedtable WHERE Item_Identifier = 'FDA15'

-- COMMAND ----------

-- now lets see the history of this table operations first to see which version of data we want to retrieve.

DESCRIBE HISTORY sparksql_catelog.sparksql_schema.sales_managedtable

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC **VIMP** - now we can retrieve any particular version from above using **"Time Travel"**

-- COMMAND ----------

-- Time Travel

RESTORE sparksql_catelog.sparksql_schema.sales_managedtable TO VERSION AS OF 0
