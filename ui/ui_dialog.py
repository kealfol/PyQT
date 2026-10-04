# -*- coding: utf-8 -*-
"""
Скомпилированный модуль диалогового окна для PyQt6.
Светлая тема: белый фон, синие акценты.
"""

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddCredentialDialog(object):
    """Класс интерфейса диалога добавления/редактирования учетной записи."""

    def setupUi(self, Dialog):
        """Настраивает все виджеты диалогового окна."""
        Dialog.setObjectName("AddCredentialDialog")
        Dialog.resize(500, 450)
        Dialog.setMinimumSize(QtCore.QSize(450, 400))
        Dialog.setStyleSheet(
            "QDialog { background-color: #F5F7FA; color: #1A202C; }"
        )

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")

        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setStyleSheet(
            "font-size: 18pt; font-weight: bold; color: #2B6CB0;"
        )
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setText("Новая учетная запись")
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")

        self.serviceLabel = QtWidgets.QLabel("Название сервиса:")
        self.serviceLabel.setStyleSheet("color: #1A202C; font-weight: bold;")
        self.serviceLabel.setObjectName("serviceLabel")

        self.serviceLineEdit = QtWidgets.QLineEdit()
        self.serviceLineEdit.setPlaceholderText("Например: GitHub, Google, VK")
        self.serviceLineEdit.setStyleSheet(
            "QLineEdit { background-color: #FFFFFF; color: #1A202C; "
            "border: 1px solid #CBD5E0; border-radius: 5px; padding: 5px; }"
        )
        self.serviceLineEdit.setObjectName("serviceLineEdit")
        self.formLayout.addRow(self.serviceLabel, self.serviceLineEdit)

        self.usernameLabel = QtWidgets.QLabel("Логин / Email:")
        self.usernameLabel.setStyleSheet("color: #1A202C; font-weight: bold;")
        self.usernameLabel.setObjectName("usernameLabel")

        self.usernameLineEdit = QtWidgets.QLineEdit()
        self.usernameLineEdit.setPlaceholderText("user@example.com")
        self.usernameLineEdit.setStyleSheet(
            "QLineEdit { background-color: #FFFFFF; color: #1A202C; "
            "border: 1px solid #CBD5E0; border-radius: 5px; padding: 5px; }"
        )
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.addRow(self.usernameLabel, self.usernameLineEdit)

        self.categoryLabel = QtWidgets.QLabel("Категория:")
        self.categoryLabel.setStyleSheet("color: #1A202C; font-weight: bold;")
        self.categoryLabel.setObjectName("categoryLabel")

        self.categoryComboBox = QtWidgets.QComboBox()
        self.categoryComboBox.setStyleSheet(
            "QComboBox { background-color: #FFFFFF; color: #1A202C; "
            "border: 1px solid #CBD5E0; border-radius: 5px; padding: 5px; }"
            "QComboBox::drop-down { border: none; }"
            "QComboBox QAbstractItemView { background-color: #FFFFFF; "
            "color: #1A202C; selection-background-color: #BEE3F8; }"
        )
        self.categoryComboBox.setObjectName("categoryComboBox")
        self.formLayout.addRow(self.categoryLabel, self.categoryComboBox)

        self.passwordLabel = QtWidgets.QLabel("Пароль:")
        self.passwordLabel.setStyleSheet("color: #1A202C; font-weight: bold;")
        self.passwordLabel.setObjectName("passwordLabel")

        self.passwordLayout = QtWidgets.QHBoxLayout()
        self.passwordLayout.setObjectName("passwordLayout")

        self.passwordLineEdit = QtWidgets.QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Введите или сгенерируйте пароль")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordLineEdit.setStyleSheet(
            "QLineEdit { background-color: #FFFFFF; color: #1A202C; "
            "border: 1px solid #CBD5E0; border-radius: 5px; padding: 5px; }"
        )
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordLayout.addWidget(self.passwordLineEdit)

        self.togglePasswordButton = QtWidgets.QPushButton("Показать")
        self.togglePasswordButton.setFixedSize(80, 30)
        self.togglePasswordButton.setStyleSheet(
            "QPushButton { background-color: #E2E8F0; color: #1A202C; "
            "border-radius: 5px; }"
            "QPushButton:hover { background-color: #CBD5E0; }"
        )
        self.togglePasswordButton.setObjectName("togglePasswordButton")
        self.passwordLayout.addWidget(self.togglePasswordButton)

        self.generateButton = QtWidgets.QPushButton("Ген.")
        self.generateButton.setFixedSize(50, 30)
        self.generateButton.setToolTip("Сгенерировать случайный пароль")
        self.generateButton.setStyleSheet(
            "QPushButton { background-color: #48BB78; color: #FFFFFF; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #38A169; }"
        )
        self.generateButton.setObjectName("generateButton")
        self.passwordLayout.addWidget(self.generateButton)

        self.formLayout.addRow(self.passwordLabel, self.passwordLayout)

        self.notesLabel = QtWidgets.QLabel("Заметки:")
        self.notesLabel.setStyleSheet("color: #1A202C; font-weight: bold;")
        self.notesLabel.setObjectName("notesLabel")

        self.notesTextEdit = QtWidgets.QTextEdit()
        self.notesTextEdit.setPlaceholderText("Дополнительная информация (необязательно)")
        self.notesTextEdit.setMaximumHeight(80)
        self.notesTextEdit.setStyleSheet(
            "QTextEdit { background-color: #FFFFFF; color: #1A202C; "
            "border: 1px solid #CBD5E0; border-radius: 5px; padding: 5px; }"
        )
        self.notesTextEdit.setObjectName("notesTextEdit")
        self.formLayout.addRow(self.notesLabel, self.notesTextEdit)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setObjectName("buttonLayout")

        self.buttonLayout.addStretch()

        self.cancelButton = QtWidgets.QPushButton("Отмена")
        self.cancelButton.setStyleSheet(
            "QPushButton { background-color: #E2E8F0; color: #1A202C; "
            "border-radius: 5px; padding: 8px 20px; }"
            "QPushButton:hover { background-color: #CBD5E0; }"
        )
        self.cancelButton.setObjectName("cancelButton")
        self.buttonLayout.addWidget(self.cancelButton)

        self.saveButton = QtWidgets.QPushButton("Сохранить")
        self.saveButton.setStyleSheet(
            "QPushButton { background-color: #3182CE; color: #FFFFFF; "
            "border-radius: 5px; padding: 8px 20px; font-weight: bold; }"
            "QPushButton:hover { background-color: #2B6CB0; }"
        )
        self.saveButton.setObjectName("saveButton")
        self.buttonLayout.addWidget(self.saveButton)

        self.verticalLayout.addLayout(self.buttonLayout)

        self.cancelButton.clicked.connect(Dialog.reject)
        self.saveButton.clicked.connect(Dialog.accept)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        """Устанавливает переводы для виджетов."""
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(
            _translate("AddCredentialDialog", "Добавление учетной записи")
        )
