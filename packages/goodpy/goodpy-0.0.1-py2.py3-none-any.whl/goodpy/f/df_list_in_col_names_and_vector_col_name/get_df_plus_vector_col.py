from goodpy.k.spark.spark_session import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import DenseVector
from pyspark.sql import DataFrame
from typing import List

def f(df: DataFrame, in_cols: List[str], out_col: str):
  return VectorAssembler(inputCols=in_cols, outputCol=out_col).transform(df)

def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ]
  )
  out = f(df, ['id', 'open'], 'vector')
  out = out.sort('id')
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))

  y = [
    {'id': 1, 'open': 1, 'vector': DenseVector([1.0, 1.0])},                       
    {'id': 2, 'open': 2, 'vector': DenseVector([2.0, 2.0])},
    {'id': 3, 'open': 3, 'vector': DenseVector([3.0, 3.0])},
    {'id': 4, 'open': 4, 'vector': DenseVector([4.0, 4.0])}
  ]
  
  return out_dicts == y
