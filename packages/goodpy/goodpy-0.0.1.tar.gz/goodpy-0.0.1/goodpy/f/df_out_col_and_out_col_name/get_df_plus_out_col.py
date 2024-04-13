from pyspark.sql.types import BooleanType
from goodpy.k.spark import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql import DataFrame
from pyspark.sql import Column

def f(df: DataFrame, out_col: Column, out_col_name: str):
  return df.withColumn(out_col_name, out_col)

def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ]
  )
  
  def compare(x, y): return x > y
  compare_udf = udf(compare, BooleanType())
  out = f(df, compare_udf('id', 'open'), 'compare_result')
  return True