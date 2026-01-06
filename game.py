import pygame
import random
import os

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
GOLD = (171, 128, 0)

# Utwórz okno
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laura's Frisbee Game")

# Zegar
clock = pygame.time.Clock()
FPS = 60

# High Score (globalny)
high_score = 0

# Ładowanie grafik
def load_image(filename, width=None, height=None):
    """Ładuje obrazek i opcjonalnie skaluje go"""
    try:
        path = os.path.join('assets', filename)
        image = pygame.image.load(path).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except:
        print(f"Nie można załadować {filename}, używam prostokąta")
        return None

# Załaduj grafiki
laura_img = load_image('laura.png', 80, 60)
frisbee_img = load_image('frisbee.png', 40, 40)
tree_img = load_image('tree.png', 50, 70)

# Klasa dla Laury (naszego psa)
class Dog:
    def __init__(self):
        self.width = 80
        self.height = 60
        self.x = 100
        self.y = SCREEN_HEIGHT - 120 - self.height  # Trawa wyżej (było -150)
        self.velocity_y = 0
        self.is_jumping = False
        self.gravity = 0.8
        self.jump_power = -18
        self.image = laura_img
        self.ground_level = SCREEN_HEIGHT - 120 - self.height
        
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_power
            self.is_jumping = True
    
    def update(self):
        # Grawitacja
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # Sprawdź czy pies jest na ziemi
        if self.y >= self.ground_level:
            self.y = self.ground_level
            self.velocity_y = 0
            self.is_jumping = False
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Fallback - rysuj prostokąt
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
            pygame.draw.circle(screen, BROWN, (self.x + self.width, self.y + 10), 15)
            pygame.draw.line(screen, BROWN, (self.x, self.y + 20), (self.x - 15, self.y + 10), 5)

# Klasa dla frisbee
class Frisbee:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = SCREEN_WIDTH
        # Dostosowane do nowej wysokości trawy
        self.y = random.randint(SCREEN_HEIGHT - 280, SCREEN_HEIGHT - 180)
        self.speed = 5
        self.image = frisbee_img
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.circle(screen, ORANGE, (int(self.x + self.width//2), int(self.y + self.height//2)), 15)
        
    def is_off_screen(self):
        return self.x < -self.width

# Klasa dla przeszkód
class Obstacle:
    def __init__(self):
        self.width = 50
        self.height = random.randint(50, 70)
        self.x = SCREEN_WIDTH
        # Dostosowane do nowej wysokości trawy
        self.y = SCREEN_HEIGHT - 120 - self.height
        self.speed = 6
        self.image = tree_img
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
            screen.blit(scaled_image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
            pygame.draw.circle(screen, GREEN, (self.x + self.width//2, self.y - 20), 25)
        
    def is_off_screen(self):
        return self.x < -self.width

# Funkcja sprawdzająca kolizję
def check_collision(dog, obj):
    dog_rect = pygame.Rect(dog.x + 10, dog.y + 10, dog.width - 20, dog.height - 20)
    
    if isinstance(obj, Frisbee):
        obj_rect = pygame.Rect(obj.x + 5, obj.y + 5, obj.width - 10, obj.height - 10)
    else:
        obj_rect = pygame.Rect(obj.x + 5, obj.y + 5, obj.width - 10, obj.height - 10)
    
    return dog_rect.colliderect(obj_rect)

# Główna funkcja gry
def main():
    global high_score
    
    dog = Dog()
    frisbees = []
    obstacles = []
    score = 0
    running = True
    game_over = False
    new_record = False
    
    # Liczniki do tworzenia obiektów
    frisbee_timer = 0
    obstacle_timer = 0
    
    # Czcionki
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 48)
    
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
            if frisbee_timer > 150:
                frisbees.append(Frisbee())
                frisbee_timer = 0
            
            # Tworzenie przeszkód
            obstacle_timer += 1
            if obstacle_timer > 100:
                obstacles.append(Obstacle())
                obstacle_timer = 0
            
            # Aktualizacja frisbee
            for frisbee in frisbees[:]:
                frisbee.update()
                
                if check_collision(dog, frisbee):
                    frisbees.remove(frisbee)
                    score += 10
                    # Sprawdź czy nowy rekord
                    if score > high_score:
                        high_score = score
                        new_record = True
                elif frisbee.is_off_screen():
                    frisbees.remove(frisbee)
            
            # Aktualizacja przeszkód
            for obstacle in obstacles[:]:
                obstacle.update()
                
                if check_collision(dog, obstacle):
                    game_over = True
                elif obstacle.is_off_screen():
                    obstacles.remove(obstacle)
        
        # Rysowanie
        # Tło - niebo i trawa (wyżej - było -100, teraz -120)
        screen.fill(BLUE)
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120))
        
        # Rysuj wszystkie obiekty
        dog.draw(screen)
        
        for frisbee in frisbees:
            frisbee.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Wyświetl punkty i high score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        high_score_text = small_font.render(f"High Score: {high_score}", True, GOLD)
        screen.blit(high_score_text, (10, 50))
        
        # Instrukcje
        if not game_over:
            instruction_text = small_font.render("SPACJA = Skok", True, BLACK)
            screen.blit(instruction_text, (SCREEN_WIDTH - 150, 10))
        
        # Game Over
        if game_over:
            game_over_text = big_font.render("GAME OVER!", True, BLACK)
            restart_text = small_font.render("Naciśnij R aby zagrać ponownie", True, BLACK)
            final_score_text = font.render(f"Twój wynik: {score}", True, BLACK)
            
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            
            screen.blit(game_over_text, text_rect)
            screen.blit(restart_text, restart_rect)
            screen.blit(final_score_text, score_rect)
            
            # Jeśli nowy rekord
            if new_record:
                record_text = big_font.render("NOWY REKORD!", True, GOLD)
                record_rect = record_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
                screen.blit(record_text, record_rect)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()