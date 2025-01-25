"""
    romgen.py generates a rom for the pic10c202
    Copyright (C) 2025 6f6626

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from itertools import zip_longest
 
# Group function using zip_longest to split
def group(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)
def splitnchars(string,n):
    return [''.join(lis) for lis in group(n,string,'')]
#123456789abc
#abc789456123
import sys
#we expect an INTEL HEX file as input
high="0000"
line=0
mem=["00" for i in range(1024)]
while True:
 line+=1
 try:
  entry=input()
 except:
  break
 embedded=entry[1:-2]#ignore checksum and :
 count=int(embedded[0:2],16)#parse the length
 addr=int(embedded[2:6],16)&1023
 rtype=embedded[6:8]
 data=embedded[8:8+count*2]
 if count==0:
  data=""
 prev=""
 tmp=""
 data=[[tmp:=prev+i if prev!="" else "",prev:=i if prev=="" else "",tmp][-1] for i in data]
 data=[i for i in data if i!=""]
 if rtype=="00":
  for i in range(count):
   mem[i+addr]=data[i]
 elif rtype=="01":
  break
 elif rtype=="02":
  print(f"ERROR: Extended Segment Address is unexpected in this context.(line {line})",file=sys.stderr)
  exit(-1)
 elif rtype=="03":
  print(f"ERROR: Start Segment Address is unexpected in this context.(line {line})",file=sys.stderr)
  exit(-1)
 elif rtype=="04":
  if data!=["00","00"]:
   print(f"ERROR: Invalid high address(wanted '0000', got '{data}')",file=sys.stderr)
   exit(-1)
 elif rtype=="05":
  print(f"ERROR: Start Linear Address is unexpected in this context.(line {line})",file=sys.stderr)
  exit(-1)
 else:
  print(f"ERROR:Did not find valid record type on line {line}",file=sys.stderr)
  exit(-1)
mem=group(2,mem,'')
nmem=[i[1][1]+i[0] for i in mem]
mem=nmem
mem=list(group(4,mem,''))
nmem=["".join(reversed(i)) for i in mem]
for i in nmem:
 print(f"set instr 0x{i}#rom")
 print("jump instrsobtained always#rom")