# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:25:24 2019

@author: Greeshma
"""

import numpy as np 
import shapefile
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid
import statistics
import astar
import crimemap
import showpath

sf = shapefile.Reader("crime_dt.shp") 
median =0
thresh=0

def makegrid(grid_size):
    print("grid_size:",grid_size)
    x = np.linspace(-73.59, -73.55, grid_size+1) 
    y = np.linspace(45.53, 45.49, grid_size+1)  
    x_1, y_1 = np.meshgrid(x, y)
    plt.plot(x_1, y_1, marker='.', color='k', linestyle='none')  
    return x_1, y_1


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
    
    def __init__(self,p_bottomleft,p_bottomright,p_topleft,p_topright) :
        self.__points=[]
        self.__risky=0
        self.__topleft = p_topleft
        self.__topright = p_topright
        self.__bottomleft = p_bottomleft
        self.__bottomright = p_bottomright
             
    def addpoint(self,p):
        self.__points.append(p)     
    def getpoints(self):
        return self.__points
    
    def setcrime(self):
        self.__crimerate+=1  
    def getcrime(self):
        return self.__crimerate 
    
    def gettl(self):
        return self.__topleft 
    def gettr(self):
        return self.__topright
    def getbl(self):
        return self.__bottomleft 
    def getbr(self):
        return self.__bottomright
    
    def setriskytrue(self):
        self.__risky = 1
    def setriskyfalse(self):
        self.__risky= 0
    def getrisk(self):
        return self.__risky


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
    print("Calculating crime rates...")
    for i in range(size):
        for j in range(size):
            grid[i][j]=addCrimePoints(grid[i][j])
            crimes.append(grid[i][j].getcrime())
    global thresh
#    thresh=80
    thresh= int(input("\nEnter threshold percentage (50,75,90,etc..):"))
    crimes.sort()
    leng= len(crimes)
    ind= thresh * leng // 100
    global median
    median = crimes[ind]  
    print("Median:",median)
    totalcrimes= sum(crimes)
    print("Total crimes:",totalcrimes)
    mean= statistics.mean(crimes)
    print("Mean:",mean)
    std= statistics.stdev(crimes, xbar=None)
    print("Standard Deviation:",std)
    print()
    print("Plotting graph..")
    for i in range(size):
        for j in range(size):
            gridblock= grid[i][j]
            if gridblock.getcrime()>median :
                plt.plot(*zip(*gridblock.getpoints()), marker='.', color='r', ls='')
                gridblock.setriskytrue()
                grid[i][j]= gridblock
                continue
            elif gridblock.getcrime() <=median :
                plt.plot(*zip(*gridblock.getpoints()), marker='.', color='g', ls='')
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

  
def addCrimePoints(gridblock):
    for val in sf.shapes() :
        px= val.points[0][0]
        py= val.points[0][1]
        if insidegrid(gridblock, px, py):
            gridblock.setcrime()
            gridblock.addpoint([px,py])
    return gridblock    

def findpath(grid):
    print("\nCrime rates in each area")
    print()
    global maze1
    maze1=[]
    for i in range(size):
        row=[]
        for j in range(size):
            gb= grid[i][j]
            row.append(gb.getcrime())
        maze1.append(row)      
    crimemap.disp(np.array(maze1),grid_size,median)   
    maze=[]
    for i in range(size):
        row=[]
        for j in range(size):
            gb= grid[i][j]
            row.append(gb.getrisk())
        maze.append(row)    
    print("Calculating path...")
    global path

    print("Enter start cordinate:([0 to",size-1,"])")
    x1=int(input("x:"))
    y1=int(input("y:"))
    print("Enter destination cordinate:([0 to",size-1,"])")
    x2=int(input("x:"))
    y2=int(input("y:"))
    
    start = (x1,y1)
    end = (x2,y2)
    
    path= astar.main(maze,grid_size,start,end) 
    print("Path found!!!:",path)
    
    for i in path:
        maze1[i[0]][i[1]]=-3*thresh-1
    showpath.disp(np.array(maze1),size,median)   
            
        

size=0.003
size= float(input("\nEnter grid size (eg.0.002,0.003):"))
grid_size = 0.04 / size
x, y = makegrid(grid_size)
n= int(grid_size)
size=int(n)
print("grid size=xxxxxxxx",n) 
grid=initgrid(x,y)
grid= setcrimerates(grid)
findpath(grid)





