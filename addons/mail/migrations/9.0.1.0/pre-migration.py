# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
import logging
logger = logging.getLogger('OpenUpgrade.stock')


def create_res_user_fields(cr):
    """ This function reduce creation time of the stock_move fields
       This part of the function (pre) just create the field and let
       the other function in post script fill the value, because orm is needed
    """
    logger.info("Fast creation of the field res_users.chatter_needaction_auto "
                "(pre)")

    cr.execute("""
        ALTER TABLE res_users
        ADD COLUMN "chatter_needaction_auto" BOOLEAN DEFAULT FALSE""")


@openupgrade.migrate()
def migrate(cr, version):

    # # if email_template is installed, uninstall it
    # cr.execute(
    #     "update ir_module_module set state='to remove' "
    #     "where name='email_template' "
    #     "and state in ('installed', 'to install', 'to upgrade')")

    create_res_user_fields(cr)


    openupgrade.logged_query(cr, """
        DELETE FROM ir_ui_view v
        USING ir_model_data d
        WHERE v.id=d.res_id
        AND d.module = 'email_template'
        """)
