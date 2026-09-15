-- Databricks notebook source
-- MAGIC %md
-- MAGIC ### Dynamic Data Masking

-- COMMAND ----------

select * from sparksql_catelog.sparksql_schema.sales_managedtable limit 5

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC #### Create a MASK function

-- COMMAND ----------

CREATE OR REPLACE FUNCTION sparksql_catelog.sparksql_schema.dyn_mask(p_userid STRING)
RETURN
CASE WHEN is_account_group_member('admins') THEN p_userid ELSE '*****' END;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC #### Applying Mask Function to the Column "Userid"

-- COMMAND ----------

ALTER TABLE sparksql_catelog.sparksql_schema.sales_managedtable
ALTER COLUMN Item_MRP SET MASK sparksql_catelog.sparksql_schema.dyn_mask;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Now if someone in not a part of Admins group, then that user will see ********  in the column "Item_MRP"

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Remove Previously created masks 

-- COMMAND ----------

-- Remove column masks from all columns
ALTER TABLE sparksql_catelog.sparksql_schema.sales_managedtable 
ALTER COLUMN Item_MRP DROP MASK;

