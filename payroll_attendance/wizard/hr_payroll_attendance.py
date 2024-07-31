# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil import relativedelta

from odoo import api, fields, models


class PayrollAttendanceWizard(models.TransientModel):
    _name = 'payroll.attendance.wiz'
    _description = 'Generate Payroll Attendance'

    date_from = fields.Date(string='Date From', required=True,
        default=datetime.now().strftime('%Y-%m-%d'))
    date_to = fields.Date(string='Date To', required=True,
        default=str(datetime.now()))



    def generate_payroll_attendance(self):
        print("----------------------------")
       
