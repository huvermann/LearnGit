import pygame

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

class status():
    running = True


def handleEvents():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            status.running = False


def runGame():
    pygame.init()
    pygame.display.set_caption("SimpleGame")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

    while status.running:
        handleEvents()


        pygame.display.flip()
        clock.tick(80)

    pygame.quit()



if __name__ == "__main__":
    runGame()

    
