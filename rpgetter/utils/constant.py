"""
Constant types in Python.
"""
import os
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG_DIR = os.path.join(PROJECT_ROOT, 'config')
DEFAULT_CONFIG_JSON = os.path.join(CONFIG_DIR, 'rpgetter.json')

LIB_DIR = os.path.join(PROJECT_ROOT, 'lib')
CHROME_DRIVER_PATH = os.path.join(LIB_DIR, 'chromedriver')
RAKUTEN_ADD_ON_PATH = os.path.join(LIB_DIR, 'extension_4_648_0_0.crx')


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
