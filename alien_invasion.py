import sys
import pygame

# --- Configuration & Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, shoot_sound):
        super().__init__()
        # Using ship2(no bg).png as the player spaceship
        try:
            self.image = pygame.image.load('ship2(no bg).png').convert_alpha()
        except pygame.error:
            # Fallback if image is missing so the game still runs
            self.image = pygame.Surface((64, 64))
            self.image.fill((0, 255, 0)) # green square fallback
            
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5
        self.shoot_sound = shoot_sound

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def shoot(self):
        # Create a missile at the ship's current location
        missile = Missile(self.rect.centerx, self.rect.top)
        self.shoot_sound.play()
        return missile

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Using laserBlast.png as the missile
        try:
            self.image = pygame.image.load('laserBlast.png').convert_alpha()
        except pygame.error:
            # Fallback if image is missing
            self.image = pygame.Surface((10, 20))
            self.image.fill((255, 0, 0)) # red rectangle fallback
            
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10 # Move upwards

    def update(self):
        self.rect.y += self.speed
        # Kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

def main():
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()

    # Load Sound Effects
    # Note: Ensure laser.mp3 is in the same folder as this script
    try:
        laser_fx = pygame.mixer.Sound('laser.mp3')
    except pygame.error:
        # Create a dummy object if file is missing to prevent crashes
        laser_fx = type('dummy', (), {'play': lambda: None})

    # Load Background (StarBasesnow.png)
    try:
        background = pygame.image.load('StarBasesnow.png').convert()
    except pygame.error:
        # Fallback background
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((0, 0, 0)) # plain black background
        
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    missiles = pygame.sprite.Group()

    player = Player(laser_fx)
    all_sprites.add(player)

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    m = player.shoot()
                    all_sprites.add(m)
                    missiles.add(m)

        # 2. Update
        all_sprites.update()

        # 3. Draw
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
