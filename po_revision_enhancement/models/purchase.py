from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    revised_po = fields.Boolean(string="Revised PO", default=False, copy=False,
                                readonly=True, tracking=True)
    po_id = fields.Many2one('purchase.order', default=False, copy=False,
                            readonly=True)
    revision_ids = fields.One2many('revision.history', 'revision_purchase_id',
                                   default=False, copy=False, tracking=True)
    sequence = fields.Integer(default=0,copy=False)
    revision_id = fields.Many2one('revision.history', "Revision Reference",copy=False)
    latest_revision_date = fields.Datetime(copy=False, invisible=True)
    revision_purchase_name = fields.Char(string='Purchase Order', default=False, copy=False)
    last_rev_id = fields.Many2one('revision.history', compute='_compute_get_last_record', copy=False, invisible=True)
    confirm_po_partner_id = fields.Many2one('res.partner',copy=False,default=False)


    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.write({'confirm_po_partner_id': self.env.user.partner_id.id})
        return res


    def _compute_get_last_record(self):
        record = self.env['revision.history'].search([('revision_purchase_id', '=', self.id)], limit=1,
                                                     order='create_date desc')
        if record:
            self.last_rev_id = record.id
            self.latest_revision_date = record.revision_date
            self.revision_purchase_name = record.revision_level
        else:
            self.last_rev_id = False
            self.latest_revision_date = False


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    order_id = fields.Many2one('purchase.order', default=lambda self: self.env[
        'purchase.order'].browse(self._context.get('active_id')))
