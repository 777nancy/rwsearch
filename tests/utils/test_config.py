from rpgetter.utils import config


class TestConfig(object):

    @classmethod
    def setup_class(cls):
        cls.conf = config.JsonConfig()

    def test_get_ad_mail_addresses(self):
        ad_mail_addresses = self.conf.get_ad_mail_addresses()
        assert type(ad_mail_addresses) is list

    def test_get_ad_mail_image_urls(self):
        image_urls = self.conf.get_ad_mail_image_urls()

        assert type(image_urls) is list

    def test_ad_mail_login_url(self):
        login_url = self.conf.get_ad_mail_login_url()

        assert type(login_url) is str

    def test_ad_mail_login_kes(self):
        login_keys = self.conf.get_ad_mail_login_keys()

        assert type(login_keys) is list

    def test_get_web_search_url(self):

        search_url = self.conf.get_web_search_url()

        assert type(search_url) is str

    def test_get_web_search_login_url(self):

        login_url = self.conf.get_ad_mail_login_url()

        assert type(login_url) is str
