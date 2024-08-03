from odoo import fields, api, models, exceptions, _
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError 
from odoo.exceptions import UserError
from odoo.tools import format_datetime
from datetime import datetime , timedelta
from dateutil.relativedelta import relativedelta
import logging
import pytz


import requests
_logger = logging.getLogger(__name__)

class Hr_Zk(models.Model):
    _inherit = "hr.attendance"
    code_employee = fields.Char(string="Code")
    state = fields.Selection([('auto', 'Auto'), ('manual', 'Manual'),],default='manual')
    

    _sql_constraints = [
        ('unique_employee_checkin_checkout', 'unique(code_employee, check_in, check_out)',
         'Employee code, check-in, and check-out times must be unique!')
    ]

    

    # _sql_constraints = [
    #     ('unique_id_api', 'unique(id_api)', 'ID API must be unique!'),
    # ]
    # @api.depends('check_in','check_out')
    # def _compute_over_time(self):
    #    # employee = self.env['hr.employee'].search([('code_employee','=',self.code_employee)])
    # #    work_hours_day = employee.contract_id.x_working_hours
    # #    print(work_hours_day)
    #    for attendance in self:
    #         employee = self.env['hr.employee'].search([('code_employee','=',attendance.code_employee)])
    # #        work_hours_day = employee.contract_id.x_working_hours
    #         # attendance.ensure_one()
    #         if attendance.check_out and attendance.check_in:
    #             delta = attendance.check_out - attendance.check_in
    #             worked_hours = delta.total_seconds() / 3600.0
    #      #       if employee.contract_id.x_working_hours!= 0:
    #             #  if worked_hours > work_hours_day :
                    
    #             #     attendance.over_time = worked_hours-work_hours_day
    #                 # over = 
    #         #      else:
    #         #        attendance.over_time = 0.0
    #         #    else:
    #         #        attendance.over_time = 0.0
    #         # else:

    #         #    attendance.over_time = False 

    def get_attendance_data(self, date_from, date_to):
        # print(date_from)
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
                # Parsing dates and times
                date_format = "%Y-%m-%d %H:%M:%S"
                check_in_date_str = f"{item['att_date']} {item['check_in']}" 
                check_out_date_str = f"{item['att_date']} {item['check_out']}" if item['check_out'] else None
                punch_data = datetime.strptime(check_in_date_str, date_format)
                date_object = datetime.strptime(check_out_date_str, date_format) if check_out_date_str else None

                punch_data_local = local_tz.localize(datetime.strptime(check_in_date_str, date_format))
                print(punch_data_local)
                punch_data_utc = punch_data_local.astimezone(pytz.utc)
                punch_data_str = punch_data_utc.strftime(date_format)
                # date_object_utc = None
                
                date_object_local = local_tz.localize(datetime.strptime(check_out_date_str, date_format))
                date_object_utc = date_object_local.astimezone(pytz.utc)
                date_object_str = date_object_utc.strftime(date_format)


                if not punch_data or not date_object:
                    _logger.error(f"Missing check_in or check_out time for item: {item}")
                    continue

                # punch_time = datetime.strptime(check_in_time, date_format)
                # upload_time = datetime.strptime(check_out_time, date_format)

                # Using savepoint for transaction management
                employees = self.env['hr.employee'].search([('code_employee', '=', item.get('emp_code'))])
                if employees:
                    with self.env.cr.savepoint():
                      self.create({
                        'employee_id': employees.id,
                       
                        'code_employee': item.get('emp_code'),
                        # 'date_day': item
                        'check_in': punch_data_str,
                        'check_out': date_object_str ,
                        'state': 'auto'
                       })
            except Exception as e:
                _logger.error(f"Error processing item: {item} with error: {e}")








    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for attendance in self:
            # attendance.ensure_one()
            if attendance.check_out and attendance.check_in:
                delta = attendance.check_out - attendance.check_in
                attendance.worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.worked_hours = False

    @api.constrains('check_in', 'check_out')
    def _check_validity_check_in_check_out(self):
        """ verifies if check_in is earlier than check_out. """
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                if attendance.check_out < attendance.check_in:
                    raise exceptions.ValidationError(_('"Check Out" time cannot be earlier than "Check In" time.'))

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" attendance record (without check_out)
                * no overlapping time slices with previous employee records
        """
        for attendance in self:
            last_attendance_before_check_in = self.env['hr.attendance'].search([
                ('employee_id', '=', attendance.employee_id.id),
                ('check_in', '<=', attendance.check_in),
                ('id', '!=', attendance.id),
            ], order='check_in desc', limit=1)
