#!/usr/bin/python
# Daniel Noyes, ECE565F2015 HW#1
# HW#1 create program to read and print a file
# Programming Language : Python
# Environment: Linux
# Instructions: run in bash "python ece565hw01code.py ece565hw01.txt"
import sys

def printfile(fname):
  print('Input file is : %s' % fname)
  fh = open(fname)
  for line in fh:
    print(line)

if __name__ == "__main__":
  printfile(str(sys.argv[1]))
