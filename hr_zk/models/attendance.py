from odoo import fields, models ,api
import requests
import logging
from datetime import datetime
from odoo import exceptions
import pytz


_logger = logging.getLogger(__name__)

class AttendanceGetData(models.Model):
    _name = "attendance.get.data"
    _description = "Get Attendance Data"

    emp_code = fields.Integer(string="code")
    employee_id = fields.Many2one('hr.employee',string="employee id" , required=True)
    punch_time = fields.Datetime(string="check in")
    upload_time = fields.Datetime(string="check out")


    _sql_constraints = [
        ('unique_all_att_employee_checkin_checkout', 'unique(emp_code, punch_time)',
         'Employee check-in, and check-out times must be unique!')
    ]

    def get_all_attendance_data(self, date_from, date_to):
        print(date_from)
        url = (f"http://142.132.129.24:8080/att/api/firstInLastOutReport/?page=1&page_size=80000&start_date={date_from}&end_date={date_to}&departments=1,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44&areas=-1&groups=-1&employees=-1")
        # url = (f"http://142.132.129.24:8080/att/api/firstInLastOutReport/?page_size=500000&start_date={date_from}&end_date={date_to}&departments=1%2C29%2C30%2C31%2C32%2C33%2C34%2C35%2C36%2C37%2C38%2C39%2C40%2C41%2C42%2C43%2C44&areas=-1&groups=-1&employees=-1")
        headers = {
            'Authorization': 'Token f32eafa83433b8e0769025b4d879f074b943fe65',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            get_response = response.json()  # Attempt to decode JSON
        except requests.exceptions.HTTPError as http_err:
            _logger.error(f"HTTP error occurred: {http_err}")
            return
        except requests.exceptions.RequestException as req_err:
            _logger.error(f"Request error occurred: {req_err}")
            return
        except ValueError as json_err:
            _logger.error(f"JSON decode error: {json_err}")
            return

        get_data = get_response.get('data', [])
        _logger.info(f"Fetched data: {get_data}")
        local_tz = pytz.timezone('Africa/Cairo')
        for item in get_data:
            try:
              
              if item['check_in'] and item['check_out']:
                # Parsing dates and times
                date_format = "%Y-%m-%d %H:%M:%S"
                check_in_date_str = f"{item['att_date']} {item['check_in']}"
                check_out_date_str = f"{item['att_date']} {item['check_out']}"
                # punch_data = datetime.strptime(check_in_date_str, date_format)
                # date_object = datetime.strptime(check_out_date_str, date_format)
                

                punch_data_local = local_tz.localize(datetime.strptime(check_in_date_str, date_format))
                punch_data_utc = punch_data_local.astimezone(pytz.utc)
                punch_data_str = punch_data_utc.strftime(date_format)

                date_object_local = local_tz.localize(datetime.strptime(check_out_date_str, date_format))
                date_object_utc = date_object_local.astimezone(pytz.utc)
                date_object_str = date_object_utc.strftime(date_format)

                # if not date_object:
                #     employees = self.env['hr.employee'].search([('code_employee', '=', item.get('emp_code'))])
                #     with self.env.cr.savepoint():
                #      self.create({
                #         'employee_id': employees.id,
                #         'emp_code': item.get('emp_code'),
                #         'punch_time': punch_data,
                #         # 'upload_time': date_object,
                #     })

                # punch_time = datetime.strptime(check_in_time, date_format)
                # upload_time = datetime.strptime(check_out_time, date_format)

                # Using savepoint for transaction management
                employees = self.env['hr.employee'].search([('pin', '=', item.get('emp_code'))])
                if employees:
                   with self.env.cr.savepoint():
                     self.create({
                        'employee_id': employees.id,
                        'emp_code': item.get('emp_code'),
                        'punch_time': punch_data_str,
                        'upload_time': date_object_str,
                      })
              if not item['check_out']:
                   # Parsing dates and times
                date_format = "%Y-%m-%d %H:%M:%S"
                check_in_date_str = f"{item['att_date']} {item['check_in']}"
                # check_out_date_str = f"{item['att_date']} {item['check_out']}"
                punch_data_local = local_tz.localize(datetime.strptime(check_in_date_str, date_format))
                punch_data_utc = punch_data_local.astimezone(pytz.utc)
                punch_data_str = punch_data_utc.strftime(date_format)
                # date_object = datetime.strptime(check_out_date_str, date_format)


                # if not date_object:
                #     employees = self.env['hr.employee'].search([('code_employee', '=', item.get('emp_code'))])
                #     with self.env.cr.savepoint():
                #      self.create({
                #         'employee_id': employees.id,
                #         'emp_code': item.get('emp_code'),
                #         'punch_time': punch_data,
                #         # 'upload_time': date_object,
                #     })

                # punch_time = datetime.strptime(check_in_time, date_format)
                # upload_time = datetime.strptime(check_out_time, date_format)

                # Using savepoint for transaction management
                employees = self.env['hr.employee'].search([('pin', '=', item.get('emp_code'))])
                if employees:
                   with self.env.cr.savepoint():
                     self.create({
                        'employee_id': employees.id,
                        'emp_code': item.get('emp_code'),
                        'punch_time': punch_data_str,
                        # 'upload_time': date_object,
                     })
                  
            except Exception as e:  
                _logger.error(f"Error processing item: {item} with error: {e}")

    


    @api.depends('punch_time', 'upload_time')
    def _compute_worked_hours(self):
        for attendance in self:
            # attendance.ensure_one()
            if attendance.upload_time and attendance.punch_time:
                delta = attendance.upload_time - attendance.punch_time
                attendance.worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.worked_hours = False

    @api.constrains('punch_time', 'upload_time')
    def _check_validity_punch_time_upload_time(self):
        """ verifies if punch_time is earlier than upload_time. """
        for attendance in self:
            if attendance.punch_time and attendance.upload_time:
                if attendance.upload_time < attendance.punch_time:
                    raise exceptions.ValidationError(_('"Check Out" time cannot be earlier than "Check In" time.'))

    @api.constrains('punch_time', 'upload_time', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" attendance record (without upload_time)
                * no overlapping time slices with previous employee records
        """
        for attendance in self:
            last_attendance_before_punch_time = self.env['attendance.get.data'].search([
                ('employee_id', '=', attendance.employee_id.id),
                ('punch_time', '<=', attendance.punch_time),
                # ('id', '!=', attendance.id),
            ], order='punch_time desc', limit=1)

