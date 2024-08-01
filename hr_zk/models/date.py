from odoo import fields, models,api
import requests
from datetime import datetime

class Attendance_get_data(models.TransientModel):
    _name = "get.data"
    date_from = fields.Date("date from",required=True)
    date_to = fields.Date("date to",required=True)

    days_in_month = fields.Integer("days_in_month",required=True,default=26)


   
    def get_all_api(self):
        data_format= "%Y-%m-%d"
        date_from_send = self.date_from.strftime(data_format)
        date_to_send = self.date_to.strftime(data_format)
        self.env['hr.attendance'].get_attendance_data(str(date_from_send),str(date_to_send))


    def get_all_att(self):
        data_format= "%Y-%m-%d"
        date_from_send = self.date_from.strftime(data_format)
        date_to_send = self.date_to.strftime(data_format)
        self.env['attendance.get.data'].get_all_attendance_data(str(date_from_send),str(date_to_send))
    
