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

def convert_template_id_to_product_id(cr):
    openupgrade.logged_query(cr, """
        UPDATE product_price_history ph
        SET product_id = p.id
        FROM product_product p
        WHERE ph.product_template_id = p.product_tmpl_id
        """)
    cr.execute("Select product_id from product_price_history")
    s = cr.fetchall()
    print "\n\nconvert_template_id_to_product_id &&&&&&&&&&&&&&&&&&&&&&&&&&", s

def map_base(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('base'),
        'base',
        [('1', 'pricelist'), ('2', 'list_price')],
        table='product_pricelist_item', write='sql')

@openupgrade.migrate()
def migrate(cr, version):
    print "\n\nPOST #############################", version, cr
#    openupgrade.logged_query(cr, """ALTER TABLE product_price_history
#              ADD COLUMN product_id integer
#              """)
    a = openupgrade.column_exists(cr, 'product_price_history', 'product_id')
    print "\n\nRETURNS column_exists ================================", a
#    convert_template_id_to_product_id(cr)
    print "Pre #############################", version, cr
    map_base(cr)
