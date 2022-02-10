from odoo import fields, models


class RevisionHistory(models.Model):
    _name = 'revision.history'
    _description = 'Revision History'
    _rec_name = 'revision_level'

    revision_level = fields.Char(string='Revision Level', default=False,
                                 copy=False)
    desc_of_change = fields.Text(string='Description of Change', default=False,
                                 copy=False)
    revision_date = fields.Datetime(string='Revision Date', default=False,
                                    copy=False)
    approval_stamp_id = fields.Many2one('res.users', string='Approval Stamp',
                                        copy=False)
    revision_purchase_id = fields.Many2one("purchase.order")
