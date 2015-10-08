#!/usr/bin/python
# Daniel Noyes, ECE565F2015 HW#4
#
# HW#4 Write a program that downloads a webpage with hyperlinks.
#  Consider your downloaded webpage as a local replica, i.e., a 
#  self contained webpage with all directories and files in the
#  same domain downloaded. Your code can stop going circular
#  links if exist, leave broken links, and not download files
#  outside the original webpage domain.
#
#  Test your system on this course webpage:
#  http://www.faculty.umassd.edu/hong.liu/ece565.html
#
# Note: Python wrapper that will call wget to download the site.
#
# wget --mirror --no-parent --no-verbose ${URL}
#
# --mirror       : mirror the site
# --no-parent    : don't ascend to the parent directory.
# --no-verbose   : turn off verboseness, without being quiet.
#
# Programming Language : Python
# Environment: Linux
# Instructions: run in bash "python ece565hw04code.py [site]"
import sys
import os

print(sys.argv[0])
if len(sys.argv) != 2:
  print("usage: ece565hw04code.py [site]")
  sys.exit(0)

url = sys.argv[1]
print("downloading " + url)

cmd = "wget --mirror --no-parent --no-verbose " + str(url)
print(cmd)
os.system( cmd )

