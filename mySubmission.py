'''
Strategy: Local Search Model with Linked Lists

NumDrivers = num loads

1. Each driver will have a LL starting and ending with self
2. Iteration 1: all drivers will have 1 route inserted into their list.
3. Iteration 2: combine lists of drivers 1 pair at a time
    > Each iteration of this should be a logn, since the data being traversed is halved each time
4. Iteration n: 
5. Return the iteration with the min difference between the total_drivers and 
    > This way, the total_cost formula is as small as possible
'''

import sys
import math

def convertFileToMatrix():
    if len(sys.argv) != 2:
        print('Add valid file path and nothing else.')
        return []
    
    file_path = sys.argv[1]
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    matrix = []
    for line in lines[1:]:
        parsedLine = line.rstrip('\n').split(" ")
        matrix.append(parsedLine)

    return matrix

def calculateDist(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def calculateTotalCost(num_drivers, total_min_driven):
    return 500*num_drivers + total_min_driven

def solution():    
    data = convertFileToMatrix()
    if not data:
        return
    
    for r in data:
        print(r)


solution()

