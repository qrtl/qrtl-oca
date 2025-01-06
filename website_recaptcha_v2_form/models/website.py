from odoo import api, models
from odoo.exceptions import AccessDenied


class Website(models.Model):
    _inherit = "website"

    def valid_recaptcha(self, values):
        valid, message = self.is_recaptcha_v2_valid(values)
        if not valid:
            raise AccessDenied(message)
        return True

    @api.model
    def get_recaptcha_v2_site_key(self):
        return self.sudo().get_current_website().recaptcha_v2_site_key
