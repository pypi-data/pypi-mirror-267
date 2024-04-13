
from goodpy.k.spark.spark_session import SparkSession
from pyspark.sql import Column
from pyspark.sql.types import BooleanType
from pyspark.sql.functions import udf
from pyspark.sql import DataFrame

def f(df: DataFrame, condition_col: Column): return df.filter(condition_col)

def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ]
  )
  func = udf(lambda x: x >= 4, BooleanType())
  out = f(df, func('open'))
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [{'id': 4, 'open': 4}]
  return y == out_dicts
