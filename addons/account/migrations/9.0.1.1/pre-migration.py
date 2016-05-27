# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


column_renames = {
    'account_bank_statement': [
        ('closing_date', 'date_done'),
    ],
    'account_cashbox_line': [
        ('number_opening', None),
        ('number_closing', None),
    ],
    'account_account_type': [
        ('close_method', None),
    ],
    'account_bank_statement_line': [
        ('journal_entry_id', None),
    ],
}

column_copy = {
    'account_bank_statement': [
        ('state', None, None),
    ],
    'account_journal': [
        ('state', None, None),
    ]
}


@openupgrade.migrate()
def migrate(cr, version):

    openupgrade.rename_columns(cr, column_renames)
    openupgrade.copy_columns(cr, column_copy)
