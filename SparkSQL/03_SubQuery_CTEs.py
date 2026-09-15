# Databricks notebook source
# MAGIC %md
# MAGIC ### SubQuery

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from sparksql_catelog.sparksql_schema.sales_managedtable limit 5
# MAGIC
# MAGIC --Subquery (inside Where, from mainly or in joins )
# MAGIC
# MAGIC --1. inside query
# MAGIC select * from sparksql_catelog.sparksql_schema.sales_managedtable where order_status = 'Delivered' and product_category = 'Fashion'
# MAGIC
# MAGIC --2. outside query
# MAGIC select * 
# MAGIC from (
# MAGIC   select * from sparksql_catelog.sparksql_schema.orders_managedtable where order_status = 'Delivered' and product_category = 'Fashion'
# MAGIC ) as tbl1
# MAGIC where payment_method = 'PayPal'

# COMMAND ----------

# MAGIC %md
# MAGIC ### CTEs

# COMMAND ----------

WITH tbl2 AS (

WITH tbl1 AS (
  SELECT * FROM sparksql_catelog.sparksql_schema.orders_managedtable WHERE order_status = 'Delivered' AND product_category = 'Fashion'
)
SELECT * FROM tbl1 WHERE payment_method = 'PayPal' -- outer query using CTE.

) 
SELECT * FROM tbl2 where product_name = 'Sunglasses'