import networkx as nx
import math

class Maze:

    def __init__(self):
        self.g = nx.MultiGraph()
        self.newNodeUid = 0
        self.startNode = None
        self.finishNode = None
        self.distTol = 75 # Distance tolerance to consider two nodes to be the same
        self.farAway = 10000 # A long distance...

    def addNode(self, nbPathsOut = 0, start = False, finish = False,):
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

    def addPath(self, fromNode, toNode, outHeading, inHeading, length):
        newPath = Path(fromNode, toNode, outHeading, inHeading)
        self.g.add_edge(fromNode, toNode, newPath, weight = length)

    def areNeighbors(self, node1, node2):
        for neighbor in self.g.neighbors(node1):
            if neighbor == node2:
                areNeighbors = True
            else:
                areNeighbors = False
        return areNeighbors

    # Method to be called when exploring the maze. It will create a new node at position x, y if it does
    # not already exists. It will create a path object from the source node to the current node position.
    def exploreNode(self, sourceNode, x, y, nbPathsOut, pathLength, outHeading, inHeading, start = False, finish = False):
        # Check if already exists
        if self.nodeExistsAtPos(x, y):
            currentNode = self.getNodeAtPos(x, y)
            print "Current node: ", currentNode.uid, " (existing)"
            # Check if path loops back to sourceNode
            if currentNode == sourceNode:
                if currentNode.nbPathsOut <= 1:
                    currentNode.nbPathsOut = 0
                else:
                    currentNode.nbPathsOut -= 1
                print "Loop to self, reducing nbPathsOut for node ", currentNode.uid, " to ", currentNode.nbPathsOut
        else:
            # Create new node
            currentNode = self.addNode(nbPathsOut, start, finish)
            currentNode.setPos(x, y)
            print "Current node: ", currentNode.uid, " (new)"
        # Create path edge from sourceNode to node
        self.addPath(sourceNode, currentNode, outHeading, inHeading, pathLength)
        return currentNode  

    def getHeadingToGoal(self, currentNode, goalNode):
        nextNode = self.getNextNodeInShortestPath(currentNode, goalNode)
        nextPath = self.getPathToNeighbor(currentNode, nextNode)
        return nextPath.getHeadingToNode(nextNode)
    
    def getNewNodeUid(self):
        uid = self.newNodeUid
        self.newNodeUid += 1
        return uid

    # Finds the nearest node from which there are unvisited paths
    def getNearestUnvisited(self, currentNode):
        shortestLength = self.farAway
        for node in self.g.nodes():
            if self.g.degree(node) < node.nbPathsOut + 1:
                length = nx.shortest_path_length(self.g, currentNode, node, weight = 'weight')
                print "Length to node ", node.uid, ": ", length
                if length < shortestLength:
                    nearestUnvisited = node
                    shortestLength = length
        print "Distance to nearest node with unvisited paths: ", shortestLength
        return nearestUnvisited


    def getNextNodeInShortestPath(self, currentNode, goalNode):
        path = nx.shortest_path(self.g, currentNode, goalNode, weight = 'weight')
        if len(path) ==1:
            return path[0]
        else:
            return path[1]
    
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

    def getPathToNeighbor(self, currentNode, neighborNode):
        paths = self.g[currentNode][neighborNode].items()
        shortestLength = self.farAway
        for path in paths:
            if path[1]['weight'] < shortestLength:
                shortestPath = path[0]
                shortestLength = path[1]['weight']
        return shortestPath

    def hasUnvisitedPaths(self):
        hasUnvisitedPaths = False
        for node in self.g.nodes():
            if self.g.degree(node) < node.nbPathsOut + 1:
                hasUnvisitedPaths = True
        return hasUnvisitedPaths

    def headingIsUnvisited(self, currentNode, heading):
        visitedHeadings = []
        for node in self.g.neighbors(currentNode):
		paths = self.g[currentNode][node].items()
		for path in paths:
		    visitedHeadings.append(path[0].getHeadingToNode(node))
	headingIsUnvisited = True
	if visitedHeadings.count(heading) == 1:
            headingIsUnvisited = False
        return headingIsUnvisited

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

    def getPos(self):
        return self.x, self.y

class Path:

    def __init__(self, nodeFrom, nodeTo, nodeFromOutHeading, nodeToInHeading):
        self.node0 = nodeFrom
        self.node0OutHeading = nodeFromOutHeading
        self.node1 = nodeTo
        self.node1OutHeading = self.inverseHeading(nodeToInHeading)
        
    def inverseHeading(self, heading):
        inHeading = ['E', 'N', 'W', 'S']
        outHeading = ['W', 'S', 'E', 'N']
        return outHeading[inHeading.index(heading)]

    def getHeadingToNode(self, node):
        if node == self.node0:
            return self.node1OutHeading
        elif node  == self.node1:
            return self.node0OutHeading
        
