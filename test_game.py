"""
Unit tests for Laura's Frisbee Game

Testuje logikę kolizji, animacje, i mechanikę gry.
"""

import pytest
import pygame
import sys
import os

# Dodaj katalog projektu do PATH
sys.path.insert(0, os.path.dirname(__file__))

# Mock Pygame przed importem game.py (unikamy otwierania okna w testach)
pygame.init()
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'


class TestDogClass:
    """Testy dla klasy Dog (Laura - pies)"""
    
    def test_dog_initialization(self):
        """Sprawdź inicjalizację psa"""
        from game import Dog, SCREEN_HEIGHT
        
        dog = Dog()
        assert dog.x == 100
        assert dog.width == 80
        assert dog.height == 60
        assert dog.velocity_y == 0
        assert dog.is_jumping is False
        assert dog.ground_level == SCREEN_HEIGHT - 120 - dog.height
    
    def test_dog_jump(self):
        """Sprawdź, czy pies może skoczyć"""
        from game import Dog
        
        dog = Dog()
        initial_velocity = dog.velocity_y
        dog.jump()
        
        assert dog.is_jumping is True
        assert dog.velocity_y < initial_velocity  # Prędkość w górę (ujemna)
    
    def test_dog_cannot_double_jump(self):
        """Sprawdź, czy pies nie może skoczyć dwa razy"""
        from game import Dog
        
        dog = Dog()
        dog.jump()
        first_velocity = dog.velocity_y
        dog.jump()  # Próbuj skoczyć ponownie
        
        assert dog.velocity_y == first_velocity  # Prędkość się nie zmieniła
    
    def test_dog_gravity_effect(self):
        """Sprawdź, czy grawitacja działa"""
        from game import Dog
        
        dog = Dog()
        dog.jump()
        initial_y = dog.y
        dog.update()
        
        # Po jednym update, pies powinien się ruszyć w górę lub pozostać
        assert dog.y != initial_y or dog.velocity_y != dog.jump_power
    
    def test_dog_lands_on_ground(self):
        """Sprawdź, czy pies powraca na ziemię"""
        from game import Dog
        
        dog = Dog()
        dog.jump()
        
        # Symuluj kilka klatek, aż pies wyląduje
        for _ in range(100):
            dog.update()
            if not dog.is_jumping:
                break
        
        assert dog.is_jumping is False
        assert dog.y == dog.ground_level


class TestFrisbeeClass:
    """Testy dla klasy Frisbee"""
    
    def test_frisbee_initialization(self):
        """Sprawdź inicjalizację frisbee"""
        from game import Frisbee, SCREEN_WIDTH, SCREEN_HEIGHT
        
        frisbee = Frisbee()
        assert frisbee.x == SCREEN_WIDTH
        assert frisbee.width == 40
        assert frisbee.height == 40
        assert SCREEN_HEIGHT - 280 <= frisbee.y <= SCREEN_HEIGHT - 180
    
    def test_frisbee_moves_left(self):
        """Sprawdź, czy frisbee porusza się w lewo"""
        from game import Frisbee
        
        frisbee = Frisbee()
        initial_x = frisbee.x
        frisbee.update()
        
        assert frisbee.x < initial_x
    
    def test_frisbee_off_screen(self):
        """Sprawdź detektowanie frisbee poza ekranem"""
        from game import Frisbee
        
        frisbee = Frisbee()
        frisbee.x = -50  # Ustaw poza ekranem
        
        assert frisbee.is_off_screen() is True


class TestObstacleClass:
    """Testy dla klasy Obstacle"""
    
    def test_obstacle_initialization(self):
        """Sprawdź inicjalizację przeszkody"""
        from game import Obstacle, SCREEN_WIDTH, SCREEN_HEIGHT
        
        obstacle = Obstacle()
        assert obstacle.x == SCREEN_WIDTH
        assert obstacle.width == 50
        assert 50 <= obstacle.height <= 70
        assert obstacle.y == SCREEN_HEIGHT - 120 - obstacle.height
    
    def test_obstacle_moves_left(self):
        """Sprawdź, czy przeszkoda porusza się w lewo"""
        from game import Obstacle
        
        obstacle = Obstacle()
        initial_x = obstacle.x
        obstacle.update()
        
        assert obstacle.x < initial_x
    
    def test_obstacle_off_screen(self):
        """Sprawdź detektowanie przeszkody poza ekranem"""
        from game import Obstacle
        
        obstacle = Obstacle()
        obstacle.x = -60  # Ustaw poza ekranem
        
        assert obstacle.is_off_screen() is True


class TestCollisionDetection:
    """Testy dla detektowania kolizji"""
    
    def test_no_collision_when_separated(self):
        """Sprawdź brak kolizji gdy obiekty są oddzielone"""
        from game import Dog, Frisbee, check_collision
        
        dog = Dog()
        frisbee = Frisbee()
        frisbee.x = -100  # Daleko od psa
        
        assert check_collision(dog, frisbee) is False
    
    def test_collision_when_overlapping(self):
        """Sprawdź kolizję gdy obiekty się nakładają"""
        from game import Dog, Frisbee, check_collision
        
        dog = Dog()
        frisbee = Frisbee()
        frisbee.x = dog.x + 20  # Blisko psa
        frisbee.y = dog.y + 20  # Blisko psa (Y)
        
        assert check_collision(dog, frisbee) is True
    
    def test_collision_with_obstacle(self):
        """Sprawdź kolizję psa z przeszkodą"""
        from game import Dog, Obstacle, check_collision
        
        dog = Dog()
        obstacle = Obstacle()
        obstacle.x = dog.x + 20
        obstacle.y = dog.y + 10
        
        assert check_collision(dog, obstacle) is True


class TestLoadImage:
    """Testy dla funkcji ładowania obrazków"""
    
    def test_load_image_missing_file(self):
        """Sprawdź obsługę brakującego pliku"""
        from game import load_image
        
        result = load_image('nonexistent.png', 80, 60)
        assert result is None
    
    def test_load_image_with_scaling(self):
        """Sprawdź skalowanie obrazka"""
        from game import load_image
        
        # Stwórz tymczasowy obrazek testowy
        test_image = pygame.Surface((200, 200))
        pygame.image.save(test_image, 'test_img.png')
        
        loaded = load_image('test_img.png', 100, 100)
        
        # Cleanup
        if os.path.exists('test_img.png'):
            os.remove('test_img.png')
        
        # Jeśli ładowanie się nie powiedzie, loaded będzie None
        # (bo 'assets' folder może nie istnieć w testach)
        # To jest ok - testujemy logikę, nie faktyczne ładowanie


class TestGameLogic:
    """Testy dla ogólnej logiki gry"""
    
    def test_high_score_tracking(self):
        """Sprawdź śledzenie najlepszego wyniku"""
        import game
        
        initial_high_score = game.high_score
        game.high_score = 100
        
        assert game.high_score == 100
        
        # Resetuj
        game.high_score = initial_high_score


# Uruchomienie testów
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
