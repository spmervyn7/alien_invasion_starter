import pygame
import sys
from settings import Settings
from ship import Ship

class AlienInvasion:
    
    def __init__(self) -> None:

        #from alien_fleet import AlienFleet
    
        pygame.init()
        self.settings = Settings()

        #self.screen = pygame.display.set_mode((1200, 800))
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        #self.running = True
        
        
        
        """self.settings.initialize_dynamic_settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )"""
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w, self.settings.screen_h))
        """
        pygame.display.set_caption(self.settings.name)"""
        
        self.running = True
        self.clock = pygame.time.Clock()

        self.ship = Ship(self)
        """

        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.aliens = AlienFleet(self)

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
"""

    def run_game(self) -> None:
        # Game loop
        while self.running:
             self._check_events()

             self._update_screen()
             self.clock.tick(self.settings.FPS)

    def _update_screen(self) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        pygame.display.flip()
    
    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
       
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()