
import math


def takesecond(elem):
    return elem[1]


class Node:
    __nodecoord = ()            # Needs to know neighbors, distance from end, distance to all neighbors
    __distend = 0
    __cost = 0
    __weight = 0                  # Cost to Node + Distance to the end point
    __previousnode = 0

    def __init__(self, coord, endcoord, prevnode=None):
        self.__nodecoord = coord
        self.__dist = math.sqrt((endcoord[0] - self.__nodecoord[0])**2 + (endcoord[1] - self.__nodecoord[1])**2)
        if prevnode is not None:
            self.__previousnode = prevnode
            self.__cost = prevnode.getcost() + 1
            self.__weight = self.__dist + self.__cost
        E1.setvisited(self.__nodecoord)

    def printcoord(self):
        print(self.__nodecoord[0], ",", self.__nodecoord[1])

    def getcoord(self):
        return self.__nodecoord[0], self.__nodecoord[1]

    def getx(self):
        return self.__nodecoord[0]

    def gety(self):
        return self.__nodecoord[1]

    def getweight(self):
        return self.__weight

    def getdist(self):
        return self.__dist

    def getcost(self):
        return self.__cost

    def getprevcoord(self):
        try:
            return self.__previousnode.getcoord()
        except AttributeError:
            return 0, 0

    def getprevnode(self):
        return self.__previousnode


class BinaryHeap:   # Code for binary heap is based off of code found on interactivepython.org
    def __init__(self, nodelist):
        self.__heapsize = 0
        self.__heaplist = nodelist.copy()

    def moveup(self, x):
        while x // 2 > 0:
            if self.__heaplist[x].getweight() < self.__heaplist[x // 2].getweight():
                temp = self.__heaplist[x // 2]
                self.__heaplist[x // 2] = self.__heaplist[x]
                self.__heaplist[x] = temp
            x = x // 2

    def insert(self, i):
        self.__heaplist.append(i)
        self.__heapsize += 1
        self.moveup(self.__heapsize)

    def movedown(self, y):
        while(y * 2) <= self.__heapsize:
            mc = self.minChild(y)
            if self.__heaplist[y].getweight() > self.__heaplist[mc].getweight():
                temp = self.__heaplist[y]
                self.__heaplist[y] = self.__heaplist[mc]
                self.__heaplist[mc] = temp
            y = mc

    def minChild(self, i):
        if i * 2 + 1 > self.__heapsize:
            return i * 2
        else:
            if self.__heaplist[i * 2].getweight() < self.__heaplist[i*2+1].getweight():
                return i * 2
            else:
                return i * 2 + 1

    def makeHeap(self, newheap):
        i = len(newheap) // 2
        self.__heapsize = len(newheap)
        self.__heaplist = [0] + newheap[:]
        while i > 0:
            self.movedown(i)
            i = i-1

    def popmin(self):
        ret = self.__heaplist[1]
        self.__heaplist[1] = self.__heaplist[self.__heapsize]
        self.__heapsize -= 1
        self.__heaplist.pop()
        self.movedown(1)
        return ret

    def printheap(self):
        for i in range(1, len(self.__heaplist)):
            print(self.__heaplist[i].getcoord())


class Environment:                # Needs to print maze, needs 2D array of [coordinates : Node]

    __startcoord = ()
    __endcoord = ()
    __nodes = []
    __visitedlist = []
    __pathlist = []

    nodecount = 0

    __line = []                 # Array of strings, represents each line of the board

    __line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
    __line.append(['#', 'S', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
    __line.append(['#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#'])
    __line.append(['#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#'])
    __line.append(['#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#'])
    __line.append(['#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#'])
    __line.append(['#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#'])
    __line.append(['#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', 'E', '#'])
    __line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])

    def printmazestart(self):
        for i in range(len(self.__line)):
            for j in range(len(self.__line[0])):
                print(self.__line[i][j], end="")
            print()

    def setvisited(self, coord):
        self.__visitedlist.append(coord)

    def checkvisited(self, coord):
        if coord in self.__visitedlist:
            return 1
        return 0

    def genstartend(self):                    # Finds all "." on the maze and makes a Node object with their coordinate
        for i in range(1, len(self.__line) - 1): # Finds start and end of the maze
            for j in range(1, len(self.__line[0]) - 1):
                if self.__line[i][j] == "S":
                    self.__startcoord = (j, i)
                    # print(self.__startcoord[0], ",", self.__startcoord[1], " START")
                elif self.__line[i][j] == "E":
                    self.__endcoord = (j, i)
                    # print(self.__endcoord[0], ",", self.__endcoord[1], " END")

    def checkaround(self, node):  # Takes a node, returns a list of all neighboring nodes that have not been visited
        hlist = []
        if self.checkvisited((node.getx(), node.gety() - 1)) == 0 and \
                (self.__line[node.gety() - 1][node.getx()] == "." or self.__line[node.gety() - 1][node.getx()] == "E"):
            hlist.append(Node((node.getx(), node.gety() - 1), self.__endcoord, node))
        if self.checkvisited((node.getx() + 1, node.gety())) == 0 and \
                (self.__line[node.gety()][node.getx() + 1] == "." or self.__line[node.gety()][node.getx() + 1] == "E"):
            hlist.append(Node((node.getx() + 1, node.gety()), self.__endcoord, node))
        if self.checkvisited((node.getx(), node.gety() + 1)) == 0 and \
                (self.__line[node.gety() + 1][node.getx()] == "." or self.__line[node.gety() + 1][node.getx()] == "E"):
            hlist.append(Node((node.getx(), node.gety() + 1), self.__endcoord, node))
        if self.checkvisited((node.getx() - 1, node.gety())) == 0 and \
                (self.__line[node.gety()][node.getx() - 1] == "." or self.__line[node.gety()][node.getx() - 1] == "E"):
            hlist.append(Node((node.getx() - 1, node.gety()), self.__endcoord, node))

        for i in hlist:
            if i.getcoord() == self.__endcoord:
                return i.getcoord(), i
        return hlist

    def Asearch(self):
        s = Node(self.__startcoord, self.__endcoord)
        heap = BinaryHeap([])
        heap.makeHeap(E1.checkaround(s))
        while True:
            nextnode = heap.popmin()
            nextneighbors = E1.checkaround(nextnode)
            if isinstance(nextneighbors, tuple):
                print("End found!")
                endnode = nextneighbors[1]
                break
            for i in nextneighbors:
                heap.insert(i)

        while True:                                           # Walks backward through previous nodes to generate path
            if endnode.getprevcoord() == self.__startcoord:
                break
            self.__pathlist.append(endnode.getprevcoord())
            endnode = endnode.getprevnode()

        '''for i in self.__pathlist:
            print(i)'''

        for i in self.__pathlist:
            self.__line[i[1]][i[0]] = '!'

        E1.printmazestart()


E1 = Environment()
E1.printmazestart()
E1.genstartend()
E1.Asearch()
