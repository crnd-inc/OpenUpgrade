# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade
logger = logging.getLogger('OpenUpgrade')

def map_order_state(cr):
    # Mapping values of state field for hr_expense
    openupgrade.map_values(
        cr, openupgrade.get_legacy_name('state'), 'state', 
        [('confirm', 'submit'), ('accepted', 'approve'), ('done', 'post'),
         ('paid', 'done'), ('cancelled', 'cancel')],
        table='hr_expense')

@openupgrade.migrate()
def migrate(cr, version):
    map_order_state(cr)
    cr.execute("""
    UPDATE hr_expense h SET product_id = l.product_id, unit_amount = 
    l.unit_amount, quantity = l.unit_quantity FROM hr_expense_line l 
    WHERE l.expense_id = h.id
    """)

    cr.execute("""
    SELECT * from (SELECT expense_id, COUNT(expense_id) AS "no_of_expenses", 
    case when COUNT(expense_id)>1 then true else null end as "consider" 
    FROM hr_expense_line GROUP BY expense_id) as voila where consider is not null
    """)
    a=cr.dictfetchall()
    for x in a:
        expense = x['expense_id']
        no_of_expense = x['no_of_expenses']
        cr.execute("""
            select id from hr_expense_line where expense_id = %s
            """ %expense)
        e=cr.fetchall()
        line_ids = [n[0] for n in e[1:]]
        g=cr.fetchall()
        for z,p in zip(range(no_of_expense-1),line_ids):
            #    analytic_account_id, payment_mode, description
            cr.execute("""
            INSERT INTO hr_expense 
                (company_id, currency_id, journal_id, employee_id, state, date, account_move_id, name, bank_journal_id, product_uom_id, unit_amount, quantity, product_id)
                SELECT company_id, currency_id, journal_id, employee_id, state, date, account_move_id, name, bank_journal_id, 1,
                (select unit_amount from hr_expense_line where id = %(a)s),
                (select quantity from hr_expense_line where id = %(a)s),
                (select product_id from hr_expense_line where id = %(a)s)
                FROM hr_expense where id = %(b)s
            """ %{'a' : z, 'b':expense})
