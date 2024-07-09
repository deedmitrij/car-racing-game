import pygame


def handle_quit_event() -> None:
    """
    Handle the quit event for the game. If a quit event is detected, this function will
    stop the Pygame library and terminate the program.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
