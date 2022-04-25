#!/usr/bin/env python
# coding: utf-8

# In[21]:


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


# In[22]:


spark = SparkSession     .builder     .appName("PySpark App")     .config("spark.jars", "postgresql-42.3.2.jar")     .getOrCreate()


# In[12]:


us_url = 'https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMM_EPM0U_PTE_NUS_DPG&f=W'
r = requests.get(us_url)

# Check status
r.status_code

# Get text from website
soup= BeautifulSoup(r.text, 'lxml')


# In[13]:


table = soup.find('table', {'class' : "FloatTitle"})

row_data=[]
for row in table.find('tbody').find_all('tr')[1:]:
    data = row.find_all('td')
    col = [td.text.strip() for td in data]
    row_data.append(col)


# In[14]:


for i in row_data:
    if len(i) < 10:
        row_data.remove(i)
        
len(row_data)


# In[15]:


for i in row_data:
    i[1] = i[0][:4]+ '/' + i[1]
    i[3] = i[0][:4]+ '/' + i[3]
    i[5] = i[0][:4]+ '/' + i[5]
    i[7] = i[0][:4]+ '/' + i[7]
    i[9] = i[0][:4]+ '/' + i[9] 
    
df = pd.DataFrame(row_data)


# In[16]:


dictionary = dict(zip(df[1], df[2]))
i=3

while i <=9:
    diction = dict(zip(df[i], df[i+1]))
    dictionary.update(diction)
    i+=2


# In[17]:


us_fuelprice = pd.DataFrame(list(dictionary.items()),columns = ['Date','Price'] )
us_fuelprice


# In[18]:


us_fuelprice.drop( (us_fuelprice[us_fuelprice['Price'].map(len) < 1]).index, inplace=True)

# Sort the dataframe by time
us_fuelprice.sort_values(by='Date', inplace= True)


# In[19]:


us_fuelprice.reset_index(drop = True, inplace = True)
us_fuelprice = us_fuelprice.rename(columns = {'Date':'date','Price': 'price'})


# In[23]:


us_fuelprice_df = spark.createDataFrame(us_fuelprice)
us_fuelprice_df.write.parquet("/project/DataEngineering/parquet_files/us_fuelprice.parquet", mode = 'overwrite')
us_fuelprice_df.printSchema()


# In[25]:


make_checkpoint()


# In[ ]:




