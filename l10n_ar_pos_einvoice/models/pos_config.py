from odoo import fields, models


class pos_config(models.Model):
    _inherit = "pos.config"

    print_pdf_invoice = fields.Boolean("Print PDF Invoice", default=1)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    print_pdf_invoice = fields.Boolean(
        "Print PDF Invoice",
        readonly=False,
        related="pos_config_id.print_pdf_invoice",
    )
