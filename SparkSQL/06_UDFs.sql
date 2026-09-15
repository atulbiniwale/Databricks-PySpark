-- Databricks notebook source
-- MAGIC %md
-- MAGIC
-- MAGIC ### **User Defined Functions**
-- MAGIC
-- MAGIC 1. Scalar functions
-- MAGIC
-- MAGIC 2. table functions

-- COMMAND ----------

select * from sparksql_catelog.sparksql_schema.sales_managedtable limit 5

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC #### 1. Scalar Function

-- COMMAND ----------

-- Define a function

CREATE OR REPLACE FUNCTION sparksql_catelog.sparksql_schema.discount_price(p_price decimal(10,2))
RETURNS DECIMAL(10,2)
LANGUAGE SQL
RETURN p_price * 0.95

-- COMMAND ----------

-- Use a function

select Item_Identifier, Item_MRP, sparksql_catelog.sparksql_schema.discount_price(Item_MRP) 
from sparksql_catelog.sparksql_schema.sales_managedtable
limit 5

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### 2. Table Function

-- COMMAND ----------

-- Define a function

CREATE OR REPLACE FUNCTION sparksql_catelog.sparksql_schema.discount_price2(p_category STRING) 
RETURNS TABLE
LANGUAGE SQL
RETURN
(SELECT * FROM sparksql_catelog.sparksql_schema.sales_managedtable WHERE Item_Type = p_category)


-- COMMAND ----------

-- Use a function 

select * from sparksql_catelog.sparksql_schema.discount_price2('Dairy')