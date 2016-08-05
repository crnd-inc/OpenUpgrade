# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def map_account_tax_type(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('type'), 'type',
        [('code', 'code')],
        table='account_tax', write='sql')


def map_account_tax_template_type(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('type'), 'type',
        [('code', 'code')],
        table='account_tax_template', write='sql')


@openupgrade.migrate()
def migrate(cr, version):
    map_account_tax_type(cr)
    map_account_tax_template_type(cr)
