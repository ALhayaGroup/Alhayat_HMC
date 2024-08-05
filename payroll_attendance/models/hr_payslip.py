# -*- coding:utf-8 -*-

import babel
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from pytz import timezone
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'


    def compute_employee_attendance(self):
        att_lines = self.env['payroll.attendance.line'].search([('employee_id','=', self.employee_id.id),
                                                                ('date', '>=', self.date_from),
                                                                ('date', '<=', self.date_to)])

        line_dict = {'absent':0, '1_late':0, '2_late':0}
        for line in att_lines:
            for key in line_dict.keys():
                if line.status == key:
                    line_dict[key] = line_dict.get(line.status) + 1
        for input_id in self.input_line_ids:
            if line_dict.get('1_late') > 0:
                if input_id.code == 'LATE_1':
                    input_id.update({'amount':line_dict.get('1_late')})
                policy_line_1_late = self.env['hr.policy.line'].search([('policy_id.attendance_status','=', '1_late'),('no', '=', str(line_dict.get('1_late')))])
                act_1_late_amount = policy_line_1_late.actual_policy
                if input_id.code == 'PEN_LATE_1':
                    input_id.update({'amount':act_1_late_amount})

            if line_dict.get('2_late') > 0:
                if input_id.code == 'LATE_2':
                    input_id.update({'amount':line_dict.get('2_late')})
                policy_line_2_late = self.env['hr.policy.line'].search([('policy_id.attendance_status','=', '2_late'),('no', '=', str(line_dict.get('2_late')))])
                act_2_late_amount = policy_line_2_late.actual_policy
                print("============act_2_late_amount==============", act_2_late_amount)
                if input_id.code == 'PEN_LATE_2':
                    input_id.update({'amount':act_2_late_amount})

            if line_dict.get('absent') > 0:
                if input_id.code == 'ABS_INPUT':
                    input_id.update({'amount':line_dict.get('absent')})
                policy_line_absent = self.env['hr.policy.line'].search([('policy_id.attendance_status','=', 'absent'),('no', '=', str(line_dict.get('absent')))])
                absent_amount = policy_line_absent.actual_policy
                if input_id.code == 'PEN_ABS':
                    input_id.update({'amount':absent_amount})
            

    
