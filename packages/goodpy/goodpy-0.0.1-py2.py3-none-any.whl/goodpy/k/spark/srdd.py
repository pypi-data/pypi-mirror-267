from pyspark.serializers import AutoBatchedSerializer, CPickleSerializer
from goodpy.k.spark.spark_context import SparkContext
from pyspark.rdd import RDD
from pyspark.sql import Row
from typing import Callable

def is_correct_format(x: RDD)->bool: return set(x.take(1)[0].asDict().keys()) == {'id', 'data'}

class SRDD(RDD):
  def __init__(self, rdd: RDD):
    if is_correct_format(rdd):
      RDD.__init__(self, rdd._jrdd, rdd.context, AutoBatchedSerializer(CPickleSerializer()))
    else:
      raise ValueError('RDD does not have the right index and data fields')
    
f : Callable[[dict], SRDD] = lambda x: SRDD(**x)

def t()->bool:
  x = SparkContext().parallelize(
    [
      Row(id=1, data=Row(date='2023-01-01', open=2, low=0, high=2, close=1.5)),      
      Row(id=2, data=Row(date='2023-01-02', open=3, low=1, high=3, close=2.5)),
      Row(id=3, data=Row(date='2023-01-03', open=4, low=2, high=4, close=3.5)),
      Row(id=4, data=Row(date='2023-01-04', open=5, low=3, high=5, close=4.5)),
      Row(id=5, data=Row(date='2023-01-05', open=6, low=4, high=6, close=5.5))
    ]
  )
  z = f({'rdd': x})
  joined = z.join(x).map(lambda x: x[1][0] == x[1][1])
  return all(joined.collect())
