# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui


class GuiMain(QtWidgets.QMainWindow):
    W = 440
    H = 516
    H_plus = 620

    def setupUi(self, main_window):
        # super(AppMain, self).__init__()
        # MainWindow.setWindowTitle("Feedback steam bot      @by Mango")

        main_window.setObjectName("MainWindow")
        main_window.setMinimumSize(QtCore.QSize(self.W, self.H))
        main_window.setMaximumSize(QtCore.QSize(self.W, self.H_plus))
        main_window.setEnabled(True)
        # main_window.setStyleSheet("color: rgb(100,100,100);")

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.creation_LineEdit()
        self.creation_LayoutAccount()
        self.creation_PushButton()
        self.creation_ComboBox()
        self.creation_CheckBox()
        self.creation_ProgressBar()
        self.creation_TextLabel()
        self.func_SetGeometry_for_all()

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        main_window.setCentralWidget(self.centralwidget)
        self.setWindowIcon(QtGui.QIcon('image/mstitel.jpg'))

    def SetDefaultStyle(self):
        self.lineEdit_link.setStyleSheet('QLineEdit {font: 75 12pt "Times New Roman";}')
        self.lineEdit_comment.setStyleSheet('font: 75 12pt "Times New Roman";')
        self.pb_status.setStyleSheet('QPushButton {font: 75 18pt "Sitka";}')
        self.pb_leave.setStyleSheet('QPushButton {font: 75 18pt "Sitka";}')
        self.pb_OpenLink.setStyleSheet('QPushButton {font: 75 12pt "Times New Roman";}')
        self.pb_bot_start.setStyleSheet('QPushButton {font: 75 12pt "Times New Roman";}')
        self.pb_AdditWindow.setStyleSheet('QPushButton {font: 75 8pt "Times New Roman";}')
        self.comboxSetLanguage.setStyleSheet('font: 75 10pt "Times New Roman";')
        self.comboxTime.setStyleSheet('font: 75 12pt "Times New Roman";')
        self.textLabelStatus.setStyleSheet('color: red;')
        self.PrBarText.setStyleSheet('color: black; font: 75 12pt "Times New Roman"; margin:0px;')
        self.textLabelCheck.setStyleSheet('font: 75 12pt "Times New Roman";')
        self.textLabelWelcome.setStyleSheet('font: 75 18pt "Sitka"')
        self.check_accuracy.setStyleSheet('font: 75 12pt "Times New Roman";')
        self.l_Login.setStyleSheet('font: 75 18pt "Sitka";')

    def func_SetGeometry_for_all(self):
        self.pb_exit.setGeometry(QtCore.QRect(GuiMain.W - 34, 4, 30, 20))
        self.lineEdit_link.setGeometry(QtCore.QRect(20, GuiMain.H - 410, GuiMain.W - 130, 40))
        self.lineEdit_comment.setGeometry(QtCore.QRect(20, GuiMain.H - 350, GuiMain.W - 40, 40))
        self.pb_status.setGeometry(QtCore.QRect(20, GuiMain.H - 220, GuiMain.W - 40, 80))
        self.pb_leave.setGeometry(QtCore.QRect(20, GuiMain.H - 130, GuiMain.W - 40, 60))
        self.pb_OpenLink.setGeometry(QtCore.QRect(GuiMain.W - 100, GuiMain.H - 410, 80, 40))
        self.pb_bot_start.setGeometry(QtCore.QRect(GuiMain.W - 110, GuiMain.H - 270, 90, 30))
        # self.pb_AdditWindow.setGeometry(QtCore.QRect(0, AppMain.H - 60, AppMain.W, 20))
        self.comboxTime.setGeometry(QtCore.QRect(GuiMain.W - 210, GuiMain.H - 269, 90, 28))
        self.comboxSetLanguage.setGeometry(QtCore.QRect(GuiMain.W - 20 - 50, GuiMain.H - 480, 50, 24))
        self.textLabelWelcome.setGeometry(QtCore.QRect(20, GuiMain.H - 490, GuiMain.W - 130, 40))
        self.textLabelCheck.setGeometry(QtCore.QRect(20, GuiMain.H - 266, GuiMain.W - 220, 20))
        self.textLabelStatus.setGeometry(QtCore.QRect(20, GuiMain.H - 450, GuiMain.W - 40, 30))
        self.check_accuracy.setGeometry(QtCore.QRect(20, GuiMain.H - 300, 300, 20))
        self.PrBar.setGeometry(QtCore.QRect(20, GuiMain.H - 60, GuiMain.W - 40, 30))
        self.PrBarText.setGeometry(QtCore.QRect(20, GuiMain.H - 60, GuiMain.W - 10, 30))
        self.pb_AdditWindow.setGeometry(QtCore.QRect(0, GuiMain.H - 20, GuiMain.W, 22))

    def creation_PushButton(self):
        self.pb_status = QtWidgets.QPushButton(self.centralwidget)
        self.pb_status.setObjectName("pushButton_big")

        self.pb_leave = QtWidgets.QPushButton(self.centralwidget)
        self.pb_leave.setObjectName("pushButton_big")

        self.pb_OpenLink = QtWidgets.QPushButton(self.centralwidget)
        self.pb_OpenLink.setObjectName("OpenLink")

        self.pb_bot_start = QtWidgets.QPushButton(self.centralwidget)
        self.pb_bot_start.setObjectName("pushButtonComBox")

        self.pb_AdditWindow = QtWidgets.QPushButton(self.centralwidget)
        self.pb_AdditWindow.setIcon(QtGui.QIcon('image/arrow-down.png'))
        self.pb_AdditWindow.setObjectName("pb_AdditWindow")

        self.pb_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pb_exit.setObjectName('pb_exit')

    def creation_LineEdit(self):
        self.lineEdit_link = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_link.setObjectName("lineEdit_link")

        self.lineEdit_comment = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_comment.setObjectName("lineEdit_comment")

    def creation_ComboBox(self):
        self.comboxTime = QtWidgets.QComboBox(self.centralwidget)
        self.comboxTime.setObjectName("comboxTime")
        self.comboxTime.addItem('5 ', 5)
        self.comboxTime.addItem('10 ', 10)
        self.comboxTime.addItem('15 ', 15)
        self.comboxTime.addItem('30 ', 30)
        self.comboxTime.addItem('1 ', 60)
        self.comboxTime.addItem('2 ', 2 * 60)
        self.comboxTime.addItem('3 ', 3 * 60)
        self.comboxTime.addItem('6 ', 6 * 60)
        self.comboxTime.addItem('12 ', 12 * 60)
        self.comboxTime.addItem('24 ', 24 * 60)

        self.comboxSetLanguage = QtWidgets.QComboBox(self.centralwidget)
        self.comboxSetLanguage.setObjectName("comboxLanguage")
        self.comboxSetLanguage.addItem('Eng', 0)
        self.comboxSetLanguage.addItem('Rus', 1)

    def creation_ComboboxTime(self):
        self.comboxTime.setItemText(0, '5 ' + self.time[1])
        self.comboxTime.setItemText(1, '10 ' + self.time[1])
        self.comboxTime.setItemText(2, '15 ' + self.time[1])
        self.comboxTime.setItemText(3, '30 ' + self.time[1])
        self.comboxTime.setItemText(4, '1 ' + self.time[2])
        self.comboxTime.setItemText(5, '2 ' + self.time[3])
        self.comboxTime.setItemText(6, '3 ' + self.time[3])
        self.comboxTime.setItemText(7, '6 ' + self.time[4])
        self.comboxTime.setItemText(8, '12 ' + self.time[4])
        self.comboxTime.setItemText(9, '24 ' + self.time[3])

    def creation_TextLabel(self):
        self.textLabelWelcome = QtWidgets.QLabel(self.centralwidget)
        self.textLabelWelcome.setObjectName("textLabelWelcome")

        self.textLabelCheck = QtWidgets.QLabel(self.centralwidget)
        self.textLabelCheck.setObjectName("textLabelCheck")

        self.textLabelStatus = QtWidgets.QLabel(self.centralwidget)
        self.textLabelStatus.setObjectName("textLabelStatus")

        self.PrBarText = QtWidgets.QLabel(self.centralwidget)
        self.PrBarText.setObjectName("PrBarText")

    def creation_CheckBox(self):
        self.check_accuracy = QtWidgets.QCheckBox(self.centralwidget)
        self.check_accuracy.setObjectName("check_accuracy")

    def creation_ProgressBar(self):
        self.PrBar = QtWidgets.QProgressBar(self.centralwidget)
        self.PrBar.setValue(0)
        self.PrBar.setTextVisible(False)

    def creation_LayoutAccount(self):
        self.widget_login = QtWidgets.QFrame(self.centralwidget)
        self.widget_login.setGeometry(QtCore.QRect(10, GuiMain.H - 30, GuiMain.W, GuiMain.H_plus - GuiMain.H))
        self.widget_login.setObjectName("widget_login")

        self.AccLayout = QtWidgets.QVBoxLayout(self.widget_login)
        self.AccLayout.setContentsMargins(10, 10, 40, 0)
        self.AccLayout.setSpacing(8)
        self.AccLayout.setObjectName("AccLayout")

        self.l_Login = QtWidgets.QLabel(self.widget_login)
        self.l_Login.setObjectName("l_Login")
        self.AccLayout.addWidget(self.l_Login)

        self.lE_Login = QtWidgets.QLineEdit(self.widget_login)
        self.lE_Login.setObjectName("lE_Login")
        self.AccLayout.addWidget(self.lE_Login)

        self.lE_password = QtWidgets.QLineEdit(self.widget_login)
        self.lE_password.setObjectName("lE_password")
        self.lE_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.AccLayout.addWidget(self.lE_password)

    def languageEnglish(self):
        self.textLabelWelcome.setText('Welcome to Feedbacker')
        self.statusTextBar = {
            'InitProcess': 'Initialization process',
            'EnterData': 'Entering data',
            'WaitConfirm': 'Waiting for confirmation',
            'GoToLink': 'Go to profile page',
            'Complete': 'Complete!',
        }
        self.status = {
            'empty_field_link': 'Enter profile link',
            'empty_field_comment': 'Fill in the comment field',
            'empty_field_account': 'Enter account information',
            'error_link': 'The link is incorrect or contains an error',
            'error_account': 'Invalid password or account name',
            'RuntimeError': 'Timeout exceeded...',
            'AppError': 'Application error...',
            'LoginError': 'Check your password and account name',
            'ManyTriesError': 'Lots of failed login attempts',
        }
        self.dialog = 'The selected page already has this comment.\nLeave one more?'
        self.time = ['seconds', 'minutes', 'hour', 'hours', 'hours']
        self.Bot_states = {
            'start': 'Run',
            'stop': 'Stop',
        }
        self.pb_OpenLink.setText("Open")
        self.pb_bot_start.setText('Run')
        self.textLabelCheck.setText('Check comment every:')
        self.check_accuracy.setText('Verbatim comment check')
        self.pb_status_text = 'Comment status unknown'
        self.pb_status.setText(self.pb_status_text)
        self.pb_leave.setText("Leave feedback")
        self.l_Login.setText('Data of Steam account')
        self.lE_Login.setPlaceholderText('Login')
        self.lE_password.setPlaceholderText('Password')
        self.lineEdit_link.setPlaceholderText('Link')
        self.lineEdit_comment.setPlaceholderText('Comment')
        self.exit_program = ['Exit from the program', 'Save data (link to profile, comment, login)?']
        self.creation_ComboboxTime()

    def languageRussian(self):
        self.textLabelWelcome.setText('Добро пожаловать в Feedbaсker')
        self.statusTextBar = {
            'InitProcess': 'Инициализация процесса',
            'EnterData': 'Ввод данных',
            'WaitConfirm': 'Ожидание подтверждения входа',
            'GoToLink': 'Переход на страницу профиля',
            'Complete': 'Готово!',
        }
        self.status = {
            'empty_field_link': 'Введите ссылку на профиль',
            'empty_field_comment': 'Заполните поле комментария',
            'empty_field_account': 'Введите данные учетной записи',
            'error_link': 'Ссылка не верна или в ней допущена ошибка',
            'error_account': 'Неверный пароль или имя аккаунта',
            'RuntimeError': 'Превышено время ожидания...',
            'AppError': 'Ошибка приложения...',
            'LoginError': 'Проверьте свой пароль и имя аккаунта',
            'ManyTriesError': 'Много неудачных попыток входа в Steam',
        }
        self.dialog = 'На выбранной странице уже есть данный комментарий.\nОставить еще один?'
        self.time = ['секунд', 'минут', 'час', 'часа', 'часов']
        self.Bot_states = {
            'start': 'Запустить',
            'stop': 'Остановить',
        }
        self.pb_OpenLink.setText("Открыть")
        self.pb_bot_start.setText(self.Bot_states.get('start'))
        self.textLabelCheck.setText('Проверять комментарий через:')
        self.check_accuracy.setText('Дословная проверка комментария')
        self.pb_status_text = 'Проверить статус комментария'
        self.pb_status.setText(self.pb_status_text)
        self.pb_leave.setText("Оставить комментарий")
        self.l_Login.setText('Данные аккаунта Steam')
        self.lE_Login.setPlaceholderText('Логин')
        self.lE_password.setPlaceholderText('Пароль')
        self.lineEdit_link.setPlaceholderText('Ссылка')
        self.lineEdit_comment.setPlaceholderText('Комментарий')
        self.exit_program = ['Выход из программы', 'Сохранить данные (ссылку на профиль, комментарий, логин)?']
        self.creation_ComboboxTime()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Feedback steam bot      @by Mango"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GuiMain()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
