# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenUpgrade module for Odoo
#    @copyright 2014-Today: Odoo Community Association
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openupgradelib import openupgrade
logger = logging.getLogger('OpenUpgrade')

# copied from pre-migration
column_copies = {
    'project_task': [
        ('description', None, None),
    ],
}


def map_priority(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('priority'),
        'priority',
        [('2', '1')],
        table='project_task', write='sql')


def map_template_state(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('state'),
        'state',
        [('template', 'draft')],
        table='project_project', write='sql')

def migrate_stock_warehouse(cr, pool):
    """Enable manufacturing on all warehouses. This will trigger the creation
    of the manufacture procurement rule"""
    warehouse_obj = pool['account.analytic.account']
    warehouse_ids = warehouse_obj.search(cr, SUPERUSER_ID, [])
    print "post-migration &&&&&&&&&&&&&&&&&&&&&&&&&&&&", warehouse_ids
#    warehouse_obj.write(
#        cr, SUPERUSER_ID, warehouse_ids, {'manufacture_to_resupply': True})
#    if len(warehouse_ids) > 1:
#        openupgrade.message(
#            cr, 'mrp', False, False,
#            "Manufacturing is now enabled on all your warehouses. If this is "
#            "not appropriate, disable the option 'Manufacture in this "
#            "Warehouse' on the warehouse settings. You need to have 'Manage "
#            "Push and Pull inventory flows' checked on your user record in "
#            "order to access this setting.")

#@openupgrade.migrate()
#def migrate(cr, version):
#    with api.Environment.manage():
#    env = api.Environment(cr, SUPERUSER_ID, {})
#    pool = pooler.get_pool(cr.dbname)
#    bom_product_template(cr)
#    migrate_bom_lines(cr, pool)
#    fix_domains(cr, pool)
#    update_stock_moves(env)
#    update_stock_picking_name(cr, pool)
#    migrate_product_supply_method(cr, pool)
#    migrate_product(cr, pool)
#    migrate_stock_warehouse(cr, pool)
#    migrate_procurement_order(cr, pool)
#    openupgrade_80.set_message_last_post(
#        cr, SUPERUSER_ID, pool,
#        ['mrp.bom', 'mrp.production', 'mrp.production.workcenter.line'])

@openupgrade.migrate()
def migrate(cr, version):
    pool = pooler.get_pool(cr.dbname)
    migrate_stock_warehouse(cr, pool)
    map_priority(cr)
    map_template_state(cr)
    for table_name in column_copies.keys():
        for (old, new, field_type) in column_copies[table_name]:
            openupgrade.convert_field_to_html(cr, table_name, openupgrade.get_legacy_name(old), old)
