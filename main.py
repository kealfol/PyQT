"""
Главный модуль приложения SecurePass Manager.
Содержит основной класс MainWindow и точку входа в приложение.
"""

import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog,
    QTableWidgetItem, QHeaderView, QMenu, QDialog,
    QAbstractItemView, QInputDialog, QLineEdit
)
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtGui import QAction, QKeyEvent, QPixmap

from ui.ui_main_window import Ui_MainWindow
from ui.ui_dialog import Ui_AddCredentialDialog
from database import DatabaseManager
from crypto_utils import CryptoManager
from dialogs import PasswordGeneratorDialog, AboutDialog, ChangeMasterKeyDialog
from utils import PathManager, SoundManager


class AddCredentialDialog(QDialog):
    """
    Диалоговое окно добавления/редактирования учетной записи.
    Наследует UI из скомпилированного модуля.
    """

    def __init__(
        self,
        db: DatabaseManager,
        crypto: CryptoManager,
        credential_id: int = None,
        parent=None
    ):
        """
        Инициализация диалога.

        Args:
            db: Менеджер базы данных
            crypto: Менеджер криптографии
            credential_id: ID записи для редактирования (None = новая запись)
            parent: Родительское окно
        """
        super().__init__(parent)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        # Инициализация UI
        self.ui = Ui_AddCredentialDialog()
        self.ui.setupUi(self)

        self.db = db
        self.crypto = crypto
        self.credential_id = credential_id
        self._password_visible = False

        # Загрузка категорий
        self._load_categories()

        # Если редактируем - загружаем данные
        if credential_id:
            self._load_credential_data()
            self.ui.titleLabel.setText("Редактирование записи")

        # Подключение сигналов
        self.ui.togglePasswordButton.clicked.connect(self._toggle_password_visibility)
        self.ui.generateButton.clicked.connect(self._generate_password)

    def _load_categories(self) -> None:
        """Загружает категории в комбобокс."""
        self.ui.categoryComboBox.clear()
        categories = self.db.get_all_categories()

        for category in categories:
            self.ui.categoryComboBox.addItem(
                category['name'],
                category['id']
            )

    def _load_credential_data(self) -> None:
        """Загружает данные записи для редактирования."""
        credentials = self.db.get_all_credentials()

        for cred in credentials:
            if cred['id'] == self.credential_id:
                self.ui.serviceLineEdit.setText(cred['service_name'])
                self.ui.usernameLineEdit.setText(cred['username'])

                try:
                    decrypted_password = self.crypto.decrypt(cred['encrypted_password'])
                    self.ui.passwordLineEdit.setText(decrypted_password)
                except Exception:
                    self.ui.passwordLineEdit.setText("[Ошибка дешифрования]")

                self.ui.notesTextEdit.setPlainText(cred['notes'] or '')

                for i in range(self.ui.categoryComboBox.count()):
                    if self.ui.categoryComboBox.itemData(i) == cred.get('category_id'):
                        self.ui.categoryComboBox.setCurrentIndex(i)
                        break
                break

    def _toggle_password_visibility(self) -> None:
        """Переключает видимость пароля."""
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.ui.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.togglePasswordButton.setText("Скрыть")
        else:
            self.ui.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.togglePasswordButton.setText("Показать")

    def _generate_password(self) -> None:
        """Генерирует случайный пароль и вставляет его в поле."""
        password = CryptoManager.generate_secure_password(16)
        self.ui.passwordLineEdit.setText(password)

    def accept(self) -> None:
        """Валидирует данные, сохраняет запись и закрывает диалог."""
        service_name = self.ui.serviceLineEdit.text().strip()
        username = self.ui.usernameLineEdit.text().strip()
        password = self.ui.passwordLineEdit.text().strip()

        if not service_name:
            QMessageBox.warning(self, "Ошибка", "Введите название сервиса")
            return

        if not username:
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            return

        if not password:
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            return

        category_id = self.ui.categoryComboBox.currentData()
        notes = self.ui.notesTextEdit.toPlainText().strip()

        try:
            encrypted_password = self.crypto.encrypt(password)

            if self.credential_id:
                self.db.update_credential(
                    self.credential_id,
                    category_id,
                    service_name,
                    username,
                    encrypted_password,
                    notes
                )
            else:
                self.db.add_credential(
                    category_id,
                    service_name,
                    username,
                    encrypted_password,
                    notes
                )

            super().accept()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка валидации", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить запись:\n{str(e)}")


class MainWindow(QMainWindow):
    """
    Главное окно приложения SecurePass Manager.
    Наследует UI из скомпилированного модуля и добавляет бизнес-логику.
    """

    def __init__(self):
        """Инициализация главного окна и всех компонентов."""
        super().__init__()

        # Инициализация UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Инициализация менеджеров
        self.db = DatabaseManager()
        self.crypto = CryptoManager()
        self.sound_manager = SoundManager()

        # Загрузка данных
        self._load_categories()
        self._load_credentials()

        # Подключение сигналов
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Подключает все сигналы к слотам."""
        self.ui.addButton.clicked.connect(self._on_add_button_clicked)
        self.ui.deleteButton.clicked.connect(self._on_delete_button_clicked)
        self.ui.exportButton.clicked.connect(self._on_export_button_clicked)
        self.ui.generatePasswordButton.clicked.connect(self._on_generate_password_clicked)

        self.ui.categoryFilterCombo.currentIndexChanged.connect(
            self._on_category_filter_changed
        )
        self.ui.searchLineEdit.textChanged.connect(self._on_search_text_changed)

        self.ui.credentialsTable.cellDoubleClicked.connect(
            self._on_table_double_clicked
        )
        self.ui.credentialsTable.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.credentialsTable.customContextMenuRequested.connect(
            self._on_table_context_menu
        )

        self.ui.actionAbout.triggered.connect(self._on_about_clicked)

    def _load_categories(self) -> None:
        """Загружает категории в комбобокс фильтра."""
        self.ui.categoryFilterCombo.clear()
        self.ui.categoryFilterCombo.addItem("Все категории", 0)

        categories = self.db.get_all_categories()
        for category in categories:
            self.ui.categoryFilterCombo.addItem(
                category['name'],
                category['id']
            )

    def _load_credentials(self, category_id: int = 0, search_query: str = '') -> None:
        """
        Загружает учетные записи в таблицу.

        Args:
            category_id: ID категории для фильтрации (0 = все)
            search_query: Строка для поиска
        """
        self.ui.credentialsTable.setRowCount(0)

        if search_query:
            credentials = self.db.search_credentials(search_query)
        elif category_id > 0:
            credentials = self.db.get_credentials_by_category(category_id)
        else:
            credentials = self.db.get_all_credentials()

        for row_index, credential in enumerate(credentials):
            self.ui.credentialsTable.insertRow(row_index)

            id_item = QTableWidgetItem(str(credential['id']))
            id_item.setData(Qt.ItemDataRole.UserRole, credential['id'])
            self.ui.credentialsTable.setItem(row_index, 0, id_item)

            self.ui.credentialsTable.setItem(
                row_index, 1,
                QTableWidgetItem(credential['service_name'])
            )

            self.ui.credentialsTable.setItem(
                row_index, 2,
                QTableWidgetItem(credential['username'])
            )

            self.ui.credentialsTable.setItem(
                row_index, 3,
                QTableWidgetItem(credential.get('category_name') or 'Без категории')
            )

            self.ui.credentialsTable.setItem(
                row_index, 4,
                QTableWidgetItem(credential['created_at'])
            )

        header = self.ui.credentialsTable.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        count = self.ui.credentialsTable.rowCount()
        self.ui.statusLabel.setText(f"Записей в таблице: {count}")

    # ===== Обработчики кнопок =====

    def _on_add_button_clicked(self) -> None:
        """Открывает диалог добавления новой записи."""
        dialog = AddCredentialDialog(self.db, self.crypto, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_credentials()
            self.sound_manager.play_success()
            self.ui.statusLabel.setText("Запись добавлена")

    def _on_delete_button_clicked(self) -> None:
        """Удаляет выбранную запись после подтверждения."""
        selected_rows = self.ui.credentialsTable.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(
                self,
                "Внимание",
                "Выберите запись для удаления"
            )
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выбранную запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = selected_rows[0].row()
            credential_id = self.ui.credentialsTable.item(row, 0).data(
                Qt.ItemDataRole.UserRole
            )

            self.db.delete_credential(credential_id)
            self._load_credentials()
            self.ui.statusLabel.setText("Запись удалена")

    def _on_export_button_clicked(self) -> None:
        """Экспортирует базу данных в выбранный файл."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт базы данных",
            "",
            "SQLite Database (*.db);;All Files (*)"
        )

        if file_path:
            try:
                shutil.copy(self.db.DB_FILE, file_path)
                QMessageBox.information(
                    self,
                    "Успех",
                    f"База данных успешно экспортирована в:\n{file_path}"
                )
                self.ui.statusLabel.setText("База данных экспортирована")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Не удалось экспортировать базу данных:\n{str(e)}"
                )

    def _on_generate_password_clicked(self) -> None:
        """Открывает диалог генератора паролей."""
        dialog = PasswordGeneratorDialog(parent=self)
        dialog.exec()

    def _on_about_clicked(self) -> None:
        """Открывает диалог 'О программе'."""
        dialog = AboutDialog(parent=self)
        dialog.exec()

    # ===== Обработчики фильтров и поиска =====

    def _on_category_filter_changed(self, index: int) -> None:
        """Обработчик изменения фильтра по категории."""
        category_id = self.ui.categoryFilterCombo.itemData(index)
        self._load_credentials(category_id=category_id)

    def _on_search_text_changed(self, text: str) -> None:
        """Обработчик изменения текста поиска."""
        self._load_credentials(search_query=text)

    # ===== Обработчики событий мыши =====

    def _on_table_double_clicked(self, row: int, column: int) -> None:
        """
        Обработчик двойного клика по таблице.
        Открывает диалог редактирования записи.
        """
        credential_id = self.ui.credentialsTable.item(row, 0).data(
            Qt.ItemDataRole.UserRole
        )

        dialog = AddCredentialDialog(
            self.db,
            self.crypto,
            credential_id=credential_id,
            parent=self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_credentials()
            self.sound_manager.play_success()
            self.ui.statusLabel.setText("Запись обновлена")

    def _on_table_context_menu(self, position) -> None:
        """
        Обработчик контекстного меню таблицы (правый клик мыши).
        """
        row = self.ui.credentialsTable.rowAt(position.y())
        if row < 0:
            return

        menu = QMenu(self)
        menu.setStyleSheet(
            "QMenu { background-color: #FFFFFF; color: #1A202C; }"
            "QMenu::item:selected { background-color: #BEE3F8; }"
        )

        copy_username_action = QAction("Копировать логин", self)
        copy_username_action.triggered.connect(
            lambda: self._copy_to_clipboard(row, 2)
        )
        menu.addAction(copy_username_action)

        copy_password_action = QAction("Копировать пароль", self)
        copy_password_action.triggered.connect(
            lambda: self._copy_password_to_clipboard(row)
        )
        menu.addAction(copy_password_action)

        menu.addSeparator()

        edit_action = QAction("Редактировать", self)
        edit_action.triggered.connect(
            lambda: self._on_table_double_clicked(row, 0)
        )
        menu.addAction(edit_action)

        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self._on_delete_button_clicked)
        menu.addAction(delete_action)

        menu.exec(self.ui.credentialsTable.viewport().mapToGlobal(position))

    def _copy_to_clipboard(self, row: int, column: int) -> None:
        """
        Копирует текст из ячейки в буфер обмена.

        Args:
            row: Номер строки
            column: Номер столбца
        """
        item = self.ui.credentialsTable.item(row, column)
        if item:
            clipboard = QApplication.clipboard()
            clipboard.setText(item.text())
            self.sound_manager.play_success()
            self.ui.statusLabel.setText(f"Скопировано: {item.text()}")

    def _copy_password_to_clipboard(self, row: int) -> None:
        """
        Дешифрует и копирует пароль в буфер обмена.

        Args:
            row: Номер строки
        """
        credential_id = self.ui.credentialsTable.item(row, 0).data(
            Qt.ItemDataRole.UserRole
        )
        credentials = self.db.get_all_credentials()

        for cred in credentials:
            if cred['id'] == credential_id:
                try:
                    decrypted_password = self.crypto.decrypt(cred['encrypted_password'])
                    clipboard = QApplication.clipboard()
                    clipboard.setText(decrypted_password)
                    self.sound_manager.play_success()
                    self.ui.statusLabel.setText("Пароль скопирован")
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Ошибка",
                        f"Не удалось дешифровать пароль:\n{str(e)}"
                    )
                break

    # ===== Обработчики событий клавиатуры =====

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Обработчик нажатий клавиш.

        Args:
            event: Событие нажатия клавиши
        """
        if (
            event.modifiers() == Qt.KeyboardModifier.ControlModifier
            and event.key() == Qt.Key.Key_F
        ):
            self.ui.searchLineEdit.setFocus()
            self.ui.searchLineEdit.selectAll()
            self.ui.statusLabel.setText("Поиск активирован")

        elif (
            event.modifiers() == Qt.KeyboardModifier.ControlModifier
            and event.key() == Qt.Key.Key_N
        ):
            self._on_add_button_clicked()

        elif event.key() == Qt.Key.Key_Delete:
            self._on_delete_button_clicked()

        elif event.key() == Qt.Key.Key_F5:
            self._load_credentials()
            self.ui.statusLabel.setText("Таблица обновлена")

        elif event.key() == Qt.Key.Key_F2:
            self._on_change_master_key()

        elif event.key() == Qt.Key.Key_Escape:
            self.close()

        else:
            super().keyPressEvent(event)

    def _on_change_master_key(self) -> None:
        """
        Демонстрация QInputDialog и смены мастер-ключа.
        Вызывается по F2.
        """
        new_key_name, ok = QInputDialog.getText(
            self,
            "Смена мастер-ключа",
            "Введите имя нового ключа (для подтверждения):",
            QLineEdit.EchoMode.Normal,
            ""
        )

        if ok and new_key_name.strip():
            dialog = ChangeMasterKeyDialog(parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if os.path.exists(CryptoManager.KEY_FILE):
                    os.remove(CryptoManager.KEY_FILE)
                QMessageBox.information(
                    self,
                    "Успех",
                    "Мастер-ключ сброшен. При следующем запуске будет создан новый."
                )
                self.ui.statusLabel.setText("Мастер-ключ сброшен")

    def closeEvent(self, event) -> None:
        """
        Обработчик закрытия окна.
        Закрывает соединение с БД.
        """
        self.db.close()
        event.accept()


def main():
    """Точка входа в приложение."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
