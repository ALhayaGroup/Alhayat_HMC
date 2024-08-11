# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from odoo import models, fields, api, _


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'


    x_day_vacation=fields.Float(string='ايام الغياب')
    x_day_attendance=fields.Float(string='ايام الحضور ')
    x_over_time=fields.Float(string="اجمالى ساعات عمل اضافية")

    x_working_hours=fields.Float(string="عدد ساعات العمل")

    def statment(self):
        self.write({'x_settlement_allowance':0,'x_day_vacation':0,'x_rival':0})

    def attendance_write(self):
        print("55" * 30)
        attend = self.env['hr.payslip'].search([('contract_id', '=', 3)])
        print(attend.contract_id.name)

        for contract in self:
            attend = self.env['hr.payslip'].search([('contract_id', '=', 3)])

            print(contract)
            total = 0

            for rec in attend.worked_days_line_ids:
                total += rec.number_of_days
            contract.write({'x_day_attendance': total})

        return print('@' * 20)

