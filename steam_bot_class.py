import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from parser import get_status_comment, get_soup


class SteamBot:
    autoRepeat = False
    flagPrBar = True

    def __init__(self):
        super().__init__()
        self.https_profile = ''
        self.login = ''
        self.id_profile = ''
        self.progress = (0, 100, '')
        self.message_error = {'message': '',
                              'end_flag': False, }
        self.stop_process = False
        self.error = ''
        self.pword = ''

    def get_id(self, link_to_profile: str):
        """
        Получает ссылку на профиль.
        Возвращает id заданного профиля.
        :return: str: id профиля
        """

        def search_id(text: str, mark: str):
            """
            :param text: html код страницы в виде строки
            :param mark: фраза, которую необходимо найти (является маркером)
            :return: str: id профиля/ False при невозможности найти id
            """
            dot = text.find(mark) + len(mark)
            profile_id = text[dot:dot + 17]
            try:
                return profile_id if len(profile_id) == 17 else False
            except ValueError:
                return False

        if 'profiles/' in link_to_profile:
            return search_id(link_to_profile, 'profiles/')
        else:
            return search_id(get_soup(link_to_profile).decode(), '"steamid":"')

    def leave_comment(self, commenters):

        def action_when_exception(message):
            self.flagPrBar = False
            self.message_error['message'] = message
            try:
                if self.autoRepeat:
                    self.stop_processAutoLeave()
            except(Exception,):
                pass

        self.id_profile = self.get_id(self.https_profile)
        try:
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            self.progress = (20, 35, 'InitProcess')
            driver = webdriver.Chrome(options=op)

            if self.stop_process:
                return

            driver.get('https://steamcommunity.com/login/home')
            WebDriverWait(driver, 30).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'newlogindialog_TextInput_2eKVn')))

            if self.stop_process:
                return

            self.progress = (36, 49, 'EnterData')
            driver.find_element(By.CLASS_NAME, 'newlogindialog_TextInput_2eKVn').send_keys(self.login)
            driver.find_element(By.XPATH, "//input[@type='password']").send_keys(self.pword)
            driver.find_element(By.CLASS_NAME, 'newlogindialog_CheckboxFieldLabel_2yrCY').click()
            WebDriverWait(driver, 60).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'newlogindialog_SignInButtonContainer_14fsn')))
            driver.find_element(By.CLASS_NAME, 'newlogindialog_SignInButtonContainer_14fsn').click()

            self.progress = (50, 51, 'WaitConfirm')

            if self.login_reaction(driver):
                driver.quit()
                action_when_exception(self.error)
                return

            WebDriverWait(driver, 600).until(ec.url_matches('https://steamcommunity.com/profiles'))

            driver.get(self.https_profile)  # Переход на страницу профиля
            self.progress = (70, 89, 'GoToLink')
            WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.CLASS_NAME, 'commentthread_textarea')))
            self.progress = (90, 99, 'GoToLink')
            driver.find_element(By.CLASS_NAME, 'commentthread_textarea').send_keys(commenters)
            WebDriverWait(driver, 60).until(
                ec.element_to_be_clickable((By.ID, 'commentthread_Profile_' + self.id_profile + '_submit')))
            driver.find_element(By.ID, 'commentthread_Profile_' + self.id_profile + '_submit').click()
            driver.quit()
            self.progress = (100, 100, 'Complete')
            return 'Complete!'

        except RuntimeError:
            action_when_exception('RuntimeError')
        except (Exception,):
            action_when_exception('AppError')

    def open_link(self, link):
        """
        Открывает ссылку в браузере
        """
        try:
            webdriver.Firefox().get(link)
        except (Exception,):
            return

    @staticmethod
    def information_about_profile(commentary: str, link: str, accuracy_phrase: bool):
        """
        Проверяет наличие комментария на странице и возвращает строку с состоянием и временем проверки.
        :param commentary: str: комментарий
        :param link: str: ссылка на профиль
        :param accuracy_phrase: bool: дословность поиска комментария
        :return: str: информация о наличии комментария, время и дату проверки
        """
        exit_examination = get_status_comment(commentary, link, accuracy_phrase)
        return str('\n'.join([exit_examination[0]] + [exit_examination[1]]))

    def login_reaction(self, driver):
        """
        Проверка реакции на заполнение формы (Login-Password).
        Возвращает True - если есть ошибка входа, False - данные верны и запущен процесс инициализации.
        :return: bool
        """
        while driver.current_url == 'https://steamcommunity.com/login/home':
            time.sleep(0.4)
            try:
                try:
                    if driver.find_element(By.CLASS_NAME, "newlogindialog_Danger_1-HwJ"):
                        self.error = 'LoginError'
                        return True
                except (Exception,):
                    pass
                try:
                    if driver.find_element(By.CLASS_NAME, 'newlogindialog_FailureTitle_A3Y-u'):
                        self.error = 'ManyTriesError'
                        return True
                except (Exception,):
                    pass
                try:
                    if driver.find_element(By.CLASS_NAME, 'newlogindialog_AwaitingMobileConfText_7LmnT'):
                        return False
                except (Exception,):
                    pass
                try:
                    if driver.find_element(By.CLASS_NAME, 'newlogindialog_Label_2SE9Z'):
                        return False
                except (Exception,):
                    pass
                if self.stop_process:
                    return True
            except (Exception,):
                pass
        return False

    def autoRepeatLeave(self, sleep_time: int, comment: str, link: str, accuracy_checked: bool):
        """
        Основной цикл проверки комментария через заданное время.
        При отсутствии комментария на странице запускает процесс написания комментария.
        """
        next_check = 0
        while self.autoRepeat:
            if next_check <= int("{:.0f}".format(time.time())):
                if get_status_comment(comment=comment, link=link, accuracy_phrase=accuracy_checked)[2]:
                    self.leave_comment(commenters=comment)
                last_check = int("{:.0f}".format(time.time()))
                next_check = last_check + sleep_time
            time.sleep(1 - time.time() % 1)
        self.message_error['end_flag'] = True


def initial():
    bot = SteamBot
    print(bot.information_about_profile(commentary := str(input('Enter commentary for check: ')),
                                        link := str(input('Enter link: ')), False))


if __name__ == "__main__":
    initial()
