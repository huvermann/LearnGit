import pygame
from GameState import GameState
from GameColors import GameColors

class ViewModelBase:
    """description of class"""
    def __init__(self, state, screen):
        self.state = state
        self.screen = screen
        self.colors = GameColors()
        # Container for all sprites
        self.allSprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)


        
    def runView(self):
        self.handleEvent()
        self.updateScreen()
        self.flipScreen()
        pass

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.done = True
    
    def updateScreen(self):
        """Paint the screen."""
        
        self.screen.fill(self.colors.WHITE)
        background = self.screen.convert()
        text = self.font.render("The base screen", 1, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
        self.screen.blit(background, (0,0))
        

        self.moveSprites()
    
    def flipScreen(self):
        """Flip the screen."""
        pygame.display.flip()
        self.state.clock.tick(60)
    
    def moveSprites(self):
        self.allSprites.draw(self.screen)
        pass









