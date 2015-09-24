#!/usr/bin/python
# Daniel Noyes, ECE565F2015 HW#2
#
# HW#2 Simulate content switching conducted by OS Process Manager.
#Context switching saves the state of the currently running process 
# from CPU to PCB (unless this process has completed its execution)
# and restores the state of the newly scheduled process from PCB to
# CPU. Test your Process Manager on my file “ece565hw02.txt”.
#
# Programming Language : Python
# Environment: Linux
# Instructions: run in bash "python ece565hw02code.py ece565hw02.txt"
import sys
import os
import argparse

#input Parser
parser = argparse.ArgumentParser(description='HW 2 Content Switching Simulation')
parser.add_argument("-i", "--input", dest='INPUT', help="Input File")
parser.add_argument("-o", "--output", dest='OUTPUT', help="Output File")
parser.add_argument("-d", "--debug", dest='DEBUG', help="Enable Debugging Mode", action='store_true')
global args
args = parser.parse_args()

#setup output file
if args.OUTPUT:
  sys.stdout = open(args.OUTPUT, "w")

#Process Class
class process:
  #INIT
  def __init__(self): #no input
    self.state = 'Unknown'
    self.pid = 0
    self.ppid = 0
    self.pc = 0
    self.ax = 0
    self.bx = 0
    self.cx = 0
    self.dx = 0
    self.pr = 0
    self.st = 0
    self.cpu = 0

  #process(['Running',12,1,8000,12,12,12,12,3,15,6])
  def __init__(self,data):
    self.state = data[0]
    self.pid = int(data[1])
    self.ppid = int(data[2])
    self.pc = int(data[3])
    self.ax = int(data[4])
    self.bx = int(data[5])
    self.cx = int(data[6])
    self.dx = int(data[7])
    self.pr = int(data[8])
    self.st = int(data[9].split(':')[1])
    self.cpu = int(data[10])

  def info(self):
    print("State: " + str(self.state))
    print("PID:   " + str(self.pid))
    print("pPID:  " + str(self.ppid))
    print("PC:    " + str(self.pc))
    print("AX:    " + str(self.ax))
    print("BX:    " + str(self.bx))
    print("CX:    " + str(self.cx))
    print("DX:    " + str(self.dx))
    print("Pr:    " + str(self.pr))
    print("ST:    " + str(self.st))
    print("CPU:   " + str(self.cpu))

  #Run one CPU cycle
  def run(self):
    self.cpu = self.cpu -1
    if self.cpu <= 0:
      return False
    else:
      return True

  def getstate(self):
    if self.state == 'Running':
      return 0 #Running
    elif self.state == 'Ready':
      return 1 #Ready
    elif self.state == 'Blocked':
      return 2 #Blocked
    else:
      return 3 #Unknown

#CPU Class
class CPU:
  def __init__(self):
    self.proc = process()

  def push(self,proc):
    oldproc = self.proc
    self.proc = proc
    return oldproc

  def pop(self):
    oldproc = self.proc
    self.proc = process()
    return oldproc

  def current(self):
    self.proc.info()

#First Come, First Server Scheduling
def fcfs(cpuque):
  ctime = 0 #cpu time
  #goes through the cpu que and skips any blocked
  for proc in cpuque:
    if proc.getstate() < 2:
      print("Loading CPU With PID: " + str(proc.pid))
      if args.DEBUG == True: proc.info()
      ptime = proc.cpu
      while(ptime > 0):
        print("Running ... Time Remaining: " + str(ptime))
        ptime = ptime -1
        ctime = ctime +1
      print("Process("+ str(proc.pid) +") Complete")
      print("CPU Time: " + str(ctime))

  print("No more Ready Process in Que")

#parseprocess: Will parse text data and build process data and add to the cpu que
def parseprocess(textfile):
  cpuque = []
  data = []
  text = open(textfile)
  for line in text:
    if line != '\n':
      data.append(line.split()[1])
  text.close()

  offset = 0
  while(True):
    if offset +11 < len(data)+1:
      cpuque.append(process(data[0+offset:11+offset]))
    else:
      break
    offset = offset + 11
  return cpuque

#consim: Content Switching Simulator main routine
def consim():
  print('Starting Content Switching Simulator')
  cpuque = parseprocess(args.INPUT)
  fcfs(cpuque)

#Main Run routine
if __name__ == "__main__":
  consim() #run consim
