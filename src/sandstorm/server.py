# -*- coding: utf-8 -*-
import sys
import argparse
import configparser

from tornado.web import Application
from tornado.ioloop import IOLoop

from azoth.sessions import (
    SessionSetup,
    DEFAULT_TARGET,
    )

from .config import Configurator
from .handlers import YAStaticFileHandler


DEFAULT_COOKIE_SECRET = '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__'


def setup(*args, **kwds):
    SessionSetup.setup_from_file(*args, **kwds)


class SandstormServer(object):
    def __init__(self, no_db=False):
        self.config = Configurator()
        self.no_db = no_db
        self.port = 8000

    def setup_from_file(self, confpath):
        conf = configparser.SafeConfigParser()
        conf.read([confpath])

        kwds = {
            'confpath': confpath,
            'module': conf.get('application', 'module'),
            'route_prefix': conf.get('application', 'route_prefix'),
            'debug': bool(conf.get('application', 'debug')),
            'port': int(conf.get('application', 'port')),
            'cookie_secret': conf.get('application', 'cookie_secret'),
            'frontend': conf.get('application', 'frontend'),
            'db_section': (conf.get('application', 'db_section') or 'alembic'),
            'db_alias': (conf.get('application', 'db_alias') or DEFAULT_TARGET),
            }
        self.setup(**kwds)

    def setup(self, confpath=None, module=None, route_prefix='', debug=False,
              cookie_secret=DEFAULT_COOKIE_SECRET, frontend=None, port=8000,
              db_section='alembic', db_alias=DEFAULT_TARGET):
        self.port = port if port else self.port
        if not self.no_db and confpath:
            SessionSetup.setup_from_file(confpath, db_section, db_alias)
        if module:
            self.config.include(module, route_prefix)

        settings = {
            'debug': debug,
            'cookie_secret': cookie_secret,
            }

        urls = []
        if frontend:
            urls.append((u'/(.*)', YAStaticFileHandler, {'path': frontend}))

        self.config.settings.update(settings)
        self.config.urls.extend(urls)

    def start(self):
        for url, handler, kwds in self.config.urls:
            print('{} : {} : {}'.format(url, handler, kwds))
        app = Application(self.config.urls, **self.config.settings)
        app.listen(self.port)
        loop = IOLoop.instance()
        loop.start()


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', default='alembic.ini')
    opts = parser.parse_args(argv)

    server = SandstormServer()
    server.setup_from_file(opts.conf)
    server.start()

if __name__ == '__main__':
    main()
