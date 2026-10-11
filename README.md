# SecurePass Manager

Менеджер паролей на Python с PyQt6. Хранит учетные данные в зашифрованном виде в локальной SQLite базе.

## Что умеет

- Добавлять, редактировать и удалять записи (сервис, логин, пароль, категория, заметки)
- Шифровать пароли алгоритмом Fernet (AES-128) перед записью в БД
- Генерировать случайные пароли заданной длины
- Искать по названию сервиса и логину
- Фильтровать записи по категориям
- Экспортировать базу данных в файл
- Копировать логин или пароль в буфер обмена через контекстное меню

## Технологии

- Python 3.10+
- PyQt6 — интерфейс
- SQLite3 — база данных
- cryptography (Fernet) — шифрование
- PyInstaller — сборка в exe

## Структура проекта

securepass-manager/

── main.py — точка входа, главное окно
│
├── database.py — работа с БД, CRUD-операции
│
├── crypto_utils.py — шифрование и генерация паролей
│
├── dialogs.py — диалоги (генератор паролей, о программе)
│
├── utils.py — пути к ресурсам, воспроизведение звуков
│
├── ui/
│
│ ├── init.py
│
│ ├── ui_main_window.py — интерфейс главного окна
│
│ └── ui_dialog.py — интерфейс диалога добавления записи
│
├── assets/
│
│ ├── icons/
│
│ └── sounds/
│
├── requirements.txt
│
└── README.md


## База данных

Две таблицы, связаны внешним ключом:

**categories** — справочник категорий (Social, Work, Finance, Email, Other)
- id, name, icon_path

**credentials** — учетные записи
- id, category_id (FK), service_name, username, encrypted_password, notes, created_at

Все запросы к БД используют параметризованные плейсхолдеры `?`, значения не конкатенируются в SQL-строку. Входные данные валидируются по типу и длине перед записью.

## Запуск из исходников

```bash
python -m venv venv
source venv/bin/activate      # Linux
.\venv\Scripts\activate       # Windows

pip install -r requirements.txt
python main.py
