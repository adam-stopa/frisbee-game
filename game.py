import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Rozmiary okna
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Kolory (format RGB)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Utwórz okno gry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laura's Frisbee Game")

# Zegar do kontrolowania szybkości gry
clock = pygame.time.Clock()
FPS = 60  # Frames per second (60 klatek na sekundę)

# Flaga do zamykania gry
running = True

# Klasa przeszkody
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=60, height=80):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((101, 67, 33))  # Ciemnobrązowy (drewno)
        
        # Rysuj prostą grafię drzewa
        pygame.draw.polygon(self.image, (34, 139, 34), [
            (width // 2, 0),
            (width, height // 2),
            (0, height // 2)
        ])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 3  # Prędkość opadania
    
    def update(self):
        self.rect.y += self.vel_y
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Klasa frisbee
class Frisbee(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Stwórz okrąg (frisbee)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (15, 15), 15)
        pygame.draw.circle(self.image, (255, 200, 0), (15, 15), 12)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Lekko opada
        self.vel_y = 0
        self.gravity = 0.3
    
    def update(self):
        # Fizyka — frisbee opada
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        # Jeśli frisbee wyleci poza ekran, zrespawnuj je
        if self.rect.y > SCREEN_HEIGHT:
            self.respawn()
    
    def respawn(self):
        """Zrespawnuj frisbee w losowej pozycji u góry"""
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(-200, -50)
        self.vel_y = 0
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Klasa gracza (Laura)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Narysuj prostego psa (kreskówkę)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        
        # Ciało (brązowy prostokąt)
        pygame.draw.ellipse(self.image, BROWN, (10, 20, 35, 25))
        
        # Głowa (koło)
        pygame.draw.circle(self.image, BROWN, (38, 18), 12)
        
        # Ucho
        pygame.draw.polygon(self.image, (139, 69, 19), [
            (35, 5),
            (42, 0),
            (40, 12)
        ])
        
        # Oczy
        pygame.draw.circle(self.image, BLACK, (42, 15), 2)
        pygame.draw.circle(self.image, WHITE, (43, 14), 1)
        
        # Nos
        pygame.draw.circle(self.image, BLACK, (45, 18), 2)
        
        # Ogon
        pygame.draw.line(self.image, BROWN, (15, 22), (5, 10), 3)
        
        # Nogi
        pygame.draw.line(self.image, (101, 67, 33), (20, 45), (20, 48), 3)
        pygame.draw.line(self.image, (101, 67, 33), (30, 45), (30, 48), 3)
        pygame.draw.line(self.image, (101, 67, 33), (40, 45), (40, 48), 3)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        
        self.is_jumping = False
        self.vel_y_jump = 0
        self.gravity = 0.6
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.vel_y_jump = -15
        
        if self.is_jumping:
            self.vel_y_jump += self.gravity
            self.rect.y += self.vel_y_jump
            
            if self.rect.y >= SCREEN_HEIGHT - 100:
                self.rect.y = SCREEN_HEIGHT - 100
                self.is_jumping = False
                self.vel_y_jump = 0
        
        if not self.is_jumping:
            self.rect.y = SCREEN_HEIGHT - 100
        
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Utwórz Laurę
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

# Utwórz frisbee
frisbee = Frisbee(random.randint(0, SCREEN_WIDTH - 30), random.randint(-200, -50))

# Lista przeszkód
obstacles = []

# Zmienne gry
score = 0
font = pygame.font.Font(None, 36)
obstacle_spawn_timer = 0

# Główna pętla gry
while running:
    clock.tick(FPS)
    
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Aktualizuj gracza i frisbee
    player.update()
    frisbee.update()
    
    # Spawn przeszkód co 60 klatek (co 1 sekundę przy 60 FPS)
    obstacle_spawn_timer += 1
    if obstacle_spawn_timer > 80:
        new_obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 60), -80)
        obstacles.append(new_obstacle)
        obstacle_spawn_timer = 0
    
    # Aktualizuj przeszkody
    for obstacle in obstacles:
        obstacle.update()
        
        # Sprawdź kolizję z graczem
        if player.rect.colliderect(obstacle.rect):
            print(f"Game Over! Final Score: {score}")
            running = False
    
    # Usuń przeszkody, które wyjechały poza ekran
    obstacles = [obs for obs in obstacles if obs.rect.y < SCREEN_HEIGHT]
    
    # Sprawdź kolizję (czy Laura złapała frisbee)
    if player.rect.colliderect(frisbee.rect):
        score += 1
        frisbee.respawn()
    
    # Tło
    screen.fill(GREEN)
    
    # Rysuj ziemię
    pygame.draw.rect(screen, (139, 90, 43), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    
    # Rysuj gracza, frisbee i przeszkody
    player.draw(screen)
    frisbee.draw(screen)
    
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # Rysuj wynik
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Aktualizuj ekran
    pygame.display.flip()

# Zamknij grę
pygame.quit()