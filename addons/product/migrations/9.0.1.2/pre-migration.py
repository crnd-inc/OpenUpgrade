# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


# For 'base' map_values in post-migration
column_renames = {
    'product_pricelist_item': [
        ('base', None),
        ('price_version_id', None)
    ],
    'product_price_history': [
        ('product_template_id', None)
    ],
}


@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.logged_query(cr, """ALTER TABLE product_price_history
              ADD COLUMN product_id integer
              """)
    openupgrade.logged_query(cr, """
        ALTER TABLE product_pricelist_item
        ALTER COLUMN base
        TYPE VARCHAR
        """)
    openupgrade.rename_columns(cr, column_renames)

    openupgrade.logged_query(cr, """
        ALTER TABLE product_packaging ALTER COLUMN rows DROP NOT NULL
        """)

    openupgrade.logged_query(cr, """
        ALTER TABLE product_packaging ALTER COLUMN ul DROP NOT NULL
        """)

    openupgrade.logged_query(cr, """
        ALTER TABLE product_packaging ALTER COLUMN ul_container DROP NOT NULL
        """)
