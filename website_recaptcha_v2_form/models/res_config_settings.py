from odoo import api, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.onchange("recaptcha_v2_site_key")
    def onchange_recaptcha_v2_site_key(self):
        views_recaptcha = (
            self.env["ir.ui.view"]
            .sudo()
            .search(
                [
                    ("arch_db", "ilike", 'class="g-recaptcha"'),
                    ("website_id", "!=", False),
                ]
            )
        )
        site_key_old = views_recaptcha.arch_db.split('data-sitekey="')
        if len(site_key_old) > 1:
            site_key_old = site_key_old[1].split('"')[0]
            if site_key_old:
                div_start = '<div class="g-recaptcha" data-sitekey='
                div_end = """data-callback='callback_success_recaptcha'
                            data-expired-callback='callback_expired_recaptcha'"""
                updated_arch = views_recaptcha.arch_db.replace(
                    f'{div_start}"{site_key_old}" {div_end}/>',
                    f'{div_start} "{self.recaptcha_v2_site_key}" {div_end}/>',
                )
                views_recaptcha.sudo().write({"arch": updated_arch})
