import networkx as nx
import math

import matplotlib.pyplot as plt

class Node:

    def __init__(self, uid, visited = False, start = False, finish = False):
        self.uid = uid
        self.visited = visited
        self.start = start
        self.finish = finish

    def getDistance(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)

    def setPos(self, x, y):
        self.x = x
        self.y = y

class Maze:

    def __init__(self):
        self.g = nx.Graph()
        self.newNodeUid = 0
        self.startNode = None
        self.finishNode = None
        self.distTol = 20 # Distance tolerance to consider two nodes to be the same
        self.farAway = 10000 # Large distance to be given to new edges with unknown length

    def addNode(self, sourceNode = None, visited = False, start = False, finish = False,):

        uid = self.getNewNodeUid()
        # Create intersection node object
        newNode = Node(uid, visited, start, finish)
        # If start, define object as maze start
        if start:
            self.setStartNode(newNode)
        if finish:
            self.setFinishNode(newNode)
        # Create corresponding graph node
        self.g.add_node(newNode)
        # Create graph edge from source node to new node
        if sourceNode is not None:
            self.g.add_edge(sourceNode, newNode, weight = self.farAway)
            self.farAway += .01
        # Return id of new intersection
        return newNode

    def setStartNode(self, node):
        if self.startNode is None:
            self.startNode = node
        else:
            print 'Error: Start node already defined'

    def setFinishNode(self, node):
        if self.finishNode is None:
            self.finishNode = node
        else:
            print 'Error: Finish node already defined'

    def getNodeByUid(self, uid):
        for node in self.g.nodes():
            if node.uid == uid:
                return node

    def getNewNodeUid(self):
        uid = self.newNodeUid
        self.newNodeUid += 1
        return uid

    def nodeExistsAtPos(self, x, y):
        for node in self.g.nodes():
            if node.visited and node.getDistance(x, y) < self.distTol:
                return True

    def getNodeAtPos(self, x, y):
        for node in self.g.nodes():
            if node.visited and node.getDistance(x, y) < self.distTol:
                return node

    def visitNode(self, node, sourceNode, x, y, dist, nbPathsOut):
        # Check if node is not already visited
        if not node.visited:
            # Check if already exists
            if self.nodeExistsAtPos(x, y):
                print 'Intersection already exists'
                # if yes: delete incoming edge and reconnect sourceNode with found node
            # if not:
            else:
                # set position
                node.visited = True
                node.setPos(x, y)
                # set incoming heading to incoming path
                # set distance to incoming path
                self.g[node][sourceNode]['weight'] = dist
                # create outgoing paths edges and corresponding intersections nodes
                for path in range(nbPathsOut):
                    self.addNode(node)
        # Else do nothing

    def getNearestUnvisitedNode(self, sourceNode):
        shortestDist = self.farAway**2
        for node in self.g.nodes():
            if not node.visited:
                dist = nx.shortest_path_length(self.g, sourceNode, node, weight = 'weight')
                if dist < shortestDist:
                    nearestNode = node
                    shortestDist = dist
        return nearestNode
