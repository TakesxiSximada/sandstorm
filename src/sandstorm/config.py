# -*- coding: utf-8 -*-
import inspect
import configparser

from pyramid.path import DottedNameResolver
from .errors import SandstormConfigLoadError


class URLConfigurator(list):
    def load(self, urls):
        self.extend(urls)


class SettingConfigurator(dict):
    def load(self, settings):
        self.update(settings)


class Configurator(object):
    resolver = DottedNameResolver()

    def __init__(self):
        self.urls = []
        self.settings = {}
        self.prefixes = []

    def include(self, name, route_prefix=''):
        self.prefixes.append(route_prefix)
        frame = inspect.currentframe()
        prev_frame = frame.f_back
        parent_name = prev_frame.f_globals['__name__']
        modules = parent_name.split('.')
        modules.append('.')
        if name.startswith('.'):
            while name.startswith('.'):
                name = name[1:]
                modules = modules[:-1]
        else:
            modules = []
        modules.append(name)
        abs_dotted_name = '.'.join(modules)
        abs_dotted_name = (
            abs_dotted_name[1:]
            if abs_dotted_name.startswith('.') else abs_dotted_name)
        module = self.resolver.maybe_resolve(abs_dotted_name)
        includeme = getattr(module, 'includeme')
        includeme(self)
        self.prefixes.pop()

    def get_current_prefix(self):
        return '/' + '/'.join(filter(lambda x: x, self.prefixes))

    def add_route(self, url, handler, params):
        prefix = self.get_current_prefix()
        prefix += '' if prefix.endswith('/') else '/'
        url = url[1:] if url.startswith('/') else url
        real_url = prefix + url
        self.urls.append(
            (real_url, handler, params)
            )

    def load(self, package_names):
        for package in package_names:
            module = __import__(package, fromlist=True)
            includeme = getattr(module, 'includeme')
            includeme(self.urls, self.settings)

    def load_from_file(self, conf, section, option, ignore_errors=False):
        parser = configparser.SafeConfigParser()
        parser.read([conf])
        try:
            buf = parser.get(section, option)
        except Exception as err:
            if ignore_errors:
                print('WARNING: [{}] {}'.format(section, option))
            else:
                raise SandstormConfigLoadError(err)
        else:
            package_names = buf.split()
            self.load(package_names)


if __name__ == '__main__':
    conf = Configurator()
    conf.load_from_file('test.conf', 'testsection', 'testoption')
