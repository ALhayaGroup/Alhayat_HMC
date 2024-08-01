import requests
from datetime import datetime
from odoo import fields, models ,api


class Attendance_get_data(models.TransientModel):
    _name = "get.payslip"
    date_from = fields.Date("date from",required=True)
    date_to = fields.Date("date to",required=True)


    def get_data(self ):

        employee=self.env['hr.employee'].search([])
        for emp in employee:
            self.env['hr.payslip'].create({
                'employee_id': emp.id,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'contract_id': emp.contract_id.id,
                'struct_id': emp.contract_id.struct_id.id,
                'journal_id':4,


            })
        pay =  self.env['hr.payslip'].sudo().search([('date_from','>=',self.date_from),('date_to','<=',self.date_to)])
        for payslip in pay:
                payslip.attendance()
                payslip.compute_sheet()
            
