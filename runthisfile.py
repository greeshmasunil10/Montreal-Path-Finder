# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:25:24 2019

@author: Greeshma
"""

import numpy as np 
import shapefile
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from builtins import int, input
from matplotlib.pyplot import grid
import statistics
import pathfinder
from test.test_lzma import INPUT

sf = shapefile.Reader("crime_dt.shp") 

def makegrid(size):
    fl = sf.fields
    n = 0.04 / size
    print("n:",n)
    x = np.linspace(-73.59, -73.55, n+1) 
    y = np.linspace(45.53, 45.49, n+1)  
    x_1, y_1 = np.meshgrid(x, y)
    plt.plot(x_1, y_1, marker='.', color='k', linestyle='none')  
    return x_1, y_1


def checkgrid():
    i = 1
    for name in sf.shapes() :
        print(name.points)
        print(type(name.points))
        print
        i += 1
        if i == 10:
            break

class vertex :
    __topleft=[]
    __topright=[]
    __bottomleft=[]
    __bottomright=[]
    __row=0
    __column=0
    __crimerate=0
    __points=[]
    __risky = 0
    
    def __init__(self,c,d,a,b) :
        self.__points=[]
        self.__risky=0
        self.__topleft=a
        self.__topright=b
        self.__bottomleft=c
        self.__bottomright=d
        
    def setindex(self,i,j):
        self.__row=i
        self.__column=j        
    def addpoint(self,p):
        self.__points.append(p)       
    def setcrime(self):
        self.__crimerate+=1  
    def getcrime(self):
        return self.__crimerate 
    def getrow(self):
        return self.__row
    def getcolumn(self):
        return self.__column
    def gettl(self):
        return self.__topleft 
    def gettr(self):
        return self.__topright
    def getbl(self):
        return self.__bottomleft 
    def getbr(self):
        return self.__bottomright
    def getpoints(self):
        return self.__points
    def setriskytrue(self):
        self.__risky = 1
    def setriskyfalse(self):
        self.__risky= 0
    def getrisk(self):
        return self.__risky
        
        
def plotgraph(str):
    points = gpd.read_file(str)


def initgrid(x,y) :
    print("Creating grid..")
    print("size====",size)
    grid = [[vertex(0,0,0,0) for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            grid[i][j]=vertex([x[i+1][j],y[i+1][j]], [x[i+1][j+1],y[i+1][j+1]] 
                             , [x[i][j],y[i][j]] , [x[i][j+1],y[i][j+1]] )
    return grid

def setcrimerates(grid):
    crimes=[]
    high=[]
    low=[]
    print("Calculating crime rates...")
    for i in range(size):
        for j in range(size):
            grid[i][j]=checkifcontains(grid[i][j])
    print("Calculating threshold..")
    for i in range(size):
        for j in range(size):
            gridblock= grid[i][j]
#             print("grid:[",i,j,"] crimerate:",gridblock.getcrime())
#             print("points:",gridblock.getpoints)
            crimes.append(gridblock.getcrime())

#     thresh=90

    thresh= int(input("\nEnter threshold percentage (50,75,90,etc..):"))
    if thresh == 50:
        median=statistics.median(crimes)
    elif thresh == 75:
        crimes.sort()
        crimes1= crimes[len(crimes)//2:]
        median= statistics.median(crimes1)
    else :
        crimes.sort()
        leng= len(crimes)
        ind= thresh * leng // 100
        median = crimes[ind]
    print()    
    print("Median:",median)
    totalcrimes= sum(crimes)
    print("Total crimes:",totalcrimes)
    mean= statistics.mean(crimes)*8
    print("Mean:",mean)
    std= statistics.stdev(crimes, xbar=None)
    print("Standard Deviation:",std)
    print()
    print("Plotting graph..")
    for i in range(size):
        for j in range(size):
            gridblock= grid[i][j]
            if gridblock.getcrime()>median :
                plt.plot(*zip(*gridblock.getpoints()), marker='.', color='y', ls='')
                gridblock.setriskytrue()
                grid[i][j]= gridblock
                continue
            elif gridblock.getcrime() <=median :
                plt.plot(*zip(*gridblock.getpoints()), marker='.', color='b', ls='')
                gridblock.setriskyfalse()
                grid[i][j]= gridblock
                continue
    plt.show()

    
    return grid  

def insidegrid(gridblock,px,py):
    if (float(px) > float(gridblock.gettl()[0]) and  float(px) < float(gridblock.gettr()[0]) and float(py) > float(gridblock.getbl()[1]) and float(py) < float(gridblock.gettl()[1])) :
        return True
    else :
        return False

  
def checkifcontains(gridblock):
    i=1
    for name in sf.shapes() :
        px= name.points[0][0]
        py= name.points[0][1]
        points=[]
        points.append(px)
        points.append(py)
        if insidegrid(gridblock, px, py):
            gridblock.setcrime()
            gridblock.addpoint([px,py])
    return gridblock    

def findpath(grid):
    print("\nCrime rates in each area")
    print()
    maze1=[]
    for i in range(size):
        row=[]
        for j in range(size):
            gb= grid[i][j]
            row.append(gb.getcrime())
        maze1.append(row)    
    
    for i in maze1:
        print(i)  
        
        
    print("\nRisky Areas ( 1 for risky vertex, 0 for less risky vertex :-")
    print()    
    maze=[]
    for i in range(size):
        row=[]
        for j in range(size):
            gb= grid[i][j]
            row.append(gb.getrisk())
        maze.append(row)    
    
    for i in maze:
        print(i)
    
    print()    
      
        
#     print(maze)    
    print()
    print("Calculating path...")
    path= pathfinder.main(maze,size) 
#     for i in path:
#         print("(",grid[i[0]][i[1]],")")   
 

    
plotgraph("crime_dt.shp")  
# size=0.002
size= float(input("\nEnter grid size (eg.0.002,0.003):"))
x, y = makegrid(size)
print()
n = 0.04 / size
n= int(n)
size=int(n-1)
print("grid size=",n) 
grid=initgrid(x,y) 
grid= setcrimerates(grid)
findpath(grid)





