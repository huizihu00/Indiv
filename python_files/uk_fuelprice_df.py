#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import os

from dvc.api import make_checkpoint
from pyspark.sql import SparkSession
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/project/spark-3.2.1-bin-hadoop3.2"





spark = SparkSession     .builder     .appName("PySpark App")     .config("spark.jars", "postgresql-42.3.2.jar")     .getOrCreate()





file = pd.read_excel(r'/project/DataEngineering/UK_Weekly_Fuel_Prices.xlsx', sheet_name = 'All years')



# In[3]:


# Extract useful information
file.columns =file.iloc[5]
file = file.iloc[6: , :]


# In[4]:


from datetime import datetime

# Convert into date type
file['Date'] = [i.date() for i in file['Date']]


# In[5]:


# Select the first three columms
uk_fuelprice = file.iloc[: ,  :3]
uk_fuelprice.columns = ["date", 'uk_price', 'uk_diff']


# In[6]:


uk_fuelprice['uk_diff'] =[float(i) for i in uk_fuelprice['uk_diff'] ]
uk_fuelprice['uk_diff'].round(decimals = 3)


# In[7]:


uk_fuelprice_df = spark.createDataFrame(uk_fuelprice)
uk_fuelprice_df.printSchema()
uk_fuelprice_df.write.parquet("/project/DataEngineering/parquet_files/uk_fuelprice.parquet", mode= 'overwrite')


# In[ ]:




