# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade, openupgrade_merge_records

QUANT_MERGE_OPS = {
    # The rest of the values are good with default merge operation
    'in_date': 'min',
    'removal_date': 'max',
}


def merge_quants(env):
    group_list = [
        'product_id', 'package_id', 'lot_id', 'location_id', 'owner_id',
    ]
    StockQuant = env['stock.quant']
    groups = StockQuant.read_group([], group_list, group_list, lazy=False)
    for group in groups:
        quants = StockQuant.search(group['__domain'])
        if len(quants) == 1:
            continue
        openupgrade_merge_records.merge_records(
            env, 'stock.quant', quants[1:].ids, quants[0].id, QUANT_MERGE_OPS,
        )


def merge_stock_production_lots(env):

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
        if len(res) == 0:
            return False
        recs = []
        for i in res:
            rec = {}
            for j in range(len(columns)):
                rec[columns[j]] = i[j]
            recs.append(rec)
        return recs

    def find_duplicates(cr, table, duplicated_keys):
        """
        Look for duplicates in `table` using filtered columns `duplicate`
        :param cr: db cursor
        :param table: table name
        :param duplicate: dict of duplicated to be found.
        :return: list of ids first one will merge into others.
        """
        conds = []
        for key, value in duplicated_keys.items():
            conds.append("%s = '%s'" % (key, value))
        cond = ' AND '.join(conds)
        query = ('SELECT id FROM %s WHERE %s ORDER BY id ASC' % (table, cond))
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

    _TABLE = 'stock_production_lot'

    _COLUMNS = ['name', 'product_id']

    _MERGE_OPS = {
        'ref': 'ignore',
        'name': 'ignore',
    }

    duplicates = list_duplicates(env.cr, _TABLE, _COLUMNS)
    if duplicates:
        for duplicate in duplicates:
            stock_production_lot = find_duplicates(
                env.cr, _TABLE, duplicated_keys=duplicate)
            if stock_production_lot:
                openupgrade_merge_records.merge_records(
                    env, 'stock.production.lot', stock_production_lot['to'],
                    stock_production_lot['from'], _MERGE_OPS, method='orm'
                )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    merge_quants(env)
    merge_stock_production_lots(env)
