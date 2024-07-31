# -*- coding:utf-8 -*-

from odoo import api, fields, models


class LeaveType(models.Model):
    _inherit = 'hr.leave.type'

    affect_payroll = fields.Boolean(string='Affect payroll?')

