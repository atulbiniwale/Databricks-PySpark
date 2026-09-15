# Databricks notebook source
# MAGIC %md
# MAGIC **LLM call using std Python API endpoint provided by Databricks**

# COMMAND ----------

from openai import OpenAI
import os

# How to get your Databricks token: https://docs.databricks.com/en/dev-tools/auth/pat.html
# DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')
# Alternatively in a Databricks notebook you can use this:
DATABRICKS_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-df5a845d-03da.cloud.databricks.com/serving-endpoints"
)

response = client.chat.completions.create(
    model="databricks-gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "What is an LLM agent?"
        }
    ],
    max_tokens=5000
)

print(response.choices[0].message.content)

# COMMAND ----------

# MAGIC %md
# MAGIC **LLM call using SQL query**

# COMMAND ----------

# MAGIC %sql
# MAGIC select ai_query('databricks-gpt-oss-120b', 'can i do AI engineering without data engineering')

# COMMAND ----------

