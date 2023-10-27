from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ShipmentRequest(models.Model):
    _name = 'shipment.maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    partner_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.uid)
    state = fields.Selection([('new_request', 'NEW REQUEST'), ('approved', 'APPROVED'), ('inspection', 'INSPECTION'),
                              ('maintenance', 'MAINTENANCE'), ('done', 'Done')], default='new_request',
                             group_expand=True)
    user_id = fields.Many2one('res.users', string='User')
    attachment = fields.Binary(string='Attach File')
    request_priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')],
                                        string='Priority')
    services = fields.Selection([('electrical', 'Electrical'), ('mechanical', 'Mechanical'), ('other', 'Other')])
    maintenance_request_detail = fields.Text()
    list_of_damage = fields.Html()
    manager_approved = fields.Boolean(string='Manager')
    department_approved = fields.Boolean(string='Department')
    maintenance_time = fields.Datetime()
    maintenance_schedule_date = fields.Datetime()
    maintenance_duration = fields.Float()
    maintenance_responsible_id = fields.Many2one('res.users', string='Responsible ')

    # inspection
    # inspection_team_id = fields.Many2one('maintenance.team', string='Inspection Team')
    inspection_responsible_id = fields.Many2one('res.users', string='Responsible ')
    inspection_scheduled_date = fields.Datetime(string='Scheduled Date ', default=fields.datetime.now())
    inspection_duration = fields.Float(string='Duration')
    inspection_priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')],
                                           string='Priority')

    # notebook
    time_sheet_ids = fields.One2many('maintenance.time.sheet', 'name')
    spare_parts_ids = fields.One2many('spare.parts', 'name')
    customer_id = fields.Many2one('res.partner', string='Customer')
    type = fields.Char(string='Type')
    description = fields.Html()
    request_date = fields.Datetime(default=fields.datetime.now())
    tug_name_id = fields.Many2one('ship.info')

    def set_to_maintenance_func(self):
        self.check_inspection_result()
        self.state = 'maintenance'

    def create_inspection_func(self):
        self.state = 'inspection'
        if self.tug_name_id:
            self.env['ship.move.time'].create({
                'ship_info_id': self.tug_name_id.id,
                'maintenance_request_id': self.id,
                'time': self.inspection_scheduled_date,
                'duration': self.inspection_duration,
            })

    def work_in_progress_func(self):
        pass

    def set_to_done_func(self):
        for line in self.time_sheet_ids:
            if line.maintenance_result == 'need_to_repair':
                raise ValidationError('There is a maintenance result in process')
        self.state = 'done'

    def check_inspection_result(self):
        if self.time_sheet_ids.filtered(lambda l: l.inspection_result == 'not_checked'):
            raise ValidationError('you have record in process inspection result Not Checked')

    @api.onchange('manager_approved')
    def change_state(self):
        if self.manager_approved:
            self.department_approved = True
            self.state = 'approved'
        else:
            self.department_approved = False
            self.state = 'new_request'


class MaintenanceTimeSheet(models.Model):
    _name = 'maintenance.time.sheet'
    _description = 'Maintenance Time Sheet'

    name = fields.Many2one('shipment.maintenance')
    date = fields.Date(default=fields.Date.today())
    user_id = fields.Many2one('res.users', default=lambda self: self.env.uid)
    service_type_desc = fields.Char()
    # service_type = fields.Selection([('full_service', 'Full Service')])
    duration = fields.Float(string='Duration (Hours)')
    inspection_result = fields.Selection(
        [('done', 'Done'), ('need_to_repair', 'Need to repair'), ('not_checked', 'Not Checked')])
    maintenance_result = fields.Selection(
        [('done', 'Done'), ('need_to_repair', 'In process')])


class SpareParts(models.Model):
    _name = 'spare.parts'
    _description = 'Spare Parts'

    name = fields.Many2one('shipment.maintenance')
    product_id = fields.Many2one('product.product', string="Product")
    qty = fields.Integer(string="Quantity")
    barcode = fields.Char(related="product_id.barcode", string="Barcode")
    unit = fields.Many2one(related="product_id.uom_id", string="Unit Of Measure")
    note = fields.Char(string="Note")
