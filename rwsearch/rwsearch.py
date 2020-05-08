import argparse
import contextlib
import logging
import sys
import time

import mimesis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from rwsearch import constant


def rwsearch(args):
    """
    seleniumを使用して、検索ワードの検索を行う
    :param args: コマンドライン引数
    """
    text = mimesis.Text()
    word_list = [text.word() for _ in range(args.num)]
    if args.add_on is None:
        args.add_on = constant.R_ADD_ON
    options = Options()
    options.add_extension(args.add_on)
    if args.chrome_driver is None:
        args.chrome_driver = constant.CHROME_DRIVER
    driver = webdriver.Chrome(args.chrome_driver, options=options)
    with contextlib.ExitStack() as stack:
        stack.callback(driver.quit)
        driver.get(constant.LOGIN_URL)

        user_id_element = driver.find_element_by_xpath('//*[@id="loginInner_u"]')
        user_id_element.send_keys(args.user)
        time.sleep(3)
        password_element = driver.find_element_by_xpath('//*[@id="loginInner_p"]')
        password_element.send_keys(args.password)
        time.sleep(3)
        login_submit = driver.find_element_by_xpath('//*[@id="loginInner"]/p[1]/input')
        login_submit.click()
        time.sleep(3)
        if 'login' in driver.current_url:
            raise ValueError('user id or password is incorrect')

        for search_word in word_list:
            driver.get(constant.WEB_SEARCH_URL)
            search_window = driver.find_element_by_xpath('//*[@id="search-input"]')
            search_window.send_keys(search_word)
            time.sleep(3)
            search_submit = driver.find_element_by_xpath('//*[@id="search-submit"]')
            search_submit.click()
            time.sleep(3)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user', required=True, help='R user id')
    parser.add_argument('-p', '--password', required=True, help='R Password')
    parser.add_argument('-n', '--num', default=30, type=int, help='num of searching words')
    parser.add_argument('--chrome-driver', default=None, help='default: chrome 81')
    parser.add_argument('--add-on', default=None, help='chrome add on file path(.crx)')
    parser.add_argument('--debug', action='store_true', help='debug mode')

    cli_args = parser.parse_args()

    if cli_args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
        level=log_level
    )

    for k, v in cli_args.__dict__.items():
        logging.info(f'{k}: {v}')
    try:
        rwsearch(cli_args)

    except Exception as e:
        error_type = type(e).__name__
        sys.stderr.write('{}: {}'.format(error_type, e))
        sys.exit(1)


if __name__ == '__main__':
    main()
