from odoo import models, fields, api


class ShipInfo(models.Model):
    _name = 'ship.info'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Ship Info'

    image_128 = fields.Image("Logo", max_width=128, max_height=128)
    model = fields.Char()
    state = fields.Selection(
        [('new_request', 'New Request'), ('to_order', 'To order'), ('registered', 'Registered')], default='new_request')
    # state not in views
    type_ship = fields.Selection(
        [('tug_boat', 'Tug Boat'), ('pilot_boat', 'Pilot Boat'), ('mooring_boat', 'Mooring  Boat')],
        default='tug_boat', group_expand=True)
    name = fields.Char(string="Ship Name")
    IMO_number = fields.Char(string="IMO#")
    grt = fields.Char(string="GRT")
    # grt not
    draft = fields.Char(string="Draft")
    # draft not
    length_overall = fields.Char(string="Length Overall") #
    width = fields.Char(string="Width")#
    call_sign = fields.Char(string="Call Sign")
    total_hp = fields.Integer(string="Total HP")
    total_kw = fields.Integer(string="Total KW")
    flag = fields.Char(string="Flag")
    flag_b = fields.Char()
    fuel_capacity = fields.Float(string="Fuel Capacity")#
    puller_pull_capacity = fields.Float(string="Puller Pull Capacity")#
    #
    m_e_manufacture = fields.Char(string="M/E Manufacture")#
    m_e_model = fields.Char(string="M/E Model#")#
    stbd_me_sr = fields.Char(string="STBD M/E SR#")#
    psd_me_sr = fields.Char(string="PSD M/E SR#")#
    a_e_manufacture = fields.Char(string="A/E Manufacture")#
    a_e_model = fields.Char(string="A/E Model#")#
    a_e1_sr = fields.Char(string="A/E1 SR#")#
    a_e2_sr = fields.Char(string="A/E2 SR#")#
    a_e3_sr = fields.Char(string="A/E2 SR#")#
    type = fields.Selection([])#
    port_if_register = fields.Char()
    #
    tank_capacity = fields.Float(required=True)
    fuel_exist_in_tank = fields.Float(compute='_compute_fuel_exist_in_tank_func')
    fuel_progress_bar = fields.Float(compute='_compute_fuel_progress_bar', string="Fuel")
    current_running_hours = fields.Float(compute='_compute_fuel_progress_bar', string="Running Hours", store=True)
    #
    gross_tonnage = fields.Char()
    net_tonnage = fields.Char()
    dead_weight = fields.Char()
    overall_length = fields.Char()
    lpp = fields.Char()
    breadth = fields.Char()
    depth = fields.Char()
    draught = fields.Integer()
    free_board = fields.Integer()
    #
    main_manufacturer = fields.Char()
    main_model = fields.Char()
    main_stbd_sr_no = fields.Char()
    main_psd_sr_no = fields.Char()
    main_center_sr_no = fields.Char()#
    auxiliary_manufacturer = fields.Char()
    auxiliary_model = fields.Char()
    auxiliary_stbd_sr_no = fields.Char()
    auxiliary_psd_sr_no = fields.Char()
    auxiliary_center_sr_no = fields.Char()
    certificate_ids = fields.One2many('ship.certificate', 'ship_id')
    certificate_id = fields.Many2one('ship.certificate', compute='_compute_last_certificate')
    certificate_state = fields.Selection(related='certificate_id.state')
    certificate_number = fields.Char(related='certificate_id.number')
    certificate_type = fields.Selection(related='certificate_id.type')
    certificate_start_date = fields.Date(related='certificate_id.start_date')
    certificate_expire_date = fields.Date(related='certificate_id.expire_date')
    certificate_attach_file = fields.Binary(related='certificate_id.attach_file')
    certificate_attach_file_1 = fields.Binary(related='certificate_id.attach_file_1')
    report_ids = fields.One2many('ship.report', 'name')

    @api.depends('model', 'type', 'tank_capacity', 'report_ids.fuel_consumption')
    def _compute_fuel_progress_bar(self):
        for rec in self:
            if rec.report_ids:
                rec.fuel_progress_bar = 0
                fuel_consumption = sum([x.fuel_consumption for x in rec.report_ids])
                fuel_add = sum([x.add_fuel for x in rec.report_ids])

                if rec.tank_capacity:
                    rec.fuel_progress_bar = (rec.fuel_exist_in_tank / rec.tank_capacity) * 100
                rec.current_running_hours = sum([x.running_hours for x in rec.report_ids])
            else:
                rec.fuel_progress_bar = 0
                rec.current_running_hours = 0

    @api.depends('model', 'type', 'tank_capacity', 'report_ids.fuel_consumption')
    def _compute_fuel_exist_in_tank_func(self):
        for rec in self:
            if rec.report_ids:
                fuel_consumption = sum([x.fuel_consumption for x in rec.report_ids])
                fuel_add = sum([x.add_fuel for x in rec.report_ids])
                rec.fuel_exist_in_tank = fuel_add - fuel_consumption
            else:
                rec.fuel_exist_in_tank = 0

    @api.depends('certificate_ids')
    def _compute_last_certificate(self):
        for rec in self:
            if rec.certificate_ids:
                if len(rec.certificate_ids) == 1:
                    certificate = rec.certificate_ids.filtered(
                        lambda l: l.create_date == max(
                            [max([x.create_date for x in rec.certificate_ids]) if rec.certificate_ids else 0]))
                else:
                    certificate = rec.certificate_ids.filtered(
                        lambda l: l.create_date == max(
                            [x.create_date for x in rec.certificate_ids if
                             x.create_date]))
                rec.certificate_id = certificate.id or False
            else:
                rec.certificate_id = False

    def open_request_maintenance(self):
        return {
            'name': 'Request Maintenance',
            'type': 'ir.actions.act_window',
            'res_model': 'request.maintenance',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('naval_fleet.request_maintenance_form_view').id,
            'context': {'default_ship_id': self.id},
            'target': 'new',
        }

    def open_create_report_daily(self):
        return {
            'name': 'Report Daily',
            'type': 'ir.actions.act_window',
            'res_model': 'report.daily.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('naval_fleet.report_daily_form_view').id,
            'context': {'default_name': self.id},
            'target': 'new',
        }

    def print_report_daily(self):
        return {
            'name': 'Report Daily',
            'type': 'ir.actions.act_window',
            'res_model': 'print.report.daily.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('naval_fleet.print_report_daily_form_view_wizard').id,
            'context': {'default_name': self.id},
            'target': 'new',
        }

    def add_fuel_func(self):
        return {
            'name': 'Add Fuel',
            'type': 'ir.actions.act_window',
            'res_model': 'add.fuel.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('naval_fleet.add_fuel_form_view').id,
            'context': {'default_name': self.id},
            'target': 'new',
        }

    ship_status = fields.Selection([
     ('1', 'Available'),
     ('2', 'In Maintenance'),
     ('3', 'Out Of Service'),
    ], string='Ship Status', widget='circle_selection', default='1')
