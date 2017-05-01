#!/usr/bin/python
import math
import re
import sys
import os
import time
import BeautifulSoup
import linecache

# # Fetch EnergySimualtion resutls

html = linecache.getline('Output/bTable.html',37)

print html

m=re.findall(r"\d+\.\d+", html)


print ("Total Energy =")

print m[0]




print ("Process Completed")

