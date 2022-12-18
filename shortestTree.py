import pygame
import time
# shortest tree
class Node : 
    def __init__(self,data):
        self.data = data
        self.left = None
        self.bottom = None
        self.right = None

class Tree :
    def __init__(self) : 
        self.root = None
        self.soal = [[Node(0),Node(4),Node(6),Node(8),Node(9)],
                    [Node(3),Node(2),Node(5),Node(1),Node(2)],
                    [Node(6),Node(2),Node(9),Node(9),Node(8)],
                    [Node(5),Node(1),Node(2),Node(3),Node(4)],
                    [Node(7),Node(8),Node(5),Node(3),Node(2)]]
    
    def create_tree(self,start,end):
        self.root = self.soal[start[0]][start[1]]
        dest = self.soal[end[0]][end[1]]
        self.create_tree_util(start,dest)
    
    
    def create_tree_util(self,start,dest):
        x = start[1] - 1 #kenapa minus 1?
        y = start[0] + 1
        cond = False
        if y > 4:
            return False
        for i in range(3):
            if x < 0 or x > 4:
                x+=1
                continue
            else : 
                if(self.soal[y][x] == dest):
                    if(i == 0):
                        self.soal[start[0]][start[1]].left = self.soal[y][x]
                    elif i == 1 :
                        self.soal[start[0]][start[1]].bottom = self.soal[y][x]
                    elif i == 2 : 
                        self.soal[start[0]][start[1]].right = self.soal[y][x]
                    return True
                else :
                    if (self.create_tree_util([y,x],dest)):
                        if(i == 0):
                            self.soal[start[0]][start[1]].left = self.soal[y][x]
                        elif i == 1 :
                            self.soal[start[0]][start[1]].bottom = self.soal[y][x]
                        elif i == 2 : 
                            self.soal[start[0]][start[1]].right = self.soal[y][x]
                        cond = True
                x+=1
        return cond

    def print_all(self,start:Node,path:list = []):
        path.append(start.data)
        if start.left is not None:
            self.print_all(start.left,path)
        if start.bottom is not None:
            self.print_all(start.bottom,path)
        if start.right is not None:
            self.print_all(start.right,path)
        if start.left is None and start.bottom is None and start.right is None : 
            for i in path:
                print(i,end ="-->")
            print()
        path.pop(path.__len__()-1)

    def fastest(self,start:Node,path:list = [0,[]],fixedPath = [0,[]]):
        path[1].append(start.data)
        path[0] = path[0]+start.data
        if start.left is not None:
            self.fastest(start.left,path,fixedPath)
        if start.bottom is not None:
            self.fastest(start.bottom,path,fixedPath)
        if start.right is not None:
            self.fastest(start.right,path,fixedPath)
        if start.left is None and start.bottom is None and start.right is None :
            if fixedPath[0] == 0 or fixedPath[0] > path[0] :
                fixedPath[1] = path[1][:]
                fixedPath[0] = path[0]
        path[0] = path[0] - start.data
        path[1].pop(path[1].__len__()-1)
        return fixedPath
class Snake:
    def __init__(self):
        pass
class Game:
    def __init__(self,size=8):
        pygame.init()
        pygame.display.set_caption("Snake Labyrinth")
        self.data = [
                    [Node(5),Node(1),Node(0),Node(1),Node(1),Node(5),Node(1),Node(0)],
                    [Node(0),Node(1),Node(0),Node(0),Node(0),Node(0),Node(1),Node(0)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(1),Node(0)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    [Node(0),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(3)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    [Node(1),Node(0),Node(1),Node(0),Node(1),Node(0),Node(0),Node(1)],
                    ]
        
        # buat windownya
        display = pygame.display.set_mode((50 * size,50*size))   
        # Initialing RGB Color 
        color = (255, 255, 255)
        # Changing window color
        display.fill(color)
        # buat visual petanya 
        
        self.drawMap()
    
    def drawMap(self):
        
        pygame.display.flip()
        time.sleep(100)

        
        
       
t = Tree()
t.create_tree([0,1],[4,2])
t.print_all(t.soal[0][1])
print(t.fastest(t.root)[0])
print(t.fastest(t.root)[1])
game = Game()
