import pygame as pg
from sys import exit
from CELL import Simulator
from CELL import getCompleteSurrounding, getVonNeumanSurrounding, AustralianFire, ProbabilisticFire, NorthWindFire



FPS = 30
WIDTH = 200
HEIGHT = 510
MIN = 5
MAX = 20
BACKGROUND_COLOR = (150,150,150)
TEXT_COLOR = (0,0,0)
BUTTON_COLOR = (255,255,255)


ITERATIONS_MIN = 50
SAMPLING_MIN = 10
ITERATIONS_MAX = 400
SAMPLING_MAX = 50
SURROUNDING = {"Complete" : getCompleteSurrounding, "VonNeuman" : getVonNeumanSurrounding}
FIRE = {"Australian" : AustralianFire, "Probabilistic" : ProbabilisticFire, "NorthWind" : NorthWindFire}



class Selection(object):


    def __init__(self):
        pg.init()
        pg.display.set_caption('Fire Spread Selection') 
        self._screen = pg.display.set_mode((WIDTH,HEIGHT),flags=pg.DOUBLEBUF)
        self._font = pg.font.SysFont('Arial',200)
        self.fireCursor = 0
        self.surroundingCursor = 0
        self.iteration = ITERATIONS_MIN
        self.sampling = SAMPLING_MIN
        self._loop()


    def _loop(self):
        done = False
        clock = pg.time.Clock()
        while not done:
            clock.tick(FPS)
            self._drawMe()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    done=True
                    break
                if event.type == pg.MOUSEBUTTONDOWN:
                    self._mouseClicHandeler()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        done=True
                        break
        pg.quit()
        exit()



    def _drawMe(self):
        self._screen.fill(BACKGROUND_COLOR)

        text = self._font.render("Iterations", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (100, 30))
        self._screen.blit(text, (50, 10))
        pg.draw.rect(self._screen, BUTTON_COLOR, (50, 50, 100, 50))
        text = self._font.render("<", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (50, 50))
        text = self._font.render(">", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (140, 50))
        text = self._font.render(str(self.iteration), True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (40, 30))
        self._screen.blit(text, (80, 60))
                    
        text = self._font.render("Sampling", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (100, 30))
        self._screen.blit(text, (50, 110))
        pg.draw.rect(self._screen, BUTTON_COLOR, (50, 150, 100, 50))
        text = self._font.render("<", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (50, 150))
        text = self._font.render(">", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (140, 150))
        text = self._font.render(str(self.sampling), True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (40, 30))
        self._screen.blit(text, (80, 160))

        text = self._font.render("Surrounding", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (100, 30))
        self._screen.blit(text, (50, 210))
        pg.draw.rect(self._screen, BUTTON_COLOR, (50, 250, 100, 50))
        text = self._font.render("<", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (50, 250))
        text = self._font.render(">", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (140, 250))
        text = self._font.render(list(SURROUNDING.keys())[self.surroundingCursor], True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (60, 30))
        self._screen.blit(text, (70, 260))

        text = self._font.render("Fire type", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (100, 30))
        self._screen.blit(text, (50, 310))
        pg.draw.rect(self._screen, BUTTON_COLOR, (50, 350, 100, 50))
        text = self._font.render("<", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (50, 350))
        text = self._font.render(">", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (140, 350))
        text = self._font.render(list(FIRE.keys())[self.fireCursor], True,  TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (60, 30))
        self._screen.blit(text, (70, 360))

        pg.draw.rect(self._screen, BUTTON_COLOR, (50, 450, 100, 50))
        text = self._font.render("START", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (100, 50))
        self._screen.blit(text, (50, 450))


    def _mouseClicHandeler(self):
        (x,y) = pg.mouse.get_pos()
            
        if x <= 150 and x>=140 and y >=50 and y <= 100:
            self.iteration = self.iteration + 25 if self.iteration < ITERATIONS_MAX else ITERATIONS_MAX
        elif x <= 60 and x>=50 and y >=50 and y <= 100:
            self.iteration = self.iteration - 25 if self.iteration > ITERATIONS_MIN else ITERATIONS_MIN
        elif x <= 150 and x>=140 and y >=150 and y <= 200:
            self.sampling = self.sampling + 5 if self.sampling < SAMPLING_MAX else SAMPLING_MAX
        elif x <= 60 and x>=50 and y >=150 and y <= 200:
            self.sampling = self.sampling - 5 if self.sampling > SAMPLING_MIN else SAMPLING_MIN
        elif x <= 150 and x>=140 and y >=250 and y <= 300:
            self.surroundingCursor = (self.surroundingCursor + 1) % len(SURROUNDING)
        elif x <= 60 and x>=50 and y >=250 and y <= 300:
            self.surroundingCursor = (self.surroundingCursor - 1) % len(SURROUNDING)
        elif x <= 150 and x>=140 and y >=350 and y <= 400:
            self.fireCursor = (self.fireCursor + 1) % len(FIRE)
        elif x <= 60 and x>=50 and y >=350 and y <= 400:
            self.fireCursor = (self.fireCursor - 1) % len(FIRE)
        elif x <= 150 and x>=50 and y >=450 and y <= 500:
            pg.quit()
            Simulator(self.sampling, self.iteration, SURROUNDING[list(SURROUNDING.keys())[self.surroundingCursor]], FIRE[list(FIRE.keys())[self.fireCursor]]).display()



