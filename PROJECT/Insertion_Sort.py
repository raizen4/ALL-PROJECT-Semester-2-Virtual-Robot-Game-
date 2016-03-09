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
