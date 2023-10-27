from odoo import fields, models, api


class ShipBerth(models.Model):
    _name = 'ship.berth'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Selection([('waiting', 'Waiting'),
                             ('anchor', 'Anchor'), ('alongside', 'Alongside'),
                             ('sailing', 'Sailing')])
    berth_line_ids = fields.One2many('ship.berth.line', 'berth_id')


# ShipBerthLine Model Hasn't a View File #
class ShipBerthLine(models.Model):
    _name = 'ship.berth.line'

    name = fields.Char()
    berth_id = fields.Many2one('ship.berth')
