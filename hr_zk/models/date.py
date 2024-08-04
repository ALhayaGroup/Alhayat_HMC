from odoo import fields, models,api
import requests

class Attendance_get_data(models.TransientModel):
    _name = "get.data"
    date_from = fields.Date("date from",required=True)
    date_to = fields.Date("date to",required=True)

    days_in_month = fields.Integer("days_in_month",required=True,default=26)


   
    def get_all_api(self):
        self.env['attendance.get.data'].get_attendance_data(self.date_from,self.date_to)


    
    
    def get_all_attendance(self):
        self.env['hr.attendance'].create_from_api_response(self.date_from,self.date_to)
        # contract=self.env['hr.contract'].search([])
        # for rec in contract:
        #     rec.write({'x_day_attendance':self.days_in_month})
