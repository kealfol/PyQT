# -*- coding: utf-8 -*-
"""
Скомпилированный модуль диалогового окна для PyQt6.
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
            "QDialog { background-color: #1e1e2e; color: #cdd6f4; }"
        )
        
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setStyleSheet(
            "font-size: 18pt; font-weight: bold; color: #89b4fa;"
        )
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setText("🔑 Новая учетная запись")
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        
        self.serviceLabel = QtWidgets.QLabel("Название сервиса:")
        self.serviceLabel.setStyleSheet("color: #cdd6f4; font-weight: bold;")
        self.serviceLabel.setObjectName("serviceLabel")
        
        self.serviceLineEdit = QtWidgets.QLineEdit()
        self.serviceLineEdit.setPlaceholderText("Например: GitHub, Google, VK")
        self.serviceLineEdit.setStyleSheet(
            "QLineEdit { background-color: #313244; color: #cdd6f4; "
            "border: 1px solid #45475a; border-radius: 5px; padding: 5px; }"
        )
        self.serviceLineEdit.setObjectName("serviceLineEdit")
        self.formLayout.addRow(self.serviceLabel, self.serviceLineEdit)
        
        self.usernameLabel = QtWidgets.QLabel("Логин / Email:")
        self.usernameLabel.setStyleSheet("color: #cdd6f4; font-weight: bold;")
        self.usernameLabel.setObjectName("usernameLabel")
        
        self.usernameLineEdit = QtWidgets.QLineEdit()
        self.usernameLineEdit.setPlaceholderText("user@example.com")
        self.usernameLineEdit.setStyleSheet(
            "QLineEdit { background-color: #313244; color: #cdd6f4; "
            "border: 1px solid #45475a; border-radius: 5px; padding: 5px; }"
        )
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.addRow(self.usernameLabel, self.usernameLineEdit)
        
        self.categoryLabel = QtWidgets.QLabel("Категория:")
        self.categoryLabel.setStyleSheet("color: #cdd6f4; font-weight: bold;")
        self.categoryLabel.setObjectName("categoryLabel")
        
        self.categoryComboBox = QtWidgets.QComboBox()
        self.categoryComboBox.setStyleSheet(
            "QComboBox { background-color: #313244; color: #cdd6f4; "
            "border: 1px solid #45475a; border-radius: 5px; padding: 5px; }"
            "QComboBox::drop-down { border: none; }"
            "QComboBox QAbstractItemView { background-color: #313244; "
            "color: #cdd6f4; selection-background-color: #45475a; }"
        )
        self.categoryComboBox.setObjectName("categoryComboBox")
        self.formLayout.addRow(self.categoryLabel, self.categoryComboBox)
        
        self.passwordLabel = QtWidgets.QLabel("Пароль:")
        self.passwordLabel.setStyleSheet("color: #cdd6f4; font-weight: bold;")
        self.passwordLabel.setObjectName("passwordLabel")
        
        self.passwordLayout = QtWidgets.QHBoxLayout()
        self.passwordLayout.setObjectName("passwordLayout")
        
        self.passwordLineEdit = QtWidgets.QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Введите или сгенерируйте пароль")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordLineEdit.setStyleSheet(
            "QLineEdit { background-color: #313244; color: #cdd6f4; "
            "border: 1px solid #45475a; border-radius: 5px; padding: 5px; }"
        )
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordLayout.addWidget(self.passwordLineEdit)
        
        self.togglePasswordButton = QtWidgets.QPushButton("👁")
        self.togglePasswordButton.setFixedSize(35, 30)
        self.togglePasswordButton.setStyleSheet(
            "QPushButton { background-color: #45475a; color: #cdd6f4; "
            "border-radius: 5px; }"
            "QPushButton:hover { background-color: #585b70; }"
        )
        self.togglePasswordButton.setObjectName("togglePasswordButton")
        self.passwordLayout.addWidget(self.togglePasswordButton)
        
        self.generateButton = QtWidgets.QPushButton("")
        self.generateButton.setFixedSize(35, 30)
        self.generateButton.setToolTip("Сгенерировать случайный пароль")
        self.generateButton.setStyleSheet(
            "QPushButton { background-color: #a6e3a1; color: #1e1e2e; "
            "border-radius: 5px; font-weight: bold; }"
            "QPushButton:hover { background-color: #94e2d5; }"
        )
        self.generateButton.setObjectName("generateButton")
        self.passwordLayout.addWidget(self.generateButton)
        
        self.formLayout.addRow(self.passwordLabel, self.passwordLayout)
        
        self.notesLabel = QtWidgets.QLabel("Заметки:")
        self.notesLabel.setStyleSheet("color: #cdd6f4; font-weight: bold;")
        self.notesLabel.setObjectName("notesLabel")
        
        self.notesTextEdit = QtWidgets.QTextEdit()
        self.notesTextEdit.setPlaceholderText("Дополнительная информация (необязательно)")
        self.notesTextEdit.setMaximumHeight(80)
        self.notesTextEdit.setStyleSheet(
            "QTextEdit { background-color: #313244; color: #cdd6f4; "
            "border: 1px solid #45475a; border-radius: 5px; padding: 5px; }"
        )
        self.notesTextEdit.setObjectName("notesTextEdit")
        self.formLayout.addRow(self.notesLabel, self.notesTextEdit)
        
        self.verticalLayout.addLayout(self.formLayout)
        
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setObjectName("buttonLayout")
        
        self.buttonLayout.addStretch()
        
        self.cancelButton = QtWidgets.QPushButton("❌ Отмена")
        self.cancelButton.setStyleSheet(
            "QPushButton { background-color: #45475a; color: #cdd6f4; "
            "border-radius: 5px; padding: 8px 20px; }"
            "QPushButton:hover { background-color: #585b70; }"
        )
        self.cancelButton.setObjectName("cancelButton")
        self.buttonLayout.addWidget(self.cancelButton)
        
        self.saveButton = QtWidgets.QPushButton("💾 Сохранить")
        self.saveButton.setStyleSheet(
            "QPushButton { background-color: #89b4fa; color: #1e1e2e; "
            "border-radius: 5px; padding: 8px 20px; font-weight: bold; }"
            "QPushButton:hover { background-color: #74c7ec; }"
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
