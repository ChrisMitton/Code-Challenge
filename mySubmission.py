'''
Strategy: Local Search Model with Linked Lists
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
'''
def merge2Lists(l1, l2):

    '''
    How to determine which node goes first:

    the eulic distance from the previous node. Which ever has a smaller distance goes first
    '''
    def shallow_copy_node(node):
        return DistanceNode(node.load_id, node.start_coord, node.end_coord)
    
    l1 = l1.head.next
    l2 = l2.head.next    

    # Create a dummy node to hold the new merged list
    merged_head = merged_tail = DistanceNode(0)
    previous_end_coord = (0, 0)  # Initialize with the start coordinates of the dummy node

    # Traverse both lists and merge based on euclidean distance
    while l1.next and l2.next:
        # Create shallow copies of the nodes
        node1 = shallow_copy_node(l1)
        node2 = shallow_copy_node(l2)

        # Calculate euclidean distances from previous node's end_coord
        distance_from_prev_n1 = euclideanDistance(previous_end_coord, node1.start_coord)
        distance_from_prev_n2 = euclideanDistance(previous_end_coord, node2.start_coord)

        # Choose the node with smaller euclidean distance
        if distance_from_prev_n1 < distance_from_prev_n2:
            # Update accumulated time
            node1.accumulated_time = merged_tail.accumulated_time + euclideanDistance(merged_tail.end_coord, node1.start_coord)
            # print('new acc time: ', node1.accumulated_time)
            merged_tail.next = node1
            l1 = l1.next
            merged_tail = merged_tail.next                 
            # print('new merge tail acc time: ', merged_tail.accumulated_time)
        else:
            # Update accumulated time
            node2.accumulated_time = merged_tail.accumulated_time + euclideanDistance(merged_tail.end_coord, node2.start_coord)
            # print('new acc time: ', node2.accumulated_time)
            merged_tail.next = node2
            l2 = l2.next
            merged_tail = merged_tail.next
            # print('new merge tail acc time: ', merged_tail.accumulated_time)
        
        # Update previous end coordinates
        previous_end_coord = merged_tail.end_coord

    # print('############new merge tail acc time: ', merged_tail.accumulated_time)

    # Append the remaining nodes from l1 or l2 if any
    while l1.next:
        node = shallow_copy_node(l1)
        node.accumulated_time = merged_tail.accumulated_time + euclideanDistance(merged_tail.end_coord, node.start_coord)

        merged_tail.next = node
        l1 = l1.next
        merged_tail = merged_tail.next
    
    while l2.next:
        node = shallow_copy_node(l2)
        node.accumulated_time = merged_tail.accumulated_time + euclideanDistance(merged_tail.end_coord, node.start_coord)

        merged_tail.next = node
        l2 = l2.next
        merged_tail = merged_tail.next

    # merged_tail.next = l1 if l1.next else l2
    # print('*******new merge tail acc time: ', merged_tail.accumulated_time)


    # Create new LL
    res_ll = LinkedList(0)
    res_ll.head.next = merged_head.next
    # print()
    # print('this is merged_tail acc time', merged_tail.accumulated_time, )
    merged_tail.next = res_ll.tail

    
    # complete round trip
    res_ll.tail.accumulated_time = merged_tail.accumulated_time + euclideanDistance(merged_tail.end_coord, res_ll.tail.start_coord)
    
    return res_ll


'''
total_cost = 500*number_of_drivers + total_number_of_driven_minutes
'''
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

    while getCost(driverLists) < min_total_cost:
        # track best solution found so far
        solution = [ll.getArrList() for ll in driverLists.values()]
        min_total_cost = getCost(driverLists)

        # go through all driver lists, merge the valid ones
        drivers_to_delete = []
        for driver_id, ll_1 in driverLists.items():
            if driver_id not in drivers_to_delete:  # Check if driver has been marked for deletion
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
                    if lowest_cost_driver_id not in drivers_to_delete and resulting_merge.tail.accumulated_time <= 720:
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