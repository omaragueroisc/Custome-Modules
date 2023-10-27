from odoo import models, fields, api


class RequestMaintenance(models.TransientModel):
    _name = 'request.maintenance'
    _description = 'Request Maintenance'

    name = fields.Char(string='Name')
    ship_id = fields.Many2one('ship.info')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.uid)
    date_request = fields.Datetime(default=fields.datetime.now())
    request_priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')],
                                        string='Priority')
    services = fields.Selection([('electrical', 'Electrical'), ('mechanical', 'Mechanical'), ('other', 'Other')])
    maintenance_request_detail = fields.Text()
    list_of_damage = fields.Html()
    attachment = fields.Binary(string='Attach File')

    def create_request_maintenance(self):
        request = self.env['shipment.maintenance'].create(
            {'services': self.services, 'maintenance_request_detail': self.maintenance_request_detail,
             'list_of_damage': self.list_of_damage, 'request_priority': self.request_priority,
             'attachment': self.attachment, 'name': self.name, 'request_date': self.date_request
                , 'user_id': self.user_id.id, 'tug_name_id': self.ship_id.id})
