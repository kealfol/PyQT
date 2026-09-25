"""
Модуль для работы с базой данных SQLite.
Реализует CRUD операции для управления категориями и учетными записями.
"""

import sqlite3
from typing import List, Dict


class DatabaseManager:
    """Менеджер базы данных."""
    
    DB_FILE = "securepass.db"
    
    def __init__(self):
        """Инициализация менеджера БД и создание таблиц."""
        self.conn = sqlite3.connect(self.DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Доступ к полям по имени
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
                ('Соцсети', 'assets/icons/social.png'),
                ('Работа', 'assets/icons/work.png'),
                ('Финансы', 'assets/icons/finance.png'),
                ('Почта', 'assets/icons/email.png'),
                ('Другое', 'assets/icons/other.png')
            ]
            self.cursor.executemany(
                'INSERT INTO categories (name, icon_path) VALUES (?, ?)',
                default_categories
            )
            self.conn.commit()
    
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
        """Добавляет новую учетную запись."""
        self.cursor.execute('''
            INSERT INTO credentials (category_id, service_name, username, encrypted_password, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (category_id, service_name, username, encrypted_password, notes))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_credential(self, credential_id: int, category_id: int, service_name: str, 
                          username: str, encrypted_password: str, notes: str = '') -> None:
        """Обновляет существующую учетную запись."""
        self.cursor.execute('''
            UPDATE credentials
            SET category_id = ?, service_name = ?, username = ?, encrypted_password = ?, notes = ?
            WHERE id = ?
        ''', (category_id, service_name, username, encrypted_password, notes, credential_id))
        self.conn.commit()
    
    def delete_credential(self, credential_id: int) -> None:
        """Удаляет учетную запись по ID."""
        self.cursor.execute('DELETE FROM credentials WHERE id = ?', (credential_id,))
        self.conn.commit()
    
    def search_credentials(self, search_query: str) -> List[Dict]:
        """Ищет учетные записи по названию сервиса или имени пользователя."""
        query = f'%{search_query}%'
        self.cursor.execute('''
            SELECT c.id, c.service_name, c.username, c.encrypted_password, 
                   c.notes, c.created_at, cat.name as category_name
            FROM credentials c
            LEFT JOIN categories cat ON c.category_id = cat.id
            WHERE c.service_name LIKE ? OR c.username LIKE ?
            ORDER BY c.created_at DESC
        ''', (query, query))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()
