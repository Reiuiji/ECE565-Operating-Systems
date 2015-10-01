#!/usr/bin/python
# Daniel Noyes, ECE565F2015 HW#3
#
# HW#3 Simulate a virtual memory system with multiprogramming,
#  e.g., Pthreads. Assume that your machine has 4-bit virtual
#  addresses and 8-bit physical address with 2 Byte page size.
#  You need to implement two processes/threads:
# 1) Virtual Address Generation – generates a sequence of 4-bit
#  random number, as virtual addresses, and writes them into an
#  integer buffer of size N.
# 2) Address Translation – reads the next virtual address from
#  the buffer and translates it to a physical address, keeping
#  track of page faults as occurring.
# Test your system on my file “ece565hw03.txt” that contains the
#  page table for your starting point.
#
# Programming Language : Python
# Environment: Linux
# Instructions: run in bash "python ece565hw03code.py ece565hw03.txt"
import sys
import os
import argparse
import random
import time
from multiprocessing import Process, Queue

#input Parser
parser = argparse.ArgumentParser(description='HW 3 Virtual memory system')
parser.add_argument("-i", "--input", dest='INPUT', help="Input File")
parser.add_argument("-o", "--output", dest='OUTPUT', help="Output File")
parser.add_argument("-d", "--debug", dest='DEBUG', help="Enable Debugging Mode", action='store_true')
global args
args = parser.parse_args()

#setup output file
if args.OUTPUT:
  sys.stdout = open(args.OUTPUT, "w")

#Pagetable Class
class pagetable:
  #INIT
  def __init__(self):
    self.frame = []
    self.valid = []
    self.size  = 8 #Page Table Size
  def info(self):
    print("Page table: " + str(self.size))
    for i in range(0,self.size):
        print(str(self.frame[i]) + ":" + str(self.valid[i]))
  def append(self,frame,valid):
    self.frame.append(frame)
    self.valid.append(valid)
  def p(page):
    return self.frame[page]
  def v(page):
    return self.valid[page]

#parseprocess: Will parse text data and build process data and add to the cpu que
def parseprocess(textfile):
  table = pagetable()
  text = open(textfile)
  for line in text:
    if line != '\n':
      parse = line.split()
      table.append(parse[0],parse[1])
  text.close()
  if args.DEBUG:
    print("Table inported")
    table.info()
  return table

#Virtual Address Generator:
def vadrsgen(que):
  while True:
    num = random.getrandbits(4)
    print("VA:" + "%2d" % num + " | ", end="",flush=True)
    que.put(num)
    time.sleep(1)

#Address Translation:
def adrstran(table,que):
  while True:
    num = que.get()
    #Calculate various specifications
    page   = num / 2
    offset = num % 2
    valid  = table.valid[int(page)]

    print("PAGE" + "%2d" % page + " | " + "OFFSET" + "%2d" % offset + " | " + "VALID " + str(valid), end="",flush=True)

    if valid == 'v':
      frame = int(table.frame[int(page)])
      phyadrs = frame * 2 + offset
      print(" | " + "FRAME" + "%2d" % frame + " | " + "PHYADRS " + "%2d" % phyadrs)
    else:
      print(" | " + "PAGE FAULT!")


#main routine
def main():
  print('Starting virtual memory Simulation')
  table = parseprocess(args.INPUT)
  que = Queue() #Que to send data back and forth
  #Virtual Address Generator Process
  randp = Process(target=vadrsgen,args=(que,))
  randp.start()
  #Address Translation Process
  adrsp = Process(target=adrstran,args=(table,que,))
  adrsp.start()
  #Waits till the simulation is ctrl-c
  while True:
    try:
      time.sleep(1)
    except KeyboardInterrupt:
      print("Exiting Simulation")
      break
  randp.terminate()
  adrsp.terminate()
  sys.exit(0)

#Main Run routine
if __name__ == "__main__":
  main()
