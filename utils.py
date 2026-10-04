"""
Модуль вспомогательных функций и утилит.
"""

import os
import sys
import struct
import math
import wave


class PathManager:
    """Менеджер путей к ресурсам приложения."""

    @staticmethod
    def get_base_path() -> str:
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        base_path = PathManager.get_base_path()
        return os.path.join(base_path, relative_path)


class SoundManager:
    """Менеджер звуковых эффектов. Работает и на Windows, и на Linux."""

    def __init__(self):
        self.sounds_dir = os.path.join(PathManager.get_base_path(), "assets", "sounds")
        os.makedirs(self.sounds_dir, exist_ok=True)
        self.success_path = os.path.join(self.sounds_dir, "success.wav")
        self.error_path = os.path.join(self.sounds_dir, "error.wav")

        # Генерируем звуки, если их нет
        if not os.path.exists(self.success_path) or os.path.getsize(self.success_path) == 0:
            self._generate_success_sound()
        if not os.path.exists(self.error_path) or os.path.getsize(self.error_path) == 0:
            self._generate_error_sound()


    def play_success(self) -> None:
        """Воспроизводит звук успеха."""
        self._play_sound(self.success_path)

    def play_error(self) -> None:
        """Воспроизводит звук ошибки."""
        self._play_sound(self.error_path)

    def _play_sound(self, sound_path: str) -> None:
        """Воспроизводит звуковой файл."""
        if not os.path.exists(sound_path):
            return

        if sys.platform == 'win32':
            # Windows
            try:
                import winsound
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass
        else:
            # Linux
            try:
                import subprocess
                subprocess.run(['paplay', sound_path], capture_output=True)
            except FileNotFoundError:
                try:
                    import subprocess
                    subprocess.run(['aplay', sound_path], capture_output=True)
                except FileNotFoundError:
                    pass