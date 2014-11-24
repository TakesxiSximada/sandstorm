# -*- coding: utf-8 -*-
from zope.interface import (
    Interface,
    Attribute,
    )


class IRegistryManager(Interface):
    """レジストリを管理するためのクラス
    zope.interfaceの不足している機能をこのクラスで提供する
    """
    required = Attribute(u'要求するInterfaceのリスト')
    provided = Attribute(u'提供するInterface')
    registry_factory = Attribute(u'使用するRegistryを返すcallable object')

    def __enter__():
        """For with statement
        """
        return object()  # pragma: no cover

    def __exit__(exec_type, exec_val, exec_tb):
        """For with statement
        """

    def verify(impl):
        """implがinterfaceを提供しているかどうかを確認する
        """

    def implemented_by(impl):
        """implがinterfaceを提供しているかどうかを確認する
        提供していればTrue、していなければFalseを返す。
        """
        return True or False  # pragma: no cover

    def names():
        """管理しているレジストリに登録されている名前の一覧のリストを返す
        """
        return list()  # pragma: no cover

    def register(name, impl, update=False):
        """管理しているレジストリに実装を登録する
        """

    def lookup(name):
        """nameから登録されている実装を取得する
        無い場合はNoneを返す
        """
        return object or None  # pragma: no cover

    def create(name, *args, **kwds):
        """nameから登録されている実装を用いてそれをインスタンス化する
        無い場合はNoneを返す
        """
        return object() or None  # pragma: no cover
