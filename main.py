import pygame
import utils
from screens import LevelScreen, GameOverScreen
from timer import Timer


class Game:
    """Main class to manage the game flow."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.level_screen = LevelScreen()
        self.game_over_screen = GameOverScreen()
        self.timer = Timer()
        self.running = True

    def run(self) -> None:
        """
        Run the main game loop, managing the level loading, input handling, collisions, and screen updates.
        """
        while self.running:
            # Load current level
            self.level_screen.load_current_level()

            while self.level_screen.level_timer > 0:
                # Handle quit event
                utils.handle_quit_event()

                # Handle player car input
                self.level_screen.player_car.handle_input()

                # Handle collisions
                self.level_screen.handle_collision()

                if self.level_screen.player_car.current_lives <= 0:
                    self.game_over_screen.display()
                    self.game_over_screen.handle_events()

                self.level_screen.update_level()
                self.level_screen.draw_level()

                pygame.display.flip()
                self.timer.tick()

            self.level_screen.display_level_completed()

            if not self.level_screen.next_level():
                self.running = False

        pygame.quit()
        quit()


if __name__ == "__main__":
    game = Game()
    game.run()
