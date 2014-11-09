import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'gevent',
    'tornado',
    'gevent-websocket==0.3.6',
    'pyramid_sockjs',
]

setup(
    name='webvim',
    version='0.0.1',
    license="AGPL v3.0",
    description='Stream Vim to the web browser with Docker.',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Britt Gresham',
    author_email='brittcgresham@gmail.com',
    url='http://www.brittg.sexy/',
    keywords='web pyramid pylons vim docker',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="webvim",
    entry_points="""\
    [paste.app_factory]
    main = webvim:main
    """,
)
