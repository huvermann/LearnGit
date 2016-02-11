import pygame
from pygame.locals import *

class wurfCalculator(object):
    def __init__(self, g, v0, vx):
        #super().__init__(**kwargs)
        self.g = g * 1000 #9.81 #Erdbeschleunigung
        self.v0 = v0 # Geschwindigkeit (pixex/s)
        self.vx = vx

    def calcY(self, time):
        t = time / 1000
        result = int(self.v0 * t - self.g / 2 * t * t)
        return result

    def calcX(self, time):
        result = int(time / 1000 * self.vx)
        return result



class jumper(pygame.sprite.Sprite):
    def __init__(self, g, v, vx, color):
        super().__init__()
        self.image = pygame.Surface([32, 32])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image, color, self.rect)
        self.rect.top= 500
        self.rect.left = self.rect.width + 2
        self.calculator = wurfCalculator(g, v, vx)

    def saveStartPosition(self):
        self.startTime = pygame.time.get_ticks()
        self.startPosition = self.rect.copy()

        pass
        

    def update(self, *args):
        super().update(*args)
        if args:
            time = args[0]
            delay = time - self.startTime
            moveY = self.calculator.calcY(delay)
            moveX = self.calculator.calcX(delay)
            self.rect.top = self.startPosition.top - moveY
            self.rect.left = self.startPosition.left + moveX

        pass


def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)
    


    player = jumper(1, 500, 100, (255,0,0))
    player2 = jumper(0.01, 100, 100, (0, 255, 0))
    spriteList = pygame.sprite.Group()
    spriteList.add(player)
    spriteList.add(player2)

    clock = pygame.time.Clock()
    
    player.saveStartPosition()
    player2.saveStartPosition()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        time = pygame.time.get_ticks()
        
        screen.blit(background, (0,0))
        spriteList.update(time)
        spriteList.draw(screen)
        pygame.display.flip()
    pass

if __name__ == '__main__': main()
pygame.quit()


