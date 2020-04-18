# -*- coding: utf-8 -*-

__author__ = "MELO CAVALCANTE, Roberto"
__copyright__ = "Copyright 2020, Roberto Melo Cavalcante"
__credits__ = ["Niklaus Wirth", "José Ramalho", "Nilo Manezes"]
__license__ = "MIT"

__version__ = "1.0.0"

__maintainer__ = "Roberto"
__email__ = ""
__status__ = "Production"

from collections import Iterable

def cube(n):
  assert isinstance(n, int), "parameter is not a number"
  return n*n*n

def factorial(n):
  assert isinstance(n, int), "parameter is not a number"
  assert n > -1, "parameter must non-negative"
  if(n==0):
    return 1
  return n * factorial(n-1)

def counter_pattern(pattern, lst):
  assert isinstance(pattern, list), "pattern parameter is not a tuple"
  assert isinstance(lst, list), "lst parameter is not a tuple"
  p_len = len(pattern)
  l_len = len(lst)
  start = 0
  pattern_counter = 0
  while (start + p_len) <= l_len:
    matched = True
    for x in range(p_len):
      if(lst[start+x] != pattern[x]):
        matched = False;
        break;
    if(matched):
      pattern_counter = pattern_counter + 1
    start = start + 1
  return pattern_counter

def depth(e):
  d = {}
  last_level = 0
  depth_detailed(e, d, last_level)
  vMaxDepth = 0
  for key in d: 
    vMaxDepth = max(vMaxDepth, key)
  return vMaxDepth

def depth_detailed( e, d, last_level):
  if( not (isinstance(e, list) or isinstance(e, tuple))):
    return 0
  if(len(e) == 1):
    return 0
  current_level = last_level + 1
  #print "current_level:" + str(current_level)
  d[current_level] = 1
  index = 0
  len_tuple = len(e)
  for x in e:
    depth_detailed(x, d, current_level)

def tree_ref(tree, index):
  assert isinstance(tree, Iterable), "tree parameter is not a tuple"
  assert isinstance(index, Iterable), "index parameter is not a tuple"
  assert isinstance(index[0], int), "index first parameter is not a number"
  tl = len(tree)
  if( index[0] > (tl-1)):
    return None
  il = len(index)
  node = tree[index[0]]
  if(il == 1):
    return node
  return tree_ref(node,index[1:])


