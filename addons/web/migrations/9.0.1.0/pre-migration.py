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

    # delete a qweb template from obsolete module web_gantt
    cr.execute(
        "delete from ir_ui_view v "
        "where name = 'web_gantt assets'")

    # delete a qweb template from obsolete module web_graph
    cr.execute(
        "delete from ir_ui_view v "
        "where name = 'web_graph assets'")

    # delete a qweb template from obsolete module web_graph
    cr.execute(
        "delete from ir_ui_view v "
        "where name = 'share assets'")

    cr.execute(
        "delete from ir_ui_view v "
        "where name = 'im_chat assets'")

# delete a qweb template from obsolete module web_graph
    cr.execute(
        "delete from ir_ui_view v "
        "where name = 'Webclient Bootstrap - Share'")


    cr.execute(
        "delete from ir_ui_view v "
        "where name = 'base_setup assets'")
