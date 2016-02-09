import sys,pygame
import pytmx
import random
class Resource(pygame.sprite.Sprite):
    def __init__(self,name,image,weight,toughness,value,mined=False):
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.image_name=image
        self.image=pygame.image.load(self.image_name)
        self.rect=self.image.get_rect()
        self.toughness=toughness
        self.value=value
        self.mined=mined


    def set_position_on_grid(self,x_pos,y_pos):
        self.rect.x=x_pos*map_tilesize
        self.rect.y=y_pos*map_tilesize

    def update_status(self,did_robot_mine_resource=False):#flag method,to see if the resource was mined,did_robot_mine_resource should return a bool
        if did_robot_mine_resource==True:
            self.mined=True


class Robot(pygame.sprite.Sprite):
    def __init__(self,name,image,max_loadout):
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.image_name=image
        self.image=pygame.image.load(self.image_name)
        self.rect=self.image.get_rect()
        self.inventory = {}#still in development

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
    def inventory(self):
        pass
    def mine(self,resource):
        pass



"""------------------MAIN PROGRAM--------------------"""
#initialize some global variables
pygame.init()
map_tilesize=32
map_height=20
map_width=32

#initialize display
size=(map_width*map_tilesize,map_height*map_tilesize)
screen=pygame.display.set_mode(size)


#create the groups to handle sprites more easy
robot_group=pygame.sprite.Group()
resource_group=pygame.sprite.Group()

#initialize robot and add it to it's group
robot=Robot("josh","rsz_player.png",200)
robot.set_grid(8,7)
robot_group.add(robot)

#put some resources on the map randomly
someresource=Resource("gold","images.png",20,3,100,mined=False)
someresource.set_position_on_grid(random.randint(1,map_width),random.randint(1,map_height))
resource_group.add(someresource)

#load map.tmx
map=pytmx.load_pygame("map2.tmx")

#iterate through all layers and draw them
for layer in map.layers:
     for x,y, image in layer.tiles():
        screen.blit(image,(x*map_tilesize,y*map_tilesize))
robot_group.draw(screen)
resource_group.draw(screen)

groups_to_be_updated=pygame.sprite.Group
for sprite in resource_group,robot_group:
    groups_to_be_updated.add(sprite)



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
            if pygame.sprite.spritecollideany(robot,resource_group,collided=None):
                pass


   # pygame.display.flip()



pygame.quit()
quit()