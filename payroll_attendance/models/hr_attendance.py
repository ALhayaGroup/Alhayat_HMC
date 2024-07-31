# -*- coding:utf-8 -*-

from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    _description = 'Attendance'


    payroll_attendance_id = fields.Many2one("payroll.attendance.line", string="Payroll attendance")
    