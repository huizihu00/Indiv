#!/usr/bin/env python
# coding: utf-8

# In[1]:



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


# In[2]:


us_url = 'https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMM_EPM0U_PTE_NUS_DPG&f=W'
r = requests.get(us_url)

# Check status
r.status_code

# Get text from website
soup= BeautifulSoup(r.text, 'lxml')


# In[3]:


table = soup.find('table', {'class' : "FloatTitle"})

row_data=[]
for row in table.find('tbody').find_all('tr')[1:]:
    data = row.find_all('td')
    col = [td.text.strip() for td in data]
    row_data.append(col)

row_data


# In[4]:


for i in row_data:
    if len(i) < 10:
        row_data.remove(i)
        
len(row_data)


# In[5]:


for i in row_data:
    i[1] = i[0][:4]+ '/' + i[1]
    i[3] = i[0][:4]+ '/' + i[3]
    i[5] = i[0][:4]+ '/' + i[5]
    i[7] = i[0][:4]+ '/' + i[7]
    i[9] = i[0][:4]+ '/' + i[9] 
    
df = pd.DataFrame(row_data)


# In[6]:


dictionary = dict(zip(df[1], df[2]))
i=3

while i <=9:
    diction = dict(zip(df[i], df[i+1]))
    dictionary.update(diction)
    i+=2


# In[7]:


us_fuelprice = pd.DataFrame(list(dictionary.items()),columns = ['Date','Price'] )
us_fuelprice.drop( (us_fuelprice[us_fuelprice['Price'].map(len) < 1]).index, inplace=True)

# Sort the dataframe by time
us_fuelprice.sort_values(by='Date', inplace= True)
us_fuelprice.reset_index(drop = True, inplace = True)
us_fuelprice = us_fuelprice.rename(columns = {'Date':'date','Price': 'price'})


# In[8]:


us_fuelprice.sort_values(by='date', inplace= True)
us_fuelprice.reset_index(drop = True, inplace=True)

# Get the position of where we should start
us_fuelprice.loc[us_fuelprice['date'] == "2012/04/16"]


# In[9]:


us_price= us_fuelprice[906:-1]
us_price.reset_index( drop = True, inplace=True)

# Change the 'price' type to numeric 
us_price['price'] = pd.to_numeric(us_price['price'])
us_price


# In[10]:


difference = []

i=520
while i >= 0:
    diff = us_price['price'].iloc[i+1] -us_price['price'].iloc[i]
    difference.append(diff)
    i -= 1

difference = difference[ : : -1] 

# Manually calculate the differnce
float(us_fuelprice['price'].iloc[-1])-float(us_fuelprice['price'].iloc[-2])


# In[11]:


difference.append(-0.027)

us_price['us_price_diff'] = difference
us_price['us_price_diff'].round(decimals = 3)
us_price.columns = ['date', 'us_price', 'us_price_diff']


# In[12]:


us_price['date'] = [i.replace("/", '-') for i in us_price['date']]


# In[20]:


uk_fuelprice=spark.read.parquet("/project/DataEngineering/parquet_files/uk_fuelprice.parquet").toPandas()


# In[22]:


timestampStr = [i.strftime("%Y/%m/%d") for i in uk_fuelprice['date']]
uk_fuelprice['date'] = timestampStr

# Locate the date we want
uk_fuelprice[uk_fuelprice['date'] == '2012/04/16']


# In[24]:


uk_price = uk_fuelprice[462:].reset_index( drop=True)
uk_price['uk_diff'] = uk_price['uk_diff'].round(decimals = 3)

# Uniform the date format
uk_price['date'] = [i.replace("/", '-') for i in uk_price['date']]
uk_price


# In[25]:


fuel_price = pd.merge(us_price, uk_price, on='date')


# In[26]:


fuel_price = spark.createDataFrame(fuel_price)
fuel_price.printSchema()

# Concert into Parquet format
fuel_price.write.parquet("/project/DataEngineering/parquet_files/fuel_price.parquet", mode = "overwrite")


# In[ ]:




