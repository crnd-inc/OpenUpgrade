# Copyright 2018 Eficent - Héctor Villarreal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade, openupgrade_merge_records


def merge_crm_lead_tag(env):

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

    _TABLE = 'crm_lead_tag'

    _COLUMNS = ['name']

    _MERGE_OPS = {
        'name': 'ignore',
    }

    duplicates = list_duplicates(env.cr, _TABLE, _COLUMNS)
    if duplicates:
        for duplicate in duplicates:
            ir_model_fields = find_duplicates(
                env.cr, _TABLE, kwargs=duplicate)
            print(ir_model_fields)
            if ir_model_fields:
                openupgrade_merge_records.merge_records(
                    env, 'crm.lead.tag', ir_model_fields['to'],
                    ir_model_fields['from'], _MERGE_OPS, method='orm'
                )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    merge_crm_lead_tag(env)
