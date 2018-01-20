# -*- coding: utf-8 -*-
class WriteDBProtectionError(Exception):
    """ 書き込み権限のないDBに書き込みに行った時のエラー
    """
    pass


class DefaultDBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ('service_api', 'account', 'team', 'competition'):
            return 'service_api'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ('service_api', 'account', 'team', 'competition'):
            return 'service_api'
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return obj1._meta.app_label == obj2._meta.app_label

    def allow_migrate(self, db, app_label, model=None, **hints):
        return model and app_label == model._meta.app_label
