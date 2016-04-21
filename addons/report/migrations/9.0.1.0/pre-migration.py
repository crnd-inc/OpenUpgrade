# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

#tables_renames = [
#    (
#        'im_chat_presence',
#        'bus_presence'
#    ),
#]

@openupgrade.migrate()
def migrate(cr, version):
#    openupgrade.rename_tables(cr, tables_renames)

    openupgrade.logged_query(cr, """
        DELETE FROM ir_ui_view v
        USING ir_model_data d
        WHERE v.id=d.res_id
        AND d.module = 'report'
        AND v.name = 'layout'
        """)
