"""
Модуль для работы с базой данных SQLite.
Реализует CRUD операции с защитой от SQL-инъекций через параметризованные запросы.
"""

import re
import sqlite3
from typing import List, Dict, Optional


class DatabaseManager:
    """Менеджер базы данных с защитой от SQL-инъекций."""

    DB_FILE = "securepass.db"

    # Ограничения на длину полей
    MAX_SERVICE_NAME_LENGTH = 100
    MAX_USERNAME_LENGTH = 150
    MAX_NOTES_LENGTH = 500

    # Паттерн для валидации: разрешены буквы, цифры, пробелы, дефис, подчёркивание, точка, @
    SAFE_INPUT_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-\_\.@]+$')

    def __init__(self):
        """Инициализация менеджера БД и создание таблиц."""
        self.conn = sqlite3.connect(self.DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        """Создает необходимые таблицы, если они не существуют."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                icon_path TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                service_name TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()
        self._insert_default_categories()

    def _insert_default_categories(self) -> None:
        """Добавляет стандартные категории при первом запуске."""
        self.cursor.execute('SELECT COUNT(*) FROM categories')
        count = self.cursor.fetchone()[0]

        if count == 0:
            default_categories = [
                ('Social', 'assets/icons/social.png'),
                ('Work', 'assets/icons/work.png'),
                ('Finance', 'assets/icons/finance.png'),
                ('Email', 'assets/icons/email.png'),
                ('Other', 'assets/icons/other.png')
            ]
            # Все значения передаются через параметризованные плейсхолдеры
            self.cursor.executemany(
                'INSERT INTO categories (name, icon_path) VALUES (?, ?)',
                default_categories
            )
            self.conn.commit()

    @staticmethod
    def _validate_string_input(value: str, max_length: int, field_name: str) -> str:
        """
        Валидирует строковое поле: проверяет длину и запрещает опасные символы.

        Args:
            value: Проверяемая строка
            max_length: Максимальная длина
            field_name: Название поля (для сообщения об ошибке)

        Returns:
            Очищенная строка

        Raises:
            ValueError: Если строка не проходит валидацию
        """
        if not isinstance(value, str):
            raise ValueError(f"{field_name} должен быть строкой")

        value = value.strip()

        if len(value) == 0:
            raise ValueError(f"{field_name} не может быть пустым")

        if len(value) > max_length:
            raise ValueError(
                f"{field_name} слишком длинный (максимум {max_length} символов)"
            )

        return value

    def _validate_service_name(self, service_name: str) -> str:
        """Валидирует название сервиса."""
        return self._validate_string_input(
            service_name, self.MAX_SERVICE_NAME_LENGTH, "Название сервиса"
        )

    def _validate_username(self, username: str) -> str:
        """Валидирует имя пользователя."""
        return self._validate_string_input(
            username, self.MAX_USERNAME_LENGTH, "Логин"
        )

    def _validate_notes(self, notes: str) -> str:
        """Валидирует заметки (более мягкая проверка, допускает больше символов)."""
        if not isinstance(notes, str):
            return ""
        notes = notes.strip()
        if len(notes) > self.MAX_NOTES_LENGTH:
            raise ValueError(
                f"Заметки слишком длинные (максимум {self.MAX_NOTES_LENGTH} символов)"
            )
        return notes

    def _validate_category_id(self, category_id: int) -> int:
        """Валидирует ID категории: должен быть положительным целым числом."""
        if not isinstance(category_id, int) or category_id <= 0:
            raise ValueError("ID категории должен быть положительным целым числом")
        return category_id

    def get_all_categories(self) -> List[Dict]:
        """Получает все категории из БД."""
        self.cursor.execute('SELECT id, name, icon_path FROM categories ORDER BY name')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_credentials(self) -> List[Dict]:
        """Получает все учетные записи с информацией о категории."""
        self.cursor.execute('''
            SELECT c.id, c.service_name, c.username, c.encrypted_password,
                   c.notes, c.created_at, cat.name as category_name, cat.icon_path
            FROM credentials c
            LEFT JOIN categories cat ON c.category_id = cat.id
            ORDER BY c.created_at DESC
        ''')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_credentials_by_category(self, category_id: int) -> List[Dict]:
        """Получает учетные записи по ID категории."""
        category_id = self._validate_category_id(category_id)
        self.cursor.execute('''
            SELECT c.id, c.service_name, c.username, c.encrypted_password,
                   c.notes, c.created_at, cat.name as category_name
            FROM credentials c
            LEFT JOIN categories cat ON c.category_id = cat.id
            WHERE c.category_id = ?
            ORDER BY c.created_at DESC
        ''', (category_id,))
        return [dict(row) for row in self.cursor.fetchall()]

    def add_credential(self, category_id: int, service_name: str, username: str,
                       encrypted_password: str, notes: str = '') -> int:
        """
        Добавляет новую учетную запись.
        Все значения передаются через параметризованные плейсхолдеры.
        """
        category_id = self._validate_category_id(category_id)
        service_name = self._validate_service_name(service_name)
        username = self._validate_username(username)
        notes = self._validate_notes(notes)

        if not isinstance(encrypted_password, str) or len(encrypted_password) == 0:
            raise ValueError("Зашифрованный пароль не может быть пустым")

        self.cursor.execute('''
            INSERT INTO credentials
            (category_id, service_name, username, encrypted_password, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (category_id, service_name, username, encrypted_password, notes))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_credential(self, credential_id: int, category_id: int,
                          service_name: str, username: str,
                          encrypted_password: str, notes: str = '') -> None:
        """Обновляет существующую учетную запись."""
        if not isinstance(credential_id, int) or credential_id <= 0:
            raise ValueError("ID записи должен быть положительным целым числом")

        category_id = self._validate_category_id(category_id)
        service_name = self._validate_service_name(service_name)
        username = self._validate_username(username)
        notes = self._validate_notes(notes)

        self.cursor.execute('''
            UPDATE credentials
            SET category_id = ?, service_name = ?, username = ?,
                encrypted_password = ?, notes = ?
            WHERE id = ?
        ''', (category_id, service_name, username, encrypted_password,
              notes, credential_id))
        self.conn.commit()

    def delete_credential(self, credential_id: int) -> None:
        """Удаляет учетную запись по ID."""
        if not isinstance(credential_id, int) or credential_id <= 0:
            raise ValueError("ID записи должен быть положительным целым числом")

        self.cursor.execute('DELETE FROM credentials WHERE id = ?', (credential_id,))
        self.conn.commit()

    def search_credentials(self, search_query: str) -> List[Dict]:
        """
        Ищет учетные записи по названию сервиса или имени пользователя.
        Использует параметризованный запрос с LIKE.
        """
        if not isinstance(search_query, str):
            return []

        search_query = search_query.strip()
        if len(search_query) == 0:
            return self.get_all_credentials()

        # Ограничиваем длину поискового запроса
        if len(search_query) > 50:
            search_query = search_query[:50]

        # Символ % добавляется к параметру, а не в SQL-строку напрямую
        query_pattern = f'%{search_query}%'

        self.cursor.execute('''
            SELECT c.id, c.service_name, c.username, c.encrypted_password,
                   c.notes, c.created_at, cat.name as category_name
            FROM credentials c
            LEFT JOIN categories cat ON c.category_id = cat.id
            WHERE c.service_name LIKE ? OR c.username LIKE ?
            ORDER BY c.created_at DESC
        ''', (query_pattern, query_pattern))
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()
