import pygame 
from pygame.locals import *
import time
import random
from enum import Enum
from sys import maxsize
from collections import deque
# shortest tree


class Node : 
    counter = 0
    def __init__(self,data):
        self.data = data
        self.left = None
        self.bottom = None
        self.right = None
        self.path_id = Node.counter
        Node.counter += 1
class Graph:
    # src = https://www.geeksforgeeks.org/shortest-path-unweighted-graph/
    def __init__(self,map,source,dest):
        self.map = map
        # array of vectors is used to store the graph in the form of an adjacency list
        self.adj = [[] for i in range(len(self.map) * len(self.map[0]))]
        self.shortesPaths = []
        # create graph from map
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j].data != 1:
                    # kalo punya kanan
                    if j+1 < len(self.map[i]) and self.map[i][j+1].data != 1:
                        self.add_edge(self.adj,self.map[i][j].path_id,self.map[i][j+1].path_id)
             
                    # kalo punya kiri
                    if j-1 > -1 and self.map[i][j-1].data != 1:
                        self.add_edge(self.adj,self.map[i][j].path_id,self.map[i][j-1].path_id)
   
                    # kalo punya bawah
                    if i+1 < len(self.map) and self.map[i+1][j].data != 1:
                        self.add_edge(self.adj,self.map[i][j].path_id,self.map[i+1][j].path_id)

                    # kalo punya atas
                    if i-1 > -1 and self.map[i-1][j].data != 1:
                        self.add_edge(self.adj,self.map[i][j].path_id,self.map[i-1][j].path_id)
        self.print_paths(self.adj,len(self.map) * len(self.map[0]),source,dest)
        # self.printShortestDistance(self.adj, source, dest, len(self.map) * len(self.map[0]))
    

    def displayAjd(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                print(self.map[i][j].data,end=" ")
            print()

    def printAdj(self):
        for i in range(len(self.adj)):
            for j in range(len(self.adj[i])):
                print(self.map[i][j].path_id, end=" ")
            print()

    # utility function to form edge between two vertices source and dest
    def add_edge(self,adj, src, dest):
        # directed 
        try:
            adj[src].append(dest)
        except IndexError:
            print(src,' ',dest)

   # Function which finds all the paths and stores it in paths array
    def find_paths(self,paths, path, parent, n, u):
        # Base Case
        if (u == -1):
            paths.append(path.copy())
            return
    
        # Loop for all the parents of the given vertex
        for par in parent[u]:
    
            # Insert the current vertex in path
            path.append(u)
    
            # Recursive call for its parent
            self.find_paths(paths, path, parent, n, par)
    
            # Remove the current vertex
            path.pop()
    
    # Function which performs bfs from the given source vertex
    def bfs(self,adj, parent, n, start) -> None:
    
        # dist will contain shortest distance from start to every other vertex
        dist = [maxsize for _ in range(n)]
        q = deque()
    
        # Insert source vertex in queue and make its parent -1 and distance 0
        q.append(start)
        parent[start] = [-1]
        dist[start] = 0
    
        # Until Queue is empty
        while q:
            u = q[0]
            q.popleft()
            for v in adj[u]:
                if (dist[v] > dist[u] + 1):
    
                    # A shorter distance is found So erase all the previous parents and insert new parent u in parent[v]
                    dist[v] = dist[u] + 1
                    q.append(v)
                    parent[v].clear()
                    parent[v].append(u)
    
                elif (dist[v] == dist[u] + 1):
    
                    # Another candidate parent for shortes path found
                    parent[v].append(u)
 
    # Function which prints all the paths from start to end
    def print_paths(self,adj, n, start, end):
        paths = []
        path = []
        parent = [[] for _ in range(n)]
    
        # Function call to bfs
        self.bfs(adj, parent, n, start)
    
        # Function call to find_paths
        self.find_paths(paths, path, parent, n, end)
        print('Shortest Paths : ')
        for v in paths:
            temp = []
            # Since paths contain each path in reverse order,so reverse it
            v = reversed(v)
            # Print node for the current path
            for u in v:
                print(u, end = " ")
                temp.append(u)
            self.shortesPaths.append(temp)
            print()
    
    def getShortestPath(self):
        return self.shortesPaths
            
class Game:
    def __init__(self,size=8):
        self.pixel = 60
        pygame.init()
        pygame.display.set_caption("Snake Labyrinth")
        self.map = [
                    [Node(0),Node(0),Node(0),Node(1),Node(1),Node(1),Node(1),Node(0)],
                    [Node(0),Node(0),Node(0),Node(0),Node(0),Node(0),Node(1),Node(0)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(0)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(1),Node(0)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(0)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    ]

        # buat jalur tercepat
        source = 0
        dest = 47
        for i in range(len(self.map)): #ngeset letak start dan end nya snake di map
            for j in range(len(self.map[i])):
                if self.map[i][j].path_id == source:
                    self.map[i][j].data = 5
                elif self.map[i][j].path_id == dest:
                    self.map[i][j].data = 3
        # source e path_id ke 0 dan end nya path_id ke 
        self.graph = Graph(self.map,source,dest)
        self.shortestPaths = self.graph.getShortestPath()

        # buat windownya
        self.display = pygame.display.set_mode((self.pixel  * size,self.pixel *size))   

        # Initialing RGB Color 
        color = (234,182,118)
        # Changing window color
        self.display.fill(color)

        # buat visual petanya 
        # buat snake dan cari letak snake
        letakSnake = 0
        row = None
        col = None
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j].data == 5:
                    letakSnake = self.map[i][j].path_id
                    row = i
                    col = j

        self.snake = Snake(self.display,letakSnake,row,col)
        pygame.display.flip()
        self.drawMap()
        self.play()
        
    def printMap(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                print(self.map[i][j].data, end=" ")
            print('')
    
    def drawMap(self):
        for atas in range (len(self.map)):
            for kiri in range (len(self.map[atas])):
                if self.map[atas][kiri].data == 5 : #kalo 5 = snake
                    self.draw_land(atas * self.pixel ,kiri * self.pixel )
                    self.snake.draw(atas * self.pixel ,kiri * self.pixel )
                elif self.map[atas][kiri].data == 0: #kalo 0 : boleh di lewati
                    self.draw_land(atas * self.pixel ,kiri * self.pixel )
                    pass
                elif self.map[atas][kiri].data == 1: #kalo tembok : gk boleh di lewati
                    self.draw_wall(atas * self.pixel ,kiri * self.pixel )
                elif self.map[atas][kiri].data == 3: #kalo end : tujuan /apple
                    self.draw_land(atas * self.pixel ,kiri * self.pixel )
                    self.draw_apple(atas * self.pixel ,kiri * self.pixel )
        pygame.display.update()
        

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    print('berhenti')

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        print('berhenti 1')
                        running = False

                    elif event.key == K_LEFT:
                        self.snake.move_left(self.map)
                        print('kiri')
                        print(self.snake.path)
                        self.drawMap()
                    elif event.key == K_RIGHT:
                        self.snake.move_right(self.map)
                        print('kanan')
                        print(self.snake.path)
                        self.drawMap()

                    elif event.key == K_UP:
                        self.snake.move_up(self.map)
                        print('atas')
                        print(self.snake.path)
                        self.drawMap()

                    elif event.key == K_DOWN:
                        self.snake.move_down(self.map)
                        print('bawah')
                        print(self.snake.path)
                        self.drawMap()

            time.sleep(.1)
    
    def draw_wall(self,atas,kiri):
        image = pygame.image.load("snakegame/resources/wall60x60.png").convert()
        self.display.blit(image,(kiri,atas))
    
    def draw_apple(self,atas,kiri): #tujuan
        image = pygame.image.load("snakegame/resources/apple60x60.png").convert()
        image.set_colorkey((0, 0, 0))
        self.display.blit(image,(kiri,atas))

    def draw_land(self,atas,kiri): #tujuan
        image = pygame.image.load("snakegame/resources/land60x60.jpg").convert()
        self.display.blit(image,(kiri,atas))

class Face(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
class Snake:
    def __init__(self,display,path_id,row,col):
        self.row = row
        self.col = col
        self.path = [path_id]
        self.display = display
        self.position = None
        self.image = self.snakeDown()
        self.image.set_colorkey((0, 0, 0))

    def draw(self,atas,kiri):
        self.display.blit(self.image,(kiri,atas))
    
    def move_right(self,map):
        self.image = self.snakeRight()
        self.image.set_colorkey((0, 0, 0))
        # TODO animasi ke kanan

        if self.col < len(map[0])-1 and self.col > -1 and map[self.row][self.col+1].data == 0: #kalo boleh dilewati
            map[self.row][self.col].data = 0
            self.col +=1
            map[self.row][self.col].data = 5
            #kalau misal snake e mundur ke tempat sebelumnya
            if self.path[len(self.path) - 2] == map[self.row][self.col].path_id:
                self.path.pop()
            else:
                self.path.append(map[self.row][self.col].path_id)
        return map
    
    def move_left(self,map):
        self.image = self.snakeLeft()
        self.image.set_colorkey((0, 0, 0))
        # TODO animasi ke kanan

        if self.col < len(map[0]) and self.col > 0 and map[self.row][self.col-1].data == 0: #kalo boleh dilewati
            map[self.row][self.col].data = 0
            self.col -=1
            map[self.row][self.col].data = 5
            #kalau misal snake e mundur ke tempat sebelumnya
            if self.path[len(self.path) - 2] == map[self.row][self.col].path_id:
                self.path.pop()
            else:
                self.path.append(map[self.row][self.col].path_id)
        return map
        
    def move_down(self,map):
        self.image = self.snakeDown()
        self.image.set_colorkey((0, 0, 0))
        # TODO animasi ke kanan
        print('ROW : ',self.row)
        print(len(map))
        if self.row < len(map)-1 and self.row > -1 and map[self.row+1][self.col].data == 0 : #kalo boleh dilewati
            map[self.row][self.col].data = 0
            self.row +=1
            map[self.row][self.col].data = 5
            #kalau misal snake e mundur ke tempat sebelumnya
            if self.path[len(self.path) - 2] == map[self.row][self.col].path_id:
                self.path.pop()
            else:
                self.path.append(map[self.row][self.col].path_id)
            # print('bawah 2')
        # else:
        #     print('gagal')
        return map

    def move_up(self,map):
        self.image = self.snakeUp()
        self.image.set_colorkey((0, 0, 0))
        # TODO animasi ke kanan

        if self.row < len(map[0]) and self.row > 0 and map[self.row-1][self.col].data == 0: #kalo boleh dilewati
            map[self.row][self.col].data = 0
            self.row -=1
            map[self.row][self.col].data = 5
            #kalau misal snake e mundur ke tempat sebelumnya
            if self.path[len(self.path) - 2] == map[self.row][self.col].path_id:
                self.path.pop()
            else:
                self.path.append(map[self.row][self.col].path_id)
        return map

    def face(self,direction):
        self.position = direction
    
    def snakeRight(self):
        right_img =pygame.image.load("snakegame/resources/snake60x60.png").convert()
        right_img =  pygame.transform.rotate(right_img, 270)
        self.face(Face.RIGHT)
        return right_img
        #harus di return soalnya dia cmn image blm di load. 

    def snakeLeft(self):
        left_img =pygame.image.load("snakegame/resources/snake60x60.png").convert()
        left_img =  pygame.transform.rotate(left_img, 90)
        self.face(Face.LEFT)
        return left_img
        
    def snakeDown(self):
        down_img =pygame.image.load("snakegame/resources/snake60x60.png").convert()
        down_img =  pygame.transform.rotate(down_img, 180)
        self.face(Face.DOWN)
        return down_img
        
    def snakeUp(self):
        # up_img = pygame.image.load("snakegame/resources/snake60x60.png").convert()
        up_img =  pygame.transform.rotate(pygame.image.load("snakegame/resources/snake60x60.png").convert(), 0)
        self.face(Face.UP)
        return up_img
        

game = Game()
pygame.quit()