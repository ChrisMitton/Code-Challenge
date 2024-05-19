'''
Strategy: Local Search Model with Linked Lists

maxNumDrivers = num loads

1. Each driver will have a LL starting and ending with self
2. Iteration 1: all drivers will have 1 route inserted into their list.
3. Iteration 2: merge lists of drivers 1 pair at a time. 
    > choose pair with smallest trip time. 
    > Don't exceed 720min
4. Iteration n: 
5. Return the iteration with the min difference between the total_drivers and 
    > This way, the total_cost formula is as small as possible
'''

import sys
import math
import copy

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

# takes numeric values
def euclideanDistance(c1, c2):    
    return math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2)

def calculateTotalCost(num_drivers, total_min_driven):
    return 500*num_drivers + total_min_driven

# contains nodes representing distance between 2 coordinates
class DistanceNode:
    def __init__(self, load_id, start_coord=(0,0), end_coord=(0,0)):
        self.load_id = load_id
        self.start_coord = start_coord
        self.end_coord = end_coord
        
        self.distance = euclideanDistance(self.start_coord, self.end_coord)

        self.accumulated_time = 0 # time needed to reach this node from previous one; tail.accumulated time == entire route time
        self.next = None

class LinkedList:
    def __init__(self, driver_id):
        self.driver_id = driver_id
        # all drivers start from 0,0 and end with 0,0, hence they get initialized with: dummy_load_ID of 0, coords of (0,0)
        self.head = DistanceNode(0)
        self.tail = DistanceNode(0)
        self.head.next = self.tail
    
    # return List[int] of load_id's within a LL 
    def getArrList(self):
        res = []
        ptr = self.head.next
        while ptr.next:
            res.append(ptr.load_id)
            ptr = ptr.next
        return res
    
    def insertNodeAtBeginning(self, node):
        node.next = self.head.next
        self.head.next = node
        self.tail.accumulated_time = euclideanDistance(node.end_coord, (0,0)) # gets roundtrip time and stores it in tail


'''
create a new list with shallow copies

won't be super optimal becauyse I'm just merging all of the routes together that could work. Better soultions are out there but will try to at least get this to
'''
def merge2Lists(l1, l2):
    return 
    # l1 = l1.head.next
    # l2 =l2.head.next
    # tail = dummy = DistanceNode(-1)
            
    # while l1.next and l2.next:
    #     # check if addition of eulicedan distance from 1 end coord to the other start coord is < 720

    # #     if l1.val < l2.val:
    # #         tail.next = l1
    # #         l1 = l1.next
    # #     else:
    # #         tail.next = l2
    # #         l2 = l2.next
    # #     tail = tail.next
    
    # # if l1 != None:
    # #     tail.next = l1
    # # if l2 != None:
    # #     tail.next = l2
    
    # return dummy.next

# total_cost = 500*number_of_drivers + total_number_of_driven_minutes
def getCost(driversList):
    num_drivers, total_min = len(driversList.keys()), 0
    for ll in driversList.values():
        total_min += ll.tail.accumulated_time
    
    return 500*num_drivers + total_min

def solution():    
    data = convertFileToMatrix()
    if not data:
        return
        
    # There will be a max of (loadNumber) drivers. Each driver will point to a LL. Num Drivers will be continually reduced via merges
    driverLists = {}
    for driver_id, line in enumerate(data):
        load_id, start_coord, end_coord = line
        start_coord = tuple(map(float, start_coord.strip('()').split(',')))
        end_coord = tuple(map(float, end_coord.strip('()').split(',')))
        
        distanceNode = DistanceNode(load_id, start_coord, end_coord)
        distanceNode.accumulated_time = euclideanDistance((0,0), start_coord)

        driverLists[driver_id] = LinkedList(driver_id)
        driverLists[driver_id].insertNodeAtBeginning(distanceNode) # add 1 distance node to the drivers ll

    min_total_cost = float('inf') # gets current total cost of drivers list 
    solution = []

    '''
    iteration == merge smallest lists together

    While current iteration results in a new min total cost:
        For each list, get it's accumulated cost and find the next list with the lowest cost. If the sum of their accumlated costs < 720 add it 
    '''
    while getCost(driverLists) < min_total_cost:
        # track best solution found so far
        solution = [ll.getArrList() for ll in driverLists.values()]
        min_total_cost = getCost(driverLists)

        # go through all driver lists, merge the valid ones
        drivers_to_delete = []
        for driver_id, ll_1 in driverLists.items():
            # find next driver with smallest route time            
            lowest_cost_driver_id, lowest_route_time = -1, float('inf')
            for other_driver_id, ll_2 in driverLists.items():                                
                # track if driver 1 and 2 are not the same, and the other route has the lowest time so far
                ll_2_route_time = ll_2.tail.accumulated_time
                if driver_id != other_driver_id and ll_2_route_time < lowest_route_time:
                    lowest_cost_driver_id = other_driver_id
                    lowest_route_time = ll_2_route_time
                    
            # if a valid list has been found, try merging it with the 1st driver list
            if lowest_cost_driver_id != -1:
                resulting_merge = merge2Lists(driverLists[driver_id], driverLists[lowest_cost_driver_id])
                # only keep merge if roundtrip time is <= 720
                if resulting_merge.tail.accumulated_time <= 720:     
                    driverLists[driver_id] = resulting_merge
                    drivers_to_delete.append(lowest_cost_driver_id)
        
        # delete drivers that had their list merged
        for id in drivers_to_delete:
            del driverLists[id]

    print('min_total_cost: ',min_total_cost)
    solution = [[int(i) for i in l] for l in solution]
    for l in solution:
        print(l)

solution()