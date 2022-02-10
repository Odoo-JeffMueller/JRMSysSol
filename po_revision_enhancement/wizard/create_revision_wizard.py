from odoo import fields, models
from datetime import date, datetime


class CreateRevisionWizard(models.TransientModel):
    _name = "create.revision.wizard"
    _description = "Create Revision Wizard"

    def get_po_lines(self):
        active_id = self._context.get('active_id')
        if active_id:
            po = self.env['purchase.order'].browse(active_id)
            return [(6, 0, po.order_line.ids)]

    description_of_change = fields.Text(string='Description on Revised PO',
                                        required=True)
    po_id = fields.Many2one("purchase.order",
                            default=lambda self: self.env[
                                'purchase.order'].browse(
                                self._context.get('active_id')))
    po_lines = fields.Many2many("purchase.order.line", default=get_po_lines)

    def update_purchase_order(self):
        po = self.env['purchase.order'].browse(self._context.get('active_id'))
        self.po_lines.order_id = po.id
        po.sequence += 1
        revision_id = self.env['revision.history'].create({
            'desc_of_change': self.description_of_change,
            'revision_date': date.today(),
            'approval_stamp_id': self.env.user.id,
            'revision_level': 'REV' + str(po.sequence),
            'revision_purchase_id': po.id,
        })
        po.revision_id = revision_id.id
        if po.sequence == 1:
            self.env['mail.message'].create({
                'model': 'purchase.order',
                'res_id': po.id,
                'date': datetime.now(),
                'author_id': self.env.user.partner_id.id,
                'message_type': 'notification',
                'body': f"<b>Initial Revision History :</b>"
                        f" {revision_id.revision_level},<br/>"
                        f" <b>Description For Change:</b>"
                        f" {revision_id.desc_of_change}<br/> "
                        f"<b>Date:</b> {revision_id.revision_date}"
            })
