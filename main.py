import pygame, sys

import settings
from level import Level

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("if you're seeing this, something went wrong")
        self.clock = pygame.time.Clock()

        self.level_num = 9
        self.max_level = 10
        self.newLevel()

        self.level_complete = pygame.font.Font(None, 50)
    
    def run(self) -> None:
        while True:
            self.update()
            self.clock.tick(settings.FPS)

    def update(self) -> None:
        """called once per frame""" 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        self.screen.fill('black')
        
        self.level.update()

        if self.level.main_block.tlrect.topleft == (1*settings.UNIT_SIZE, 3*settings.UNIT_SIZE):
            self.displayCompletedLevel()
            pygame.time.wait(1000)
            self.level_num += 1
            self.newLevel()

        pygame.display.update()
    
    def newLevel(self) -> None:
        """loads the current level it's on"""
        if self.level_num > self.max_level:
            return
        self.level = Level(f"level{self.level_num}.txt")
        pygame.display.set_caption(f"swipe puzzle - level {self.level_num}/{self.max_level}")
    
    def displayCompletedLevel(self) -> None:
        text = self.level_complete.render("LEVEL COMPLETE!", True, "white")
        t_rect = text.get_rect()
        t_rect.center = (self.screen.get_width()//2, self.screen.get_height()//2)
        self.screen.blit(text, t_rect)
        pygame.display.update()


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()