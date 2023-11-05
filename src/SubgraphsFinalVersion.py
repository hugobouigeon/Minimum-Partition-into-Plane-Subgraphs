
## downloads

from cgshop2022utils.io import read_instance

## imports

import matplotlib.pyplot as plt
import time as ti
import random as rd
import json

## instance

# adapt the filename depending on location

instance = read_instance("C:/Users/hugob/Desktop/instances/reecn3382.instance.json")

## data extraction function

def accessData(instance):       #The goal is just to get the data and put it in easier to use lists
    nodeList = [node for node in instance["graph"].nodes]
    edgeList = [edge for edge in instance["graph"].edges]
    return nodeList,edgeList

## intersetion algorithm


def intersect(edge1,edge2):
    A,B = edge1
    C,D = edge2
    x1,y1 = A
    x2,y2 = B
    x3,y3 = C
    x4,y4 = D
    x2x1 = x2-x1
    y2y1 = y2-y1
    x3x1 = x3-x1
    y3y1 = y3-y1
    x4x1 = x4-x1
    y4y1 = y4-y1
    if (x2x1)*(y4-y3) == (x4-x3)*(y2y1):                             #check if parallel
        if x1*y3 == y1*y3:                                           #check if same line
            if x1 == x2:                                             #check if vertical
                if (y1 < y3 and y3 < y2) or (y1 < y4 and y4 < y2):   #check if overlapping
                    return True #overlaps & vertical
            elif (x1 < x3 and x3 < x2) or (x1 < x4 and x4 < x2):     #check if overlapping
                return True     #overlaps
            else:                                                    #not overlaping
                return False    #same line but no overlap
        else:                                                        #not same line
            return False        #parallel but not same line
    else:                                                            #not parallel
        if A == C or A == D or B == C or B == D:                     #check if common edge
            return False        #not parallel
        else:                                                        #general case
            return ((y4y1) * (x3x1) > (y3y1) * (x4x1)) != ((y4-y2) * (x3-x2) > (y3-y2) * (x4-x2)) and ((y3y1) * (x2x1) > (y2y1) * (x3x1)) != ((y4y1) * (x2x1) > (y2y1) * (x4x1))

"""
creating a new non oriented graph were edges now become verticies and are connected to one another if they intersect
"""

def intersectionGraph(graph):       #graph conversion : step 1 of algorithm
    nodeList,edgeList = graph
    n = len(nodeList)
    m = len(edgeList)
    adjList = [[] for i in range(m)]
    for i in range(m):
        for j in range(i):
            if intersect(edgeList[j],edgeList[i]):
                adjList[i].append(j)
                adjList[j].append(i)
    return adjList

## coloring algorithm

def sortEdgesByDegree(adjList):     #sorting our edges by their degree results in smaller partitions
    m = len(adjList)
    adjLengthList = [(-len(adjList[i]),i) for i in range(m)]
    adjLengthList.sort()
    indexOfSortedAdjList=[adjLengthList[i][1] for i in range(m)]
    return indexOfSortedAdjList

def isBipartite(adj):               #code for finding partitions with only two groups: linear
    n= len(adj)
    colorArr = [-1]* n
    queue = []

    for u in range(n):
        if colorArr[u] == -1:
            queue.append(u)
            colorArr[u] = 1
        while queue:
            u = queue.pop()
            for v in adj[u]:
                if colorArr[v] == -1:
                    colorArr[v] = 1 - colorArr[u]
                    queue.append(v)
                elif colorArr[v] == colorArr[u]:
                    return False,colorArr

    return True,colorArr

# greedy algorithm for graph coloring

# Assigns colors (starting with the vertex with maximum degree)to all
# vertices and prints the assignment of colors
def greedyColoring(graph):

    adj = intersectionGraph(graph)
    print("preprocessing done")

    #first test if a bipartite partitioning exist (linear complexity)

    b,colorArr = isBipartite(adj)
    if b:
        print("is bipartite")
        return colorArr

    #if not, go with a greedy algorithm

    m = len(adj)
    result = [-1] * m   # Assign the first color to first vertex

    indexAdj = sortEdgesByDegree(adj)   # Sorting algorithm sorts vertices by degree

    result[indexAdj[0]] = 0;


    # A temporary array to store the available colors.
    # True value of available[cr] would mean that the
    # color cr is assigned to one of its adjacent vertices
    available = [False] * m

    # Assign colors to remaining m-1 vertices
    for u in indexAdj[1:]:

        # Process all adjacent vertices and
        # flag their colors as unavailable
        for i in adj[u]:
            if (result[i] != -1):
                available[result[i]] = True

        # Find the first available color
        cr = 0
        while cr < m:
            if (available[cr] == False):
                break

            cr += 1

        # Assign the found color
        result[u] = cr

        # Reset the values back to false
        # for the next iteration
        for i in adj[u]:
            if (result[i] != -1):
                available[result[i]] = False
    print("num_colors:" +str(max(result)+1))
    return result


## visualisation functions

def associateColor(i,n):        # A little programm used to generate as many colors as needed to represent the partition
    color = [0,0,0,1-0.5*i/(n+1)]
    color[i%3] = 1
    color[(i%6)//2] = max(color[(i%6)//2],rd.random()*0.3+0.5)
    color[(i%9)//3] = max(color[(i%9)//3],rd.random()*0.3+0.4)
    color = (color[0],color[1],color[2],color[3])
    return color

def plotColoredGraph(graph,num_colors,colors):  #plots the graph, can then be showed by executing plt.show()
    nodeList,edgeList = graph
    for i in range(len(nodeList)):
        plt.plot([nodeList[i][0]],[nodeList[i][1]],"bo")
    for i in range(len(edgeList)):
        plt.plot([edgeList[i][0][0],edgeList[i][1][0]],[edgeList[i][0][1],edgeList[i][1][1]],color=associateColor(colors[i],num_colors))

def visualOutputMain():         # Final function to plot the partition
    t = ti.time()
    colors = greedyColoring(accessData(instance))
    num_colors = max(colors)+1
    print(ti.time()-t)
    plotColoredGraph(accessData(instance),num_colors,colors)

## main

def main(instance):
    colors = greedyColoring(accessData(instance))
    num_colors = max(colors)+1

    # Define Variable
    type = instance["type"]
    instance = instance["id"]
    num_colors = num_colors
    colors = colors

    # Create Dictionary
    value = {
        "type": type,
        "instance": instance,
        "num_colors": num_colors,
        "colors": colors
    }

    # Dictionary to JSON Object using dumps() method
    # Return JSON Object
    return json.dumps(value)

## test all instances:

# getting all runtime mesures and partition cardinalitys of the instances given

instanceli = [read_instance("C:/Users/hugob/Desktop/instances/reecn3382.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/rsqrp4641.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/rvisp5013.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/rvispecn2615.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/sqrp7730.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/sqrpecn3020.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/vispecn2518.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/vispecn26025.instance.json"),
read_instance("C:/Users/hugob/Desktop/instances/visp26405.instance.json")]

def giveUsNumbers(instanceli):
    color_numbers = []
    time_numbers = []
    edge_numbers = []
    t = ti.time()
    for instance in instanceli:
        t = ti.time()
        colors = greedyColoring(accessData(instance))
        num_colors = max(colors)+1
        color_numbers.append(num_colors)
        time_numbers.append(ti.time()-t)
        edge_numbers.append(len(colors))
    return color_numbers,time_numbers,edge_numbers






