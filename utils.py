"""
Модуль вспомогательных функций и утилит.
Обеспечивает корректную работу путей при сборке в .exe и воспроизведение звуков.
"""

import os
import sys
import subprocess


class PathManager:
    """Менеджер путей к ресурсам приложения."""
    
    @staticmethod
    def get_base_path() -> str:
        """
        Получает базовый путь к приложению.
        Работает как при запуске из исходников, так и из .exe.
        """
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))
    
    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        """Получает полный абсолютный путь к ресурсу."""
        base_path = PathManager.get_base_path()
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def ensure_directory(directory_path: str) -> None:
        """Создает директорию, если она не существует."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


class SoundManager:
    """
    Менеджер звуковых эффектов.
    Использует системный 'paplay' или 'aplay' для надежности на Linux без доп. зависимостей.
    """
    
    def __init__(self):
        self.sounds_dir = PathManager.get_resource_path("assets/sounds")
        PathManager.ensure_directory(self.sounds_dir)
        self._create_default_sound()
    
    def _create_default_sound(self) -> None:
        """Создает простой WAV-файл заглушку, если его нет (опционально)."""
        sound_path = os.path.join(self.sounds_dir, "success.wav")
        if not os.path.exists(sound_path):
            # Пустой файл-заглушка, чтобы код не падал, если звука нет
            open(sound_path, 'a').close()
    
    def play_success(self) -> None:
        """Воспроизводит звук успешного действия."""
        sound_path = os.path.join(self.sounds_dir, "success.wav")
        if os.path.exists(sound_path) and os.path.getsize(sound_path) > 0:
            try:
                # Пробуем PulseAudio/PipeWire (стандарт для Arch)
                subprocess.run(['paplay', sound_path], capture_output=True)
            except FileNotFoundError:
                try:
                    # Фоллбэк на ALSA
                    subprocess.run(['aplay', sound_path], capture_output=True)
                except FileNotFoundError:
                    pass  # Если звуковой подсистемы нет, просто игнорируем
