# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(cr, version):

    # cr.execute(
    #     """delete from ir_ui_view v where name = 'web_gantt assets'""")
    #
    # cr.execute(
    #     """delete from ir_ui_view v where name = 'web_graph assets'""")
    #
    # cr.execute(
    #     """delete from ir_ui_view v where name = 'share assets'""")

    cr.execute(
        """delete from ir_ui_view v where name = 'im_chat assets'""")

    # cr.execute(
    #     """delete from ir_ui_view v
    #     where name = 'Webclient Bootstrap - Share'""")
    #
    # cr.execute(
    #     """delete from ir_ui_view v where name = 'base_setup assets'""")
