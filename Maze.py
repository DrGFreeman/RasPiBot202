import networkx as nx
import math

class Maze:

    def __init__(self):
        self.g = nx.MultiGraph()
        self.newNodeUid = 0
        self.startNode = None
        self.finishNode = None
        self.distTol = 20 # Distance tolerance to consider two nodes to be the same
        self.farAway = 10000 # A long distance...

    def addNode(self, nbPathsOut = 0, sourceNode = None, start = False, finish = False,):
        uid = self.getNewNodeUid()
        # Create intersection node object
        newNode = Node(uid, nbPathsOut, start, finish)
        # If start, define object as maze start
        if start:
            self.setStartNode(newNode)
        if finish:
            self.setFinishNode(newNode)
        # Create corresponding graph node
        self.g.add_node(newNode)
        # Return new node
        return newNode

    def addPath(self, sourceNode, node, outHeading, inHeading, length):
        newPath = Path(sourceNode, node, outHeading, inHeading)
        self.g.add_edge(sourceNode, node, newPath, weight = length)

    def areNeighbors(self, node1, node2):
        for neighbor in self.g.neighbors(node1):
            if neighbor == node2:
                areNeighbors = True
            else:
                areNeighbors = False
        return areNeighbors

    def explPathToNode(self, sourceNode, x, y, nbPathsOut, pathLength, start = False, finish = False):
        # Check if already exists
        if self.nodeExistsAtPos(x, y):
            node = self.getNodeAtPos(x, y)
            print "Current node: ", node.uid, " (existing)"
            # Check if path loops back to sourceNode
            if node == sourceNode:
                if node.nbPathsOut <= 1:
                    node.nbPathsOut = 0
                else:
                    node.nbPathsOut -= 1
                print "Loop to self, reducing nbPathsOut for node ", node.uid, " to ", node.nbPathsOut
        else:
            # Create new node
            node = self.addNode(nbPathsOut, sourceNode, start, finish)
            node.setPos(x, y)
            print "Current node: ", node.uid, " (new)"
        # Create path edge from sourceNode to node
        self.addPath(sourceNode, node, "N", "N", pathLength)
        # set incoming heading to incoming path
        return node  

    def getNewNodeUid(self):
        uid = self.newNodeUid
        self.newNodeUid += 1
        return uid

    # Finds the nearest node from which there are unvisited paths
    def getNearestUnvisited(self, currentNode):
        shortestLength = self.farAway
        for node in self.g.nodes():
            if len(self.g.neighbors(node)) < node.nbPathsOut + 1:
                length = nx.shortest_path_length(self.g, currentNode, node, weight = 'weight')
                print "Length to node ", node.uid, ": ", length
                if length < shortestLength:
                    nearestUnvisited = node
                    shortestLength = length
        print "Distance to nearest node with unvisited paths: ", shortestLength
        return nearestUnvisited

    # Finds the next node in the path to the nearest node with unvisited paths
    def getNextNodeToNearestUnvisited(self, currentNode):
        nearestUnvisited = self.getNearestUnvisited(currentNode)
        path = nx.shortest_path(self.g, currentNode, nearestUnvisited, weight = 'weight')
        if len(path) == 1:
            print "Next node with unvisited paths: ", path[0].uid, " (current node)"
            return path[0]
        else:
            print "Next node with unvisited paths: ", path[1].uid
            return path[1]

    def getNodeAtPos(self, x, y):
        for node in self.g.nodes():
            if node.getDistance(x, y) < self.distTol:
                return node

    def getNodeByUid(self, uid):
        for node in self.g.nodes():
            if node.uid == uid:
                return node

    def getPathToNeighbor(self, fromNode, toNode):
        if self.areNeighbors(fromNode, toNode):
            paths = self.g[fromNode][toNode].items()
            shortestLength = self.farAway
            for path in paths:
                if path[1]['weight'] < shortestLength:
                    shortestPath = path[0]
                    shortestLength = path[1]['weight']
            return shortestPath
        else:
            print "Nodes ", fromNode.uid, "and", toNode.uid, "are not neighbors"
            return None

    def nodeExistsAtPos(self, x, y):
        for node in self.g.nodes():
            if node.getDistance(x, y) < self.distTol:
                return True

    def setFinishNode(self, node):
        if self.finishNode is None:
            self.finishNode = node
        else:
            print 'Error: Finish node already defined'

    def setStartNode(self, node):
        if self.startNode is None:
            self.startNode = node
        else:
            print 'Error: Start node already defined'

class Node:

    def __init__(self, uid, nbPathsOut, start = False, finish = False):
        self.uid = uid
        self.start = start
        self.finish = finish
        self.nbPathsOut = nbPathsOut

    def getDistance(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)

    def setPos(self, x, y):
        self.x = x
        self.y = y

class Path:

    def __init__(self, nodeFrom, nodeTo, nodeFromOutHeading, nodeToInHeading):
        self.node1 = nodeFrom
        self.node1OutHeading = nodeFromOutHeading
        self.node2 = nodeTo
        self.node2OutHeading = self.inverseHeading(nodeToInHeading)
        
    def inverseHeading(self, heading):
        inHeading = ['E', 'N', 'W', 'S']
        outHeading = ['W', 'S', 'E', 'N']
        return outHeading[inHeading.index(heading)]

    def getHeadingToNode(self, node):
        if node == self.node1:
            return self.node2OutHeading
        elif node  == self.node2:
            return self.node1OutHeading
        
