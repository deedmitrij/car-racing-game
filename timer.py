import pygame
from settings import FPS


class Timer:
    """
    Singleton class to manage game timing, including converting between seconds and frames,
    and controlling the game frame rate.
    """

    _instance = None

    def __new__(cls) -> 'Timer':
        """
        Ensure that only one instance of the Timer class is created.

        Returns:
            Timer: The singleton instance of the Timer class.
        """
        if not cls._instance:
            cls._instance = super(Timer, cls).__new__(cls)
            cls._instance.clock = pygame.time.Clock()
            cls._instance.fps = FPS
        return cls._instance

    def seconds_to_frames(self, seconds: float) -> int:
        """
        Convert seconds to frames based on the FPS setting.

        Args:
            seconds (float): The number of seconds to convert.

        Returns:
            int: The equivalent number of frames.
        """
        return int(seconds * self._instance.fps)

    def frames_to_seconds(self, frames: int) -> float:
        """
        Convert frames to seconds based on the FPS setting.

        Args:
            frames (int): The number of frames to convert.

        Returns:
            float: The equivalent number of seconds.
        """
        return frames // self._instance.fps

    def tick(self) -> int:
        """
        Control the frame rate of the game.

        Returns:
            int: The number of milliseconds that passed since the last call.
        """
        return self.clock.tick(self.fps)
