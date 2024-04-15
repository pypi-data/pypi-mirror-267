#!/usr/bin/env python3
"""
 These modules should contain one function each...

MODIFIY THE original codeframe adding these functions only + editing CONFIG

... they need some common connect point to have common objects:
 1. config ?
  -  yes, but is there possible to do without?
     - ? for the sake of codeframe initial paradigm? or is that ok?

"""

from fire import Fire
from console import fg,bg


def load():  print("in load @ fn_load ... but this doeasnt happen normally")

def main(*args,**kwargs):
    print(f"D... @main @fn_load /{args}/{kwargs}/. module loaded, function called")

if __name__=="__main__":
    Fire(main)
