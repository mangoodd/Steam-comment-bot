import json
import re
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon

import Work_proc
import parser
from Work_proc import Worker
from gui_dialog import UiDialog
from gui_main import GuiMain
from steam_bot_class import SteamBot


class MainFlow(GuiMain, SteamBot):
    oldData = []
    style_str = ''

    def __init__(self, app):
        super().__init__()
        self.setThreads()
        self.app = app
        self.setupUi(self)

        self.readOldData()  # reading data of text fields
        self.set_language()  # setting interface language
        self.setReactions()  # setting reactions on push buttons and another
        self.centralwidget.installEventFilter(self)
        self.cursor_pos_in_window = False
        self.pass_is_visible = False
        self.last_error = ''

        try:
            self.setStyleS('DarkStyle.qss')  # reading settings of StyleSheet
        except FileNotFoundError:
            self.SetDefaultStyle()  # setting default StyleSheet
        self.defaulSS_lE = self.lineEdit_link.styleSheet()  # saving default StyleSheet of LineEdit
        self.setWindowModality(Qt.ApplicationModal)

    def saveDataTo(self, flag):
        """
        Перезапись данных в json файл из последней сессии.
        Flag=True - перезапись всех данных, Flag=False - перезапись данных текущего языка интерфейса.
        :param flag: bool
        """
        with open('exLinkCommentary.json', 'r') as f:
            profiles_read = json.load(f)
        if flag:
            profiles_read['link'] = self.get_link()
            profiles_read['commentary'] = self.get_comment()
            profiles_read['login'] = self.get_login()
        profiles_read['language'] = self.comboxSetLanguage.currentData()
        with open('exLinkCommentary.json', 'w') as f:
            json.dump(profiles_read, f)

    def readOldData(self):
        """
        Чтение данных о последней сессии из файла json.
        """
        with open('exLinkCommentary.json', 'r') as f:
            profiles_read = json.load(f)
            self.lineEdit_link.setText(profiles_read.setdefault('link', ''))
            self.lineEdit_comment.setText(profiles_read.setdefault('commentary', ''))
            self.lE_Login.setText(profiles_read.setdefault('login', ''))
            self.comboxSetLanguage.setCurrentIndex(profiles_read.setdefault('language', 0))
            MainFlow.oldData = [profiles_read.get('link'), profiles_read.get('commentary'), profiles_read.get('login')]
            self.oldSetLanguage = profiles_read.setdefault('language', 0)  # Используется при выходе из программы

    def setReactions(self):
        """
        Установка реакций на действия пользователя в окне программы.
        """
        self.pb_OpenLink.clicked.connect(self.afore_opening_link)
        self.pb_leave.clicked.connect(self.afore_leaving_comment)
        self.pb_status.clicked.connect(self.refreshStatus)
        self.pb_bot_start.clicked.connect(self.start_ProcessAutoLeave)
        self.comboxSetLanguage.activated.connect(self.set_language)
        self.pb_AdditWindow.clicked.connect(self.resize_mainwindow)
        self.pb_exit.clicked.connect(self.close)

    def setThreads(self):
        """
        Задание основных параметров создаваемых потоков.
        """
        self.threadpool = QThreadPool()
        self.threadpoolBot = QThreadPool()
        self.threadpool.setMaxThreadCount(2)
        self.threadpoolBot.setMaxThreadCount(2)

    def setStyleS(self, file):
        """
        Установка темы фона окна программы.
        :param file: путь до файла qss.
        """
        with open(file) as f:
            MainFlow.style_str = f.read()
        self.setStyleSheet(MainFlow.style_str)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def resize_mainwindow(self):
        """
        Работа с основным окном при изменении его высоты.
        """
        if self.size().height() == GuiMain.H:
            self.resize(GuiMain.W, GuiMain.H_plus)
            self.pb_AdditWindow.setIcon(QIcon('image/arrow-up.png'))
            self.app.processEvents()
            time.sleep(.02)
        else:
            self.pb_AdditWindow.setIcon(QIcon('image/arrow-down.png'))
            self.resize(GuiMain.W, GuiMain.H)
            self.app.processEvents()
            time.sleep(.02)

    def set_language(self):
        """
        Задание языка интерфейса.
        """
        if self.comboxSetLanguage.currentData():
            self.languageRussian()
        else:
            self.languageEnglish()
        if self.textLabelStatus.text():
            self.textLabelStatus.setText(self.status[self.last_error])

    def stop_ProcessAutoLeave(self):
        """
        Остановка запущенного потока автоматического написания комментария (steamBot-a).
        Установка клавиши запуска в состояние "не активна" до завершения потока, вызванного этой клавишей.
        """

        def sleep(t):
            """
            Ожидание завершения потока и перевод клавиши в состояние "активна".
            """
            while not self.message_error.get('end_flag'):
                time.sleep(0.5)
            self.pb_bot_start.setEnabled(True)
            self.message_error['end_flag'] = False

        self.stop_process = True
        if self.message_error.get('message'):
            self.last_error = self.message_error.get('message')
            self.textLabelStatus.setText(self.status[self.last_error])
        if self.threadpoolBot.activeThreadCount():
            self.pb_bot_start.setEnabled(False)
            self.threadpoolBot.start(Worker(sleep, None))
        self.comboxTime.setEnabled(True)
        self.autoRepeat = False
        self.pb_bot_start.setText(self.Bot_states.setdefault('start', 'Run'))
        self.message_error['message'] = ''

    def verification_link(self):
        """
        Проверка введенной ссылки на валидность.
        :return: bool: валидность ссылки
        """
        link = self.get_link()
        try:
            if re.findall(r'(\bhttps://steamcommunity.com)', link):
                return True
            elif re.findall(r'steamcommunity.com', link):
                new_link = 'https://' + link[re.search(r'steamcommunity.com', link).span()[0]:]
                self.lineEdit_link.setText(new_link)
                return True
            else:
                self.lineEdit_link.setStyleSheet(self.defaulSS_lE + 'border: 2px solid red;')
                self.last_error = 'error_link'
                self.textLabelStatus.setText(self.status.get(self.last_error))
                self.pb_status.setText(self.pb_status_text)
                return False
        except (BaseException,):
            return False

    def get_id_profile(self):
        """
        Получение id профиля введенного в поле https_profile.
        :return:
        """
        if self.verification_link():
            self.id_profile = self.get_id(self.get_link())
            if not self.id_profile:
                self.pb_status.setText(self.pb_status_text)
                self.last_error = 'error_link'
                self.textLabelStatus.setText(self.status.get('error_link'))
                return False
            return True
        return False

    def refreshStatus(self):
        """
        Обновление информации о наличии комментария на странице/
        и отображение ее в кнопке pushButton_status со световой индикацией.
        """
        if self.field_LinkComm_isFilled() and self.verification_link():
            self.get_link()
            try:
                new_information_about_profile = SteamBot.information_about_profile(self.get_comment(),
                                                                                   self.https_profile,
                                                                                   self.check_accuracy.isChecked())
                if 'YES' in new_information_about_profile:
                    self.pb_status.setStyleSheet('QPushButton {color: green;}')
                else:
                    self.pb_status.setStyleSheet('QPushButton {color: red;}')
                self.pb_status.setText(new_information_about_profile)
            except (BaseException,):
                self.pb_status.setStyleSheet('QPushButton {color: red;}')
                self.pb_status.setText('Error in get_status_comment block!!!')

    def get_comment(self):
        """
        :return str: комментарий из поля комментария
        """
        # убирает лишние пробелы в комментарии (переопределяя текст строки)
        self.lineEdit_comment.setText(self.lineEdit_comment.text().strip())
        return self.lineEdit_comment.text()

    def get_link(self):
        """
        Присвоение переменной https_profile значения в текстовом поле ввода.
        :return str: комментарий из поля комментария
        """

        self.https_profile = self.lineEdit_link.text().strip()

        return self.https_profile

    def get_login(self):
        """
        Присвоение переменной login значения из текстового поле ввода.
        :return str: login
        """
        self.login = self.lE_Login.text().strip()
        return self.login

    def start_ProcessAutoLeave(self):
        """
        Запуск циклического процесса (в отдельном потоке) печати комментария через заданное время при условии его отсутствия.
        :return:
        """
        self.pword = self.lE_password.text()
        self.get_id_profile()
        self.PrBar_reset()
        if self.autoRepeat:
            self.stop_ProcessAutoLeave()
        else:
            self.stop_process = False
            if self.field_Acc_isFilled() and self.field_LinkComm_isFilled() and self.verification_link():
                self.get_login()
                self.poolBot_flag = True
                self.comboxTime.setEnabled(False)
                self.autoRepeat = True
                self.pb_bot_start.setText(self.Bot_states.setdefault('stop', 'Stop'))
                data_for_automatization_process = [self.comboxTime.currentData() * 60, self.get_comment(),
                                                   self.get_link(), self.check_accuracy.isChecked()]
                self.threadpoolBot.start(Worker(self.autoRepeatLeave, data_for_automatization_process))

    def afore_opening_link(self):
        """
        Создание нового потока для открытия ссылки из текстового поля.
        """
        if self.verification_link():
            link = self.get_link()
            self.threadpool.start(Worker(self.open_link, link))

    def afore_leaving_comment(self):
        """
        Проверка наличия комментария на странице -> (Запуск процесса написания (при отсутствии комментария)/
        Вызов диалогового окна с подтверждением (при наличии ссылки) и запуск процесса написания)./
        При запуске процесса написания - запускает 2 параллельных потока (поток написания комментария, поток прогресса отображаемого/
        в ProgressBar).
        """

        def run_threads():
            self.pword = self.lE_password.text()
            self.get_login()
            self.stop_process = False
            self.threadpool.start(Worker(self.leave_comment, comment_text))
            self.threadpool.start(Worker(self.PrBar_refresh, 0.5))
            self.pb_leave.setEnabled(False)

        if self.field_LinkComm_isFilled() and self.field_Acc_isFilled() and self.verification_link():
            if parser.get_status_comment(comment_text := self.get_comment(), self.get_link(),
                                         self.check_accuracy.isChecked())[2]:
                run_threads()
            else:
                widget = QDialog()
                about_window = UiDialog(self.dialog)
                widget.setStyleSheet(MainFlow.style_str)
                about_window.setupUi(widget)
                if widget.exec():
                    run_threads()
                else:
                    pass

    def field_LinkComm_isFilled(self):
        """
        Проверка полей ссылка-комментарий на заполненность.
        В случае если все поля или одной из полей не заполнено - запуск процесса field_is_empty.
        :return: bool
        """
        if not self.get_link():
            self.field_is_empty(self.lineEdit_link, 'empty_field_account')
            return False
        if not self.get_comment():
            self.field_is_empty(self.lineEdit_comment, 'empty_field_account')
            return False
        else:
            self.lineEdit_link.setStyleSheet(self.defaulSS_lE)
            self.lineEdit_comment.setStyleSheet(self.defaulSS_lE)
            self.textLabelStatus.setText('')
            return True

    def field_Acc_isFilled(self):
        """
        Проверка полей логин-пароль на заполненность.
        В случае если все поля или одной из полей не заполнено - запуск процесса field_is_empty.
        :return: bool
        """

        if not self.lE_Login.text():
            self.field_is_empty(self.lE_Login, 'empty_field_account')
            return False
        if not self.lE_password.text():
            self.field_is_empty(self.lE_password, 'empty_field_account')
            return False
        else:
            self.lE_Login.setStyleSheet(self.defaulSS_lE)
            self.lE_password.setStyleSheet(self.defaulSS_lE)
            return True

    def field_is_empty(self, field, text_error):
        """
        Вывод ошибки в labelStatus и позиционирование курсора на пустом поле.
        :param text_error: текст ошибки.
        :param field: поле для позиционирования курсора.
        """
        field.setStyleSheet('border: 1px solid red;')
        self.last_error = text_error
        self.textLabelStatus.setText(self.status.get(text_error))
        self.resize(GuiMain.W, GuiMain.H_plus)
        field.setFocus(Qt.MouseFocusReason)
        field.setCursorPosition(0)

    def PrBar_reset(self):
        """
        Сброс прогресса ProgressBar-a.
        """
        self.PrBar.setValue(0)
        self.PrBarText.setText('')

    def PrBar_refresh(self, time_to_sleep):
        """
        Обновление статуса ProgressBar.

        """

        def setDefault():
            self.flagPrBar = True
            self.pb_leave.setEnabled(True)
            raise Work_proc.CloseProgress('CloseProgressProcess')

        def setMessage_and_PrBarReset():
            if self.message_error.get('message'):
                self.last_error = self.message_error.get('message')
            self.textLabelStatus.setText(self.status[self.last_error])
            self.PrBar_reset()

        self.flagPrBar = True
        while self.PrBar.value() != 100:
            if self.flagPrBar:
                time.sleep(time_to_sleep)
                if self.PrBar.value() != self.progress[0]:
                    self.PrBar.setValue(self.progress[0])
                    self.PrBarText.setText(self.statusTextBar.get(self.progress[2]))
            else:
                setMessage_and_PrBarReset()
                setDefault()
                break
        if self.PrBar.value() != 100:
            setMessage_and_PrBarReset()
        setDefault()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.cursor_pos_in_window = event.pos()

    def mouseReleaseEvent(self, event):
        self.cursor_pos_in_window = False

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.cursor_pos_in_window:
            cursor_pos = QtWidgets.QApplication.desktop().cursor().pos()
            new_pos = cursor_pos - self.cursor_pos_in_window
            self.move(new_pos)

    def eventFilter(self, object, event):
        if self.centralwidget.height() == self.H:
            self.pb_AdditWindow.setIcon(QIcon('image/arrow-down.png'))
        else:
            self.pb_AdditWindow.setIcon(QIcon('image/arrow-up.png'))
        self.centralwidget.resize(GuiMain.W, self.centralwidget.height())
        self.pb_AdditWindow.move(0, self.centralwidget.height() - 20)
        return False

    def closeEvent(self, event):
        # Переопределение closeEvent

        def shutdown_all_process():
            """
            Завершение запущенных потоков.
            """
            if self.threadpool.activeThreadCount() or self.threadpoolBot.activeThreadCount():
                self.stop_process = True
                self.autoRepeat = False
                while self.threadpool.activeThreadCount() or self.threadpoolBot.activeThreadCount():
                    time.sleep(0.2)

        # Вызов контекстного окна, если были внесены изменения в текстовых полях
        if self.lineEdit_link.text() and [self.lineEdit_link.text(), self.lineEdit_comment.text(),
                                          self.lE_Login.text()] != MainFlow.oldData:
            # self.setWindowFlag(Qt.FramelessWindowHint)
            reply = QtWidgets.QMessageBox.question(self, self.exit_program[0],
                                                   self.exit_program[1],
                                                   QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No |
                                                   QtWidgets.QMessageBox.Cancel,
                                                   QtWidgets.QMessageBox.Cancel)
            # reply.setWindowFlag(Qt.FramelessWindowHint)
            if reply == QtWidgets.QMessageBox.Yes:
                # Сохранение вводимых данных и активного языка интерфейса
                self.saveDataTo(True)
                shutdown_all_process()
                event.accept()
            elif reply == QtWidgets.QMessageBox.Cancel:
                event.ignore()
            else:
                shutdown_all_process()
                event.accept()
        else:
            # Сохранение активного языка интерфейса
            if self.oldSetLanguage != self.comboxSetLanguage.currentData():
                self.saveDataTo(False)
        shutdown_all_process()
        event.accept()


def initial():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    form = MainFlow(app)
    form.show()
    app.exec_()


if __name__ == '__main__':
    initial()
