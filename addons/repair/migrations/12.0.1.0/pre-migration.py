# Copyright 2019 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


_model_renames = [
    ('mrp.repair', 'repair.order'),
    ('mrp.repair.fee', 'repair.fee'),
    ('mrp.repair.line', 'repair.line'),
]

_table_renames = [
    ('mrp_repair', 'repair_order'),
    ('mrp_repair_fee', 'repair_fee'),
    ('mrp_repair_line', 'repair_line'),
]

xmlid_renames = [
    ('mrp_repair.mrp_repair_rule', 'repair.repair_rule'),
    ('mrp_repair.seq_mrp_repair', 'repair.seq_repair'),
    ('mrp_repair.mail_template_mrp_repair_quotation',
     'repair.mail_template_repair_quotation'),
]


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    openupgrade.rename_models(cr, _model_renames)
    openupgrade.rename_tables(cr, _table_renames)
    openupgrade.rename_xmlids(env.cr, xmlid_renames)
