# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade, openupgrade_merge_records


def merge_mail_followers(env):

    def list_duplicates(cr, table, columns):
        """
        Look for rows in `table` that has duplicates for given `columns`
        :param cr: db cursor
        :param table: table name
        :param columns: list of columns to look for coincidences
        :return: list of dict entries.
        """
        items = ', '.join(columns)
        query = ('SELECT %s FROM %s GROUP BY (%s) having count(*) > 1' %
                 (items, table, items))
        cr.execute(query)
        # TODO Change fetchall() for dictfetchall() and simplify downstream
        res = cr.fetchall()
        recs = []
        for i in res:
            rec = {}
            for j in range(len(columns)):
                rec[columns[j]] = i[j]
            recs.append(rec)
        if len(res) == 0:
            return False
        return recs

    def find_duplicates(cr, table, kwargs):
        """
        Look for duplicates in `table` using filtered columns `duplicate`
        :param cr: db cursor
        :param table: table name
        :param duplicate: dict of duplicated to be found.
        :return: list of ids first one will merge into others.
        """
        conds = []
        for key, value in kwargs.items():
            conds.append("%s = '%s'" % (key, value))
        cond = ' AND '.join(conds)
        query = ('SELECT id FROM %s WHERE ' % table) + cond + ' ORDER BY id ASC'
        cr.execute(query)
        openupgrade.logged_query(cr, query)
        res = cr.fetchall()
        if len(res) <= 1:
            return False
        record = {'to': []}
        for i in res:
            if 'from' not in record:
                record['from'] = i[0]
            else:
                record['to'].append(i[0])
        return record

    _TABLE = 'mail_followers'

    _COLUMNS = ['res_model', 'res_id', 'partner_id']

    _MERGE_OPS = {
        'ref': 'ignore',
        'name': 'ignore',
        'res_model': 'ignore'
    }

    duplicates = list_duplicates(env.cr, _TABLE, _COLUMNS)
    if duplicates:
        for duplicate in duplicates:
            mail_followers = find_duplicates(
                env.cr, _TABLE, kwargs=duplicate)
            print(mail_followers)
            if mail_followers:
                openupgrade_merge_records.merge_records(
                    env, 'mail.followers', mail_followers['to'],
                    mail_followers['from'], _MERGE_OPS, method='sql'
                )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    merge_mail_followers(env)
