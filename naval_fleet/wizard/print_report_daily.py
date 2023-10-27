from odoo import models, fields


class PrintReportDaily(models.TransientModel):
    _name = 'print.report.daily.wizard'
    _description = "Print Report Daily"

    name = fields.Many2one('ship.info')
    from_date = fields.Date()
    to_date = fields.Date()

    def print_report(self):
        lines = []
        domain = []
        from_date = self.from_date
        if from_date:
            domain += [('date', '>=', from_date)]
        to_date = self.to_date
        if to_date:
            domain += [('date', '<=', to_date)]
        report_daily = self.env['ship.report'].search(domain)
        for rec in report_daily:
            lines += [{
                'name': rec.name,
                'date': rec.date,
                'running_hours': rec.running_hours,
                'fuel_consumption': rec.fuel_consumption,

            }]
        data = {
            'form': self.read()[0],
            'lines': lines,
        }
        return self.env.ref('naval_fleet.report_daily_view').report_action(None, data=data)
