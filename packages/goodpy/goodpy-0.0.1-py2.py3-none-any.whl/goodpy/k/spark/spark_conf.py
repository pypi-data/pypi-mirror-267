from goodpy.f.iterable_and_seperator.concat import f as concat
from goodpy.f.dirpath.mkdir import f as mkdir
from pyspark.conf import SparkConf as Conf
from typing_extensions import Self
from os.path import expanduser
from typing import Callable

def spark_derby_option(self)->str: return '='.concat(['-Dderby.system.home', self.spark_derby])

class SparkConf(Conf):
  def __init__(self, app_name='n', num_cores: str = '*', executor_memory: str ='20g', driver_memory: str ='20g', dir: str =None):
    Conf.__init__(self)
    self._dir = dir = mkdir(concat([mkdir(expanduser('~/.data')), 'spark'], '/')) if dir is None else dir
    self.setMaster('local[{}]'.format(num_cores))
    self.setAppName(app_name)
    self.set('spark.sql.warehouse.dir', self.dir_warehouse)
    self.set('spark.driver.bindAddress', '127.0.0.1')
    self.set('spark.driver.extraJavaOptions', self.derby_option)
    self.set('spark.executor.memory', executor_memory)
    self.set('spark.driver.memory', driver_memory)
    self.set('spark.executor.allowSparkContext', 'true')
    self.set('spark.sql.catalogImplementation', 'hive')
  
  dir               : Callable[[Self], str] = property(lambda s: s._dir)
  dir_warehouse     : Callable[[Self], str] = property(lambda s: mkdir(concat([s.dir, 'warehouse'], '/')))
  dir_derby         : Callable[[Self], str] = property(lambda s: mkdir(concat([s.dir, 'derby'], '/')))
  derby_option      : Callable[[Self], str] = property(lambda s: concat(['-Dderby.system.home', s.dir_derby], '='))
    
def f(x: dict={})->SparkConf: return SparkConf(**x)
def t(): return f({'num_cores': '4', 'executor_memory': '2g', 'driver_memory': '2g'})