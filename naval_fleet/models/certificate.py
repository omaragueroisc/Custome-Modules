from odoo import models, fields, api
from odoo.exceptions import UserError


class ShipCertificate(models.Model):
    _name = 'ship.certificate'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Ship Certificate'

    ship_id = fields.Many2one('ship.info')
    state = fields.Selection([('valid', 'Valid'), ('expire', 'Expire')], compute='_compute_state', store=True)
    name = fields.Char()
    number = fields.Char()
    type = fields.Selection([('personal_certificate', 'Personal Certificate')])
    start_date = fields.Date(default=fields.Date.today())
    expire_date = fields.Date(default=fields.Date.today())
    attach_file = fields.Binary()
    attach_file_1 = fields.Binary()

    @api.depends('expire_date', 'start_date')
    def _compute_state(self):
        for rec in self:
            if rec.expire_date:
                rec.state = 'expire' if fields.Date.today() >= rec.expire_date else 'valid'
            else:
                rec.state = False

    @api.onchange('start_date', 'expire_date')
    @api.constrains('start_date', 'expire_date')
    def check_start_and_expire_date(self):
        if self.expire_date < self.start_date:
            raise UserError('Expiry date must be Greater than start date')
