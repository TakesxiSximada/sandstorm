# -*- coding: utf-8 -*-
import os
import sys
import argparse
from azoth.sessions import DEFAULT_TARGET

from ..server import SandstormServer


def main(argv=sys.argv[1:]):  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('frontend')
    parser.add_argument('--ini', default='alembic.ini')
    parser.add_argument('--db-section', dest='db_section', default='alembic')
    parser.add_argument('--db-alias', dest='db_alias', default=DEFAULT_TARGET)
    parser.add_argument('--db-no-setup', dest='db_no_setup',
                        default=False, action='store_true')
    parser.add_argument('--ap-section', dest='ap_section', default='application')
    parser.add_argument('--ap-module', dest='ap_module', default='')
    parser.add_argument('--ap-route-prefix', dest='ap_route_prefix', default='')
    parser.add_argument('--ap-port', dest='db_alias', default=8000)
    parser.add_argument('--no-default-setup', dest='no_default_setup',
                        default=False, action='store_true')
    parser.add_argument('frontend', default=os.getcwd())
    opts = parser.parse_args(argv)

    server = SandstormServer()
    server.load(opts.ini, db_section=opts.db_section, ap_section=opts.ap_section)

    server = SandstormServer(
        frontend=opts.frontend,
        module=opts.app_module,
        route_prefix=opts.app_route_prefix,
        )

    server.setup(
        path=opts.ini,
        no_default_setup=opts.no_default_setup,
        )

if __name__ == '__main__':  # pragma: no cover
    main()
