"""
google apiの処理に関するモジュール
"""
from __future__ import print_function

import base64
import logging
import pickle
import re

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from rpgetter.utils import constant

logger = logging.getLogger(__name__)


def build_api(service_name, version, credentials):
    """
    サービス名、バージョンからgoogleのAPIを取得する
    :param service_name: サービス名
    :param version: バージョン
    :param credentials: 資格情報
    :return: google api
    """
    return build(service_name, version, credentials=credentials)


class GoogleAuthenticator(object):
    """
    Googleの認証情報を管理、サービスのリソースを取得する
    """

    @property
    def credentials(self):
        return self._credentials

    def __init__(self, credentials_json=None, token_pickle=None):
        """
        コンストラクタ
        :param credentials_json: 認証情報が格納されたJSONファイル
        :param token_pickle: 認証情報が格納されたpickleファイル
        """
        if credentials_json is None and token_pickle is None:
            raise ValueError('Both credentials_json and token_pickle are None')

        self._credentials = self._get_credentials(credentials_json=credentials_json,
                                                  token_pickle=token_pickle)

    def _get_credentials(self, credentials_json=None, token_pickle=None):
        """
        資格情報を取得する
        :param credentials_json: 認証情報が格納されたJSONファイル
        :param token_pickle: 認証情報が格納されたpickleファイル
        :return:
        """

        if token_pickle:
            credentials = self._get_credentials_by_pickle(token_pickle)
            if credentials:
                return credentials

            logger.warning('token pickle is invalid')

        if credentials_json is None:
            raise ValueError("Cant't authenticate your credentials")

        credentials = self._get_credentials_by_json(credentials_json)

        if credentials is None:
            raise ValueError("Cant't authenticate your credentials")

        return credentials

    @staticmethod
    def _get_credentials_by_pickle(token_pickle):
        """
        pickleから資格情報を取得する
        :param token_pickle: pickleのパス
        :return: 資格情報
        """
        with open(token_pickle, 'rb') as token:
            credentials = pickle.load(token)

        if credentials.valid:
            return credentials

        if credentials.expired and credentials.refresh_token:
            return credentials.refresh(Request())

        return None

    @staticmethod
    def _get_credentials_by_json(credentials_json):
        """
        Jsonから資格情報を首都ｋする
        :param credentials_json: 認証情報が格納されたJSONファイル
        :return:
        """
        flow = InstalledAppFlow.from_client_secrets_file(credentials_json, constant.SCOPES)
        credentials = flow.run_local_server(port=0)

        return credentials

    def save(self, file_path='token.pickle'):
        """
        資格情報をpickle形式で保存する
        :param file_path: 保存するファイルパス(デフォルト: token.pickle)
        """

        with open(file_path, 'wb') as token:
            pickle.dump(self._credentials, token)


class GmailManager(object):
    """
    Gmailの処理を管理する
    """

    def __init__(self, credentials, max_result=100):
        """
        コンストラクタ
        :param credentials: 認証情報
        :param 取得する最大メール数
        """
        self.user_resource = build_api('gmail', 'v1', credentials).users()
        self.message_list = self._get_messages(max_result)

    def _get_messages(self, max_result=100):
        """
        メッセージのリストを返却する
        :param max_result: 取得する最大結果数
        :return: メッセージidのリスト
        """
        message_list = self.user_resource.messages().list(userId='me', maxResults=max_result).execute()
        message_id_list = [message.get('id') for message in message_list.get('messages')]
        message_list = []
        for message_id in message_id_list:
            message_list.append(self.user_resource.messages().get(userId='me', id=str(message_id)).execute())

        return message_list

    def get_body_by_from_address(self, from_filter_address_list):
        """
        送信元メールアドレスからメール本文のhtmlを取得する
        :param from_filter_address_list: 判別するアドレスのリスト
        :return: メール本文のhtmlのリスト
        """
        body_list = []
        for message in self.message_list:
            for header in message.get('payload').get('headers'):
                if header.get('name') == 'From':
                    if self.find_address(header.get('value')) in from_filter_address_list:
                        body_list.append(
                            self.to_html_body(message)
                        )

        return body_list

    @staticmethod
    def to_html_body(message):
        """
        メッセージから本文部分を抽出し、htmlに変換する
        :param message:
        :return:
        """
        body = message.get('payload').get('body').get('data')
        return base64.urlsafe_b64decode(body).decode('utf-8')

    @staticmethod
    def find_address(html):
        """
        "<>"内のメールアドレスを取得する
        :param html: Fromのhtml
        :return: メールアドレス
        """
        if '<' in html and '>' in html:
            return re.search(r'.*<(.*)>', html).group(1)
        return html
