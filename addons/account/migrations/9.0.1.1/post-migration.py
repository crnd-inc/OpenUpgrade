# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


import logging
from openupgradelib import openupgrade
logger = logging.getLogger('OpenUpgrade')
from openerp.modules.registry import RegistryManager

def map_bank_state(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('state'), 'state',
        [('draft', 'open')],
        table='account_bank_statement', write='sql')
    
def map_journal_state(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('state'), 'state',
        [('purchase_refund', 'purchase'), ('sale_refund', 'sale'), ('situation', 'general')],
        table='account_journal', write='sql')

@openupgrade.migrate()
def migrate(cr, version):
    map_bank_state(cr)
    map_journal_state(cr)
    cr.execute("""
    UPDATE account_account SET deprecated = True WHERE active = False
    """)
    registry = RegistryManager.get(cr.dbname)
    openupgrade.m2o_to_x2m(
    cr, registry['account.bank.statement.line'],
    'account_bank_statement_line',
    'journal_entry_ids',
    openupgrade.get_legacy_name('journal_entry_id'))
    
#    cr.execute("""
#    insert into account_cashbox_line (coin_value, number) select pieces, 
#    COALESCE(%(opening)s,%(closing)s,123) 
#    from account_cashbox_line
#    """%{'opening' : openupgrade.get_legacy_name('number_opening'),
#         'closing' : openupgrade.get_legacy_name('number_closing')})

