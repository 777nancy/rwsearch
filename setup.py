from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="rwsearch",
    version="0.1.0",
    url="https://github.com/777nancy/rwsearch",
    packages=find_packages(),
    data_files=[('lib', ['lib/chromedriver']), ('lib', ['lib/extension_4_648_0_0.crx'])],
    entry_points={
        "console_scripts": [
            "rwsearch=rwsearch.rwsearch:main"
        ]
    },
    install_requires=_requires_from_file('requirements.txt'),
)
