# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil import relativedelta
import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models


class PayrollAttendanceWizard(models.TransientModel):
    _name = 'payroll.attendance.wiz'
    _description = 'Generate Payroll Attendance'

    date_from = fields.Date(string='Date From', required=True,
        default=datetime.now().strftime('%Y-%m-%d'))
    date_to = fields.Date(string='Date To', required=True,
        default=str(datetime.now()))



    def generate_payroll_attendance(self):
        date_time = datetime.combine(self.date_from,datetime.min.time())
        att_payroll = self.env['payroll.attendance.line']
        hr_attendance_ids = self.env['hr.attendance'].search([('payroll_attendance_id', '=', False), ('check_in', '>=', date_time)])
        for rec in hr_attendance_ids:
            if not rec.payroll_attendance_id:
                vals = self.prepare_payroll_attendance(rec,date_time)
                line = att_payroll.create(vals)
                self.get_status(line,date_time.strftime('%a'))
            rec.update({'payroll_attendance_id': line })
            date_time = date_time + timedelta(days=1)
            date_time = datetime.combine(self.date_from,datetime.min.time())



    def get_check_time(self,att_line):
        time_in_tz = self._get_timezone(str(att_line.check_in),3)
        time_out_tz = self._get_timezone(str(att_line.check_out),3)
        new_time_in = time_in_tz.time().strftime('%H:%M')
        new_time_out = time_out_tz.time().strftime('%H:%M')
        time_in = new_time_in.replace(':','.')
        time_out = new_time_out.replace(':','.')
        flo_time_in,flo_time_out = float(time_in),float(time_out)
        return flo_time_in, flo_time_out 


    def prepare_payroll_attendance(self,rec,date_time):
        check_in,check_out = self.get_check_time(rec)
        work_time = check_out - check_in
        vals = {
                'employee_id': rec.employee_id.id,
                'shift_id': rec.employee_id.shift_id.id,
                'day': date_time.strftime('%A'),
                'date': date_time,
                'time_in': check_in, #must be replace with time zone,
                'time_out': check_out,
                'work_time': work_time,
                'attendance_line_ids': [(6, 0, rec.ids)],
                 }
        return vals


    def get_status(self,line,day_name):
        self.get_normal_status(line)
        self.get_late_line(line)
        self.get_off_status(line,day_name)
        self.get_absent_status(line)


    def get_absent_status(self,line):
        if line.status not in ['off'] and line.time_in == 0.0 and line.time_out == 0.0:
            line.update({'status':'absent'})
      
    

    def get_off_status(self,line,day_name):       
        if line.shift_id.sat == False and day_name == 'Sat':
            line.update({'status':'off'})
        if line.shift_id.sun == False and day_name == 'Sun':
            line.update({'status':'off'})
        if line.shift_id.mon == False and day_name == 'Mon':
            line.update({'status':'off'})
        if line.shift_id.tue == False and day_name == 'Tue':
            line.update({'status':'off'})
        if line.shift_id.wed == False and day_name == 'Wed':
            line.update({'status':'off'})
        if line.shift_id.thur == False and day_name == 'Thu':
            line.update({'status':'off'})
        if line.shift_id.fri == False and day_name == 'Fri':
            line.update({'status':'off'})




    def get_late_line(self,line):
        _logger.info("============late============%s", line.time_in)
        _logger.info("============late============")
        late_time = line.shift_id.shift_start + line.shift_id.late_in
        if line.shift_id.shift_start + 0.16 < line.time_in < line.shift_id.shift_start + 0.30:
            line.update({'status':'1_late'})
        if line.shift_id.shift_start + 0.31 < line.time_in < line.shift_id.shift_start + 1.0:
            line.update({'status':'2_late'})


    def get_normal_status(self,line):
        late_time = line.shift_id.shift_start + line.shift_id.late_in
        if 0.0 < line.time_in < late_time:
            line.update({'status':'normal'})


    def _get_timezone(self, time_to_tz, tz_hr=3):
        if time_to_tz:
            new_time = datetime.strptime(time_to_tz, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=tz_hr)
            _logger.info("================%s", new_time)
            return new_time




       
