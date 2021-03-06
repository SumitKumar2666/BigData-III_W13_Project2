#%%
import pandas as pd
import numpy as np
from pyspark.ml.linalg import Vectors
from pyspark.ml.stat import Correlation
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Spark').getOrCreate()

df = spark.read.format("com.databricks.spark.csv").option("header", "true").load("flights.csv")

df2 = spark.read.format("com.databricks.spark.csv").option("header", "true").load("airports.csv")

df.registerTempTable("df")
df2.registerTempTable("df2")

# ds= spark.sql("select OriginAirportID,Sum(DepDelay) AS Total_DEP_Delay from df Group By OriginAirportID")

# ds2= spark.sql("select OriginAirportID,Sum(DepDelay) AS Total_DEP_Delay from df Group By OriginAirportID")

ds= spark.sql("select DestAirportID,Sum(DepDelay) AS Total_DepDelay from df Group by DestAirportID")

ds2= spark.sql("select airport_id,city from df2")


dataset1= ds.toPandas()
dataset2= ds2.toPandas()




#create new column in df1 for price diff


#we will replace the new transaction ids with old ones and change the items accoringly

dataset1.set_index('DestAirportID')
dataset2.set_index('airport_id')

dataset3= dataset2.loc[dataset2['airport_id'].isin(dataset1['DestAirportID'])]

# new= dataset1['DestAirportID'].isin(dataset2['airport_id'])
# dataset2['airport_id']=dataset1[new]
# dataset1.rename(columns = {'DestAirportID': 'airport_id'}, inplace = True)
# dataset2.dropna()

# dataset3= pd.merge(dataset1, dataset2, on="airport_id")
dataset3.set_index('airport_id')
dataset4= dataset1.loc[dataset1['DestAirportID'].isin(dataset2['airport_id'])]

# dataset3['Total_DepDelay']= dataset1['Total_DepDelay']
dataset3.rename(columns = {'city': 'Destination'}, inplace = True)
dataset4.rename(columns = {'DestAirportID': 'airport_id'}, inplace = True)

dataset5= pd.merge(dataset3, dataset4, on="airport_id")


#ds3= spark.sql("select DestAirportID,Sum(DepDelay) AS Total_DepDelay from df2 where DestAirportID='13851' Group by DestAirportID")
dataset5.dropna()
print(dataset5.head())
# print(spark.sql("select OriginAirportID,Sum(DepDelay) from df Group by OriginAirportID Order By OriginAirportID").show())

# %%

# %%