import pygame
from typing import Optional, Dict, Union


class Sound:
    """Class to manage game sounds."""

    def __init__(self):
        """Initialize pygame mixer module for loading and playing sounds."""
        pygame.mixer.init()

    @property
    def sounds(self) -> Dict[str, Dict[str, Union[str, int, None]]]:
        """
        Dictionary containing sound file paths and their corresponding channels.

        Returns:
            Dict[str, Dict[str, Union[str, int, None]]]: Dictionary of sound details.
        """
        return {
            'background': {'audio': 'data/sounds/background.wav', 'channel': 0},
            'cars_motion': {'audio': 'data/sounds/cars_motion.wav', 'channel': 1},
            'game_over': {'audio': 'data/sounds/game_over.wav', 'channel': 2},
            'collision': {'audio': 'data/sounds/collision.wav', 'channel': None},
            'bonus': {'audio': 'data/sounds/bonus.wav', 'channel': None},
            'level_completed': {'audio': 'data/sounds/level_completed.wav', 'channel': None},
            'win': {'audio': 'data/sounds/winner.wav', 'channel': None}
        }

    def _get_sound(self, sound_name: str) -> pygame.mixer.Sound:
        """
        Retrieve a pygame Sound object for the given sound name.

        Args:
            sound_name (str): The name of the sound to retrieve.

        Returns:
            pygame.mixer.Sound: The pygame Sound object.
        """
        return pygame.mixer.Sound(self.sounds[sound_name]['audio'])

    def _get_channel(self, sound_name: str) -> Optional[pygame.mixer.Channel]:
        """
        Retrieve a pygame Channel object for the given sound name.

        Args:
            sound_name (str): The name of the sound to retrieve the channel for.

        Returns:
            Optional[pygame.mixer.Channel]: The pygame Channel object if assigned, else None.
        """
        channel = self.sounds[sound_name]['channel']
        if channel is not None:
            return pygame.mixer.Channel(self.sounds[sound_name]['channel'])

    def play_sound(self, sound_name: str, loops: int = 0) -> None:
        """
        Play the sound.

        Args:
            sound_name (str): The name of the sound to play.
            loops (int, optional): Number of times to repeat the sound. Default is 0 (no repeat).
        """
        sound = self._get_sound(sound_name=sound_name)
        channel = self._get_channel(sound_name=sound_name)
        if channel is not None:
            channel.play(sound, loops=loops)
        else:
            sound.play(loops=loops)

    def stop_sound(self, sound_name: str) -> None:
        """
        Stop the playing sound.

        Args:
            sound_name (str): The name of the playing sound to stop.
        """
        channel = self._get_channel(sound_name=sound_name)
        if channel is not None:
            channel.stop()

    def pause_sound(self, sound_name: str) -> None:
        """
        Pause the playing sound.

        Args:
            sound_name (str): The name of the playing sound to pause.
        """
        channel = self._get_channel(sound_name=sound_name)
        if channel is not None:
            channel.pause()

    def resume_sound(self, sound_name: str) -> None:
        """
        Resume the paused sound.

        Args:
            sound_name (str): The name of the paused sound to resume.
        """
        channel = self._get_channel(sound_name=sound_name)
        if channel is not None:
            channel.unpause()
