#!/usr/bin/python
# Daniel Noyes, ECE565F2015 Midterm-Part II
#
# Programming Language : Python
# Environment: Linux
# Instructions: run in bash "python ece565midtermcode.py -i ece565midterm.txt"
import sys
import os
import argparse

#input Parser
parser = argparse.ArgumentParser(description='Midterm-Part II Content Switching Simulation')
parser.add_argument("-i", "--input", dest='INPUT', help="Input File")
parser.add_argument("-o", "--output", dest='OUTPUT', help="Output File")
parser.add_argument("-d", "--debug", dest='DEBUG', help="Enable Debugging Mode", action='store_true')
parser.add_argument("-1", "--fcfs", dest='FCFSALG', help="Run First Come First Scheduling(Default)", action='store_true')
parser.add_argument("-2", "--sjf", dest='SJFALG', help="Run Shortest Job Scheduling", action='store_true')
parser.add_argument("-3", "--ps", dest='PSALG', help="Run Priority Scheduling", action='store_true')
parser.add_argument("-4", "--rr", dest='RRALG', help="Run Round Robin Scheduling", action='store_true')
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

#Process through que
def processque(cpuque):
  ctime = 0 #cpu time
  #goes through the cpu que and skips any blocked
  for proc in cpuque:
    if proc.getstate() < 2:
      print("Loading CPU With PID: " + str(proc.pid) +" | Priority: " + str(proc.pr) )
      if args.DEBUG == True: proc.info()
      ptime = proc.cpu
      while(ptime > 0):
        print("Running ... Time Remaining: " + str(ptime))
        ptime = ptime -1
        ctime = ctime +1
      print("Process("+ str(proc.pid) +") Complete")
      print("CPU Time: " + str(ctime))

  print("No more Ready Process in Que")

#Process through que let running still go first
def nonpremp(cpuque):
  ctime = 0 #cpu time
  #pop the top running cpu
  i=0
  run=0
  for proc in cpuque:
    if proc.getstate() == 0:
      run = i
    i = i+1
  proc = cpuque.pop(run)
  print("Resuming Running CPU Process")
  print("Loading CPU With PID: " + str(proc.pid) +" | Priority: " + str(proc.pr) )
  if args.DEBUG == True: proc.info()
  ptime = proc.cpu
  while(ptime > 0):
    print("Running ... Time Remaining: " + str(ptime))
    ptime = ptime -1
    ctime = ctime +1
  print("Process("+ str(proc.pid) +") Complete")
  print("CPU Time: " + str(ctime))

  #goes through the rest of the cpu que and skips any blocked
  for proc in cpuque:
    if proc.getstate() < 2:
      print("Loading CPU With PID: " + str(proc.pid) +" | Priority: " + str(proc.pr) )
      if args.DEBUG == True: proc.info()
      ptime = proc.cpu
      while(ptime > 0):
        print("Running ... Time Remaining: " + str(ptime))
        ptime = ptime -1
        ctime = ctime +1
      print("Process("+ str(proc.pid) +") Complete")
      print("CPU Time: " + str(ctime))

  print("No more Ready Process in Que")

#First Come, First Server Scheduling
def fcfs(cpuque):
  print("Running First Come First Server Scheduling Algorithm")
  processque(cpuque)

#Shortest Job First Scheduling
def sjfs(cpuque):
  print("Running Shortest Job First Scheduling Algorithm")
  sque = sorted(cpuque, key=lambda cpuq: cpuq.cpu)
  processque(sque)

#Priority Scheduling
def ps(cpuque):
  print("Running Priority Scheduling Algorithm")
  # Set reverse to True to Prioritize with highest value
  pque = sorted(cpuque, key=lambda cpuq: cpuq.pr, reverse=False) #Sort with Highest priority first
  nonpremp(pque)

#Round-Robin Scheduling
def rrs(cpuque,interval):
  print("Running Round Robin Scheduling Algorithm")
  ctime = 0
  bque = [] #blocked que
  #goes through the cpu que with a specified round robin interval and skips any blocked
  while(True):
    if len(cpuque) == 0:
      print("Scheduling Complete")
      break
    proc = cpuque.pop(0) #remove the rist item in the cpu
    if proc.getstate() >= 2:
      print("CPU Blocked, skiping to next one")
      bque.append(proc)
      proc = cpuque.pop(0)
    print("Loading CPU With PID: " + str(proc.pid) +" | Priority: " + str(proc.pr) )
    if args.DEBUG == True: proc.info()
    #Process through a interval
    ptime = 0
    while(ptime < interval):
      if proc.cpu <= 0:
        print("Process("+ str(proc.pid) +") Complete")
        break #completed cpu
      print("Running ... Time Remaining: " + str(proc.cpu))
      proc.cpu = proc.cpu -1
      ptime = ptime +1
      ctime = ctime +1

    print("CPU Time: " + str(ctime))
    if proc.cpu <= 0:
      print("Process("+ str(proc.pid) +") Complete")
    else:
      print("Putting CPU Back in que")
      cpuque.append(proc)

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
  if args.INPUT:
    cpuque = parseprocess(args.INPUT)
  else:
    print("Error No input file selected type -h to see all options")
    sys.exit(2)
  if args.FCFSALG == True:
    fcfs(cpuque)
  if args.SJFALG == True:
    sjfs(cpuque)
  if args.PSALG == True:
    ps(cpuque)
  if args.RRALG == True:
    rrs(cpuque,2)

#Main Run routine
if __name__ == "__main__":
  consim() #run consim
