# Copyright 2023 Quartile Limited
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openupgradelib import openupgrade


def migrate(cr, version):
    openupgrade.update_module_names(
        cr,
        [('project_stage_state', 'project_task_stage_state')],
        merge_modules=True,
    )
