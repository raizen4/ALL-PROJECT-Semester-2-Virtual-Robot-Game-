"""
224 scene
"""
import pygame

pygame.init()
from pygame.locals import *

class Buttons:

    def __init__(self, screen, color, x, y, length, height, text):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.font = pygame.font.SysFont("Arial", 25)
        self.text = text
        self.gettext = self.font.render(self.text, 1, (0, 0, 0))
        self.textW = self.gettext.get_width()
        self.textH = self.gettext.get_height()
        Buttons.draw_button(self)
        # might need to initialize button and text methods here


    def draw_button(self):

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.length, self.height))  # border
        pygame.draw.rect(self.screen, self.color,(self.x + 1, self.y + 1, self.length - 2, self.height - 2))  # button inside

        self.screen.blit(self.font.render(self.text, True, (0, 0, 0)), (((self.x + (self.length / 2)) - (self.textW / 2)), ((self.y + (self.height / 2)) - (self.textH / 2))))
        pygame.display.update()

class Scene:
    def __init__(self, screen, color, text):
        self.screen = screen
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30)
        self.gettext = self.font.render(self.text, 1, (0, 0, 0))
        self.textW = self.gettext.get_width()
        self.textH = self.gettext.get_height()

        Scene.draw_scene(self)

    def draw_scene(self):
        scenebg = pygame.image.load("scenebg.png")
        self.screen.blit(scenebg, (208, 208))
        #pygame.draw.rect(self.screen, self.color, (208, 208, 224, 224))
        self.screen.blit(self.font.render(self.text, True, (255, 240, 245)), ((320-(self.textW//2)), 230))
        pygame.display.update()

class NameInput:
    def __init__(self, screen, text):
        self.screen = screen
        self.text = text
        self.font = pygame.font.SysFont("Arial", 25)
        NameInput.draw_text(self)

    def draw_text(self):
        self.screen.blit(self.font.render(self.text, True, (0, 0, 0)), (249, 270))
        pygame.display.update()

class TextBox:
    def __init__(self, screen):
        self.screen = screen
        TextBox.draw_text_box(self)

    def draw_text_box(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (245, 270, 150, 30))
        pygame.draw.rect(self.screen, (250, 250, 250), (247, 272, 146, 26))
        pygame.display.update()

def StartMenu(screen):
    x = 260
    y1 = 270
    y2 = 310
    y3 = 350
    length = 120
    height = 30

    Scene(screen, color=(138, 43, 226), text="Start Menu")
    Buttons(screen, color=(200, 200, 200), x=x, y=y1, length=length, height=height, text="New Game")
    Buttons(screen, color=(200, 200, 200), x=x, y=y2, length=length, height=height, text="Load Game")
    Buttons(screen, color=(200, 200, 200), x=x, y=y3, length=length, height=height, text="Quit")
    Run = True
    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Run = False

            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] > x:
                    if mouse[0] < (x+length):
                        if mouse[1] > y1:
                            if mouse[1] < (y1+height):
                                print("Pressed New Game")
                                Buttons(screen, color=(220, 220, 220), x=x, y=y1, length=length, height=height, text="New Game")
                                pygame.time.delay(100)
                                Buttons(screen, color=(200, 200, 200), x=x, y=y1, length=length, height=height, text="New Game")
                                NewGameDif(screen)

                            elif mouse[1] > y2:
                                if mouse[1] < (y2+height):
                                    print("Pressed Load Game")
                                    Buttons(screen, color=(220, 220, 220), x=x, y=y2, length=length, height=height, text="Load Game")
                                    pygame.time.delay(100)
                                    Buttons(screen, color=(200, 200, 200), x=x, y=y2, length=length, height=height, text="Load Game")

                                elif mouse[1] > y3:
                                    if mouse[1] < (y3+height):
                                        Buttons(screen, color=(220, 220, 220), x=x, y=y3, length=length, height=height, text="Quit")
                                        pygame.quit()
                                        Run = False
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass



def NewGameDif(screen):
    x = 260
    y1 = 270
    y2 = 310
    y3 = 350
    length = 120
    height = 30
    difficulty = ""

    Scene(screen, color=(138, 43, 226), text="Select Difficulty")
    Buttons(screen, color=(200, 200, 200), x=x, y=y1, length=length, height=height, text="Easy")
    Buttons(screen, color=(200, 200, 200), x=x, y=y2, length=length, height=height, text="Medium")
    Buttons(screen, color=(200, 200, 200), x=x, y=y3, length=length, height=height, text="Hard")
    Run = True
    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Run = False

            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] > x:
                    if mouse[0] < (x+length):
                        if mouse[1] > y1:
                            if mouse[1] < (y1+height):
                                print("Pressed Easy")
                                difficulty = "Easy"  # code to save difficulty here <----------------------------------------------------
                                Buttons(screen, color=(220, 220, 220), x=x, y=y1, length=length, height=height, text="Easy")
                                pygame.time.delay(100)
                                Buttons(screen, color=(200, 200, 200), x=x, y=y1, length=length, height=height, text="Easy")
                                NewGameName(screen)

                            elif mouse[1] > y2:
                                if mouse[1] < (y2+height):
                                    print("Pressed Medium")
                                    difficulty = "Medium"  # code to save difficulty here <----------------------------------------------
                                    Buttons(screen, color=(220, 220, 220), x=x, y=y2, length=length, height=height, text="Medium")
                                    pygame.time.delay(100)
                                    Buttons(screen, color=(200, 200, 200), x=x, y=y2, length=length, height=height, text="Medium")
                                    NewGameName(screen)

                                elif mouse[1] > y3:
                                    if mouse[1] < (y3+height):
                                        print("Pressed Hard")
                                        difficulty = "Hard"  # code to save difficulty here <--------------------------------------------
                                        Buttons(screen, color=(220, 220, 220), x=x, y=y3, length=length, height=height, text="Hard")
                                        pygame.time.delay(100)
                                        Buttons(screen, color=(200, 200, 200), x=x, y=y3, length=length, height=height, text="Hard")
                                        NewGameName(screen)

                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass

def NewGameName(screen):
    Scene(screen, color=(138, 43, 226), text="Type in your name")
    TextBox(screen)
    x = 260
    y = 305
    length = 120
    height = 30
    name = ""
    count = 0
    """
    Add button "RUN" when Return is pressed
    """
    while True:
        """
        Enter = 13
        Backspace = 8
        """
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if count == 12:
                print(name)  # code to save name here <----------------
                Buttons(screen, color=(200, 200, 200), x=x, y=y, length=length, height=height, text="Run Game")
                break

            elif event.key == K_RETURN:
                print(name)  # code to save name here <----------------
                Buttons(screen, color=(200, 200, 200), x=x, y=y, length=length, height=height, text="Run Game")
                break

            elif event.key <= 127:
                name = name + chr(event.key)
                print(name)
                NameInput(screen, text=name)
                count += 1

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

                                Buttons(screen, color=(240, 240, 240), x=x, y=y, length=length, height=height, text="Run Game")
                                pygame.time.delay(100)
                                Buttons(screen, color=(200, 200, 200), x=x, y=y, length=length, height=height, text="Run Game")
                                print("Code to do stuff...")  # code to run game here <---------------------------------------------
                                pygame.quit()
                                Run = False


                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass



if __name__ == "__main__":
    bg = pygame.image.load("bg.png")
    bg2 = pygame.image.load("bg2.png")
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Start Menu")
    screen.fill((200, 200, 200))
    screen.blit(bg, (0, 0))
    screen.blit(bg2, (176, 176))
    pygame.display.flip()
    StartMenu(screen)