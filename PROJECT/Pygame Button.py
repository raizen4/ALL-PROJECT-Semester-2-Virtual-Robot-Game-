import pygame

pygame.init()
from pygame.locals import *
global code
code=None

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
      global code
      if event.type == MOUSEBUTTONDOWN:
        pygame.init()
        for button in list_of_buttons:
            mouse=list(pygame.mouse.get_pos())
            # mouse[0]//=32
            # mouse[1]//=32
            # mouse=tuple(mouse)
            if mouse[0] > button.x:
                if mouse[0] < (button.x+button.length):
                    if mouse[1] > button.y:
                        if mouse[1] < (button.y+button.height):
                            print(button)
                            button.color=[100,100,100]
                            button.draw_button()
                            button.text(button.mytext)
                            print(button.color)
                            code=button.code
                            dissable=button.action
                            for button in list_of_buttons:
                                if button.action==dissable and button.code!=code:
                                    button.color=[200,200,20]
                                    button.draw_button()
                                    button.text(button.mytext)







screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Button")
screen.fill((255, 255, 255))
pygame.display.flip()
list_of_buttons=[]
buton1=Button(screen,[200, 200, 200], 200, 250, 100, 100, 'hello','search',1)
list_of_buttons.append(buton1)
buton2=Button(screen,[200,200,200],100,150,100,100,"bye",'search',2)
list_of_buttons.append(buton2)

Run = True
while Run:
        global code
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                Run = False
            Button.which_button_is_pressed(list_of_buttons)
            print(code)
            print(buton1.color)
            print(buton2.color)
