import time

import requests as req
from bs4 import BeautifulSoup


def get_status_comment(comment: str, link: str, accuracy_phrase=False):
    """
    Проверяет наличие комментария (из всех) в данном профиле.
    :return: list [str: Наличие комментария;
    str: время проверки;
    bool:флаг отсутствия (False если коммент. присутствует)]
    """
    try:
        comment = comment.strip()
        soup = get_soup(link, '/allcomments').find_all('div', {'class': 'commentthread_comment_text'})
        all_comments_in_list = []
        for x in soup:
            x.find('div', {'class': 'commentthread_comment_text'})
            all_comments_in_list.append(x.text.strip())
        # Дословная проверка
        if accuracy_phrase:
            if comment in all_comments_in_list:
                return ['YES', time.asctime(), False]
            return ['NO', time.asctime(), True]
        else:
            for phrase in all_comments_in_list:
                if comment in phrase:
                    return ['YES', time.asctime(), False]
            return ['NO', time.asctime(), True]
    except (BaseException,):
        return ['BaseException', time.asctime(), True]


def get_soup(link: str, additional=''):
    """
    ПАРСЕР
    Получает ссылку на профиль steam.
    Возвращает html код страницы преобразованный к строке(str).
    :return: str: html код исследуемой страницы
    """
    resp = req.get(link + additional)
    soup = BeautifulSoup(resp.text, features="html.parser")
    return soup


if __name__ == '__main__':
    get_status_comment('+rep', 'https://steamcommunity.com/id/mAnGuStDak')
