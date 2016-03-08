import pygame

pygame.init()
from pygame.locals import *


class Button:
    """
    x and y coordinates set the point on the screen from wich pygame starts drawing our button
    it is going to draw to the right of the starting point "length" pixels and down "height" pixels
    """

    def __init__(self, screen, color, x, y, length, height, mytext):
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


if __name__ == "__main__":
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Button")
    x = 200
    y = 250
    length = 200
    height = 100
    mytext = "Hello..."
    screen.fill((255, 255, 255))
    pygame.display.flip()
    Button(screen, color=(200, 200, 200), x=x, y=y, length=length, height=height, mytext=mytext)
    Run = True
    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Run = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if mouse[0] > x:
                    if mouse[0] < (x + length):
                        if mouse[1] > y:
                            if mouse[1] < (y + height):

                                Button(screen, color=(240, 240, 240), x=x, y=y, length=length, height=height,mytext=mytext)

                                while True:
                                    print("...its me")

                                """
                                To make the button clickable unlimited times change the code in the if-statement with this one:
                                Button(screen, color=(240, 240, 240), x=x, y=y, length=length, height=height,mytext=mytext)
                                pygame.time.delay(100)
                                Button(screen, color=(200, 200, 200), x=x, y=y, length=length, height=height,mytext=mytext)
                                print("Code to do stuff...")
                                """

                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

"""
colors:
pressed button - line 68
button border - line 34
button - line 35, it is written in line 53 where we call the class, changed in line 68 to show button is clicked.
text - line 39
screen - 51

Button action:
Type the code that tells the button what to do in line 71. It is an infinite loop now but you can always remove the loop
and give the button a single action to perform. Further info is in a docstring in the if-statement

Text can be changed on line 50
Font and size are on line 20

Shadow:
variable col = 255 must NOT have a value less than 250 and more than 255!

Dimensions:
x, y coordinates can be changed on lines 46, 47
button length and height are right after that on line 48, 49
"""