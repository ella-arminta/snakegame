import pygame 
from pygame.locals import *
import time
import random
from enum import Enum
# shortest tree


# class Tree :
#     def __init__(self) : 
#         self.root = None
#         self.soal = [[Node(0),Node(4),Node(6),Node(8),Node(9)],
#                     [Node(3),Node(2),Node(5),Node(1),Node(2)],
#                     [Node(6),Node(2),Node(9),Node(9),Node(8)],
#                     [Node(5),Node(1),Node(2),Node(3),Node(4)],
#                     [Node(7),Node(8),Node(5),Node(3),Node(2)]]
    
#     def create_tree(self,start,end):
#         self.root = self.soal[start[0]][start[1]]
#         dest = self.soal[end[0]][end[1]]
#         self.create_tree_util(start,dest)
    
    
#     def create_tree_util(self,start,dest):
#         x = start[1] - 1 #kenapa minus 1?
#         y = start[0] + 1
#         cond = False
#         if y > 4:
#             return False
#         for i in range(3):
#             if x < 0 or x > 4:
#                 x+=1
#                 continue
#             else : 
#                 if(self.soal[y][x] == dest):
#                     if(i == 0):
#                         self.soal[start[0]][start[1]].left = self.soal[y][x]
#                     elif i == 1 :
#                         self.soal[start[0]][start[1]].bottom = self.soal[y][x]
#                     elif i == 2 : 
#                         self.soal[start[0]][start[1]].right = self.soal[y][x]
#                     return True
#                 else :
#                     if (self.create_tree_util([y,x],dest)):
#                         if(i == 0):
#                             self.soal[start[0]][start[1]].left = self.soal[y][x]
#                         elif i == 1 :
#                             self.soal[start[0]][start[1]].bottom = self.soal[y][x]
#                         elif i == 2 : 
#                             self.soal[start[0]][start[1]].right = self.soal[y][x]
#                         cond = True
#                 x+=1
#         return cond

#     def print_all(self,start:Node,path:list = []):
#         path.append(start.data)
#         if start.left is not None:
#             self.print_all(start.left,path)
#         if start.bottom is not None:
#             self.print_all(start.bottom,path)
#         if start.right is not None:
#             self.print_all(start.right,path)
#         if start.left is None and start.bottom is None and start.right is None : 
#             for i in path:
#                 print(i,end ="-->")
#             print()
#         path.pop(path.__len__()-1)

#     def fastest(self,start:Node,path:list = [0,[]],fixedPath = [0,[]]):
#         path[1].append(start.data)
#         path[0] = path[0]+start.data
#         if start.left is not None:
#             self.fastest(start.left,path,fixedPath)
#         if start.bottom is not None:
#             self.fastest(start.bottom,path,fixedPath)
#         if start.right is not None:
#             self.fastest(start.right,path,fixedPath)
#         if start.left is None and start.bottom is None and start.right is None :
#             if fixedPath[0] == 0 or fixedPath[0] > path[0] :
#                 fixedPath[1] = path[1][:]
#                 fixedPath[0] = path[0]
#         path[0] = path[0] - start.data
#         path[1].pop(path[1].__len__()-1)
#         return fixedPath
class Node : 
    counter = 0
    def __init__(self,data):
        self.data = data
        self.left = None
        self.bottom = None
        self.right = None
        Node.counter += 1
        self.path_id = Node.counter
class Game:
    def __init__(self,size=8):
        self.pixel = 60
        pygame.init()
        pygame.display.set_caption("Snake Labyrinth")
        self.map = [
                    [Node(5),Node(0),Node(0),Node(1),Node(1),Node(1),Node(1),Node(0)],
                    [Node(0),Node(0),Node(0),Node(0),Node(0),Node(0),Node(1),Node(0)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(0)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(1),Node(0)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(1),Node(3)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    ]
        
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
        # self.position = Face.DOWN #pilihan : LEFT,RIGHT,UP,DOWN
        # if self.position == Face.UP:
        #     self.image = pygame.image.load(self.snakeUp()).convert()
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
        right_img =pygame.image.load("resources/snake60x60.png").convert()
        right_img =  pygame.transform.rotate(right_img, 270)
        self.face(Face.RIGHT)
        return right_img
        #harus di return soalnya dia cmn image blm di load. 

    def snakeLeft(self):
        left_img =pygame.image.load("resources/snake60x60.png").convert()
        left_img =  pygame.transform.rotate(left_img, 90)
        self.face(Face.LEFT)
        return left_img
        
    def snakeDown(self):
        down_img =pygame.image.load("resources/snake60x60.png").convert()
        down_img =  pygame.transform.rotate(down_img, 180)
        self.face(Face.DOWN)
        return down_img
        
    def snakeUp(self):
        # up_img = pygame.image.load("resources/snake60x60.png").convert()
        up_img =  pygame.transform.rotate(pygame.image.load("resources/snake60x60.png").convert(), 0)
        self.face(Face.UP)
        return up_img
        
       
# t = Tree()
# t.create_tree([0,1],[4,2])
# t.print_all(t.soal[0][1])
# print(t.fastest(t.root)[0])
# print(t.fastest(t.root)[1])
game = Game()
pygame.quit()