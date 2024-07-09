import os
import random
import pygame
import settings
import utils
from sound import Sound
from sprites import PlayerCar, ObstacleCar, Obstacle, Bonus
from timer import Timer


timer = Timer()


class Screen:
    """Singleton class to manage the game screen."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> 'Screen':
        """
        Ensure that only one instance of the Screen class is created.

        Returns:
            Screen: The singleton instance of the Screen class.
        """
        if not cls._instance:
            cls._instance = super(Screen, cls).__new__(cls, *args, **kwargs)
            cls._instance.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            pygame.display.set_caption('Car Racing Game')
        return cls._instance

    def get_screen(self) -> pygame.Surface:
        """Return the main game screen surface."""
        return self._instance.screen


class BaseScreen(Screen):
    """Base class for different game screens."""

    def __init__(self):
        """Initialize a BaseScreen object."""
        super().__init__()
        self.screen = self.get_screen()
        self.font = pygame.font.Font
        self.sound = Sound()


class LevelScreen(BaseScreen):
    """Class representing the level screen."""

    def __init__(self):
        """Initialize a LevelScreen object."""
        super().__init__()
        self.background_img = pygame.image.load('data/assets/background.png')
        self.collision_img = pygame.image.load('data/assets/collision.png')
        self.heart_img = pygame.image.load('data/assets/heart.png')
        self.bonus_img = pygame.image.load('data/assets/bonus.png')
        self.level_files = self._get_level_files()
        self.current_level_index = 1
        self.level_sprites = None
        self.win_screen = WinScreen()
        self.level_time = 15
        self.level_timer = 0
        self.sound.play_sound(sound_name='background', loops=-1)

    @property
    def player_car(self) -> PlayerCar:
        """Return the player's car from the level sprites."""
        for sprite in self.level_sprites:
            if isinstance(sprite, PlayerCar):
                return sprite

    @staticmethod
    def _get_level_files() -> list:
        """Return a list of level file paths."""
        path = 'data/levels'
        return [f'{path}/{file_name}' for file_name in os.listdir(path)]

    @staticmethod
    def _load_level(level_file: str) -> pygame.sprite.Group:
        """Load the level from the given file and return the group of level sprites."""
        level_sprites = pygame.sprite.Group()
        with open(level_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    entity, x, y, image_path = line.split()
                    x, y = int(x), int(y)
                    if entity == 'player_car':
                        level_sprites.add(PlayerCar(x, y, 5, image_path))
                    elif entity == 'obstacle_car':
                        level_sprites.add(ObstacleCar(x, y, random.randint(3, 7), image_path))
                    elif entity == 'obstacle':
                        level_sprites.add(Obstacle(x, y, image_path))
                    elif entity == 'bonus':
                        level_sprites.add(Bonus(x, y, image_path))
        return level_sprites

    def _display_text(self, text: str, text_font: tuple, text_color: tuple, timeout: int) -> None:
        """Display the given text on the screen with the specified font, color, and timeout."""
        font = self.font(*text_font)
        if '\n' in text:
            lines = text.split('\n')
            line_height = font.get_linesize()
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, text_color)
                text_rect = text_surface.get_rect(
                    center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + i * line_height))
                self.screen.blit(text_surface, text_rect)
        else:
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(timeout)

    def draw_timer(self) -> None:
        """Draw the timer on the screen."""
        time_font = self.font(*settings.FONT_SMALL)
        timer_text = time_font.render(
            f'Time: {timer.frames_to_seconds(frames=self.level_timer)}', True, settings.WHITE
        )
        self.screen.blit(timer_text, (settings.SCREEN_WIDTH - 120, 25))

    def display_current_level_number(self) -> None:
        """Display the current level number on the screen."""
        self.screen.fill(settings.BLACK)
        self._display_text(
            text=f'Level {self.current_level_index}',
            text_font=settings.FONT_LARGE,
            text_color=settings.WHITE,
            timeout=2000
        )

    def display_level_completed(self) -> None:
        """Display the level completed text on the screen."""
        self.sound.stop_sound(sound_name='cars_motion')
        self.sound.play_sound(sound_name='level_completed')
        self._display_text(
            text=f'Level {self.current_level_index}\nCompleted',
            text_font=settings.FONT_LARGE,
            text_color=settings.LIGHT_GREEN,
            timeout=2000
        )

    def display_player_lives(self) -> None:
        """Display the player's remaining lives on the screen."""
        for i in range(self.player_car.current_lives):
            self.screen.blit(self.heart_img, (10 + i * 40, 10))

    def load_current_level(self) -> None:
        """Load the current level."""
        current_player_lives = self.player_car.current_lives if self.level_sprites else None
        self.level_sprites = self._load_level(self.level_files[self.current_level_index - 1])
        self.level_timer = timer.seconds_to_frames(seconds=self.level_time)
        self.player_car.current_lives = current_player_lives or self.player_car.current_lives
        self.display_current_level_number()
        self.sound.play_sound(sound_name='cars_motion', loops=-1)

    def handle_collision(self) -> None:
        """Handle collision events and update player lives and invincibility."""
        if not self.player_car.invincible:
            for sprite in self.level_sprites:
                if isinstance(sprite, (ObstacleCar, Obstacle)) and pygame.sprite.collide_rect(self.player_car, sprite):
                    self.screen.blit(self.collision_img, self.player_car.rect.topleft)
                    pygame.display.flip()
                    self.sound.pause_sound(sound_name='cars_motion')
                    self.sound.play_sound(sound_name='collision')
                    pygame.time.wait(settings.COLLISION_DISPLAY_TIME)
                    self.sound.resume_sound(sound_name='cars_motion')
                    self.player_car.activate_invincibility()
                    self.player_car.current_lives -= 1

    def handle_bonus_collection(self) -> None:
        """Handle the collection of bonus items by the player."""
        for sprite in self.level_sprites:
            if isinstance(sprite, Bonus) and pygame.sprite.collide_rect(self.player_car, sprite):
                self.sound.play_sound(sound_name='bonus')
                self.level_sprites.remove(sprite)
                if self.player_car.current_lives < 3:
                    self.player_car.current_lives += 1

    def update_level(self) -> None:
        """Update the level timer and level sprites."""
        self.level_timer -= 1
        self.level_sprites.update()
        self.handle_bonus_collection()

    def draw_level(self) -> None:
        """Draw the level background, sprites, timer, and player lives."""
        self.screen.blit(self.background_img, (0, 0))
        self.level_sprites.draw(self.screen)
        self.draw_timer()
        self.display_player_lives()

    def next_level(self) -> bool:
        """Move to the next level. Return False if there are no more levels."""
        self.current_level_index += 1
        if self.current_level_index > len(self.level_files):
            self.win_screen.display()
            return False
        return True

    def reset_game(self) -> None:
        """Reset the game to the first level."""
        self.level_sprites = None
        self.current_level_index = 1
        self.sound.play_sound(sound_name='background')
        self.load_current_level()


class WinScreen(BaseScreen):
    """Class representing the Win screen."""

    def __init__(self):
        """Initialize a WinScreen object."""
        super().__init__()
        self.win_img = pygame.image.load('data/assets/win_screen.jpg')

    def display(self) -> None:
        """Display the Win screen."""
        self.sound.stop_sound(sound_name='background')
        self.sound.stop_sound(sound_name='cars_motion')
        self.sound.play_sound(sound_name='win')
        self.screen.blit(self.win_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(5000)


class GameOverScreen(BaseScreen):
    """Class representing the Game Over screen."""

    def __init__(self):
        """Initialize a GameOverScreen object."""
        super().__init__()
        self.game_over_img = pygame.image.load('data/assets/game_over.jpg')
        self.start_button_rect = pygame.Rect(settings.SCREEN_WIDTH // 2 - 120, settings.SCREEN_HEIGHT // 2 + 50, 240, 50)
        self.exit_button_rect = pygame.Rect(settings.SCREEN_WIDTH // 2 - 120, settings.SCREEN_HEIGHT // 2 + 120, 240, 50)
        self.level_screen = LevelScreen()

    def display(self) -> None:
        """Display the Game Over screen."""
        self.sound.stop_sound(sound_name='background')
        self.sound.stop_sound(sound_name='cars_motion')
        self.sound.play_sound(sound_name='game_over', loops=-1)
        self.screen.blit(self.game_over_img, (0, 0))

        # Buttons
        pygame.draw.rect(self.screen, settings.RED, self.start_button_rect)
        pygame.draw.rect(self.screen, settings.RED, self.exit_button_rect)
        pygame.draw.rect(self.screen, settings.WHITE, self.start_button_rect, 2)  # Border for start button
        pygame.draw.rect(self.screen, settings.WHITE, self.exit_button_rect, 2)  # Border for exit button

        font = pygame.font.Font(*settings.FONT_SMALL)
        start_text = font.render('START NEW GAME', True, settings.WHITE)
        exit_text = font.render('EXIT', True, settings.WHITE)

        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)

        self.screen.blit(start_text, start_text_rect)
        self.screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

    def handle_events(self) -> None:
        """Handle events on the Game Over screen."""
        game_over = True
        while game_over:
            utils.handle_quit_event()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        self.sound.stop_sound(sound_name='game_over')
                        self.level_screen.reset_game()
                        game_over = False
                    elif self.exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        quit()
