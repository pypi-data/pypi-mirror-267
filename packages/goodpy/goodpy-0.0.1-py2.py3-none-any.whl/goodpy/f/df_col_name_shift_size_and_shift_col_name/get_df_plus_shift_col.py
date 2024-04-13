from goodpy.f.df_out_col_and_out_col_name import get_df_plus_out_col
from pyspark.sql.types import IntegerType
from goodpy.k.spark import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.functions import col
from pyspark.sql import DataFrame
from pprint import pprint

def f(df: DataFrame, in_col_name: str, shift_size: int, out_col_name: str):
  shift = udf(lambda x: x + shift_size, IntegerType())
  shifted_df = get_df_plus_out_col(df, shift(col('id')), 'id')
  shifted_df = shifted_df.select('id', col(in_col_name).alias(out_col_name))
  out = shifted_df.join(df, on='id')
  return out
  
def t1(df):
  out = f(df, 'open', 2, 'shifted_open')
  out = out.sort('id')
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [
    {'id': 3, 'open': 3, 'shifted_open': 1},                                       
    {'id': 4, 'open': 4, 'shifted_open': 2}
  ]
  return y == out_dicts

def t2(df):
  out = f(df, 'open', -2, 'shifted_open', )
  out = out.sort('id')
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [
    {'id': 1, 'open': 1, 'shifted_open': 3},                                       
    {'id': 2, 'open': 2, 'shifted_open': 4}
  ]
  return y == out_dicts
  
def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ]
  )
  return all(
    [
      t1(df),
      t2(df)
    ]
  )
