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

def map_type_tax_use(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('type_tax_use'), 'type_tax_use',
        [('all', 'none')],
        table='account_tax', write='sql')

def map_type_tax_use_template(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('type_tax_use'), 'type_tax_use',
        [('all', 'none')],
        table='account_tax_template', write='sql')

def map_journal_state(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('type'), 'type',
        [('purchase_refund', 'purchase'), ('sale_refund', 'sale'), ('situation', 'general')],
        table='account_journal', write='sql')
    
def account_chart_tax_template(cr):

############################## Account CHART template ########################

    cr.execute("""
    select id from account_chart_template
    """)
    chart_ids = cr.dictfetchall()
    
    cr.execute("""
    select id from res_company
    """)
    company_ids = cr.dictfetchall()
    list_of_companies = company_ids[1:]
    
    cr.execute("""
    select count(id) from res_company
    """)
    company = cr.fetchone()
    no_of_companies = int(company[0])
    company_count = no_of_companies - 1
    
    cr.execute("""
    select count(id) from account_chart_template
    """)
    chart = cr.fetchone()
    chart_template_count = int(chart[0])
    
    cr.execute("""
    UPDATE account_chart_template SET company_id = r.id 
    from res_company r
    """)

    for n in range(company_count):
        company_id = list_of_companies[n]['id']
        for m in range(chart_template_count):
            chart_id = chart_ids[m]['id']
            cr.execute("""
            INSERT INTO account_chart_template (property_account_receivable_id, property_account_payable_id, 
            property_account_expense_categ_id, property_account_income_categ_id, property_account_expense_id, 
            property_account_income_id, transfer_account_id, create_uid, write_uid, create_date, write_date, 
            name, code_digits, visible, currency_id, complete_tax_set, account_root_id, tax_code_root_id, 
            bank_account_view_id, company_id) 
            SELECT property_account_receivable_id, property_account_payable_id, 
            property_account_expense_categ_id, property_account_income_categ_id, property_account_expense_id, 
            property_account_income_id, transfer_account_id, create_uid, write_uid, create_date, write_date, 
            name, code_digits, visible, currency_id, complete_tax_set, account_root_id, tax_code_root_id, 
            bank_account_view_id, %s from account_chart_template where id = %s
            """ %(company_id, chart_id))

############################## Account TAX template ########################
    
    cr.execute("""
    SELECT COUNT(chart_template_id), chart_template_id FROM account_tax_template GROUP BY chart_template_id
    """)
    chart_template = cr.dictfetchall()
    
    tax_ids = []
    for x in range(len(chart_template)):
        first_count = chart_template[x]['chart_template_id']
        cr.execute("""
        SELECT id FROM account_tax_template WHERE chart_template_id = %s
        """ % first_count)
        tax_ids.append(cr.dictfetchall())
    
    other_chart_templates = []
    tax_count = []
    for x in range(len(chart_template)):
        template_id = chart_template[x]['chart_template_id']
        template_count_long = chart_template[x]['count']
        tax_count.append(int(template_count_long))
        # Assuming there are no duplicate chart template with same name and bank_account_view_id
        cr.execute("""
        SELECT id, company_id FROM account_chart_template WHERE name = (SELECT name FROM account_chart_template WHERE id=%(x)s) 
        AND bank_account_view_id = (SELECT bank_account_view_id FROM account_chart_template WHERE id=%(x)s) AND id <> %(x)s
        """ %{'x' : template_id})
        other_chart_template = cr.dictfetchall()
        other_chart_templates.append(other_chart_template)

    cr.execute("""
    UPDATE account_tax_template t SET company_id = c.company_id FROM account_chart_template c WHERE t.chart_template_id = c.id
    """)
    
    for f,k in zip(range(len(tax_count)),range(len(tax_ids))):
        for i in range(tax_count[f]):
            tax_id = tax_ids[k][i]['id']
            for n in range(company_count):
                comp_id = other_chart_templates[k][n]['company_id']
                chart_tmp_id = other_chart_templates[k][n]['id']
                cr.execute("""
                INSERT INTO account_tax_template (name, chart_template_id, company_id, 
                create_uid, write_uid, create_date, write_date, child_depend, include_base_amount, 
                account_id, refund_account_id, active, price_include, description, 
                python_applicable, python_compute, 
                type_tax_use, type, applicable_type, amount, sequence, amount_type) 
                SELECT name, %(a)s, %(b)s, 
                create_uid, write_uid, create_date, write_date, child_depend, include_base_amount, 
                account_id, refund_account_id, active, price_include, description, 
                python_applicable, python_compute, 
                type_tax_use, type, applicable_type, amount, sequence , 'percent'
                FROM account_tax_template WHERE id = %(c)s
                """ %{'a' : chart_tmp_id, 'b' : comp_id, 'c' : tax_id})

@openupgrade.migrate()
def migrate(cr, version):
    map_bank_state(cr)
    map_type_tax_use(cr)
    map_type_tax_use_template(cr)
    map_journal_state(cr)
    account_chart_tax_template(cr)
    
    # If the close_method is 'none', then set to 'False', otherwise set to 'True'
    cr.execute("""
    UPDATE account_account_type SET include_initial_balance =  CASE
    WHEN %(openupgrade)s = 'none' THEN False
    ELSE True
    END 
    """%{'openupgrade' : openupgrade.get_legacy_name('close_method')})

    # Set bank_statements_source to 'manual' 
    cr.execute("""
    UPDATE account_journal SET bank_statements_source = 'manual'
    """)

    # Value 'percentage_of_total' => 'percentage' 
    cr.execute("""
    UPDATE account_operation_template SET amount_type = 'percentage' WHERE amount_type = 'percentage_of_total' 
    """)

    anglo_saxon_installed = openupgrade.is_module_installed(cr, 'account_anglo_saxon')
    if anglo_saxon_installed:
        cr.execute("""
        UPDATE res_company SET anglo_saxon_accounting = True
        """)

    # deprecate accounts where active is False
    cr.execute("""
    UPDATE account_account SET deprecated = True WHERE active = False
    """)

    # Set display_on_footer to False
    cr.execute("""
    UPDATE account_journal SET display_on_footer = False
    """)

    # Logic to move from child_ids to children_tax_ids (o2m => m2m)
    cr.execute("""
    INSERT INTO account_tax_filiation_rel (parent_tax, child_tax) 
    SELECT parent_id, id from account_tax WHERE parent_id IS NOT NULL
    """)

    # Get parent_id and insert it into children_tax_ids (m2o => m2m)
    cr.execute("""
    INSERT INTO account_tax_template_filiation_rel (parent_tax, child_tax) 
    SELECT parent_id, id from account_tax_template WHERE parent_id IS NOT NULL
    """)

    # In v8, if child_depend == True, then in v9, set amount_type='group'
    cr.execute("""
    UPDATE account_tax SET amount_type = 'group'
    WHERE child_depend IS True
    """)
    cr.execute("""
    UPDATE account_tax_template SET amount_type = 'group'
    WHERE child_depend IS True
    """)

    registry = RegistryManager.get(cr.dbname)
    openupgrade.m2o_to_x2m(
    cr, registry['account.bank.statement.line'],
    'account_bank_statement_line',
    'journal_entry_ids',
    openupgrade.get_legacy_name('journal_entry_id'))

