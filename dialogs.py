"""
Модуль дополнительных диалоговых окон приложения SecurePass Manager.
Содержит диалоги генератора паролей, информации о программе и смены ключа.
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QCheckBox, QLineEdit, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from crypto_utils import CryptoManager
from utils import PathManager, SoundManager


class PasswordGeneratorDialog(QDialog):
    """Диалоговое окно генератора паролей."""
    
    def __init__(self, parent=None):
        """Инициализация диалога генератора паролей."""
        super().__init__(parent)
        self.setWindowTitle("🎲 Генератор паролей")
        self.setFixedSize(450, 400)
        self.setStyleSheet(
            "QDialog { background-color: #1e1e2e; color: #cdd6f4; }"
        )
        self._sound_manager = SoundManager()
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Настраивает интерфейс диалога."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title = QLabel("🎲 Генератор безопасных паролей")
        title.setStyleSheet(
            "font-size: 16pt; font-weight: bold; color: #89b4fa;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Поле для отображения пароля
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setReadOnly(True)
        self.passwordLineEdit.setStyleSheet(
            "QLineEdit { background-color: #313244; color: #a6e3a1; "
            "border: 2px solid #45475a; border-radius: 5px; padding: 10px; "
            "font-size: 12pt; font-family: monospace; }"
        )
        self.passwordLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.passwordLineEdit)
        
        # Настройки генерации
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(10)
        
        # Длина пароля
        length_layout = QHBoxLayout()
        length_label = QLabel("Длина пароля:")
        length_label.setStyleSheet("font-weight: bold;")
        length_layout.addWidget(length_label)
        
        self.lengthSpinBox = QSpinBox()
        self.lengthSpinBox.setMinimum(8)
        self.lengthSpinBox.setMaximum(64)
        self.lengthSpinBox.setValue(16)
        self.lengthSpinBox.setStyleSheet(
            "QSpinBox { background-color: #313244; color: #cdd6f4; "
            "border: 1px solid #45475a; border-radius: 5px; padding: 5px; }"
        )
        length_layout.addWidget(self.lengthSpinBox)
        settings_layout.addLayout(length_layout)
        
        # Чекбоксы для типов символов
        self.uppercaseCheckBox = QCheckBox("Заглавные буквы (A-Z)")
        self.uppercaseCheckBox.setChecked(True)
        self.uppercaseCheckBox.setStyleSheet("color: #cdd6f4;")
        settings_layout.addWidget(self.uppercaseCheckBox)
        
        self.lowercaseCheckBox = QCheckBox("Строчные буквы (a-z)")
        self.lowercaseCheckBox.setChecked(True)
        self.lowercaseCheckBox.setStyleSheet("color: #cdd6f4;")
        settings_layout.addWidget(self.lowercaseCheckBox)
        
        self.digitsCheckBox = QCheckBox("Цифры (0-9)")
        self.digitsCheckBox.setChecked(True)
        self.digitsCheckBox.setStyleSheet("color: #cdd6f4;")
        settings_layout.addWidget(self.digitsCheckBox)
        
        self.symbolsCheckBox = QCheckBox("Специальные символы (!@#$%)")
        self.symbolsCheckBox.setChecked(True)
        self.symbolsCheckBox.setStyleSheet("color: #cdd6f4;")
        settings_layout.addWidget(self.symbolsCheckBox)
        
        layout.addLayout(settings_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.generateButton = QPushButton("🎲 Сгенерировать")
        self.generateButton.setStyleSheet(
            "QPushButton { background-color: #a6e3a1; color: #1e1e2e; "
            "border-radius: 5px; padding: 10px 20px; font-weight: bold; }"
            "QPushButton:hover { background-color: #94e2d5; }"
        )
        self.generateButton.clicked.connect(self._generate_password)
        buttons_layout.addWidget(self.generateButton)
        
        self.copyButton = QPushButton(" Копировать")
        self.copyButton.setStyleSheet(
            "QPushButton { background-color: #89b4fa; color: #1e1e2e; "
            "border-radius: 5px; padding: 10px 20px; font-weight: bold; }"
            "QPushButton:hover { background-color: #74c7ec; }"
        )
        self.copyButton.clicked.connect(self._copy_to_clipboard)
        buttons_layout.addWidget(self.copyButton)
        
        self.closeButton = QPushButton("❌ Закрыть")
        self.closeButton.setStyleSheet(
            "QPushButton { background-color: #45475a; color: #cdd6f4; "
            "border-radius: 5px; padding: 10px 20px; }"
            "QPushButton:hover { background-color: #585b70; }"
        )
        self.closeButton.clicked.connect(self.close)
        buttons_layout.addWidget(self.closeButton)
        
        layout.addLayout(buttons_layout)
        
        # Генерируем пароль при открытии
        self._generate_password()
    
    def _generate_password(self) -> None:
        """Генерирует пароль с учетом настроек."""
        length = self.lengthSpinBox.value()
        
        if not any([
            self.uppercaseCheckBox.isChecked(),
            self.lowercaseCheckBox.isChecked(),
            self.digitsCheckBox.isChecked(),
            self.symbolsCheckBox.isChecked()
        ]):
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите хотя бы один тип символов"
            )
            return
        
        # Собираем алфавит по выбранным чекбоксам
        import string
        import secrets
        alphabet = ""
        if self.uppercaseCheckBox.isChecked():
            alphabet += string.ascii_uppercase
        if self.lowercaseCheckBox.isChecked():
            alphabet += string.ascii_lowercase
        if self.digitsCheckBox.isChecked():
            alphabet += string.digits
        if self.symbolsCheckBox.isChecked():
            alphabet += string.punctuation
        
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        self.passwordLineEdit.setText(password)
    
    def _copy_to_clipboard(self) -> None:
        """Копирует пароль в буфер обмена."""
        password = self.passwordLineEdit.text()
        if password:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            self._sound_manager.play_success()
            QMessageBox.information(
                self,
                "Успех",
                "Пароль скопирован в буфер обмена"
            )


class AboutDialog(QDialog):
    """Диалоговое окно 'О программе'."""
    
    def __init__(self, parent=None):
        """Инициализация диалога 'О программе'."""
        super().__init__(parent)
        self.setWindowTitle("️ О программе")
        self.setFixedSize(500, 450)
        self.setStyleSheet(
            "QDialog { background-color: #1e1e2e; color: #cdd6f4; }"
        )
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Настраивает интерфейс диалога."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Логотип приложения (мультимедиа - картинка)
        logo_path = PathManager.get_resource_path("assets/icons/logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap.scaled(
                    80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
                logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(logo_label)
        
        # Заголовок
        title = QLabel("🔐 SecurePass Manager")
        title.setStyleSheet(
            "font-size: 20pt; font-weight: bold; color: #89b4fa;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Версия
        version = QLabel("Версия 1.0.0")
        version.setStyleSheet("font-size: 12pt; color: #a6adc8;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        # Описание
        description = QTextEdit()
        description.setReadOnly(True)
        description.setStyleSheet(
            "QTextEdit { background-color: #313244; color: #cdd6f4; "
            "border: 1px solid #45475a; border-radius: 5px; padding: 10px; "
            "font-size: 10pt; }"
        )
        description.setHtml("""
            <p style='text-align: center;'>
            <b>Менеджер безопасных паролей</b><br><br>
            
            Приложение для безопасного хранения и управления учетными данными.<br>
            Использует симметричное шифрование AES-128 для защиты паролей.<br><br>
            
            <b>Возможности:</b><br>
            • Создание и хранение зашифрованных паролей<br>
            • Категоризация учетных записей<br>
            • Генерация криптографически стойких паролей<br>
            • Быстрый поиск и фильтрация<br>
            • Экспорт базы данных<br><br>
            
            <b>Технологии:</b><br>
            • Python 3.10+<br>
            • PyQt6 (GUI)<br>
            • SQLite (база данных)<br>
            • cryptography.fernet (шифрование)<br><br>
            
            <b>Разработано:</b><br>
            В учебных целях для демонстрации навыков разработки<br>
            десктопных приложений с соблюдением принципов<br>
            информационной безопасности.
            </p>
        """)
        layout.addWidget(description)
        
        # Кнопка закрытия
        closeButton = QPushButton("Закрыть")
        closeButton.setStyleSheet(
            "QPushButton { background-color: #89b4fa; color: #1e1e2e; "
            "border-radius: 5px; padding: 10px 30px; font-weight: bold; }"
            "QPushButton:hover { background-color: #74c7ec; }"
        )
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton, alignment=Qt.AlignmentFlag.AlignCenter)


class ChangeMasterKeyDialog(QDialog):
    """Диалог смены мастер-ключа шифрования."""
    
    def __init__(self, parent=None):
        """Инициализация диалога смены ключа."""
        super().__init__(parent)
        self.setWindowTitle(" Смена мастер-ключа")
        self.setFixedSize(400, 200)
        self.setStyleSheet(
            "QDialog { background-color: #1e1e2e; color: #cdd6f4; }"
        )
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Настраивает интерфейс диалога."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        warning = QLabel(
            "⚠️ Внимание! Смена ключа сделает все старые пароли "
            "недоступными для расшифровки. Рекомендуется сделать резервную копию БД."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet("color: #f9e2af;")
        layout.addWidget(warning)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet(
            "QPushButton { background-color: #45475a; color: #cdd6f4; "
            "border-radius: 5px; padding: 8px 20px; }"
        )
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        confirm_button = QPushButton("Сменить ключ")
        confirm_button.setStyleSheet(
            "QPushButton { background-color: #f38ba8; color: #1e1e2e; "
            "border-radius: 5px; padding: 8px 20px; font-weight: bold; }"
        )
        confirm_button.clicked.connect(self._confirm_change)
        buttons_layout.addWidget(confirm_button)
        
        layout.addLayout(buttons_layout)
    
    def _confirm_change(self) -> None:
        """Подтверждает смену ключа."""
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены? Все старые пароли станут недоступны!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.accept()
