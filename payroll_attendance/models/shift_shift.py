# -*- coding:utf-8 -*-

from odoo import api, fields, models, _


class ShiftShif(models.Model):
    _name = 'shift.shift'
    _description = 'Employee shift'

    shift_name = fields.Char(string="Shift Name")
    name = fields.Char(string='Policy Code', required=True, readonly=True, default=lambda self: 'New')
    shift_start = fields.Float(string="Shift Start Time")
    shift_end = fields.Float(string="Shift End Time")
    shift_work_time = fields.Float(string="Work time")
    late_in = fields.Float(string="Grace start period")
    early_out = fields.Float(string="Grace end period")
    Over_time_start = fields.Float(string="Over time start")
    sat = fields.Boolean(string="Saturday")
    sun = fields.Boolean(string="Sunday")
    mon = fields.Boolean(string="Monday")
    tue = fields.Boolean(string="Tuesday")
    wed = fields.Boolean(string="Wednesday")
    thur = fields.Boolean(string="Thursday")
    fri = fields.Boolean(string="Friday")


    @api.model_create_multi
    def create(self, vals):
        if not vals[0].get('name') or vals['name'] ==  'New':
            vals[0]['name'] = self.env['ir.sequence'].next_by_code('hr.shift.seq') or 'New'
        return super(ShiftShif, self).create(vals)




    @api.onchange('shift_start','shift_end')
    def get_working_time(self):
        for record in self:
            record.shift_work_time = record.shift_end - record.shift_start


    # holidays = self.env['hr.leave'].sudo().search([
    #     ('employee_id', '!=', False),
    #     ('state', '=', 'validate'),
    #     ('date_from', '<=', today_end),
    #     ('date_to', '>=', today_start),
    # ])



