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


def setup(*args, **kwds):
    SessionSetup.setup_from_file(*args, **kwds)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('frontend')
    parser.add_argument('--ini', default='alembic.ini')
    parser.add_argument('--section', default='alembic')
    parser.add_argument('--alias', default=DEFAULT_TARGET)
    parser.add_argument('--no-db-setup', dest="no_db_setup",
                         default=False, action='store_true')

    opts = parser.parse_args(argv)

    if not opts.no_db_setup:
        setup(opts.ini, opts.section, alias=opts.alias)

    conf = configparser.SafeConfigParser()
    conf.read([opts.ini])
    app_module = conf.get('application', 'module')
    route_prefix = conf.get('application', 'route_prefix')

    configurator = Configurator()
    configurator.include(app_module, route_prefix=route_prefix)
    urls = configurator.urls
    settings = configurator.settings
    settings.update({
        'debug': True,
        'cookie_secret': "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        })
    urls.extend([
        (u'/(.*)', YAStaticFileHandler, {'path': opts.frontend}),
        ])
    print(urls)
    app = Application(urls, **settings)
    app.listen(8000)
    loop = IOLoop.instance()
    loop.start()

if __name__ == '__main__':
    main()
