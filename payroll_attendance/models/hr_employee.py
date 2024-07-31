# -*- coding:utf-8 -*-

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee Payroll Attendane'

    shift_id = fields.Many2one('shift.shift', string="Shift Name")
    