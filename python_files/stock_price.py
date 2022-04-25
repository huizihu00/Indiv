#!/usr/bin/env python
# coding: utf-8

# In[6]:



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


# In[7]:


uga = spark.read.parquet("/project/DataEngineering/parquet_files/uga_info.parquet").toPandas()
uga['High']= uga['High'].astype(float)
uga['Low']= uga['Low'].astype(float)
uga['Close']= uga['Close'].astype(float)
uga['Volume']= uga['Volume'].astype(float)


# In[8]:


# Get difference of stock price within one week
uga['uga_Difference'] = (uga['High'] - uga['Low'])/uga['Close']*100
uga.drop(labels= ['High', 'Low', 'Open', 'Adj_Close'], axis=1, inplace=True)


# In[9]:


uga = uga.rename(columns={"Date": "date", "Close":"uga_close", "Volume":"uga_volume", "uga_Difference":"uga_difference"})


# In[10]:


shell = spark.read.parquet("/project/DataEngineering/parquet_files/shell_info.parquet").toPandas()


# In[11]:


shell['High']= shell['High'].astype(float)
shell['Low']= shell['Low'].astype(float)
shell['Close']= shell['Close'].astype(float)
shell['Volume']= shell['Volume'].astype(float)


# In[12]:


shell['shell_Difference'] = (shell['High'] - shell['Low'])/shell['Close']*100
shell.drop(labels= ['High', 'Low', 'Open', 'Adj_Close'], axis=1, inplace=True)
shell = shell.rename(columns={"Date":"date", "Close":"shell_close", "Volume":"shell_volume", "shell_Difference" : "shell_difference"})


# In[13]:


stock_price = pd.merge(uga, shell, on='date')


# In[14]:


stock_price = spark.createDataFrame(stock_price)
stock_price.printSchema()
stock_price.write.parquet("/project/DataEngineering/parquet_files/stock_price.parquet", mode ='overwrite')


# In[ ]:





# In[ ]:




