import math
import networkx as nx
from Maze import Maze, Node, Path
from robotCVMazeFull1 import *

import matplotlib.pyplot as plt

maze = Maze()

# Create start node (0) and assign position
currNode = maze.addNode(0, start = True)
currNode.setPos(0, 0)


# Move and visit next node (1)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 100, 0, 3, 100, 'E', 'E')

# Find next node with unvisited paths (1)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move

# Move and visit next node (2)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 100, -100, 0, 100, 'S', 'S')

# Find next node with unvisited paths (1)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# Move and visit next node (1)
prevNode = currNode
# Robot move
currNode = nextNode

# Find next node with unvisited paths (1)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move

# Move and visit next node (3)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, 0, 3, 100, 'E', 'E')

# Find next node with unvisited paths (3)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move

# Move and visit next node (4)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, -100, 2, 100, 'S', 'S')

#  Loop to self (4)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, -100, 2, 400, 'S', 'W')

# Find next node with unvisited paths (3)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# Move and visit next node (3)
prevNode = currNode
# Robot move
currNode = nextNode

# Find next node with unvisited paths (3)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move

# Move and visit next node (5)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, 100, 2, 300, 'E', 'W')

# Find next node with unvisited paths (5)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move

# Move and visit next node (1)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 100, 0, 3, 200, 'W', 'S')

# Find next node with unvisited paths (3)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# Move and visit next node (3)
prevNode = currNode
# Robot move
currNode = nextNode
for heading in ['E', 'N', 'W', 'S']:
    if maze.headingIsUnvisited(currNode, heading):
        print heading, "is unvisited"
    else:
        print heading, "is visited"

print maze.hasUnvisitedPaths()

### Move and visit next node (5)
##prevNode = currNode
### Robot move
##currNode = maze.exploreNode(prevNode, 200, 100, 2, 100, 'N', 'N')
##print maze.hasUnvisitedPaths()

print "\n"
for node in maze.g.nodes():
    print "Node: ", node.uid, "Nb of unvisited paths: ", node.nbPathsOut + 1 - maze.g.degree(node)

print "\n"
for edge in maze.g.edges():
##    print "Edge: ", edge[0].uid, edge[1].uid, maze.g[edge[0]][edge[1]]['weight']
    print "Edge: ", edge[0].uid, edge[1].uid

##nx.draw(maze.g)
##plt.show()

node0 = maze.getNodeByUid(0)
node1 = maze.getNodeByUid(1)
node2 = maze.getNodeByUid(2)
node3 = maze.getNodeByUid(3)
node4 = maze.getNodeByUid(4)
node5 = maze.getNodeByUid(5)


print nextUnvisitedHeading(node3, 'N', 7, maze)
