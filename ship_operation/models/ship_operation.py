from odoo import models, fields, api
from datetime import datetime


class ShipOperation(models.Model):
    _name = 'ship.operation'
    _description = 'Ship Operation'

    name = fields.Many2one('res.partner', string='Vessels name')
    state = fields.Selection([('expected', 'Expected'), ('waiting', 'Waiting'),
                              ('anchor', 'Anchor'), ('alongside', 'Alongside'),
                              ('sailing', 'Sailing'), ], default='expected', group_expand=True)
    from_state_berth = fields.Many2one('ship.berth.line', string='From State Berth')
    grt = fields.Char(string='Grt')
    rotation_num = fields.Integer()
    movement_num = fields.Integer(store=True)
    movement_number = fields.Char(string="Movement Number", default=lambda self: self._default_movement_number())
    dwt = fields.Char(string='DWT')
    imo = fields.Char(string="IMO")
    vessel_type = fields.Char(string='Vessel Type')
    vessel_readiness_to_sail_time = fields.Selection([
     ('1', 'Ready'),
     ('2', 'Not Ready'),
    ], string='Vessel Readiness To Sail Time', default='1')


    flag = fields.Char(string='FLAG')
    nrt = fields.Char(string='NRT')
    vessel_agent = fields.Many2one('res.partner', string='Vessels Agent')
    loa = fields.Char(string='Length Overall')
    last_port = fields.Char(string='Last Port')
    next_port = fields.Char(string='Next Port')
    d_fwd = fields.Float(string='D-FWD')
    d_aft = fields.Float(string='D-AFT')
    date = fields.Date(string='Date')
    etd = fields.Char(string='Etd')#
    call_sign = fields.Char()
    year_of_build = fields.Integer(thousands_sep='')
    #
    from_state = fields.Selection([('expected', 'Expected'), ('waiting', 'Waiting'),
                                   ('anchor', 'Anchor'), ('alongside', 'Alongside'),
                                   ('sailing', 'Sailing'), ], compute='_calc_state')
    to_state = fields.Selection([('waiting', 'Waiting'),
                                 ('anchor', 'Anchor'), ('alongside', 'Alongside'),
                                 ('sailing', 'Sailing'), ], )
    to_state_berth = fields.Many2one('ship.berth.line', string='To State Berth')
    pco = fields.Many2one('hr.employee', string='PCO')
    proceed_from_outer_to_inner = fields.Datetime(string='Proceed From Outer to Inner')
    tower_request_time = fields.Datetime(string='Tower Request Time', widget='calendar')
    tower_request_to_be_pob = fields.Datetime(string='Tower Request to be POB', widget='calendar')
    inner_arrival = fields.Datetime(string='Inner Arrival', widget='calendar')
    duration = fields.Float()

    tug_boat = fields.Many2many('ship.info', 'tug')
    tb_leave_sh = fields.Datetime(string='Leave-SH')
    tb_back_sh = fields.Datetime(string='Back-SH')

    midfast_time = fields.Datetime(string='Midfast')
    clear_time = fields.Datetime(string='Clear')

    pilot_boat = fields.Many2many('ship.info', 'pilot')
    pb_leave_sh = fields.Datetime(string='Leave-SH-A')
    pb_back_sh = fields.Datetime(string='Back-SH-A')
    pb_leave_sh_b = fields.Datetime(string='Leave-SH-B')
    pb_back_sh_b = fields.Datetime(string='Back-SH-B')

    mooring_boat = fields.Many2many('ship.info', 'mooring')
    mb_leave_sh = fields.Datetime(string='Leave-SH')
    mb_back_sh = fields.Datetime(string='Back-SH')
    ###
    expected_arrival = fields.Datetime()
    actual_arrival = fields.Boolean()
    actual_arrival_time = fields.Datetime()
    actual_response_time_achieved_per_operation = fields.Datetime()
    actual_berthing_time_achieved_per_operation = fields.Datetime()
    actual_unberthing_time_achieved_per_operation = fields.Datetime()
    expected_departure_time = fields.Datetime()
    actual_leave = fields.Datetime()
    guide = fields.Char()#
    rise_time = fields.Char()#
    fall_time = fields.Char()#
    ###

    cargo_start_operation = fields.Datetime(string="CARGO START OPERATION")
    cargo_finish_operation = fields.Datetime(string="CARGO FINISH OPERATION")
    cargo_type = fields.Char(string="CARGO TYPE")
    quantity = fields.Float(string="QUANTITY")

    ###
    movement_type = fields.Selection([('berthing', 'Berthing'), ('shifting', 'Shifting'),
                                      ('re_position', 'Re-Position'), ('pilot_disembark', 'Pilot Disembark'),
                                      ('sailing', 'Sailing'), ], )
    pilot_id = fields.Many2one('hr.employee')

    pilot_leave_sh = fields.Datetime(string="LEAVE S/H")
    pilot_arrival = fields.Datetime(string="Pilot Arrival")
    on_board = fields.Datetime(string="ONBOARD (POB)")
    first_line = fields.Datetime(string="First Line (F/L)")
    last_rope_tied_time = fields.Datetime(string="Last Rope Tied Time")
    fru = fields.Integer(string="FRU")
    all_clear = fields.Datetime(string="ALL CLEAR (A/C)")
    pilot_away = fields.Datetime(string="DIS")
    pilot_back_sh = fields.Datetime(string="BACK TO (S/H)")

    gt_ = fields.Char(string='GT')
    max_draft = fields.Char(string='Max Draft')
    first_call = fields.Datetime(string='First Call')
    last_call = fields.Datetime(string='Last Call')


    shipment_history_ids = fields.One2many('ship.operation.history', 'shipment_id')

    basic_services = fields.Char(string="Basic Services")
    add_services = fields.Char(string="Addetional Services")
    basic_traffic_charged = fields.Float(string="Basic Traffic Charged")
    add_traffic_charged = fields.Float(string="Addetional Traffic Charged")

    shipment_id_here = fields.Many2one('ship.operation')
    shipment_ids = fields.One2many('ship.operation', 'shipment_id_here')

    @api.depends('state')
    def _calc_state(self):
        for rec in self:
            rec.from_state = rec.state

    @api.onchange('actual_arrival')
    def change_state(self):
        if self.actual_arrival:
            self.state = 'waiting'
            self.actual_arrival_time = datetime.now()
        else:
            self.state = 'expected'

    @api.onchange('name')
    def imo_onchange(self):
        if self.name:
            self.imo = self.name.imo
            self.grt = self.name.grt
            self.loa = self.name.loa
            self.vessel_type = self.name.vessel_type
            self.flag = self.name.flag
            self.nrt = self.name.nrt
            self.dwt = self.name.dwt
            self.call_sign = self.name.call_sign
            self.year_of_build = self.name.year_of_build

    @api.onchange('movement_type')
    def movement_type_onchange(self):
        if self.movement_type == 'sailing':
            self.to_state = 'sailing'
        else:
            self.to_state = False

    def action_apply_movement(self):
        if self.tug_boat:
            for tug in self.tug_boat:
                move_time = self.env['ship.move.time'].search([
                    ('ship_info_id', '=', tug.id),
                    ('shipment_id', '=', self.id),
                ], limit=1)
                if move_time:
                    move_time.write({'time': self.tower_request_to_be_pob, 'duration': self.duration})
                else:
                    # Create a new ship.move.time record with the time and duration values
                    ship_time = self.env['ship.move.time']
                    ship_time.create({
                        'ship_info_id': tug.id,
                        'shipment_id': self.id,
                        'time': self.tower_request_to_be_pob,
                        'duration': self.duration,
                    })

        if self.pilot_boat:
            for pilot in self.pilot_boat:
                move_time = self.env['ship.move.time'].search([
                    ('ship_info_id', '=', pilot.id),
                    ('shipment_id', '=', self.id),
                ], limit=1)
                if move_time:
                    move_time.write({'time': self.tower_request_to_be_pob, 'duration': self.duration})
                else:
                    # Create a new ship.move.time record with the time and duration values
                    self.env['ship.move.time'].create({
                        'ship_info_id': pilot.id,
                        'shipment_id': self.id,
                        'time': self.tower_request_to_be_pob,
                        'duration': self.duration,
                    })

        if self.mooring_boat:
            for marin in self.mooring_boat:
                move_time = self.env['ship.move.time'].search([
                    ('ship_info_id', '=', marin.id),
                    ('shipment_id', '=', self.id),
                ], limit=1)
                if move_time:
                    move_time.write({'time': self.tower_request_to_be_pob, 'duration': self.duration})
                else:
                    # Create a new ship.move.time record with the time and duration values
                    self.env['ship.move.time'].create({
                        'ship_info_id': marin.id,
                        'shipment_id': self.id,
                        'time': self.tower_request_to_be_pob,
                        'duration': self.duration,
                    })

    def action_end_movement(self):
        if self.name:
            existing_record = self.shipment_history_ids.filtered(
                lambda r: r.movement_number == self.movement_number)
            vals = {
                "name": self.name.id,
                "from_state_berth": self.from_state_berth.id,
                "grt": self.grt,
                "rotation_num": self.rotation_num,
                "movement_num": self.movement_num,
                "movement_number": self.movement_number,
                "dwt": self.dwt,
                "imo": self.imo,
                "vessel_type": self.vessel_type,
                "flag": self.flag,
                "nrt": self.nrt,
                "vessel_agent": self.vessel_agent.id,
                "vessel_readiness_to_sail_time": self.vessel_readiness_to_sail_time,
                # "max_draft": self.max_draft,
                "loa": self.loa,
                "last_port": self.last_port,
                "next_port": self.next_port,
                "d_fwd": self.d_fwd,
                "d_aft": self.d_aft,
                "date": self.date,
                "etd": self.etd,
                "call_sign": self.call_sign,
                "year_of_build": self.year_of_build,
                "from_state": self.from_state,
                "to_state": self.to_state,
                "to_state_berth": self.to_state_berth.id,
                "pco": self.pco.id,
                "proceed_from_outer_to_inner": self.proceed_from_outer_to_inner,
                "tower_request_time": self.tower_request_time,
                "tower_request_to_be_pob": self.tower_request_to_be_pob,
                "inner_arrival": self.inner_arrival,
                "duration": self.duration,
                "tug_boat_ids": self.tug_boat.ids,
                "tb_leave_sh": self.tb_leave_sh,
                "tb_back_sh": self.pilot_back_sh,
                "midfast_time": self.midfast_time,
                "clear_time": self.clear_time,
                "pilot_boat_ids": self.pilot_boat.ids,
                "pb_leave_sh": self.pb_leave_sh,
                "pb_back_sh": self.pb_back_sh,
                "pb_leave_sh_b": self.pb_leave_sh_b,
                "pb_back_sh_b": self.pb_back_sh_b,
                "mooring_boat_ids": self.mooring_boat.ids,
                "mb_leave_sh": self.mb_leave_sh,
                "mb_back_sh": self.mb_back_sh,
                "expected_arrival": self.expected_arrival,
                "actual_arrival": self.actual_arrival,
                "actual_arrival_time": self.actual_arrival_time,
                "expected_departure_time": self.expected_departure_time,
                "actual_response_time_achieved_per_operation": self.actual_response_time_achieved_per_operation,
                "actual_leave": self.actual_leave,
                "guide": self.guide,
                "rise_time": self.rise_time,
                "fall_time": self.fall_time,
                "cargo_start_operation": self.cargo_start_operation,
                "cargo_finish_operation": self.cargo_finish_operation,
                "cargo_type": self.cargo_type,
                "quantity": self.quantity,
                "movement_type": self.movement_type,
                "pilot_id": self.pilot_id.id,
                "pilot_leave_sh": self.pilot_leave_sh,
                "pilot_arrival": self.pilot_arrival,
                "on_board": self.on_board,
                "first_line": self.first_line,
                "last_rope_tied_time": self.last_rope_tied_time,
                "all_clear": self.all_clear,
                "pilot_away": self.pilot_away,
                "pilot_back_sh": self.pilot_back_sh,
                "shipment_id": self.id,
            }

            if existing_record:
                existing_record.write(vals)
            else:
                self.env['ship.operation.history'].create(vals)
            if self.to_state:
                self.state = self.to_state
            else:
                self.state = self.state

    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        last_record = self.search([], order='id desc', limit=1)

        if last_record:

            rotation_num = last_record.rotation_num + 1
        else:

            rotation_num = self.search_count([]) + 1

        res['rotation_num'] = rotation_num
        return res

    def _default_movement_number(self):
        last_record = self.search([], order='id desc', limit=1)

        if last_record:
            rotation_num = last_record.rotation_num + 1
        else:
            rotation_num = self.search_count([]) + 1

        movement_num = len(self.shipment_history_ids) + 1
        movement_number = f"{rotation_num} - {movement_num}"
        return movement_number

    def new_round(self):
        if self.name:
            self.clear_custom_fields()

        if self.shipment_history_ids:
            last_record = self.shipment_history_ids[-1]
            self.from_state_berth = last_record.to_state_berth

        for record in self:
            record.movement_num = len(record.shipment_history_ids) + 1
            record.movement_number = f"{record.rotation_num} - {record.movement_num}"

    fields_to_exclude = ['shipment_history_ids', 'id', 'name', 'imo', 'from_state_berth', 'grt', 'vessel_agent',
                         'cargotype', 'expected_arrival', 'actual_arrival', 'actual_arrival_time', 'dwt', 'nrt',
                         'expected_departure_time', 'actual_response_time_achieved_per_operation','vessel_readiness_to_sail_time', 'actual_leave', 'flag', 'vessel_type', 'loa', 'rotation_num',
                         'state', 'from_state', 'movement_num', 'movement_number',
                         'next_port', 'last_port', 'd.fwd', 'd.aft', 'cargo_start_operation',
                         'cargo_finish_operation', 'cargo_type', 'quantity', 'call_sign', 'year_of_build']

    def clear_custom_fields(self):
        customized_fields = self.env['ir.model.fields'].search(
            [('model', '=', 'ship.operation'),
             ('ttype', '!=', False),
             ('name', 'not in', self.fields_to_exclude)
             ])

        for field in customized_fields:
            field_name = field.name
            field_value = self[field_name]
            print(f"{field_name}: {field_value}")
        self.write({field_name: False for field_name in customized_fields.mapped('name')})

    @api.onchange('state', 'from_state')
    def onchange_from_state(self):
        berth_id = self.env['ship.berth'].search([('name', '=', self.from_state)])
        if self.from_state:
            return {'domain': {'berth': [('id', 'in', berth_id.berth_line_ids.ids)]}}
        else:
            return {'domain': {'berth': [('id', 'in', False)]}}

    @api.onchange('to_state')
    def onchange_to_state(self):
        berth_id = self.env['ship.berth'].search([('name', '=', self.to_state)])
        if self.from_state:
            return {'domain': {'to_state_berth': [('id', 'in', berth_id.berth_line_ids.ids)]}}
        else:
            return {'domain': {'to_state_berth': [('id', 'in', False)]}}
