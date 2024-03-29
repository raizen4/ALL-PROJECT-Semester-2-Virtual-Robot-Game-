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
__author__ = "Bogdan Nicolae Boldur"



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
    _total_worth_of_the_inv=0
    def __init__(self):
        self.inventory=[]#it should look like [[name,photo,toughness,value,initial_quantity] for each element]
        resources_list=[['gold','Gold.png',4,100,0],['diamond','Diamond.png',5,200,0],['stone','Stone.png',2,40,0],['wood','Wood.png',1,20,0],['iron','Iron.png',3,50,0]]
        for value in resources_list:
            self.inventory.append(value)

    def update_with_item(self,item,quantity):
        for value in self.inventory:
            if value[0]==item:
                 if value[4]+quantity<0:
                    value[4]=0
                 else:
                   value[4]+=quantity


    def sell_everything(self):
        global money
        total=0
        for value in self.inventory:
            total+=value[3]*value[4]
            value[4]=0
        money+=total

     #draws inventory on the desireed screen
    def draw_inventory(self,surface):
         surface.fill((0,0,0))#fills the screen with black so a new draw method can be called with the updated quantity

         inventoryFont = pygame.font.Font(None, 20)
         inventory_font_for_total_worth=pygame.font.Font(None,28)
         x_coord=0#column
         y_coord=20#row
         Inventory._total_worth_of_the_inv=0
         for value in self.inventory:
            print(value)
            Inventory._total_worth_of_the_inv+=value[3]*value[4]
            reso_image=pygame.image.load(value[1])
            surface.blit(reso_image,(x_coord,y_coord))
            Text=inventoryFont.render("("+value[0]+")"+"->"+str(value[4]),True,(255,255,0))
            surface.blit(Text,(x_coord+34,y_coord+13))
            x_coord+=150
         print('-'*20)
         x_coord-=50
         someText=inventory_font_for_total_worth.render("Worth of the inventory:"+str(Inventory._total_worth_of_the_inv),True,(255,255,0))
         surface.blit(someText,(x_coord+34,y_coord+13))
    def get_items(self):
        return self.inventory

    def sort_inventory(self,surface):
      global code_sort
      if code_sort==4:
         for i in range(0,len(self.inventory)-1):
          for j in range(i+1,len(self.inventory)):
              if self.inventory[i][4]>self.inventory[j][4]:
                  self.inventory[i],self.inventory[j]=self.inventory[j],self.inventory[i]
         robot.inventory_of_robot.draw_inventory(surface)
         screen.blit(surface,((map_width,map_height*map_tilesize-10*map_tilesize)))
      else:
          print("No other found")




    def is_empty(self):
      for value in self.inventory:
          if value[4]!=0:
              print(value)
              return False
      return True
    def total_worth_of_the_inv(self):
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




class Button:
    """
    x and y coordinates set the point on the screen from wich pygame starts drawing our button
    it is going to draw to the right of the starting point "length" pixels and down "height" pixels
    """

    def __init__(self, screen, color, x, y, length, height, mytext,action,code):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.font = pygame.font.SysFont("Arial", 25)
        self.mytext = mytext
        self.gettext = self.font.render(self.mytext, 1, (0, 0, 0))
        self.textwidth = self.gettext.get_width()
        self.textheight = self.gettext.get_height()
        self.action=action
        self.code=code
        Button.draw_button(self)
        Button.text(self, mytext)

    def draw_button(self):
        col = 255
        for i in range(1, 6):  # loop to create a shadow under the button
            col = col - 50
            pygame.draw.rect(self.screen, (col, col, col),((self.x + (6 - i)), (self.y + (6 - i)), self.length, self.height))

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.length, self.height))  # border
        pygame.draw.rect(self.screen, self.color,(self.x + 1, self.y + 1, self.length - 2, self.height - 2))  # button inside
        pygame.display.flip()

    def text(self, mytext):
        self.screen.blit(self.font.render(self.mytext, True, (0, 0, 0)), (((self.x + (self.length / 2)) - (self.textwidth / 2)), ((self.y + (self.height / 2)) - (self.textheight / 2))))
        pygame.display.update()

    def which_button_is_pressed(list_of_buttons):
      global code_search
      global code_sort
      if event.type == MOUSEBUTTONDOWN:
        pygame.init()
        for button in list_of_buttons:
            mouse=list(pygame.mouse.get_pos())
            mouse=tuple(mouse)
            if mouse[0] > button.x:
                if mouse[0] < (button.x+button.length):
                    if mouse[1] > button.y:
                        if mouse[1] < (button.y+button.height):
                            print(button.mytext)
                            #button.color=[100,100,100]
                            #button.draw_button()
                            #button.text(button.mytext)
                            dissable=button.action
                            if dissable=='search':
                                button.color=[100,100,100]
                                button.draw_button()
                                button.text(button.mytext)
                                code_search=button.code
                                for button in list_of_buttons:
                                 if button.action==dissable and button.code!=code_search:
                                    button.color=[190,190,0]
                                    button.draw_button()
                                    button.text(button.mytext)
                                 print(code_search)
                            elif dissable=='sort':
                                button.color=[100,100,100]
                                button.draw_button()
                                button.text(button.mytext)
                                code_sort=button.code
                                for button in list_of_buttons:
                                 if button.action==dissable and button.code!=code_sort:
                                    button.color=[190,190,0]
                                    button.draw_button()
                                    button.text(button.mytext)
                                print(code_sort)


class Robot(pygame.sprite.Sprite,Inventory):
    def __init__(self,name,image,max_loadout):
        pygame.sprite.Sprite.__init__(self)
        Inventory.__init__(self)
        self.name=name
        self.image_name=image
        self.image=pygame.image.load(self.image_name)
        self.rect=self.image.get_rect()
        self.inventory_of_robot =Inventory()#still in development
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
        global score
        for progress in range(180):
                        time.sleep(0.01)
                        progress_bar=pygame.draw.rect(screen, (255,255,255), pygame.Rect(robot.rect.x-7,robot.rect.y-7,0.25*progress,5))#rect(x,y,lungimea barii,grosimea barii)
                        pygame.display.update(progress_bar)

        score+=1
        self.inventory_of_robot.update_with_item(resources_information[remove_resource_from_coordinates],1)

    def advance_level(self):
        self.level+=1
    def deposit(self,item,coordinates_of_place_to_be_deposited):
        re_add_resource_to_the_map=Resource(item,resources[item][0],resources[item][1],resources[item][2])
        re_add_resource_to_the_map.set_position_on_grid(robot.rect.x//32,robot.rect.y//32)
        resource_group.add(re_add_resource_to_the_map)
        resources_information[(coordinates_of_place_to_be_deposited)]=item
        self.inventory_of_robot.update_with_item(item,-1)


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
            if (nexts not in came_from) and (matrix_with_costs_and_walls[nexts[0]][nexts[1]][1]==1):
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
            if matrix_of_costs_and_walls[nexts[0]][nexts[1]][0]>2000:
                 pass
            else:
                print(cost_so_far)
                new_cost=cost_so_far[current]+matrix_of_costs_and_walls[nexts[0]][nexts[1]][0]#accesing the cost for the neighbor

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

            new_cost=cost_so_far[current]+ matrix_of_walls_and_costs[nexts[0]][nexts[1]][0]
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
    intial_pos=list(path[0])
    modified_pos=[0,0]
    for id in path:
       print(matrix[id[0]][id[1]][4])
       if modified_pos==[0,0] and matrix[id[0]][id[1]][2]==0:
             bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)

       elif modified_pos==[0,0] and matrix[id[0]][id[1]][2]!=0:
             pygame.init()
             mouse=[pygame.mouse.get_pos()[0]//32,pygame.mouse.get_pos()[1]//32]
             print(mouse)
             if intial_pos[0]<mouse[0]:
                 bck=pygame.image.load('right.jpg')
                 matrix[id[0]][id[1]][4]='right'
                 matrix[id[0]][id[1]][3]='True'
                 matrix[id[0]][id[1]][2]=0

             elif intial_pos[0]>mouse[0]:
                 bck=pygame.image.load("left.jpg")
                 matrix[id[0]][id[1]][4]='left'
                 matrix[id[0]][id[1]][3]='True'
                 matrix[id[0]][id[1]][2]=0

             elif intial_pos[1]<mouse[1]:
                 bck=pygame.image.load("down.jpg")
                 matrix[id[0]][id[1]][4]='down'
                 matrix[id[0]][id[1]][3]='True'
                 matrix[id[0]][id[1]][2]=0

             elif intial_pos[1]>mouse[1]:
                 bck=pygame.image.load('up.jpg')
                 matrix[id[0]][id[1]][4]='up'
                 matrix[id[0]][id[1]][3]='True'
                 matrix[id[0]][id[1]][2]=0
       else:
        if matrix[id[0]][id[1]][4].decode("UTF-8")!='None' and matrix[id[0]][id[1]][2]==0 :
             bck=pygame.image.load(matrix[id[0]][id[1]][4].decode('UTF-8')+"."+'jpg')

        elif matrix[id[0]][id[1]][3].decode('UTF-8')=='False' and matrix[id[0]][id[1]][2]==0 and matrix[id[0]][id[1]][4].decode("UTF-8")=='None' :
             bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
        else:
         if id[0]==modified_pos[0]+1 and matrix[id[0]][id[1]][2]==1:
             bck=pygame.image.load('right.jpg')
             matrix[id[0]][id[1]][4]='right'
             matrix[id[0]][id[1]][3]='True'
             matrix[id[0]][id[1]][2]=0



         elif id[0]==modified_pos[0]-1 and matrix[id[0]][id[1]][2]==1:
             bck=pygame.image.load("left.jpg")
             matrix[id[0]][id[1]][4]='left'
             matrix[id[0]][id[1]][3]='True'
             matrix[id[0]][id[1]][2]=0

         elif id[1]==modified_pos[1]-1 and  matrix[id[0]][id[1]][2]==1:
             bck=pygame.image.load('up.jpg')
             matrix[id[0]][id[1]][4]='up'
             matrix[id[0]][id[1]][3]='True'
             matrix[id[0]][id[1]][2]=0


         elif id[1]==modified_pos[1]+1 and  matrix[id[0]][id[1]][2]==1:
             bck=pygame.image.load("down.jpg")
             matrix[id[0]][id[1]][4]='down'
             matrix[id[0]][id[1]][3]='True'
             matrix[id[0]][id[1]][2]=0

       screen.blit(bck,robot.get_pos())
       robot.set_grid(id[0],id[1])
       resource_group.draw(screen)
       robot_group.draw(screen)
       pygame.display.update(robot_group.sprites()+resource_group.sprites())
       time.sleep(0.3)
       if list(id)!=intial_pos:
            modified_pos=list(id)

    return path

"--------------------Functions to draw UI on the screen-------------------"
def draw_tabs():
    surface_for_score_and_money_time.fill((0,0,0))
    score_tab=font_for_score_money_time.render("Score: "+str(score),False,(190,190,0))
    money_tab=font_for_score_money_time.render("Money: "+str(money),False,(190,190,0))
    time_tab=font_for_score_money_time.render("Time: "+str(time_until_end),False,(190,190,0))
    surface_for_score_and_money_time.blit(time_tab,(0,0))
    surface_for_score_and_money_time.blit(score_tab,(0,70))
    surface_for_score_and_money_time.blit(money_tab,(0,140))
    screen.blit(surface_for_score_and_money_time,(1120,1120))
    pygame.display.update()

def update_level():
    surface_to_show_information.fill((0,0,0))
    level=font_for_level.render("Level"+" "+str(robot.level),False,(190,190,0))
    name_of_robot=font_for_screen.render("Name:"+str(robot.name),False,(190,190,0))
    surface_to_show_information.blit(level,(0,20))
    surface_to_show_information.blit(name_of_robot,(0,60))
    screen.blit(surface_to_show_information,(1115,1000))#column,row
    pygame.display.update()
def draw_options_for_buttons():
    option_search=font_for_screen.render("Choose search algorithm",False,(190,190,0))
    option_sort=font_for_screen.render("Choose sort algorithm",False,(190,190,0))
    screen.blit(option_search,(0,1150))
    screen.blit(option_sort,(400,1150))
    buton_a=Button(screen,[255,255,0],20,1200,150,100,"A*",'search',1)
    list_of_buttons.append(buton_a)
    buton_dijkstra=Button(screen,[255,255,0],180,1200,150,100,"Dijkstra's",'search',2)
    list_of_buttons.append(buton_dijkstra)
    buton_quicksort=Button(screen,[255,255,0],380,1200,150,100,"Quicksort",'sort',3)
    list_of_buttons.append(buton_quicksort)
    buton_selection_sort=Button(screen,[255,255,0],550,1200,160,100,"selection_sort",'sort',4)
    list_of_buttons.append(buton_selection_sort)

"""------------------MAIN PROGRAM--------------------"""
#initialize some global variables
time_until_end=180

global code_search,code_sort
code_search=0
code_sort=0
global score
score=0
global money
money=0
pygame.init()
map_tilesize=32
map_height=41
map_width=41
global resources
resources={'gold':['Gold.png',4,100],'diamond':['Diamond.png',5,200],'stone':['Stone.png',2,40],'wood':['Wood.png',1,20],'iron':['Iron.png',3,50]}
description_resources={'gold':"Highly valuable,get this and you get rich,its value  is "+str(resources['gold'][2]),'diamond':'the most valuable resource,its value is '+str(resources['diamond'][2]),'stone':'well, better than nothing,its value is '+str(resources['stone'][2]),
                       'wood':'the cheapest resource,its value is '+str(resources['wood'][2]),'iron':" moderate value,MINE IT,its value is "+str(resources['iron'][2])}
dict_of_arrows={"up":'up.jpg','left':'left.jpg','right':'right.jpg','down':'down.jpg'}
dict_of_buffs=[]
list_of_buttons=[]
#initialize display + any other surfaces
size=(map_width*map_tilesize,map_height*map_tilesize)
screen=pygame.display.set_mode((size))
surface_for_inv=pygame.Surface((map_width*map_tilesize-250, 100))#width,height
surface_for_inv.fill((0,0,0))
surface_to_show_information=pygame.Surface((150,90))
surface_to_show_information.fill((150,0,0))
surface_for_showing_description_of_resources=pygame.Surface((150,150))
surface_for_showing_description_of_resources.fill((153,32,221))
surface_for_score_and_money_time=pygame.Surface((190,180))
surface_for_score_and_money_time.fill((155,155,9))
surface_for_description_item=pygame.Surface((1000,30))
surface_for_description_item.fill((0,0,0))
font_for_screen=pygame.font.Font(None,35)
font_for_level=pygame.font.Font(None,50)
font_for_score_money_time=pygame.font.Font(None,40)







#create the groups to handle sprites more easy
robot_group=pygame.sprite.Group()
resource_group=pygame.sprite.Group()#group that will have all the resources in there BUT will not say where are they,
                                    # i have created a resource_information dictionary for this aspect of the game

#load map.tmx
map=pytmx.load_pygame("map2.tmx")

#initialize robot and add it to it's group
robot=Robot("josh","rsz_player.png",100)
robot.set_grid(9,7)
robot_group.add(robot)
#put some resources on the map randomly given the list of resources.Each resurce has  name, image,toughness,value
resources_information={}#dictionary that will keep track of where are the resources
keys=list(resources.keys())#make a list with keys from our resources dictionary
for resource in range(10):
    random_y_pos=random.randint(1,map_width)
    random_x_pos=random.randint(1,map_height-10)
    random_key_from_resources_dict=random.choice(keys)
    resources_information[(random_y_pos,random_x_pos)]=random_key_from_resources_dict
    someresource=Resource(random_key_from_resources_dict,resources[random_key_from_resources_dict][0],resources[random_key_from_resources_dict][1],resources[random_key_from_resources_dict][2],mined=False)
    someresource.set_position_on_grid(random_y_pos,random_x_pos)
    resource_group.add(someresource)

print(resources_information)
print(robot.inventory_of_robot.is_empty())

#iterate through all layers and draw them+make a 2D matrix for pathfinding algorithms to work on
matrix=np.zeros((map_height,map_width),dtype='i2,i1,i1,S5,S5')#lines and rows,last one is if the tile has changed over time so the arrows will be represented as they should
deposit_area={}#create a separate list of lists with deposit tiles where each tile will have its x,y and if it is occupied
for layer in map.layers:
    for x,y, image in layer.tiles():
        screen.blit(image,(x*map_tilesize,y*map_tilesize))
        obj_prop=map.get_tile_properties(x,y,0)
        is_that_obj_walkable=obj_prop['walkable']
        is_that_obj_water=obj_prop['water']
        try:
          if obj_prop['deposit_area']=='1':
            deposit_area[(x,y)]=['free','none',0]#each key in this dict represents a tile on the map which is part of the deposit area
                                               # each element is defind by its coordinates(key),if the tile is free or not,name of the resoure which is there and its value
        except:
          KeyError

        if is_that_obj_walkable=='True':
            is_that_obj_walkable=1

        elif is_that_obj_walkable=='false':
            is_that_obj_walkable=0
        cost_of_that_obj=obj_prop['cost']
        matrix[x][y][0]=cost_of_that_obj
        matrix[x][y][1]=is_that_obj_walkable
        matrix[x][y][2]=is_that_obj_water
        matrix[x][y][3]='False'
        matrix[x][y][4]=None
print(deposit_area)
#print(robot.inventory_of_robot.sort_inventory())
#draw resources and our robot.
robot_group.draw(screen)
resource_group.draw(screen)


"-----------------------DRAWING ALL THE INFO ON THE SCREEN ON THE DEISRED SURFACES----------------------------------"


"""drawing info on desired surfaces"""
#draw_inventory
robot.inventory_of_robot.draw_inventory(surface_for_inv)#draw the inventory on the surface
screen.blit(surface_for_inv,((map_width,map_height*map_tilesize-10*map_tilesize)))#blit the surface on the screen (first put all items/buttons etc. , on the surface,then blit the surface !!!!!)
screen.blit(surface_to_show_information,(map_width-25*map_tilesize,map_height-2*map_tilesize))
#details about the player
update_level()
draw_tabs()
#draw options for buttons
draw_options_for_buttons()



"""drawing the basic delimiters for ui"""
delimiter_for_interface=font_for_screen.render("-"*1200,True,(255,250,0))
screen.blit(delimiter_for_interface,(0,1090))
screen.blit(delimiter_for_interface,(0,1130))
delimiter_for_interface2=font_for_screen.render(('||'),False,(255,250,0))
for i  in range(300):
    screen.blit(delimiter_for_interface2,(1100,1000+i))
    screen.blit(delimiter_for_interface2,(350,1150+i))




clock=pygame.time.Clock()
pygame.display.update()
while True:

    mouse =list(pygame.mouse.get_pos())
    mouse[0]//=32
    mouse[1]//=32
    mouse=tuple(mouse)

    clock.tick(60)
    draw_tabs()
    update_level()
    #all events go in here
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()


        Button.which_button_is_pressed(list_of_buttons)

        if mouse in resources_information.keys():
            info_to_display=resources_information[(mouse[0],mouse[1])]
            display_description=font_for_screen.render("Description:   "+info_to_display+":"+description_resources[info_to_display],False,(255,255,9))
            surface_for_description_item.blit(display_description,(0,0))
            screen.blit(surface_for_description_item,(0,1110))
            surface_for_description_item.fill((0,0,0))
        else:
             display_description=font_for_screen.render("Description: NONE",False,(255,255,9))
             surface_for_description_item.blit(display_description,(0,0))
             screen.blit(surface_for_description_item,(0,1110))
             surface_for_description_item.fill((0,0,0))



        if event.type==pygame.KEYDOWN:
            #handle collisions and movements(up,down,right,left)
            if event.key==pygame.K_LEFT and map.get_tile_properties(robot.get_grid()[0]-1,robot.get_grid()[1],0)['walkable']=='True' and (matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][4].decode('UTF-8')=="left" or matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][4].decode('UTF-8')=='None'):

                if matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][2]==0  :

                    if  matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][3].decode('UTF-8')=='False' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False' or ( matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False'):
                        bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                        screen.blit(bck,robot.get_pos())
                        robot.move("left")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())

                    elif (matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][3].decode('UTF-8')=='False' and matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True'):
                        bck=pygame.image.load("left.jpg")
                        screen.blit(bck,robot.get_pos())
                        robot.move("left")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())
                    elif  matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True' :
                        bck=pygame.image.load(matrix[robot.get_grid()[0]][robot.get_grid()[1]][4].decode('UTF-8')+"."+'jpg')
                        screen.blit(bck,robot.get_pos())
                        robot.move("left")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())

                elif matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][2]==1:

                     if matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][3].decode('UTF-8')=='False':
                        bck=pygame.image.load("left.jpg")
                        screen.blit(bck,((robot.get_grid()[0]-1)*32 , robot.get_grid()[1]*32))
                        matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][2]=0
                        matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][3]="True"
                        matrix[robot.get_grid()[0]-1][robot.get_grid()[1]][4]="left"



            if event.key==pygame.K_RIGHT and map.get_tile_properties(robot.get_grid()[0]+1,robot.get_grid()[1],0)['walkable']=='True' and (matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][4].decode('UTF-8')=="right" or matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][4].decode('UTF-8')=='None') :

                 if matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][2]==0  :

                    if  matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][3].decode('UTF-8')=='False' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False' or ( matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False'):
                        bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                        screen.blit(bck,robot.get_pos())
                        robot.move("right")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())

                    elif  (matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][3].decode('UTF-8')=='False' and matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True'):
                        bck=pygame.image.load("right.jpg")
                        screen.blit(bck,robot.get_pos())
                        robot.move("right")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())
                    elif  matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True' :
                        bck=pygame.image.load(matrix[robot.get_grid()[0]][robot.get_grid()[1]][4].decode('UTF-8')+"."+'jpg')
                        screen.blit(bck,robot.get_pos())
                        robot.move("right")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())

                 elif matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][2]==1:

                     if matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][3].decode('UTF-8')=='False':
                        bck=pygame.image.load("right.jpg")
                        screen.blit(bck,((robot.get_grid()[0]+1)*32 , robot.get_grid()[1]*32))
                        matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][2]=0
                        matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][3]="True"
                        matrix[robot.get_grid()[0]+1][robot.get_grid()[1]][4]="right"





            if event.key==pygame.K_UP and map.get_tile_properties(robot.get_grid()[0],robot.get_grid()[1]-1,0)['walkable']=='True' and (matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][4].decode('UTF-8')=="up" or matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][4].decode('UTF-8')=='None'):
              if matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][2]==0  :

                    if  matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][3].decode('UTF-8')=='False' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False' or ( matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False'):
                        bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                        screen.blit(bck,robot.get_pos())
                        robot.move("up")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())
                    elif (matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][3].decode('UTF-8')=='False' and matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True'):
                        bck=pygame.image.load("up.jpg")
                        screen.blit(bck,robot.get_pos())
                        robot.move("up")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())


                    elif   matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True' :
                        bck=pygame.image.load(matrix[robot.get_grid()[0]][robot.get_grid()[1]][4].decode('UTF-8')+"."+'jpg')
                        screen.blit(bck,robot.get_pos())
                        robot.move("up")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())

              elif matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][2]==1:

                     if matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][3].decode('UTF-8')=='False':
                        bck=pygame.image.load("up.jpg")
                        screen.blit(bck,((robot.get_grid()[0])*32 , (robot.get_grid()[1]-1)*32))
                        matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][2]=0
                        matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][3]="True"
                        matrix[robot.get_grid()[0]][robot.get_grid()[1]-1][4]="up"


            if event.key==pygame.K_DOWN and map.get_tile_properties(robot.get_grid()[0],robot.get_grid()[1]+1,0)['walkable']=='True' and (matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][4].decode('UTF-8')=="down" or matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][4].decode('UTF-8')=='None'):
                if matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][2]==0  :

                    if  matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][3].decode('UTF-8')=='False' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False' or ( matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='False'):
                        bck=map.get_tile_image(robot.get_grid()[0],robot.get_grid()[1],0)
                        screen.blit(bck,robot.get_pos())
                        robot.move("bottom")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())
                    elif (matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][3].decode('UTF-8')=='False' and matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True'):
                        bck=pygame.image.load("down.jpg")
                        screen.blit(bck,robot.get_pos())
                        robot.move("bottom")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())
                    elif   matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][3].decode('UTF-8')=='True' and  matrix[robot.get_grid()[0]][robot.get_grid()[1]][3].decode('UTF-8')=='True' :
                        bck=pygame.image.load(matrix[robot.get_grid()[0]][robot.get_grid()[1]][4].decode('UTF-8')+"."+'jpg')
                        screen.blit(bck,robot.get_pos())
                        robot.move("bottom")
                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())

                elif matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][2]==1:

                     if matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][3].decode('UTF-8')=='False':
                        bck=pygame.image.load("down.jpg")
                        screen.blit(bck,((robot.get_grid()[0])*32 , (robot.get_grid()[1]+1)*32))
                        matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][2]=0
                        matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][3]="True"
                        matrix[robot.get_grid()[0]][robot.get_grid()[1]+1][4]="down"



            #handle collisions between rects
            if pygame.sprite.spritecollideany(robot,resource_group, collided = None):
                     if event.key==pygame.K_SPACE:
                        remove_resource_from_coordinates=(robot.rect.x//32,robot.rect.y//32)

                        robot.mine(resources_information[remove_resource_from_coordinates])
                        robot.inventory_of_robot.draw_inventory(surface_for_inv)
                        screen.blit(surface_for_inv,((map_width,map_height*map_tilesize-10*map_tilesize)))

                        resources_information.pop(remove_resource_from_coordinates)
                        resource_group.remove(pygame.sprite.spritecollideany(robot,resource_group, collided = None))
                        for layer in map.layers:
                            for x,y, image in layer.tiles():
                                if matrix[x][y][4].decode("UTF-8")=='None':
                                 screen.blit(image,(x*map_tilesize,y*map_tilesize))
                                else:
                                 bck=pygame.image.load(matrix[x][y][4].decode('UTF-8')+"."+'jpg')
                                 screen.blit(bck,(x*map_tilesize,y*map_tilesize))

                        resource_group.draw(screen)
                        robot_group.draw(screen)
                        pygame.display.update(robot_group.sprites()+resource_group.sprites())



            if event.key==pygame.K_d:
                obj_prop=map.get_tile_properties(robot.rect.x//32,robot.rect.y//32,0)
                #deposit the resources
                if robot.inventory_of_robot.is_empty()==True:
                    print("nothing to deposit,inventory empty")
                elif  robot.inventory_of_robot.is_empty()==False and obj_prop['deposit_area']=='1' and deposit_area[(robot.rect.x//32,robot.rect.y//32)][0]=='free':
                   for value in robot.inventory_of_robot.inventory:
                       if value[4]>0:
                           #value_of_random_resource_to_deposit=robot.inventory_of_robot.inventory[key][0]
                           random_resource_to_deposit=value[0]

                   robot.deposit(random_resource_to_deposit,(robot.rect.x//32,robot.rect.y//32))
                    #the pair from below update the inventory and draws in correctly on the screen
                   robot.inventory_of_robot.draw_inventory(surface_for_inv)
                   screen.blit(surface_for_inv,((map_width,map_height*map_tilesize-10*map_tilesize)))

                   deposit_area[(robot.rect.x//32,robot.rect.y//32)][0]='occupied'
                   deposit_area[(robot.rect.x//32,robot.rect.y//32)][1]=random_resource_to_deposit
                   deposit_area[(robot.rect.x//32,robot.rect.y//32)][2]=resources[random_resource_to_deposit][2]
                   resource_group.draw(screen)
                   robot_group.draw(screen)
                   pygame.display.update(robot_group.sprites()+resource_group.sprites())
                elif robot.inventory_of_robot.is_empty()==False and obj_prop['deposit_area']=='1' and deposit_area[(robot.rect.x//32,robot.rect.y//32)][0]!='free':
                    print("this is an occupied tile")
                elif robot.inventory_of_robot.is_empty()==False and obj_prop['deposit_area']!='1':
                    print("this is not a deposit area,you can't deposit here the items")


            if event.key==pygame.K_s:

                robot.inventory_of_robot.sort_inventory(surface_for_inv)
                pygame.display.update()

            if event.key==pygame.K_a:
                robot.inventory_of_robot.sell_everything()


                robot.inventory_of_robot.sort_inventory(surface_for_inv)
                pygame.display.update()



        if event.type==pygame.MOUSEBUTTONDOWN:
            global code_search
            dest=(pygame.mouse.get_pos()[0]//32,pygame.mouse.get_pos()[1]//32)
            if dest[0]<0 or dest[0]>41 or dest[1]>31 or dest[1]<0:
                print("you can t go there")
            else:

                if code_search==1:
                    print("A* in action")
                    print(reconstruct_path(A_star_search(matrix,(robot.rect.x//32,robot.rect.y//32),dest)[0],(robot.rect.x//32,robot.rect.y//32),dest))

                elif code_search==2:
                    print("DIJKSTRA IN ACTION")
                    print(reconstruct_path(dijkstra_search(matrix,(robot.rect.x//32,robot.rect.y//32),dest)[0],(robot.rect.x//32,robot.rect.y//32),dest))









pygame.quit()
quit()