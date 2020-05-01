import json

from rpgetter.utils import constant


class JsonConfig(object):

    def __init__(self, config_json=None):
        if config_json is None:
            config_json = constant.DEFAULT_CONFIG_JSON

        with open(config_json, 'r') as json_file:
            self.config = json.loads(json_file.read())

    def get_ad_mail_addresses(self):
        return self.config.get('ad_mail').get('mail').get('ad_mail_addresses')

    def get_ad_mail_image_urls(self):
        return self.config.get('ad_mail').get('mail').get('image_urls')

    def get_ad_mail_login_url(self):
        return self.config.get('ad_mail').get('login').get('url')

    def get_ad_mail_login_keys(self):
        return self.config.get('ad_mail').get('login').get('post_keys')

    def get_web_search_url(self):
        return self.config.get('web_search').get('web_search').get('url')

    def get_web_search_login_url(self):
        return self.config.get('web_search').get('login').get('url')
