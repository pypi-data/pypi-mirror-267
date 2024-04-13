from goodpy.f.df_out_col_and_out_col_name import get_df_plus_out_col
from goodpy.f.df_and_condition_col import get_filtered_df
from goodpy.k.spark.spark_session import SparkSession
from pyspark.sql.functions import collect_list
from pyspark.sql.functions import explode
from pyspark.ml.linalg import DenseVector
from pyspark.sql.types import BooleanType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import ArrayType
from pyspark.sql.functions import udf
from pyspark.sql.functions import col
from pyspark.sql import DataFrame

def f(df: DataFrame, in_col: str, out_col: str, window_size: int):
  gen_window = udf(lambda x: [x + i for i in range(window_size)], ArrayType(IntegerType()))
  flatmap_df = get_df_plus_out_col(df, gen_window('id'), 'id')
  flatmap_df = get_df_plus_out_col(flatmap_df, explode('id'), 'id')
  sliding_df = flatmap_df.groupBy('id').agg(collect_list(in_col).alias(out_col))
  check_len = udf(lambda x: len(x) == window_size, BooleanType())
  sliding_df = get_filtered_df(sliding_df, check_len(col(out_col)))
  out_df =  df.join(sliding_df, on='id', how='inner')
  return out_df

def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'vector': DenseVector([1.0, 2.0])},                       
      {'id': 2, 'vector': DenseVector([2.0, 3.0])},
      {'id': 3, 'vector': DenseVector([3.0, 4.0])},
      {'id': 4, 'vector': DenseVector([4.0, 5.0])}
    ]
  )
  out = f(df, 'vector', 'sliding_vector', 2)
  out = out.sort('id')
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [
    {
      'id': 2,
      'sliding_vector': [DenseVector([1.0, 2.0]), DenseVector([2.0, 3.0])],
      'vector': DenseVector([2.0, 3.0])
    },
    {
      'id': 3,
      'sliding_vector': [DenseVector([2.0, 3.0]), DenseVector([3.0, 4.0])],
      'vector': DenseVector([3.0, 4.0])},
    {
      'id': 4,
      'sliding_vector': [DenseVector([3.0, 4.0]), DenseVector([4.0, 5.0])],
      'vector': DenseVector([4.0, 5.0])
    }
  ]
  return out_dicts == y
