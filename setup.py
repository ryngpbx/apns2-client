# coding: utf-8

from __future__ import absolute_import
import os
from setuptools import setup, Command
from io import open


class CleanCommand(Command):
    u"""Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system(u'rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


README = open(os.path.join(os.path.dirname(__file__), u'README.md')).read()
CHANGES = open(os.path.join(os.path.dirname(__file__), u'CHANGES.md')).read()


setup(
    name=u'apns2-client',
    version=u'0.5.3',
    packages=[u'apns2'],
    include_package_data=True,
    license=u'MIT License',
    description=u'apns2-client is a python package designed for simple, flexible and fast Apple Push Notifications on iOS, OSX and Safari using the new HTTP/2 Push provider API.',
    long_description=u'\n\n'.join([README, CHANGES]),
    url=u'https://github.com/oeegor/apns2-client',
    author=u'Egor Orlov',
    author_email=u'oeegor@gmail.com',
    platforms=u'any',
    classifiers=[
        u'Intended Audience :: Developers',
        u'License :: OSI Approved :: MIT License',
        u'Operating System :: OS Independent',
        u'Programming Language :: Python',
        u'Programming Language :: Python :: 3.5',
        u'Topic :: Internet :: WWW/HTTP',
        u'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    cmdclass={
        u'clean': CleanCommand,
    },
    install_requires=[
        u'hyper',
        u'ujson',
    ],
)
