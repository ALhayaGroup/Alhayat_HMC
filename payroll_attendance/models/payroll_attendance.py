# -*- coding:utf-8 -*-

from odoo import api, fields, models


class PayrollAttendanceLine(models.Model):
    _name = 'payroll.attendance.line'
    _description = 'Hr Payroll Attendance Line'

    WEEK_DAYS = [('sat', 'Saturday'), ('sun', 'Sunday'),
                 ('mon', 'Monday'), ('tue', 'Tuesday'),
                 ('wed', 'Wednesday'), ('thur', 'Thursday'), ('fri', 'Friday')]

    ATTENDANCE_STATUS = [('1_late', "Late 0:16 to 0:30"), 
                         ('2_late', "Late 0:31 to 1:00"),
                         ('3_late', "Late more than 1H"),
                         ('1_early', "Early out 0:15 to 0:30"),
                         ('absent', "Absent"),
                         ('leave', "Leave")]

    employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    shift_id = fields.Many2one("shift.shift", string="Shift")
    day = fields.Selection(WEEK_DAYS, string="Days")
    time_in = fields.Float(string="Time In")
    time_out = fields.Float(string="Time Out")
    work_time = fields.Float(string="Work time")
    status = fields.Selection(ATTENDANCE_STATUS,string="Status")
    leave_id = fields.Many2one("hr.leave", string="Leave")
    attendance_line_ids = fields.One2many("hr.attendance", "payroll_attendance_id", string="Attendance lines")



    def create_payroll_attendance_line(self):
        print("============create_payroll_attendance_line==============")
