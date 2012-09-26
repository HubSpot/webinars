class Staged(object):
    @classmethod
    def pre_stage(kls, parent):
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute('DELETE FROM %s WHERE %s_id=%%s'%(kls._meta.db_table,parent._meta.verbose_name), [parent.id])
        transaction.commit_unless_managed()

    @classmethod
    def fill(kls, parent): raise NotImplementedError()

    @classmethod
    def post_stage(kls, parent): pass


