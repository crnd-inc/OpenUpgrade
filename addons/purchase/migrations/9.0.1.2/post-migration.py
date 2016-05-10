# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
import logging
from openerp import api, pooler, SUPERUSER_ID
from datetime import datetime


def set_purchase_method(cr):
    # Set all records to receive.
    openupgrade.logged_query(cr, """
    UPDATE product_template 
    SET purchase_method = 'receive' 
    WHERE purchase_method is NULL
    """)

def map_order_state(cr):
    # Mapping values of state field for purchase.order
    openupgrade.map_values(
        cr, openupgrade.get_legacy_name('state'), 'state', 
        [('approved', 'purchase'), ('bid', 'sent'), ('cancel', 'cancel'), ('confirmed', 'to approve'), ('done', 'done'), ('draft', 'draft'), ('except_invoice', 'purchase'), ('except_picking', 'purchase'), ('sent', 'sent')],
        table='purchase_order')

def product_id_env(env):
    # Assign product where it is NULL
    product = env['product.product'].create({'name': 'Service Product', 'type': 'service'})
    env.cr.execute("""update purchase_order_line set product_id = %s where product_id is null""" % product.id)

@openupgrade.migrate()
def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    product_id_env(env)
    map_order_state(cr)
#    set_purchase_method(cr)
