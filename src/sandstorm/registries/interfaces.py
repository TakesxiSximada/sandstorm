# -*- coding: utf-8 -*-
import zope.interface
import zope.interface.adapter


class IRegistryManager(zope.interface.Interface):
    """レジストリを管理するためのクラス
    zope.interfaceの不足している機能をこのクラスで提供する
    """
    required = zope.interface.Attribute(u'要求するInterfaceのリスト')
    provided = zope.interface.Attribute(u'提供するInterface')
    registry_factory = zope.interface.Attribute(u'使用するRegistryのファクトリ')

    def implemented_by(self, impl):
        """implがinterfaceを提供しているかどうかを確認する
        提供していればTrue、していなければFalseを返す。
        """
        return True or False

    def names(self):
        """管理しているレジストリに登録されている名前の一覧のリストを返す
        """
        return list()

    def register(self, name, impl, update=False):
        """管理しているレジストリに実装を登録する
        """
        pass

    def lookup(self, name):
        """nameから登録されている実装を取得する
        無い場合はNoneを返す
        """
        return object or None

    def create(self, name, *args, **kwds):
        """nameから登録されている実装を用いてそれをインスタンス化する
        無い場合はNoneを返す
        """
        return object() or None
