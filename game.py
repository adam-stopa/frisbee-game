import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Rozmiary okna
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Kolory
WHITE = (255, 255, 255)
GREEN = (100, 200, 100)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (135, 206, 235)

# Utwórz okno
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laura's Frisbee Game")

# Zegar
clock = pygame.time.Clock()
FPS = 60

# Klasa dla Laury (naszego psa)
class Dog:
    def __init__(self):
        self.width = 60
        self.height = 40
        self.x = 100
        self.y = SCREEN_HEIGHT - 150
        self.velocity_y = 0
        self.is_jumping = False
        self.gravity = 0.8
        self.jump_power = -15
        
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_power
            self.is_jumping = True
    
    def update(self):
        # Grawitacja
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # Sprawdź czy pies jest na ziemi
        if self.y >= SCREEN_HEIGHT - 150:
            self.y = SCREEN_HEIGHT - 150
            self.velocity_y = 0
            self.is_jumping = False
    
    def draw(self, screen):
        # Ciało psa (brązowy prostokąt)
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        # Głowa
        pygame.draw.circle(screen, BROWN, (self.x + self.width, self.y + 10), 15)
        # Ogon
        pygame.draw.line(screen, BROWN, (self.x, self.y + 20), (self.x - 15, self.y + 10), 5)

# Klasa dla frisbee
class Frisbee:
    def __init__(self):
        self.radius = 15
        self.x = SCREEN_WIDTH
        self.y = random.randint(100, SCREEN_HEIGHT - 200)
        self.speed = 5
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, ORANGE, (self.x, self.y), self.radius)
        
    def is_off_screen(self):
        return self.x < -self.radius * 2

# Klasa dla przeszkód
class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = random.randint(40, 80)
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - 100 - self.height
        self.speed = 6
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        # Drzewo (brązowy pień + zielona korona)
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, GREEN, (self.x + self.width//2, self.y - 20), 25)
        
    def is_off_screen(self):
        return self.x < -self.width

# Funkcja sprawdzająca kolizję
def check_collision(dog, obj):
    dog_rect = pygame.Rect(dog.x, dog.y, dog.width, dog.height)
    
    if isinstance(obj, Frisbee):
        obj_rect = pygame.Rect(obj.x - obj.radius, obj.y - obj.radius, 
                               obj.radius * 2, obj.radius * 2)
    else:  # Obstacle
        obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    
    return dog_rect.colliderect(obj_rect)

# Główna funkcja gry
def main():
    dog = Dog()
    frisbees = []
    obstacles = []
    score = 0
    running = True
    game_over = False
    
    # Liczniki do tworzenia obiektów
    frisbee_timer = 0
    obstacle_timer = 0
    
    # Czcionka do wyświetlania tekstu
    font = pygame.font.Font(None, 36)
    
    while running:
        clock.tick(FPS)
        
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    dog.jump()
                if event.key == pygame.K_r and game_over:
                    # Restart gry
                    return main()
        
        if not game_over:
            # Aktualizacja psa
            dog.update()
            
            # Tworzenie frisbee co jakiś czas
            frisbee_timer += 1
            if frisbee_timer > 120:  # Co 2 sekundy
                frisbees.append(Frisbee())
                frisbee_timer = 0
            
            # Tworzenie przeszkód
            obstacle_timer += 1
            if obstacle_timer > 90:  # Co 1.5 sekundy
                obstacles.append(Obstacle())
                obstacle_timer = 0
            
            # Aktualizacja frisbee
            for frisbee in frisbees[:]:
                frisbee.update()
                
                # Sprawdź kolizję z psem
                if check_collision(dog, frisbee):
                    frisbees.remove(frisbee)
                    score += 10
                elif frisbee.is_off_screen():
                    frisbees.remove(frisbee)
            
            # Aktualizacja przeszkód
            for obstacle in obstacles[:]:
                obstacle.update()
                
                # Sprawdź kolizję z psem
                if check_collision(dog, obstacle):
                    game_over = True
                elif obstacle.is_off_screen():
                    obstacles.remove(obstacle)
        
        # Rysowanie
        # Tło - niebo i trawa
        screen.fill(BLUE)
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Rysuj wszystkie obiekty
        dog.draw(screen)
        
        for frisbee in frisbees:
            frisbee.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Wyświetl punkty
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Game Over
        if game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()