"""
Constant types in Python.
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

LIB_DIR = os.path.join(PROJECT_ROOT, 'lib')
CHROME_DRIVER = os.path.join(LIB_DIR, 'chromedriver')
R_ADD_ON = os.path.join(LIB_DIR, 'extension_4_648_0_0.crx')

LOGIN_URL = 'https://grp03.id.rakuten.co.jp/rms/nid/login?service_id=r12&return_url=login?tool_id=1&tp=&id='
WEB_SEARCH_URL = 'https://websearch.rakuten.co.jp'


class Constant:

    def __init__(self):
        module_vars = vars(sys.modules[__name__]).copy()

        for key, value in module_vars.items():
            if key.isupper():
                self.__dict__[key] = value

    class ConstantError(TypeError):
        pass

    def __setattr__(self, key, value):
        raise self.ConstantError("Can't bind constant ({}={})".format(key, value))


sys.modules[__name__] = Constant()
