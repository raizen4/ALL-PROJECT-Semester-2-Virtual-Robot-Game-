import sys,pygame
import pytmx
import random
import time
import os
import collections
import numpy as np
import heapq
from pygame.locals import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements,(priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Inventory(object):
    def __init__(self):
        self.inventory={}
    def update_with_item(self,item,quantity):
        if item in self.inventory.keys():
         self.inventory[item]+=quantity
        else:
         self.inventory[item]=1
    def sell_everything(self):
        pass
    def draw_inventory(self):
        pass
    def get_items(self):
        return self.inventory.keys()

    def sort_inventory(self):
        pass



class Resource(pygame.sprite.Sprite):
    def __init__(self,name,image,toughness,value,mined=False):
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.image_name=image
        self.image=pygame.image.load(self.image_name).convert_alpha()
        self.rect=self.image.get_rect()
        self.toughness=toughness
        self.value=value
        self.mined=mined


    def set_position_on_grid(self,x_pos,y_pos):
        self.rect.x=x_pos*map_tilesize
        self.rect.y=y_pos*map_tilesize

    def get_pos_from_grod(self):
        return (sel.rect.x//map_tilesize,self.rect.y//map_tilesize)

    def update_status(self,did_robot_mine_resource=False):#flag method,to see if the resource was mined,did_robot_mine_resource should return a bool
        if did_robot_mine_resource==True:
            self.mined=True


class Robot(pygame.sprite.Sprite,Inventory):
    def __init__(self,name,image,max_loadout):
        pygame.sprite.Sprite.__init__(self)
        Inventory.__init__(self)
        self.name=name
        self.image_name=image
        self.image=pygame.image.load(self.image_name)
        self.rect=self.image.get_rect()
        self.inventory =Inventory()#still in development
        self.level=1

    #set initial position on the MATRIX
    def set_pos(self,x,y):
        self.rect.x=x
        self.rect.y=y

    def get_pos(self):
        return (self.rect.x,self.rect.y)

    #set position on the actual GRID,so it is initial position * map_tilesize to get the real position on the screen
    def set_grid(self, x, y):
        self.rect.x = x*map_tilesize
        self.rect.y = y*map_tilesize

    def get_grid(self):
        return (int(self.rect.x//map_tilesize),int(self.rect.y//map_tilesize))

    def move(self,direction):
        if direction=="left":
            self.rect.x -=map_tilesize
        if direction=="right":
            self.rect.x += map_tilesize
        if direction=="up":
            self.rect.y-=map_tilesize
        if direction=="bottom":
            self.rect.y+=map_tilesize
    def mine(self,resource):
        for progress in range(60):
                        time.sleep(0.0000001)
                        progress_bar=pygame.draw.rect(screen, (255,255,255), pygame.Rect(robot.rect.x-7,robot.rect.y-7,0.25*progress,5))#rect(x,y,lungimea barii,grosimea barii)
                        pygame.display.update(progress_bar)
        self.inventory.update_with_item(resources_information[remove_resource_from_coordinates],1)
    def advance_level(self):
        self.level+=1


"""-------------------Search Algorithms------------------------------------------------"""

"""Function to check if the neighbor tiles are passable,heuristic function for a simple up,down,right,left tile-game
and a function for calculating the cost from node a to node b"""
"""-------------------------"""
def Manhattan_distance(node_a,node_b):
    return (abs(node_a[0]-node_b[0])+abs(node_a[1]-node_b[1]))

def is_passable(id):
 if id[0]<0 or id[0]>map_width or id[1]>map_height or id[1]<0:
     return False
 else:
     return True


def neighbors(matrix_coordinates):
    (x,y)=matrix_coordinates[0],matrix_coordinates[1]
    neighbors_list=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]#putting
    for id in neighbors_list:
        if is_passable(id)==False:
            neighbors_list.remove(id)
    return neighbors_list

"""----------------------------"""


"""Actual searching algorithms"""
"""---------------------------"""

def breadth_first_search(matrix_with_costs_and_walls, start, goal):
    frontier=Queue()
    frontier.put(start)
    came_from={}
    came_from[start]=None
    while not frontier.empty():
        curent_id=frontier.get()
        neighbors_for_search=neighbors((curent_id))

        if curent_id == goal:
            break

        for nexts in neighbors_for_search:
            if (nexts not in came_from) and (matrix_with_costs_and_walls[nexts[1]][nexts[0]][1]==1):
               frontier.put(nexts)
               came_from[nexts]=curent_id
    return came_from

def dijkstra_search(matrix_of_costs_and_walls,start,goal):
    frontier=PriorityQueue()
    frontier.put(start,0)
    cost_so_far={}
    cost_so_far[start]=0
    came_from={}
    came_from[start]=None
    while not frontier.empty():
        current=frontier.get()

        if current==goal:
            break
        for nexts in neighbors(current):
            if matrix_of_costs_and_walls[nexts[1]][nexts[0]][0]>2000:
                 pass
            else:
                print(cost_so_far)
                new_cost=cost_so_far[current]+matrix_of_costs_and_walls[nexts[1]][nexts[0]][0]#accesing the cost for the neighbor

                if nexts not in came_from or new_cost< cost_so_far[nexts]:
                 cost_so_far[nexts]=new_cost
                 priority=new_cost
                 frontier.put(nexts,priority)
                 came_from[nexts]=current
    return came_from,cost_so_far



def A_star_search(matrix_of_walls_and_costs,start,goal):
    frontier=PriorityQueue()
    frontier.put(start,0)
    came_from={}
    came_from[start]=None
    cost_so_far={}
    cost_so_far[start]=0

    while not frontier.empty():
        current=frontier.get()

        if current==goal:
            break
        for nexts in neighbors(current):

            new_cost=cost_so_far[current]+ matrix_of_walls_and_costs[nexts[1]][nexts[0]][0]
            if nexts not in came_from or new_cost<cost_so_far[nexts]:
                cost_so_far[nexts]=new_cost
                priority=new_cost+ Manhattan_distance(goal,nexts)
                frontier.put(nexts,priority)
                came_from[nexts]=current
    return came_from,cost_so_far





"""the function below takes as the first argument
the search algorithm used(because depending of the algorithm we can see what path did the robot take the second argument is the start node and the goal argument is the end node"""
def reconstruct_path(came_from,start,goal):
    current=goal
    path=[current]
    while current!=start:
        current=came_from[current]
        path.append(current)
    path.reverse()
    for id in path:
        bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
        screen.blit(bck,robot.get_pos())
        robot.set_grid(id[0],id[1])
        resource_group.draw(screen)
        robot_group.draw(screen)
        pygame.display.update(robot_group.sprites()+resource_group.sprites())
        time.sleep(0.1)

    return path

class Button:#still in development
    """
    x and y coordinates set the point on the screen from wich pygame starts drawing our button
    it is going to draw to the right of the starting point "length" pixels and down "height" pixels
    """
    def __init__(self, screen, color, x, y, length, height):
        self.screen = screen
        self.colour = color
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        Button.draw_button(self)

    def draw_button(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.length, self.height))

"""------------------MAIN PROGRAM--------------------"""
#initialize some global variables
pygame.init()
map_tilesize=32
map_height=41
map_width=41
screen_offset=4*map_tilesize
resources=[('gold','Gold.png',4,100),('diamond','Diamond.png',5,200),('stone','Stone.png',2,40),('wood','Wood.png',1,20),('iron','Iron.png',3,50)]
#initialize display
size=(map_width*map_tilesize,map_height*map_tilesize)
screen=pygame.display.set_mode((size))




#create the groups to handle sprites more easy
robot_group=pygame.sprite.Group()
resource_group=pygame.sprite.Group()#group that will have all the resources in there BUT will not say where are they,
                                    # i have created a resource_information dictionary for this aspect of the game

#initialize robot and add it to it's group
robot=Robot("josh","rsz_player.png",200)
robot.set_grid(9,7)
robot_group.add(robot)

#put some resources on the map randomly given the list of resources.Each resurce has  name, image,toughness,value
resources_information={}#dictionary that will keep track of where are the resources
for resource in range(10):
    random_y_pos=random.randint(1,map_width)
    random_x_pos=random.randint(1,map_height)
    random_number_from_resources_list=resources[random.randint(0,len(resources)-1)]
    resources_information[(random_y_pos,random_x_pos)]=random_number_from_resources_list[0]
    someresource=Resource(random_number_from_resources_list[0],random_number_from_resources_list[1],random_number_from_resources_list[2],random_number_from_resources_list[3],mined=False)
    someresource.set_position_on_grid(random_y_pos,random_x_pos)
    resource_group.add(someresource)

print(resources_information)
#design the deposit area

#load map.tmx
map=pytmx.load_pygame("map2.tmx")

#iterate through all layers and draw them+make a 2D matrix for pathfinding algorithms to work on
matrix=np.zeros((map_height,map_width),dtype='i2,i1')#lines and rows
deposit_area=[]#create a separate list of lists with deposit tiles where each tile will have its x,y and if it is occupied
for layer in map.layers:
    for x,y, image in layer.tiles():
        screen.blit(image,(x*map_tilesize,y*map_tilesize))
        obj_prop=map.get_tile_properties(x,y,0)
        is_that_obj_walkable=obj_prop['walkable']
        try:
          if obj_prop['deposit_area']=='1':
            deposit_area.append((x,y,"free","none",0))#each element in this list is a tile in the map,
                                               # each element is defind by its coordinates,if the tile is free or not,name of the resoure which is there and its value
        except:
          KeyError

        if is_that_obj_walkable=='True':
            is_that_obj_walkable=1

        elif is_that_obj_walkable=='false':
            is_that_obj_walkable=0
        cost_of_that_obj=obj_prop['cost']
        matrix[y][x][0]=cost_of_that_obj
        matrix[y][x][1]=is_that_obj_walkable
print(deposit_area)
#draw resources and our robot.
robot_group.draw(screen)
resource_group.draw(screen)


clock=pygame.time.Clock()
pygame.display.update()
while True:

    clock.tick(60)
    #all events go in here
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.KEYDOWN:

            #handle collisions and movements(up,down,right,left)
            if event.key==pygame.K_LEFT and map.get_tile_properties(robot.get_grid()[0]-1,robot.get_grid()[1],0)['walkable']=='True' :
                bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                screen.blit(bck,robot.get_pos())
                robot.move("left")
                resource_group.draw(screen)
                robot_group.draw(screen)
                pygame.display.update(robot_group.sprites()+resource_group.sprites())



            if event.key==pygame.K_RIGHT and map.get_tile_properties(robot.get_grid()[0]+1,robot.get_grid()[1],0)['walkable']=='True' :
                bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                screen.blit(bck,robot.get_pos())
                robot.move("right")
                resource_group.draw(screen)
                robot_group.draw(screen)
                pygame.display.update(robot_group.sprites()+resource_group.sprites())


            if event.key==pygame.K_UP and map.get_tile_properties(robot.get_grid()[0],robot.get_grid()[1]-1,0)['walkable']=='True' :
                bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                screen.blit(bck,robot.get_pos())
                robot.move("up")
                resource_group.draw(screen)
                robot_group.draw(screen)
                pygame.display.update(robot_group.sprites()+resource_group.sprites())


            if event.key==pygame.K_DOWN and map.get_tile_properties(robot.get_grid()[0],robot.get_grid()[1]+1,0)['walkable']=='True':
                bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                screen.blit(bck,robot.get_pos())
                robot.move("bottom")
                resource_group.draw(screen)
                robot_group.draw(screen)
                pygame.display.update(robot_group.sprites()+resource_group.sprites())




            #handle collisions between rects
            if pygame.sprite.groupcollide(robot_group,resource_group,False,False,collided=None):
                     if event.key==pygame.K_SPACE:
                      try:
                        remove_resource_from_coordinates=(robot.rect.x//32,robot.rect.y//32)
                        robot.mine(resources_information[remove_resource_from_coordinates])
                        resources_information.pop(remove_resource_from_coordinates)
                        resource_group.remove(pygame.sprite.spritecollideany(robot,resource_group, collided = None))
                        print(robot.inventory.inventory)
                        for layer in map.layers:
                            for x,y, image in layer.tiles():
                                screen.blit(image,(x*map_tilesize,y*map_tilesize))
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())
                      except KeyError:
                          print("no object there")

            camera.update(robot)


        if event.type==pygame.MOUSEBUTTONDOWN:
                dest=(pygame.mouse.get_pos()[0]//32,pygame.mouse.get_pos()[1]//32)
                #print(reconstruct_path(breadth_first_search(matrix,(robot.rect.x//32,robot.rect.y//32),dest),(robot.rect.x//32,robot.rect.y//32),dest))
                #print(reconstruct_path(dijkstra_search(matrix,(robot.rect.x//32,robot.rect.y//32),dest)[0],(robot.rect.x//32,robot.rect.y//32),dest))
                print(reconstruct_path(A_star_search(matrix,(robot.rect.x//32,robot.rect.y//32),dest)[0],(robot.rect.x//32,robot.rect.y//32),dest))






pygame.quit()
quit()