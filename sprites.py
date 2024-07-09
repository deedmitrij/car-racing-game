import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.locals import *
from timer import Timer


timer = Timer()


class Car(pygame.sprite.Sprite):
    """Base class for cars in the game."""

    def __init__(self, x: int, y: int, speed: int, image_path: str):
        """
        Initialize a Car object.

        Args:
            x (int): The x-coordinate of the car's initial position.
            y (int): The y-coordinate of the car's initial position.
            speed (int): The speed at which the car moves.
            image_path (str): Path to the image file for the car.
        """
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self) -> None:
        """Update the car's position."""
        self.rect.y += self.speed


class PlayerCar(Car):
    """Class representing the player's car."""

    INVINCIBILITY_DURATION = timer.seconds_to_frames(seconds=2)
    BLINK_INTERVAL = timer.seconds_to_frames(seconds=0.25)  # Toggle alpha every 0.25 seconds

    def __init__(self, x: int, y: int, speed: int, image_path: str):
        """
        Initialize a PlayerCar object.

        Args:
            x (int): The x-coordinate of the player's car's initial position.
            y (int): The y-coordinate of the player's car's initial position.
            speed (int): The speed at which the player's car moves.
            image_path (str): Path to the image file for the player's car.
        """
        super().__init__(x, y, speed, image_path)
        self.total_lives = 3
        self.current_lives = self.total_lives
        self.invincible = False
        self.invincible_time = 0
        self.blink_timer = 0

    def handle_input(self) -> None:
        """Handle user input for moving the player's car."""
        keys = pygame.key.get_pressed()
        if keys[K_UP] and self.rect.top > 0:  # Check if moving up keeps the car within the screen
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:  # Check if moving down keeps the car within the screen
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.left > 0:  # Check if moving left keeps the car within the screen
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:  # Check if moving right keeps the car within the screen
            self.rect.x += self.speed

    def update(self) -> None:
        """Update the player's car state, handling invincibility and blinking effects."""
        if self.invincible:
            self.invincible_time -= 1
            self.blink_timer += 1

            # Toggle alpha value every BLINK_INTERVAL frames
            if self.blink_timer % self.BLINK_INTERVAL == 0:
                self.image.set_alpha(64) if self.image.get_alpha() == 255 else self.image.set_alpha(255)

            if self.invincible_time <= 0:
                self.invincible = False
                self.image.set_alpha(255)  # Reset alpha to fully visible when invincibility ends
        else:
            self.image.set_alpha(255)  # Ensure the player car is fully visible when not invincible

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player's car on the screen."""
        screen.blit(self.image, self.rect)

    def activate_invincibility(self) -> None:
        """Activate invincibility for the player's car."""
        self.invincible = True
        self.invincible_time = self.INVINCIBILITY_DURATION
        self.blink_timer = 0
        self.image.set_alpha(64)


class ObstacleCar(Car):
    """Class representing an obstacle car on the road."""

    def __init__(self, x: int, y: int, speed: int, image_path: str):
        """
        Initialize an ObstacleCar object.

        Args:
            x (int): The x-coordinate of the obstacle car's initial position.
            y (int): The y-coordinate of the obstacle car's initial position.
            speed (int): The speed at which the obstacle car moves.
            image_path (str): Path to the image file for the obstacle car.
        """
        super().__init__(x, y, speed, image_path)

    def reset_position(self) -> None:
        """Reset the obstacle car's position to a new random location."""
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-self.rect.height, -100)

    def update(self) -> None:
        """Update the obstacle car's position and reset if it moves off-screen."""
        super().update()
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


class Obstacle(pygame.sprite.Sprite):
    """Class representing an obstacle on the road."""

    def __init__(self, x: int, y: int, image_path: str):
        """
        Initialize an Obstacle object.

        Args:
            x (int): The x-coordinate of the obstacle's initial position.
            y (int): The y-coordinate of the obstacle's initial position.
            image_path (str): Path to the image file for the obstacle.
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(3, 7)

    def update(self) -> None:
        """Update the obstacle's position."""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -50)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)


class Bonus(pygame.sprite.Sprite):
    """Class representing a bonus item on the road."""

    def __init__(self, x: int, y: int, image_path: str):
        """
        Initialize a Bonus object.

        Args:
            x (int): The x-coordinate of the bonus item's initial position.
            y (int): The y-coordinate of the bonus item's initial position.
            image_path (str): Path to the image file for the bonus item.
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1

    def update(self) -> None:
        """Update the bonus item's position."""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
