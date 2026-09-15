# Databricks notebook source
# MAGIC %md
# MAGIC ### DB Utilities

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 1. dbutils.fs()

# COMMAND ----------

dbutils.fs.ls('/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume')

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 2. dbutils.widgets  (text, dropdown, combobox, multiselect etc)

# COMMAND ----------

dbutils.widgets.text("parameter_value", "test_parameter_value")

# COMMAND ----------


para_value = dbutils.widgets.get("parameter_value")
print(para_value)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 3. Secrets

# COMMAND ----------

# these are only examples.
# dbutils.secrets.list(scope = 'db_scope')  
# dbutils.secrets.get(scope = 'db_scope', key = 'db_password')