'''
Strategy: Local Search Model with Linked Lists

NumDrivers = num loads

1. Each driver will have a LL starting and ending with self
2. Iteration 1: all drivers will have 1 route inserted into their list.
3. Iteration 2: merge lists of drivers 1 pair at a time
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

def euclideanDistance(c1, c2):    
    return math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2)

def calculateTotalCost(num_drivers, total_min_driven):
    return 500*num_drivers + total_min_driven

# contains nodes representing distance between 2 coordinates
class DistanceNode:
    def __init__(self, load_id, start_coord='(0,0)', end_coord='(0,0)'):
        self.load_id = load_id
        self.start_coord = start_coord
        self.end_coord = end_coord
        
        c1 = [float(num) for num in start_coord.strip('()').split(',')]
        c2 = [float(num) for num in end_coord.strip('()').split(',')]
        self.distance = euclideanDistance(c1, c2)

        self.accumulated_time = 0 # time needed to reach this node from previous one
        self.next = None

class LinkedList:
    def __init__(self, driver_id):
        self.driver_id = driver_id
        # all drivers start from 0,0 and end with 0,0, hence they get initialized with: load_ID of 0, coords of (0,0)
        self.head = DistanceNode(0)
        self.tail = DistanceNode(0)
        self.head.next = self.tail
    
    # return [int]
    def getList():
        pass
    
    def insertNode():
        # dummy = SinglyLinkedListNode(0)
        # dummy.next = llist
        
        # prev, ptr = dummy, llist
        
        # while ptr:   
        #     position -= 1
        #     if position == 0:
        #         temp = ptr.next
        #         new = SinglyLinkedListNode(data)
        #         ptr.next = new
        #         new.next = temp
        #         return dummy.next
        #     prev = ptr
        #     ptr = ptr.next
        
        # return dummy.next
        pass

def mergeTwoLists(self, l1, l2):
    tail = dummy = DistanceNode(-1)
    
    while l1 and l2:
        if l1.val < l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    
    if l1 != None:
        tail.next = l1
    if l2 != None:
        tail.next = l2
    
    return dummy.next

def solution():    
    data = convertFileToMatrix()
    if not data:
        return
    
    # assign 1 loadNumber to every driver
    driverLists = {}
    for driver_id, line in enumerate(data):
        load_id, start_coord, end_coord = line
        distanceNode = DistanceNode(load_id)
        driverLists[driver_id + 1] = LinkedList(driver_id + 1)
        print(driverLists[driver_id + 1].head.start_coord)
        # driverLists[driver_id].insert(distanceNode) # TODO

    min_total_cost = float('inf')
    solution = {}
    placeholder = True
    while placeholder:
        # merge lists

        # if the current state of driverList is most optimal, it's a potential solution
        if min_total_cost > current_total_cost:
            min_total_cost = current_total_cost
            # TODO: deepcopy driversList to solution
        

    print([ll.getList() for ll in solution.values()])

solution()

