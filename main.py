import pygame 
from pygame.locals import *
import time
from enum import Enum
from sys import maxsize
from collections import deque
import random

class Node : 
    counter = 0
    def __init__(self,data):
        self.data = data
        self.path_id = Node.counter
        Node.counter += 1
class Graph:
    def __init__(self,map,source,dest):
        self.map = map
        Node.counter = 0
        # adjenct list
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
    def bfs(self,adj, parent, size, start) -> None:
    
        # dist will contain shortest distance from start to every other vertex
        dist = [maxsize for _ in range(size)]
        queue = deque()
    
        # Insert source vertex in queue and make its parent -1 and distance 0
        queue.append(start)
        parent[start] = [-1]
        dist[start] = 0
    
        # Until Queue is empty
        while queue:
            id = queue[0]
            queue.popleft()
            for v in adj[id]:
                if (dist[v] > dist[id] + 1):
                    # A shorter distance is found So erase all the previous parents and insert new parent u in parent[v]
                    dist[v] = dist[id] + 1
                    queue.append(v)
                    parent[v].clear()
                    parent[v].append(id)
    
                elif (dist[v] == dist[id] + 1):
                    # Another candidate parent for shortes path found
                    parent[v].append(id)
 
    # Function which prints all the paths from start to end
    def print_paths(self,adj, size, start, end):
        paths = []
        path = []
        parent = [[] for _ in range(size)]
    
        self.bfs(adj, parent, size, start)
    
        # find paths
        self.find_paths(paths, path, parent, size, end)
        print('Shortest Paths : ')
        for path in paths:
            temp = ''
            # direverse path nya
            path = reversed(path)
            # Print node buat path sekarang
            for path_id in path:
                print(path_id, end = " ")
                temp += str(path_id) + ' '
            self.shortesPaths.append(temp)
            print()
        # print(self.shortesPaths)
    
    def getShortestPath(self):
        if len(self.shortesPaths) == 0:
            return 0
        else : 
            return self.shortesPaths
            
class Game:
    def __init__(self,size=8):
        self.pixel = 60
        pygame.init()
        pygame.display.set_caption("Snake Labyrinth")
        # pygame.mixer.music.load('resources/bg_music_2.mp3')
        # pygame.mixer.music.play(-1, 0)

        self.randMap()
        # if self.randMap() == 0:
        #     self.randMap()
        # print(self.map)
        # print(self.dest)
        # print(self.source)

        # buat windownya
        self.windowX = self.pixel  * size
        self.windowY = self.pixel *size
        self.display = pygame.display.set_mode((self.windowX,self.windowY))   

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
        
    def randMap(self):
        self.map = [
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
            [Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1)),Node(random.randint(0, 1))],
        ]
        # self.map = [
        #        [Node(5),Node(0),Node(0),Node(1),Node(1),Node(1),Node(1),Node(0)],
        #             [Node(0),Node(0),Node(0),Node(0),Node(0),Node(0),Node(1),Node(0)],
        #             [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(0)],
        #             [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(1),Node(0)],
        #             [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
        #             [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(1),Node(0)],
        #             [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
        #             [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
        # ]
        # buat jalur tercepat
        self.source = 1
        self.dest = 62
        for i in range(len(self.map)): #ngeset letak start dan end nya snake di map
            for j in range(len(self.map[i])):
                if self.map[i][j].path_id == self.source:
                    self.map[i][j].data = 5
                    
                elif self.map[i][j].path_id == self.dest:
                    self.map[i][j].data = 3
                    print(self.map[i][j].data, ' ',self.map[i][j].path_id )
        self.printMap()
        # source e path_id ke 0 dan end nya path_id ke 
        self.graph = Graph(self.map,self.source,self.dest)
        self.shortestPaths = self.graph.getShortestPath()
        if self.shortestPaths == 0:
            # return 0
            self.randMap()

    def printMap(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                print(self.map[i][j].data, end=" ")
            print('')
                
    def cekJawaban(self):
        self.snake.path.append(self.dest)
        jalurSnake = ''
        for i in range(len(self.snake.path)):
            jalurSnake = jalurSnake + str(self.snake.path[i])+' '
        print(jalurSnake) #TODO
        # cek
        benar = False
        for i in range(len(self.shortestPaths)):
            if jalurSnake == self.shortestPaths[i]:
                benar = True
        return benar
            

    
    def salah(self):
        pygame.display.set_caption("YOU LOSE!!!")
        textcolor = (255, 255, 255)
        bgcolor = (255,0,0)
        self.display.fill(bgcolor)
        X = self.windowX
        Y = self.windowY

        #buat tulisan y 
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('GAME OVER. YOU LOSE!', True, textcolor)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)
        self.display.blit(text, textRect)
        pygame.display.flip()
        
        

   
    
            # if pygame.QUIT:
    
            #     # deactivates the pygame library
            #     pygame.quit()
    
            #     # quit the program.
            #     quit()
 
       
    
    def benar(self):
        pygame.display.set_caption("YOU WIN!!!")
        color = (0,255, 0)
        self.display.fill(color)
        pygame.display.flip()

        textcolor = (255,255,255)
        font = pygame.font.Font('freesansbold.ttf', 32)
        # text 1
        text = font.render('YOU WIN!!!', True, textcolor)
        textRect = text.get_rect()
        X = self.windowX
        Y = self.windowY
        textRect.center = (X // 2, Y // 2)
        self.display.blit(text, textRect)
        pygame.display.flip()
                
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
        lanjut = True
        while running:
            if lanjut == False:
                pygame.mixer.Sound.play(pygame.mixer.Sound('resources/ding.mp3'))
                if (self.cekJawaban() is True):
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(pygame.mixer.Sound('resources/win.mp3'))
                    self.benar()
                    pause = True 
                    while pause:
                        self.benar()
                        time.sleep(.1)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pause = False
                                running = False
                                print('berhenti')
                    
                        
                    
                elif (self.cekJawaban() is False):
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(pygame.mixer.Sound('resources/game_over.mp3'))
                    self.salah()
                    pause = True 
                    while pause:
                        self.salah()
                        time.sleep(.1)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pause = False
                                running = False
                                print('berhenti')
                    
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    print('berhenti')

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        print('berhenti 1')
                        running = False

                    elif event.key == K_LEFT:
                        lanjut = self.snake.move_left(self.map)
                        print('kiri')
                        print(self.snake.path)
                        self.drawMap()
                    elif event.key == K_RIGHT:
                        lanjut = self.snake.move_right(self.map)
                        print('kanan')
                        print(self.snake.path)
                        self.drawMap()

                    elif event.key == K_UP:
                        lanjut = self.snake.move_up(self.map)
                        print('atas')
                        print(self.snake.path)
                        self.drawMap()

                    elif event.key == K_DOWN:
                        lanjut = self.snake.move_down(self.map)
                        print('bawah')
                        print(self.snake.path)
                        self.drawMap()

            time.sleep(.1)
    
    def draw_wall(self,atas,kiri):
        image = pygame.image.load("resources/wall60x60.png").convert()
        self.display.blit(image,(kiri,atas))
    
    def draw_apple(self,atas,kiri): #tujuan
        image = pygame.image.load("resources/apple60x60.png").convert()
        image.set_colorkey((0, 0, 0))
        self.display.blit(image,(kiri,atas))

    def draw_land(self,atas,kiri): #tujuan
        image = pygame.image.load("resources/land60x60.jpg").convert()
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
            return True #lanjut gk 
        elif self.col < len(map[0])-1 and self.col > -1 and map[self.row][self.col+1].data == 3:
            map[self.row][self.col].data = 0
            map[self.row][self.col+1].data = 5
            return False #lanjut gk 

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
            return True
        elif self.col < len(map[0]) and self.col > 0 and map[self.row][self.col-1].data == 3:
            map[self.row][self.col].data = 0
            map[self.row][self.col-1].data = 5
            return False #lanjut gk 
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
            return True
        elif self.row < len(map)-1 and self.row > -1 and map[self.row+1][self.col].data == 3:
            map[self.row][self.col].data = 0
            map[self.row+1][self.col].data = 5
            return False #lanjut gk 
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
            return True
        elif self.row < len(map[0]) and self.row > 0 and map[self.row-1][self.col].data == 3:
            map[self.row][self.col].data = 0
            map[self.row-1][self.col].data = 5
            return False #lanjut gk 
        return map

    def face(self,direction):
        self.position = direction
    
    def snakeRight(self):
        right_img = pygame.image.load("resources/snake.png").convert()
        right_img =  pygame.transform.rotate(right_img,90 )
        self.face(Face.RIGHT)
        return right_img
        #harus di return soalnya dia cmn image blm di load. 

    def snakeLeft(self):
        left_img =pygame.image.load("resources/snake.png").convert()
        left_img =  pygame.transform.rotate(left_img, 270)
        self.face(Face.LEFT)
        return left_img
        
    def snakeDown(self):
        down_img = pygame.image.load("resources/snake.png").convert()
        down_img =  pygame.transform.rotate(down_img,0 )
        self.face(Face.DOWN)
        return down_img
        
    def snakeUp(self):
        up_img =  pygame.transform.rotate(pygame.image.load("resources/snake.png").convert(), 180)
        self.face(Face.UP)
        return up_img
        

game = Game()
pygame.quit()