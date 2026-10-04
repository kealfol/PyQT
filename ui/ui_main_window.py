# -*- coding: utf-8 -*-
"""
Скомпилированный модуль главного окна приложения для PyQt6.
Светлая тема: белый фон, синие акценты.
"""

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """Класс интерфейса главного окна приложения."""

    def setupUi(self, MainWindow):
        """Настраивает все виджеты главного окна."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))

        MainWindow.setStyleSheet(
            "QMainWindow { background-color: #F5F7FA; color: #1A202C; }"
        )

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")

        # Заголовок
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setStyleSheet(
            "font-size: 24pt; font-weight: bold; color: #2B6CB0;"
        )
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setText("SecurePass Manager")
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)

        # Панель управления
        self.controlsLayout = QtWidgets.QHBoxLayout()
        self.controlsLayout.setSpacing(10)
        self.controlsLayout.setObjectName("controlsLayout")

        self.categoryFilterCombo = QtWidgets.QComboBox(self.centralwidget)
        self.categoryFilterCombo.setMinimumSize(QtCore.QSize(200, 0))
        self.categoryFilterCombo.setStyleSheet(
            "QComboBox { background-color: #FFFFFF; color: #1A202C; "
            "border: 1px solid #CBD5E0; border-radius: 5px; padding: 5px; }"
            "QComboBox::drop-down { border: none; }"
            "QComboBox QAbstractItemView { background-color: #FFFFFF; "
            "color: #1A202C; selection-background-color: #BEE3F8; }"
        )
        self.categoryFilterCombo.setObjectName("categoryFilterCombo")
        self.controlsLayout.addWidget(self.categoryFilterCombo)

        self.searchLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchLineEdit.setPlaceholderText("Поиск по сервису или логину...")
        self.searchLineEdit.setStyleSheet(
            "QLineEdit { background-color: #FFFFFF; color: #1A202C; "
            "border: 1px solid #CBD5E0; border-radius: 5px; padding: 5px; }"
        )
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.controlsLayout.addWidget(self.searchLineEdit)

        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setStyleSheet(
            "QPushButton { background-color: #3182CE; color: #FFFFFF; "
            "border-radius: 5px; padding: 8px 16px; font-weight: bold; }"
            "QPushButton:hover { background-color: #2B6CB0; }"
        )
        self.addButton.setText("Добавить запись")
        self.addButton.setObjectName("addButton")
        self.controlsLayout.addWidget(self.addButton)

        self.generatePasswordButton = QtWidgets.QPushButton(self.centralwidget)
        self.generatePasswordButton.setStyleSheet(
            "QPushButton { background-color: #4299E1; color: #FFFFFF; "
            "border-radius: 5px; padding: 8px 16px; font-weight: bold; }"
            "QPushButton:hover { background-color: #3182CE; }"
        )
        self.generatePasswordButton.setText("Генератор паролей")
        self.generatePasswordButton.setObjectName("generatePasswordButton")
        self.controlsLayout.addWidget(self.generatePasswordButton)

        self.verticalLayout.addLayout(self.controlsLayout)

        # Таблица
        self.credentialsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.credentialsTable.setColumnCount(5)
        self.credentialsTable.setHorizontalHeaderLabels([
            "ID", "Сервис", "Логин", "Категория", "Дата создания"
        ])
        self.credentialsTable.setStyleSheet(
            "QTableWidget { background-color: #FFFFFF; color: #1A202C; "
            "alternate-background-color: #EBF4FF; border: 1px solid #CBD5E0; "
            "gridline-color: #E2E8F0; }"
            "QTableWidget::item:selected { background-color: #BEE3F8; color: #1A202C; }"
            "QHeaderView::section { background-color: #E2E8F0; color: #1A202C; "
            "padding: 5px; border: 1px solid #CBD5E0; font-weight: bold; }"
        )
        self.credentialsTable.setAlternatingRowColors(True)
        self.credentialsTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.credentialsTable.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.credentialsTable.horizontalHeader().setStretchLastSection(True)
        self.credentialsTable.verticalHeader().setVisible(False)
        self.credentialsTable.setObjectName("credentialsTable")
        self.verticalLayout.addWidget(self.credentialsTable)

        # Нижняя панель
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.setObjectName("bottomLayout")

        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setText("")
        self.statusLabel.setStyleSheet("color: #718096;")
        self.statusLabel.setObjectName("statusLabel")
        self.bottomLayout.addWidget(self.statusLabel)

        self.bottomLayout.addStretch()

        self.exportButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportButton.setStyleSheet(
            "QPushButton { background-color: #ED8936; color: #FFFFFF; "
            "border-radius: 5px; padding: 5px 10px; }"
            "QPushButton:hover { background-color: #DD6B20; }"
        )
        self.exportButton.setText("Экспорт БД")
        self.exportButton.setObjectName("exportButton")
        self.bottomLayout.addWidget(self.exportButton)

        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setStyleSheet(
            "QPushButton { background-color: #E53E3E; color: #FFFFFF; "
            "border-radius: 5px; padding: 5px 10px; }"
            "QPushButton:hover { background-color: #C53030; }"
        )
        self.deleteButton.setText("Удалить")
        self.deleteButton.setObjectName("deleteButton")
        self.bottomLayout.addWidget(self.deleteButton)

        self.verticalLayout.addLayout(self.bottomLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        # Менюбар
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setStyleSheet(
            "QMenuBar { background-color: #FFFFFF; color: #1A202C; }"
            "QMenuBar::item:selected { background-color: #BEE3F8; }"
            "QMenu { background-color: #FFFFFF; color: #1A202C; }"
            "QMenu::item:selected { background-color: #BEE3F8; }"
        )
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle("Файл")
        self.menuFile.setObjectName("menuFile")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setTitle("Справка")
        self.menuHelp.setObjectName("menuHelp")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setText("Выход")
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName("actionExit")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setText("О программе")
        self.actionAbout.setObjectName("actionAbout")

        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet(
            "QStatusBar { background-color: #EDF2F7; color: #718096; }"
        )
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionExit.triggered.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """Устанавливает переводы для виджетов."""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "SecurePass Manager")
        )
