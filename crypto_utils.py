"""
Модуль криптографических операций для шифрования и дешифрования паролей.
Использует симметричное шифрование Fernet (AES-128 в режиме CBC).
"""

import os
import base64
import secrets
import string
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoManager:
    """Менеджер криптографических операций."""
    
    KEY_FILE = "secret.key"
    SALT = b'securepass_salt_2024_arch'
    
    def __init__(self):
        """Инициализация менеджера криптографии."""
        self._fernet: Optional[Fernet] = None
        self._initialize_key()
    
    def _initialize_key(self) -> None:
        """Инициализирует ключ шифрования: загружает или генерирует новый."""
        if os.path.exists(self.KEY_FILE):
            self._load_key()
        else:
            self._generate_and_save_key()
    
    def _load_key(self) -> None:
        """Загружает существующий ключ из файла."""
        with open(self.KEY_FILE, 'rb') as key_file:
            key = key_file.read()
            self._fernet = Fernet(key)
    
    def _generate_and_save_key(self) -> None:
        """Генерирует новый мастер-ключ и сохраняет его в файл."""
        master_password = os.urandom(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.SALT,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password))
        
        with open(self.KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        
        self._fernet = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Шифрует строку данных.
        
        Args:
            data: Строка для шифрования
            
        Returns:
            Зашифрованная строка в формате base64
        """
        if self._fernet is None:
            raise RuntimeError("Ключ шифрования не инициализирован")
        encrypted_data = self._fernet.encrypt(data.encode('utf-8'))
        return encrypted_data.decode('utf-8')
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Дешифрует строку данных.
        
        Args:
            encrypted_data: Зашифрованная строка в формате base64
            
        Returns:
            Дешифрованная строка
        """
        if self._fernet is None:
            raise RuntimeError("Ключ шифрования не инициализирован")
        decrypted_data = self._fernet.decrypt(encrypted_data.encode('utf-8'))
        return decrypted_data.decode('utf-8')
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """
        Генерирует криптографически стойкий пароль.
        
        Args:
            length: Длина пароля (по умолчанию 16 символов)
            
        Returns:
            Случайный пароль заданной длины
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))
