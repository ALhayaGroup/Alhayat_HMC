from odoo import fields, models,api
import requests
from datetime import datetime


class Attendance_get_data(models.Model):
    _name = "attendance.get.data"
    _description = "Get Attendance Data"


    Attendance_id=fields.Integer(string="id" , required=True)
    emp_code = fields.Integer(string="code_attendance")
    punch_time = fields.Datetime(string="time")
    punch_state_display=fields.Char(string="status")
    upload_time = fields.Date(string="upload time")


    _sql_constraints = [
        ('unique_Attendance_id', 'unique(Attendance_id)', 'ID Attendance must be unique!'),
    ]
    
    def get_attendance_data(self,date_from,date_to):
        url = f"http://10.1.1.150:8082/iclock/api/transactions/?start_time={date_from}&end_time={date_to}&page_size=49000"
        headers = {
            'Authorization': 'Token f32eafa83433b8e0769025b4d879f074b943fe65',
            
        }
        payload = ""

        response = requests.request("GET", url, headers=headers, data=payload)

        get_response = response.json()
        get_data = get_response['data']

        for item in get_data:
            date_format = "%Y-%m-%d %H:%M:%S"
            date_object = datetime.strptime(item.get('upload_time'), date_format)
            if self.env['attendance.get.data'].search([('upload_time','=',date_object.date()),('emp_code','=',int(item.get('emp_code')))]):
                continue
            else:
                self.create({'Attendance_id':item.get('id'),
                         'emp_code':item.get('emp_code'),
                         'punch_time':item.get('punch_time'),
                         'punch_state_display':item.get('punch_state_display'),
                         'upload_time':item.get('upload_time')})
   



































