from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    ap_remit_to = fields.Char(string='AP Remit To')