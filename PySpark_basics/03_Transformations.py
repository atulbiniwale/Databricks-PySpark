# Databricks notebook source
from pyspark.sql.functions import col

df = spark.read.format("csv")\
                .option('inferSchema', 'true')\
                .option("header", "true")\
                .load("/Volumes/pyspark_catelog/pyspark_schema/pyspark_volume/BigMart Sales.csv")

df.limit(5).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create a New colmnn and Modify existing Column

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 1. Create a new Calc column based on condition

# COMMAND ----------

df.withColumn('CalcCol',
              col('Item_MRP') * col('Item_Outlet_Sales')
             ).limit(5).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 2. Modify Existing Columns based on certain conditions

# COMMAND ----------

from pyspark.sql.functions import regexp_replace, col

df.withColumn('Item_Fat_Content', regexp_replace(col('Item_Fat_Content'), 'Regular', 'Reg'))\
    .withColumn('Item_Fat_Content', regexp_replace(col('Item_Fat_Content'), 'Low Fat', 'LF'))\
    .limit(5)\
    .display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Type Casting
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import StringType

df1 = df.withColumn('Item_Weight', 
                    col('Item_Weight').cast(StringType())
                    )

df1.printSchema()   # notice here that ItemWeight data type has been changed from double to string

# COMMAND ----------

# MAGIC %md
# MAGIC ### Sorting / Order by

# COMMAND ----------

df.sort(col('Item_Outlet_Sales').desc()).display()    #sorting in desc order on column 'Item_Outlet_Sales'

# Alternatively we can use df.orderBy  also for the same result.


# COMMAND ----------

# MAGIC %md
# MAGIC #### Sort on multiple Columns

# COMMAND ----------

df.sort(
        ['Item_Weight', 'Item_Outlet_Sales'], ascending = [0,1]   # this way item weight will get sorted on asc = false (0) and item sales will get sorted on asc = true (1)
        ).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Drop Column/s

# COMMAND ----------

df1.drop("Item_Visibility", "Outlet_Establishment_Year").limit(5).display()

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### De-Dups

# COMMAND ----------

df.dropDuplicates().display()

# COMMAND ----------

#dropping dups based on values on specific columns
df.dropDuplicates(subset = ['Item_Type']).display()

# COMMAND ----------

# distinct rows

df.distinct().display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Union of 2 Dfs

# COMMAND ----------

# create first dataframe
data1 = [
        ('1', 'sid'),
        ('2','matt')
        ]
schema1 = 'id STRING, name STRING'

df1 = spark.createDataFrame(data1, schema1)

# create second dataframe
data2 = [
        ('3', 'don'),
        ('4','alan')
        ]
schema2 = 'id STRING, name STRING'

df2 = spark.createDataFrame(data2, schema2)

# COMMAND ----------

df3 = df1.unionByName(df2)   # order of columns in 2 dfs does not matter but column names should be same.
df3.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### String functions

# COMMAND ----------

from pyspark.sql.functions import initcap, upper, lower

df.select(initcap('Item_Type')).limit(2).display()
df.select(upper('Item_Type')).limit(2).display()
df.select(lower('Item_Type')).limit(2).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Date Functions

# COMMAND ----------

# Current Date

from pyspark.sql.functions import current_date

df = df.withColumn('curr_date', current_date())
df.limit(2).display()

# COMMAND ----------

# Add days, Months in Date >   date_add(), add_months() function

from pyspark.sql.functions import date_add, add_months

df = df.withColumn('days_before', date_add('curr_date', -7))
df = df.withColumn('days_after', date_add('curr_date', 7))
df = df.withColumn('month_after', add_months('curr_date', 1))
df.limit(2).display()

# COMMAND ----------

# difference between 2 dates > datediff
from pyspark.sql.functions import datediff

df = df.withColumn('days_diff', datediff('days_after', 'days_before'))
df.limit(2).display()

# COMMAND ----------

# date format > to_date()

from pyspark.sql.functions import to_date, date_format

df = df.withColumn('days_after_formatted', date_format('days_after', 'dd-MM-yyyy'))
df.limit(2).display()
# date format > to_date()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Handling NULLS

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 1.Drop NULLS

# COMMAND ----------

df.dropna('all').limit(3).display()   #'all' means drop rows where all columns are null.

df.dropna('any').limit(3).display()   #'any' means drop rows where any column value is null.

df.dropna(subset=['Outlet_Size']).display()  # drop rows where Outlet_Size is null.

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 2. Fill Nulls with appropriate values

# COMMAND ----------

df.fillna('unknown', subset=['Outlet_Size']).display()   #fills Outlet_Size with 'unknown'


# COMMAND ----------

# MAGIC %md
# MAGIC ### Split Column in Array and then Index the Array

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1. Split array   (check "Outlet_type" column)

# COMMAND ----------

from pyspark.sql.functions import split

df.withColumn('Outlet_Type', split('Outlet_Type', ' ')).limit(3).display()


# COMMAND ----------

# MAGIC %md
# MAGIC #### 2. Index an array (check "Outlet_type" column)

# COMMAND ----------

df.withColumn('Outlet_Type', split('Outlet_Type', ' ')[1]).limit(3).display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### 3.Explode  (from the array, you want each value to be in the new row.) (check "Outlet_type" column)

# COMMAND ----------

from pyspark.sql.functions import explode

df.withColumn('Outlet_Type', explode(split('Outlet_Type', ' '))).limit(5).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Array Contains something or not?  (look at Outlet_type column)

# COMMAND ----------

from pyspark.sql.functions import split

df.withColumn('Outlet_Type', split('Outlet_Type', ' ')).limit(3).display()

# COMMAND ----------

# check if the array has "Type_1" in it or not?

from pyspark.sql.functions import array_contains, split

df_split= df.withColumn('Outlet_Type', split('Outlet_Type', ' '))

df_split.withColumn('Type1_flag', array_contains('Outlet_Type', 'Type1')).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Group by

# COMMAND ----------

from pyspark.sql.functions import col, grouping, sum, avg

df4 = df.select(
            col('Item_Identifier').alias('item_id'), 
            col('Item_Fat_Content'),
            col('Item_Type'),
            col('Item_Outlet_Sales')
        ).limit(25)


#group by 'Item fat content' and 'Item_type' columns, aggregated function is sum of itemoutlet sales. In case of average, use avg().

df4.groupBy('Item_Fat_Content','Item_Type').agg(sum('Item_Outlet_Sales'), avg('Item_Outlet_Sales')).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Collect_list  (similar to Pivot)
# MAGIC

# COMMAND ----------

data1 = [
        ('user1', 'book1'),
        ('user1','book2'),
        ('user2','book2'),
        ('user2','book3'),
        ('user2','book4')
        ]
schema1 = 'user STRING, book STRING'

df1 = spark.createDataFrame(data1, schema1)
df1.display()

# COMMAND ----------

from pyspark.sql.functions import collect_list

df1.groupBy("user").agg(collect_list("book")).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Pivot

# COMMAND ----------

df.groupBy('Item_Type').pivot('Outlet_Size').avg('Item_MRP').display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### When-Otherwise (similar to CASE)

# COMMAND ----------

### this is similar to CASE statement in SQL.
from pyspark.sql.functions import col, when

df_flag = df.withColumn('veg_flag', 
            when(col('Item_Type') == "Meat", 'Non Veg').otherwise('Veg')
            )

df_flag.withColumn(
    'veg_expensive',
    when((col('veg_flag') == "Veg") & (col('Item_MRP') < 100), 'Veg_inexpensive')
    .when((col('veg_flag') == "Veg") & (col('Item_MRP') > 100), 'Veg_Expensive')
    .otherwise('Non-Veg')
).limit(3).display()

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Joins**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ###### 1. Inner Join (Use SparkSQL)
# MAGIC ###### 2. Left/ Right Join (Use SparkSQL)
# MAGIC ###### 3. Full Join (Use SparkSQL)
# MAGIC ###### 4. Anti Join    
# MAGIC df1.join(df2,df1['dept_id']==df2['dept_id'],'anti').display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Window Functions
# MAGIC
# MAGIC ##### Use from SparkSQL as they are easier and work the same.

# COMMAND ----------

# MAGIC %md
# MAGIC ### User Defined Functions in PySpark (UDF)
# MAGIC
# MAGIC UDFs give flexibility, but can reduce performance!
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 1:  Define a Normal Py Function

# COMMAND ----------


def my_func(x):
    return x*x 

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 2:  Convert into UDF of PySpark

# COMMAND ----------


my_udf = udf(my_func)
df.withColumn('mynewcol',my_udf('Item_MRP')).display()