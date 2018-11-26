# Copyright 2018 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, 'base', 'migrations/11.0.1.3/ao_noupdate_changes.xml'
    )
