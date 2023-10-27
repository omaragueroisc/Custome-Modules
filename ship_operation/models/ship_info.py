# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models


class ShipInfoInherit(models.Model):
    _inherit = 'ship.info'

    ship_move_time_ids = fields.One2many('ship.move.time', 'ship_info_id')
    time = fields.Datetime()


class ShipMoveTime(models.Model):
    _name = 'ship.move.time'
    _rec_name = 'time'

    ship_info_id = fields.Many2one('ship.info')
    shipment_id = fields.Many2one('ship.operation')
    time = fields.Datetime()
    duration = fields.Float()
    maintenance_request_id = fields.Many2one('shipment.maintenance')
