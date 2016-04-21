# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
import logging
logger = logging.getLogger('OpenUpgrade.stock')

@openupgrade.migrate()
def migrate(cr, version):


    openupgrade.logged_query(cr, """
        DELETE FROM ir_ui_view v
        USING ir_model_data d
        WHERE v.id=d.res_id
        AND d.module = 'email_template'
        AND d.model = 'ir.ui.view'
        """)
