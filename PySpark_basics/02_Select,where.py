# Databricks notebook source
df = spark.read.format("csv")\
                .option('inferSchema', 'true')\
                .option("header", "true")\
                .load("/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/BigMart Sales.csv")

df.limit(5).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Select (with Alias, limit)

# COMMAND ----------

from pyspark.sql.functions import col

df.select(
            col('Item_Identifier').alias('item_id'), 
            col('Item_Fat_Content')
        ).limit(5).display()


# COMMAND ----------

# MAGIC %md
# MAGIC ### Filter (with multiple conditions like and, or, is in, is null, not null etc)

# COMMAND ----------

df.filter(
        
        (col('Item_Fat_Content') == 'Regular')
        &     # & is AND and | is OR
        (col('Item_Type') == 'Dairy')
        &
        (col('Outlet_Size').isNull() )    # .isNULL() function
        &
        (col('Outlet_Location_Type').isin('Tier 1','Tier 2') )   # .isin() function
        
        ).limit(5).display()