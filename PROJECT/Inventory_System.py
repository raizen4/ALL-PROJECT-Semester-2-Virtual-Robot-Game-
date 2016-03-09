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
        """ Tallies up the total value of everything in the inventory clears it then returns the "total" of that """
        total = 0
        for item in self.inventory:
              total = total + item[3] * item[4] #value times qaunity

        is_empty(self)
        return total
     #draws inventory on the desireed screen
    def draw_inventory(self,surface):
         surface.fill((0,0,0))#fills the screen with black so a new draw method can be called with the updated quantity

         inventoryFont = pygame.font.Font(None, 20)
         x_coord=0#column
         y_coord=0#row
         for value in self.inventory:
            print(value)
            reso_image=pygame.image.load(value[1])
            surface.blit(reso_image,(x_coord,y_coord))
            someText=inventoryFont.render("("+value[0]+")"+"->"+str(value[4]),True,(255,255,0))
            surface.blit(someText,(x_coord+34,y_coord+13))
            x_coord+=150
         print('-'*20)
         someText=inventoryFont.render("Total worth of the deposit:"+str(Inventory._total_worth_of_the_inv),True,(255,255,0))
         surface.blit(someText,(x_coord+34,y_coord+13))
    def get_items(self):
        return self.inventory

    def sort_inventory(self,surface):

        for n in range(1,len(self.inventory)):
             pos = n #Current position in the list
             insert = self.inventory[n] # Item to be inserted

             while pos > 0 and self.inventory[pos-1] [4] > insert[4]:
                self.inventory[pos] = self.inventory[pos-1]
                pos = pos -1

             self.inventory[pos] = insert
             print (self.inventory)
             robot.inventory_of_robot.draw_inventory(surface)
             screen.blit(surface,((map_width,map_height*map_tilesize-10*map_tilesize)))





    def is_empty(self):
      for value in self.inventory:
          if value[4]!=0:
              print(value)
              return False
      return True
    def total_worth_of_the_inv(self):
        for item in self.inventory:
            self._total_worth_of_the_inv = item + item[3] * item[4]
