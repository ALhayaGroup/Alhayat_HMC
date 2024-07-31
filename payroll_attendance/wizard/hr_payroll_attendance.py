# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

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
        print("-------------------------------" )
        date_time = datetime.combine(self.date_from,datetime.min.time())
        att_payroll = self.env['payroll.attendance.line']

        hr_attendance_ids = self.env['hr.attendance'].search([('payroll_attendance_id', '=', False), ('check_in', '>=', date_time)])
        while date_time <= datetime.today():
            print("-=-=-=-=-=-=======GOOOOOOOOOOODDD==============")
            # vals = self.prepare_payroll_attendance(rec)
            date_time= date_time + timedelta(days=1)
        print("=====hr_attendance_ids=====", hr_attendance_ids)
        # for rec in hr_attendance_ids:
        #     print("=======================")
        #     vals = self.prepare_payroll_attendance(rec)
        #     print("vals=============", vals)


    def prepare_payroll_attendance(self,rec):
        self.get_status(rec)
        vals = {
                'employee_id': rec.employee_id.id,
                'shift_id': rec.employee_id.shift_id.id,
                'day': rec.check_in.strftime('%A'),
                'date': rec.check_in.date(),
                # 'time_in': rec.check_in.time(),
                # 'time_out': rec.check_out.time(),
                # 'attendance_line_ids': rec.id,
                # 'status':
                 }
        return vals


    def get_status(self,rec):
        print("-=-=-=-=-=-=-=-=-=--=-=-=-=-=-")



       
