import math
import networkx as nx
from Maze import Maze, Node, Path
import matplotlib.pyplot as plt

########################################################################
##  Maze Functions

##  Define next unvisited path heading at current node (in exploration mode)
def nextUnvisitedHeading(currentNode, currentHeading, intersection):
    currentAngle = headingToAngle(currentHeading)
    headings = []
    if intersection & 1 == 1:
        if currentAngle == 3 * math.pi / 2.:
            headings.append(angleToHeading(0))
        else:
            headings.append(angleToHeading(math.pi / 2. + currentAngle))
    if intersection & 2 == 2:
        headings.append(angleToHeading(currentAngle))
    if intersection & 4 == 4:
        if currentAngle == 0:
            headings.append(angleToHeading(3 * math.pi / 2.))
        else:
            headings.append(angleToHeading(currentAngle - math.pi / 2.))
    for heading in headings:
        if maze.headingIsUnvisited(currentNode, heading):
            nextUnvisitedHeading = heading
    print "Next heading:", nextUnvisitedHeading
    return nextUnvisitedHeading

##  Convert heading to angle
def headingToAngle(heading):
    headings = ['E', 'N', 'W', 'S']
    angles = [0., math.pi / 2., math.pi, 3 * math.pi / 2.]
    return angles[headings.index(heading)]

def angleToHeading(angle):
    headings = ['E', 'N', 'W', 'S']
    angles = [0., math.pi / 2., math.pi, 3 * math.pi / 2.]
    return headings[angles.index(angle)]

########################################################################

maze = Maze()

# Create start node (0) and assign position
currNode = maze.addNode(0, start = True)
currNode.setPos(0, 0)

# Move and visit next node (1)
prevNode = currNode
currHeading = 'E'
# Robot move
currNode = maze.exploreNode(prevNode, 100, 0, 3, 100, currHeading, 'E')

# Find next node with unvisited paths (1)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move
currHeading = nextUnvisitedHeading(currNode, currHeading, 7)

# Move and visit next node (2)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 100, -100, 0, 100, currHeading, 'S')

# Find next node with unvisited paths (1)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
currHeading = maze.getHeadingToGoal(currNode, nextNode)
print "Next heading:", currHeading
# Robot move
currNode = nextNode
currHeading = nextUnvisitedHeading(currNode, currHeading, 7)

# Move and visit next node (3)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, 0, 3, 100, currHeading, 'E')

# Find next node with unvisited paths (3)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move
currHeading = nextUnvisitedHeading(currNode, currHeading, 7)

# Move and visit next node (4)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, -100, 2, 100, currHeading, 'S')

# Find next node with unvisited paths (4)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move
currHeading = nextUnvisitedHeading(currNode, currHeading, 3)

# Move and visit next node (4)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, -100, 2, 400, currHeading, 'W')

# Find next node with unvisited paths (3)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
currHeading = maze.getHeadingToGoal(currNode, nextNode)
print "Next heading:", currHeading
# Robot move
currNode = nextNode
currHeading = nextUnvisitedHeading(currNode, currHeading, 7)

# Move and visit next node (5)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, 100, 3, 300, currHeading, 'W')

# Find next node with unvisited paths (5)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move
currHeading = nextUnvisitedHeading(currNode, currHeading, 7)

# Move and visit next node (3)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, 0, 3, 100, currHeading, 'S')

# Find next node with unvisited paths (1)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
currHeading = maze.getHeadingToGoal(currNode, nextNode)
print "Next heading:", currHeading
# Robot move
currNode = nextNode
currHeading = nextUnvisitedHeading(currNode, currHeading, 7)

# Move and visit next node (5)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, 100, 3, 200, currHeading, 'E')

# Find next node with unvisited paths (6)
nextNode = maze.getNextNodeToNearestUnvisited(currNode)
# nextNode = currNode: Do no move
currHeading = nextUnvisitedHeading(currNode, currHeading, 7)

# Move and visit next node (6)
prevNode = currNode
# Robot move
currNode = maze.exploreNode(prevNode, 200, 200, 0, 100, currHeading, 'N', finish = True)

pathRev = nx.shortest_path(maze.g, currNode, maze.startNode, weight = 'weight')
pathRevHeadings = []
for i in range(len(pathRev) - 1):
    currNode = pathRev[i]
    pathRevHeadings.append(maze.getHeadingToGoal(currNode, maze.startNode))

print "Shortest path back to start:", pathRevHeadings



print "\n"
for node in maze.g.nodes():
    print "Node: ", node.uid, "Nb of unvisited paths: ", node.nbPathsOut + 1 - maze.g.degree(node)

print "\n"
for edge in maze.g.edges():
    print "Edge: ", edge[0].uid, edge[1].uid

##nx.draw(maze.g)
##plt.show()

node0 = maze.getNodeByUid(0)
node1 = maze.getNodeByUid(1)
node2 = maze.getNodeByUid(2)
node3 = maze.getNodeByUid(3)
node4 = maze.getNodeByUid(4)
node5 = maze.getNodeByUid(5)
node6 = maze.getNodeByUid(6)

