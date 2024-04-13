
from goodpy.f.iterable_and_seperator.concat import f as concat

from typing import Callable
from os.path import exists
from os import getcwd
from os import mkdir
from os import rmdir

def f(path: str):
  if not exists(path): mkdir(path)
  return path

f   : Callable[[str], str] = lambda path: [mkdir(path) if not exists(path) else lambda: None, path][1]
up  : Callable[[], str] = lambda: concat([getcwd(), '__file__' + 'test'], '/')
dn  : Callable[[], None] = lambda: rmdir(concat([getcwd(), '__file__' + 'test'], '/'))
t   : Callable[[], bool] = lambda: [exists(f(up())), dn()][0]
