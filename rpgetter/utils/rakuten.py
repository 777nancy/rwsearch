"""
楽天に関する処理のモジュール
"""
import contextlib
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from rpgetter.utils import config, constant


class RakutenSessionManager(object):
    """
    楽天のwebアクセスに関する処理を行う
    """

    def __init__(self, user_id: str, password: str, conf: config):
        """
        コンストラクタ
        :param user_id: ユーザID
        :param password: パスワード
        :param conf: コンフィグ
        """
        self._user_id = user_id
        self._password = password
        self._conf = conf

    def get(self, url_list):
        """
        URLにログインをした状態でアクセスする
        :param url_list: アクセするURLのリスト
        """
        if type(url_list) is str:
            url_list = [url_list]
        login_session = self._login(url_list[0], self._conf.get_ad_mail_login_keys())
        with contextlib.ExitStack() as stack:
            stack.callback(login_session.close)
            if len(url_list) == 1:
                return

            for url in url_list[1:]:
                response = login_session.get(url)
                response.encoding = response.apparent_encoding

                if response.status_code != 200:
                    raise requests.HTTPError('status code is {}'.format(response.status_code))

    def _login(self, url, keys):
        """
        ログイン画面からログインを行う
        :param url: ログインURL
        :param keys: postに必要なHTML内のkey
        :return: ログイン済みのセッション
        """
        session = requests.session()
        try:
            response = session.get(url)
            response.encoding = response.apparent_encoding
            if response.status_code != 200:
                raise requests.HTTPError('status code is {}'.format(response.status_code))
            soup = BeautifulSoup(response.text, 'html.parser')
            payload = {}

            for key in keys:
                payload[key] = soup.find(attrs={'name': '{}'.format(key)}).get('value')

            payload['p'] = self._password
            payload['u'] = self._user_id
            response = session.post(self._conf.get_ad_mail_login_url(), data=payload)
            response.encoding = response.apparent_encoding
            if response.status_code != 200:
                raise requests.HTTPError('status code is {}'.format(response.status_code))
            return session
        except Exception:
            session.close()
            raise

    def search(self, search_words):
        """
        seleniumを使用して、検索ワードの検索を行う
        :param search_words: 検索ワードのリスト
        """
        if type(search_words) is str:
            search_words = [search_words]

        options = Options()
        options.add_extension(constant.RAKUTEN_ADD_ON_PATH)
        driver = webdriver.Chrome(constant.CHROME_DRIVER_PATH, options=options)
        with contextlib.ExitStack() as stack:
            stack.callback(driver.quit)
            driver.get(self._conf.get_web_search_login_url())

            user_id = driver.find_element_by_xpath('//*[@id="loginInner_u"]')
            user_id.send_keys(self._user_id)
            time.sleep(3)
            password = driver.find_element_by_xpath('//*[@id="loginInner_p"]')
            password.send_keys(self._password)
            time.sleep(3)
            login_submit = driver.find_element_by_xpath('//*[@id="loginInner"]/p[1]/input')
            login_submit.click()
            time.sleep(3)

            for search_word in search_words:
                driver.get(self._conf.get_web_search_url())
                search_window = driver.find_element_by_xpath('//*[@id="search-input"]')
                search_window.send_keys(search_word)
                time.sleep(3)
                search_submit = driver.find_element_by_xpath('//*[@id="search-submit"]')
                search_submit.click()
                time.sleep(3)

    def find_url(self, html):
        """
        htmlからポイント獲得用のURLを取得する
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, 'html.parser')
        for image_url in self._conf.get_ad_mail_image_urls():
            attr = soup.find(attrs={'src': image_url})
            if attr:
                url = attr.find_parent('a').get('href')
                return url
        return None
