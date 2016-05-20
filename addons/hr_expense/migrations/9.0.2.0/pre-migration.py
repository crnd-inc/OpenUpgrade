# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


column_copies = {
    'hr_expense': [
        ('state', None, None),
    ],
}

column_renames = {
    'product_template': [
        ('hr_expense_ok', 'can_be_expensed'),
    ],
    'hr_expense': [
        ('note', 'description'),
    ],
}

table_renames = [
    ('hr_expense_expense', 'hr_expense'),
    ]

#column_drops = [
#    ('project_config_settings', 'module_sale_service'),
#    ('project_config_settings', 'module_pad'),
#    ('project_config_settings', 'module_project_issue_sheet'),
#    ('project_config_settings', 'group_time_work_estimation_tasks'),
#    ('project_config_settings', 'module_project_timesheet'),
#    ]


@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_tables(cr, table_renames)
    openupgrade.rename_columns(cr, column_renames)
    openupgrade.copy_columns(cr, column_copies)
#    if openupgrade.column_exists(cr, 'project_project', 'members'):
#        openupgrade.rename_columns(cr, {'project_project': [('members', None)]})
#    # Removing transient tables to get rid of warnings
#    openupgrade.drop_columns(cr, column_drops)
