Mirrors and Lasers

This is a very simple python applications whic solves the cases 1-3 
from the information sheet.
It is implemented in Python 3.7 and assumes numpy installed.

Open a terminal, go to the directory and open python, then import the auxilliary functions in mirrors.py and use the summarize function:

>python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
import mirrors as mr
mr.summarize('case1.txt')
 
'2 4 3'

mr.summarize('case2.txt')
 
'0'
mr.summarize('case3.txt')
'Impossible'

This is just a draft for functionality that is covered by case 1-3 in the information sheet.
There is vast room for extension and improvement. 
The calculations are dome by brute force testing, inserting mirrors
in each square in the path of the beam and testing if the beam reaches th detectors. No conclusions about which positions could not possibly generate an ctivation is considered. Thus the calculations are at present prohibelitably slow for larger grids.

A generator for test grids should be constructed

For now all the grid information is stored on a numpy array of dimension r*c. As this matrix is sparse there are probably better ways to store the positions of the mirrors and trace the beam.

No object oriented methods nor exception catching have been implemented

The functions and parameters in mirrors.py are rather self-explicatory.
