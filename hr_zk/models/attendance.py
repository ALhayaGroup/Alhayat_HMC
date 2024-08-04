from odoo import fields, models,api
import requests
from datetime import datetime


class Attendance_get_data(models.Model):
    _name = "attendance.get.data"
    _description = "Get Attendance Data"


    Attendance_id=fields.Integer(string="id" , required=True)
    emp_code = fields.Integer(string="Attendance Code")
    punch_time = fields.Datetime(string="time")
    punch_state_display=fields.Char(string="status")
    upload_time = fields.Date(string="upload time")

    check_in = fields.Float(string="Check in")
    check_out = fields.Float(string="Check out")
    total_time = fields.Float(string="Total time")
    att_date = fields.Date(string="Attend time")


    _sql_constraints = [
        ('unique_Attendance_id', 'unique(Attendance_id)', 'ID Attendance must be unique!'),
    ]
    
    def get_attendance_data(self,date_from,date_to):
        # url = f"http://10.1.1.150:8082/iclock/api/transactions/?start_time={date_from}&end_time={date_to}&page_size=49000"
        url = f"http://142.132.129.24:8080/att/api/firstInLastOutReport/?page=1&page_size=20000&start_date={date_from}&end_date={date_to}&departments=1,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44&areas=-1&groups=-1&employees=-1"
        headers = {
            'Authorization': 'Token f32eafa83433b8e0769025b4d879f074b943fe65',
            
        }
        payload = ""

        response = requests.request("GET", url, headers=headers, data=payload)

        get_response = response.json()
        get_data = get_response['data']

        for item in get_data:
            date_format = "%Y-%m-%d %H:%M:%S"
            date_object = datetime.strptime(item.get('att_date'), date_format)
            if self.env['attendance.get.data'].search([('att_date','=',date_object.date()),('emp_code','=',int(item.get('emp_code')))]):
                continue
            else:
                self.create({'Attendance_id':item.get('id'),
                         'emp_code':item.get('emp_code'),
                         'att_date':item.get('att_date'),
                         'check_in':item.get('check_in'),
                         'check_out':item.get('check_out'),
                         'total_time':item.get('total_time')})
                         # 'punch_time':item.get('punch_time'),
                         # 'punch_state_display':item.get('punch_state_display'),
                         # 'upload_time':item.get('upload_time')})
   



































