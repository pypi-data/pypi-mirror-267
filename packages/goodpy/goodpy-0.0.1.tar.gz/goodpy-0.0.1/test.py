from time import time
from jft.directory.list_testables import f as list_testables
from jft.pickle.load_if_exists import f as load_pickle
from os.path import getmtime
from jft.pickle.save import f as save
from jft.dict.test_durations.to_tuple_list_sorted_by_duration import f as srt
from jft.test.make_Pi_to_test import f as make_Pi_t
from jft.strings.pyfiles.to_dict import f as pyfiles_to_dict
from jft.string.contains.function.test import f as has_t
from jft.string.contains.function.run import f as has_f
from jft.test.pi_test_failed import f as pi_test_failed
from jft.test.handle_pass import f as hp
from jft.check_line_lengths import f as check_line_lengths
from jft.check_final_line import f as check_final_line
from jft.print_oldest_file import f as print_oldest_file
from jft.file.remove import f as remove
from jft.test.handle_fail import f as hf
from jft.text_colours.danger import f as danger
from jft.text_colours.warning import f as warn
import re

excludables = set([
  './start.py',
  './gitter.py'
])

Γ = [
  'def f(',
  'def f():',
  'def f(x):',
  'def f(a, b):',
  'f = lambda a, b:',
  'f = lambda x:',
  'f = lambda:',
  'f = lambda',
  'f : '
]
# has_f = lambda x: print(re.sub(' +', ' ', x))
has_f = lambda x: any([_l.startswith(γ) for γ in Γ for _l in re.sub(' +', ' ', x).split('\n')])

Γ = [
  'def t(',
  'def t():',
  'def t(x):',
  'def t(a, b):',
  't = lambda a, b:',
  't = lambda x:',
  't = lambda:',
  't = lambda',
  't : '
]
has_t = lambda x: any([_l.startswith(γ) for γ in Γ for _l in re.sub(' +', ' ', x).split('\n')])

def f(test_all=False, t_0=time()):
  testables = [
    pyfilepath
    for pyfilepath
    in list_testables() if all([
      pyfilepath not in excludables
    ])
  ]

  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as _: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in testables}
  save(last_mods, './last_modified.pickle')
  _A = [_[0] for _ in srt(last_mods)[::-1]]
  _B = set(make_Pi_t(testables, test_all, prev, last_mods))
  Pi_t = [a for a in _A if a in _B]
  pyfile_data = pyfiles_to_dict(Pi_t)
  max_len = 0
  for pi_index, pi in enumerate(Pi_t):
    content = pyfile_data[pi]
    if pi[-7:] == 'args.py':
      return hp(t_0, Pi_t)
    _m = ' '.join([
      f'[{(100*(pi_index+1)/len(Pi_t)):> 7.2f} % of',
      f'{pi_index+1}/{len(Pi_t)} files.] Checking {pi}'
    ])
    max_len = max(max_len, len(_m))
    print(f'{_m:<{max_len}}')
    if not has_t(content): return hf(set(), pi, danger(" has no ")+warn('t()'))
    if not has_f(content): return hf(set(), pi, danger(" has no ")+warn('f()'))
    if pi_test_failed(pi): return hf(set(), pi, '')
  return hp(t_0, Pi_t)

if __name__ == '__main__':
  print('|'+'-'*78+'|')
  passed, message = f(False)
  print(message)
  if passed:
    check_line_lengths()
    check_final_line()
    print_oldest_file()
  print('|'+'-'*78+'|')
