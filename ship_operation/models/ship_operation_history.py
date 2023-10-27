from odoo import models, fields, api


class ShipOperation(models.Model):
    _name = 'ship.operation.history'
    _description = 'Ship Operation History'

    shipment_id = fields.Many2one('ship.operation')

    name = fields.Many2one('res.partner', string='Vessels name')
    from_state_berth = fields.Many2one('ship.berth.line', string='From State Berth')
    grt = fields.Char(string='Grt')
    rotation_num = fields.Integer()
    movement_num = fields.Integer(store=True)
    movement_number = fields.Char(string="Movement Number")
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
    max_draft = fields.Char(string='Max Draft')
    loa = fields.Char(string='Length Overall')
    last_port = fields.Char(string='Last Port')
    next_port = fields.Char(string='Next Port')
    gt = fields.Char(string='GT')
    d_fwd = fields.Float(string='D-FWD')
    d_aft = fields.Float(string='D-AFT')
    date = fields.Date(string='Date')
    etd = fields.Char(string='Etd')
    call_sign = fields.Char()
    year_of_build = fields.Integer(thousands_sep='')
    #
    from_state = fields.Selection([('expected', 'Expected'), ('waiting', 'Waiting'),
                                   ('anchor', 'Anchor'), ('alongside', 'Alongside'),
                                   ('sailing', 'Sailing'), ])
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

    tug_boat_ids = fields.Many2many('ship.info', 'tugboat_rel', 'tugboat_history')
    tb_leave_sh = fields.Datetime(string='Leave-SH')
    tb_back_sh = fields.Datetime(string='Back-SH')
    midfast_time = fields.Datetime(string='Midfast')
    clear_time = fields.Datetime(string='Clear')

    pilot_boat_ids = fields.Many2many('ship.info', 'pilot_rel', 'pilot_history')
    pb_leave_sh = fields.Datetime(string='Leave-SH-A')
    pb_back_sh = fields.Datetime(string='Back-SH-A')
    pb_leave_sh_b = fields.Datetime(string='Leave-SH-B')
    pb_back_sh_b = fields.Datetime(string='Back-SH-B')

    mooring_boat_ids = fields.Many2many('ship.info', 'mooring_rel', 'mooring_history')
    mb_leave_sh = fields.Datetime(string='Leave-SH')
    mb_back_sh = fields.Datetime(string='Back-SH')
    ###
    first_call = fields.Datetime(string='First Call')
    expected_arrival = fields.Datetime()
    actual_arrival = fields.Boolean()
    actual_arrival_time = fields.Datetime()
    expected_departure_time = fields.Datetime()
    actual_response_time_achieved_per_operation = fields.Datetime()
    actual_leave = fields.Datetime()
    guide = fields.Char()
    rise_time = fields.Char()
    fall_time = fields.Char()
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
    all_clear = fields.Datetime(string="ALL CLEAR (A/C)")
    pilot_away = fields.Datetime(string="DIS")
    pilot_back_sh = fields.Datetime(string="BACK TO (S/H)")
