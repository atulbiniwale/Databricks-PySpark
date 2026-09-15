# Databricks notebook source
# MAGIC %sql
# MAGIC select * from sparksql_catelog.sparksql_schema.sales_managedtable limit 5

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ranking

# COMMAND ----------

# MAGIC %sql
# MAGIC select Item_Type, Item_MRP as price_per_unit,
# MAGIC         Rank() over ( partition by Item_Type order by Item_MRP desc) as rank,
# MAGIC         Dense_Rank() over ( partition by Item_Type order by Item_MRP desc) as dense_rank,
# MAGIC         Row_Number() over ( partition by Item_Type order by Item_MRP desc) as row_number
# MAGIC from sparksql_catelog.sparksql_schema.sales_managedtable
# MAGIC where Item_MRP < 38
# MAGIC order by Item_MRP desc

# COMMAND ----------

# MAGIC %md
# MAGIC ### Framing / Partitions for Cumulative totals

# COMMAND ----------

# MAGIC %sql
# MAGIC select  Item_Type, Item_MRP, 
# MAGIC         sum(Item_MRP) over (order by Item_MRP rows between unbounded preceding and current row) as RunningTotal1,
# MAGIC         sum(Item_MRP) over (order by Item_MRP rows between unbounded preceding and unbounded following) as Total1,
# MAGIC         -- combinations can be done between unbounded and preceding/following, current row
# MAGIC         
# MAGIC         sum(Item_MRP) over (partition  by Item_Type order by Item_MRP rows between unbounded preceding and current row) as RunningTotal2,
# MAGIC         sum(Item_MRP) over (partition by Item_Type order by Item_MRP rows between unbounded preceding and unbounded following) as Total2
# MAGIC        
# MAGIC from sparksql_catelog.sparksql_schema.sales_managedtable