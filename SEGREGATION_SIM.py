# Program: SEGREGATION_SIM.py
# Author: JOSEPH M ABRUZZO
# Date: Jan. 2017
# ----------------------------
# This program replicates Schelling's (1973) Jornal of Mathematical Sociology
# paper modeling segregation behavior as an emergent property of a simple
# agent-based model.


import math
import random
import numpy as np
from graphics import *
import pandas as pd


GRID_DIM = 50
WIN_WIDTH = GRID_DIM * 12
NUM_GROUPS = 4
GROUP_DIST = [0.25, 0.25, 0.25, 0.25, 0, 0]
GROUP_COLORS = ["red", "blue", "yellow", "orange", "green", "purple"]
NEIGHBORHOOD_RADIUS = 5
P_EMPTY = 0.5
DENSITY_CRIT = 0.33
NEIGHBORHOOD_SIZE = (2 * float(NEIGHBORHOOD_RADIUS) + 1)**2 - 1


class agent():
    def __init__(self, color, obj):
        self.color = color
        self.obj = obj


def initGridVis(grid, win):
    for i in range(GRID_DIM):
        for j in range(GRID_DIM):
            a = grid[i][j]
            
            x1 = j * float(WIN_WIDTH / GRID_DIM)
            y1 = i * float(WIN_WIDTH / GRID_DIM)
            
            p1 = Point(x1, y1)
            p2 = Point(x1 + float(WIN_WIDTH / GRID_DIM), y1 + float(WIN_WIDTH / GRID_DIM))
            
            rect = Rectangle(p1, p2)
            
            if a != None:
                rect = Rectangle(p1, p2)
                
                rect.setFill(a.color)
                a.obj = rect
            
                rect.draw(win)


def fracSameNeighbors(a, grid, d1, d2):
    same = 0
    tot = 0
    
    for i in range(-NEIGHBORHOOD_RADIUS, NEIGHBORHOOD_RADIUS + 1):
        for j in range(-NEIGHBORHOOD_RADIUS, NEIGHBORHOOD_RADIUS + 1):
            if d1 + j >= 0 and d2 + i >= 0 and d1 + j <= GRID_DIM - 1 and d2 + i <= GRID_DIM - 1:
                if not (i == 0 and j == 0):
                    
                    n = grid[d1 + j][d2 + i]
                    
                    if n != None: 
                        
                        tot = tot + 1
                        
                        if a.color == n.color:
                            same = same + 1
    
    return float(same) / tot


def simulate(grid, win):
    
    while True:
        d1 = random.randint(0, GRID_DIM - 1)
        d2 = random.randint(0, GRID_DIM - 1)
    
        a = grid[d1][d2]
    
        if a != None: break
        
    f = fracSameNeighbors(a, grid, d1, d2)

    if f < DENSITY_CRIT:

        while True:
            d3 = random.randint(0, GRID_DIM - 1)
            d4 = random.randint(0, GRID_DIM - 1)

            if grid[d3][d4] == None: break

        q1 = d1 * float(WIN_WIDTH / GRID_DIM)
        q2 = d2 * float(WIN_WIDTH / GRID_DIM)
        q3 = d3 * float(WIN_WIDTH / GRID_DIM)
        q4 = d4 * float(WIN_WIDTH / GRID_DIM)

        a.obj.move(q4-q2, q3-q1)

        grid[d3][d4] = a
        grid[d1][d2] = None


def getAgentAttr():
    
    s = np.random.multinomial(1, GROUP_DIST)
    
    c = 0
    for i in range(0, len(GROUP_COLORS)):
        if s[i] != 0:
            c = i
    
    color = GROUP_COLORS[c]
    
    obj = None
        
    a = agent(color, obj)
    
    return a


def createAgentGrid():
    g = []
    
    for i in range(GRID_DIM):
        row = []
        
        for j in range(GRID_DIM):
            
            p = random.random()
            
            if p < P_EMPTY:
                a = None
            else:
                a = getAgentAttr()
            
            row.append(a)
        
        g.append(row)
    
    return g


def main():
    grid = createAgentGrid()
    
    win = GraphWin("SEGREGATION", WIN_WIDTH, WIN_WIDTH, autoflush = False)
    
    initGridVis(grid, win)
    
    win.getMouse()
    
    while True:
        simulate(grid, win)
        
        press = win.checkKey()
        if press == "x":
            break

    win.close()


main()