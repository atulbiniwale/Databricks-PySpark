# Databricks notebook source
# MAGIC %md
# MAGIC ### Connecting to External Data Lake ( ADLS Gen 2)
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ######## Create a Service Principle in Azure and use it as a intermediatery between DB and ADLS Gen 2. Steps are outlined below.
# MAGIC
# MAGIC https://learn.microsoft.com/en-us/azure/databricks/connect/storage/tutorial-azure-storage

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Reading from Catelog (manually uploaded files)

# COMMAND ----------

# MAGIC %md
# MAGIC ###### 1. Reading a csv

# COMMAND ----------

df = spark.read.format("csv")\
                .option('inferSchema', 'true')\
                .option("header", "true")\
                .load("/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/BigMart Sales.csv")

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ###### 2. Reading a JSON

# COMMAND ----------

df = spark.read.format("json")\
                .option('inferSchema', 'true')\
                .option("header", "true")\
                .load("/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/drivers.json")

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 3. Define and Update Schema

# COMMAND ----------

df.printSchema()    # prints a default schema of the df.

# COMMAND ----------

# MAGIC %md
# MAGIC ###### Create New Schema Definition and Use new schema to change the df.
# MAGIC

# COMMAND ----------

# Step 1: Define New Schema (notice that original forename field is changed to firstname in the new schema.)
my_ddl_schema = '''
                code string,
                dob string,
                driverId long,
                driverRef string,
                name struct<firstname:string, surname:string>,
                nationality string,
                number string,
                url string
                 '''

# Step 2: read data using this new Schema
df = spark.read.format("json")\
                .schema(my_ddl_schema)\
                .load("/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/drivers.json")
    

df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating a New DF

# COMMAND ----------

data1 = [
        ('1', 'sid'),
        ('2','matt')
        ]
schema1 = 'id STRING, name STRING'

df1 = spark.createDataFrame(data1, schema1)
df1.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Writing Data into files in Storage

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 1. To CSV  (currently inside Catelog> Volume)

# COMMAND ----------

from pyspark.sql.functions import col, to_json

newdata = [
        ('1', 'sid'),
        ('2','matt'),
        ('3','matty')
        ]
newschema = 'id STRING, name STRING'

newdf = spark.createDataFrame(newdata, newschema)
newdf.write.format('csv')\
    .option("header", "true")\
    .save("/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/written_csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 2. Append

# COMMAND ----------

newdf.write.format('csv')\
        .mode('append')\
        .save('/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/written_csv')

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 3. Overwrite

# COMMAND ----------

newdf.write.format('csv')\
            .mode('overwrite')\
            .option('/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/written_csv')\
            .save()

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 4. Error

# COMMAND ----------


newdf.write.format('csv')\
            .mode('error')\
            .option('/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/written_csv')\
            .save()

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 5. Ignore

# COMMAND ----------

newdf.write.format('csv')\
            .mode('ignore')\
            .option('/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/written_csv')\
            .save()
     

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 6. To Parquet File

# COMMAND ----------

newdf.write.format('parquet')\
            .mode('overwrite')\
            .option('/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/written_csv')\
            .save()

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 7. To a Table

# COMMAND ----------

newdf.write.format('parquet')\
            .mode('overwrite')\
            .saveAsTable('my_table')

# COMMAND ----------

# MAGIC %md
# MAGIC #### 8. To Delta Format (Delta lake - i.e. Parquet + Delta/ Transaction Logs)

# COMMAND ----------

###

# COMMAND ----------

# MAGIC %md
# MAGIC ###  Convert PySpark DF into Spark SQL.

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Create a Temp View first (this will be destroyed once the session is terminated)
# MAGIC ##### then use that Temp view for normal SQL operations

# COMMAND ----------

# Step 1: create a temp view from PySpark df
newdf.createTempView('my_view') 

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from my_view

# COMMAND ----------

# MAGIC %md
# MAGIC #### Convert spark SQL back into PySpark DF

# COMMAND ----------


df_sql = spark.sql("select * from my_view ")

df_sql.display()