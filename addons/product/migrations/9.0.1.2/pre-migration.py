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

from openupgradelib import openupgrade


# For 'base' map_values in post-migration
column_renames = {
    'product_pricelist_item': [
        ('base', None),
    ],
    'product_price_history': [
        ('product_template_id', None),
    ],
}

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

@openupgrade.migrate()
def migrate(cr, version):
    # delete a view from obsolete module account_report_company that causes
    # migration of the account module not to happen cleanly
    cr.execute(
        "delete from ir_ui_view v "
        "using ir_model_data d where "
        "v.id=d.res_id and d.model='ir.ui.view' and "
        "d.name='product_template_search_view'")
    openupgrade.logged_query(cr, """ALTER TABLE product_price_history
              ADD COLUMN product_id integer
              """)
    a = openupgrade.column_exists(cr, 'product_price_history', 'product_id')
    b = openupgrade.column_exists(cr, 'product_price_history', 'product_template_id')
    print "\n\nRETURNS column_exists ================================", a, b
    convert_template_id_to_product_id(cr)
    openupgrade.logged_query(cr, """
        ALTER TABLE product_pricelist_item
        ALTER COLUMN base
        TYPE VARCHAR
        """)
    openupgrade.rename_columns(cr, column_renames)
    b = openupgrade.column_exists(cr, 'product_price_history', 'product_template_id')
    print "\n\nRETURNS column_exists ================================", a, b
    openupgrade.rename_xmlids(cr, [('product.product_template_search_view', 'product.product_template_search_view')])
