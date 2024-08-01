from odoo import fields, api, models, exceptions, _
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError 
from odoo.exceptions import UserError
from odoo.tools import format_datetime
from datetime import datetime , timedelta
import requests

class Hr_Zk(models.Model):
    _inherit = "hr.attendance"

    id_api = fields.Integer()
    code_employee = fields.Char(string="Code")
    # over_time= fields.Float(string="Over time",compute="_compute_over_time")
    date_day= fields.Date(string="Date")


    

    _sql_constraints = [
        ('unique_id_api', 'unique(id_api)', 'ID API must be unique!'),
    ]
    # @api.depends('check_in','check_out')
    # def _compute_over_time(self):
    # #    employee = self.env['hr.employee'].search([('code_employee','=',self.code_employee)])
    # #    work_hours_day = employee.contract_id.x_working_hours
    # #    print(work_hours_day)
    #    for attendance in self:
    #         employee = self.env['hr.employee'].search([('code_employee','=',attendance.code_employee)])
    #         work_hours_day = employee.contract_id.x_working_hours
    #         attendance.ensure_one()
    #         if attendance.check_out and attendance.check_in:
    #             delta = attendance.check_out - attendance.check_in
    #             worked_hours = delta.total_seconds() / 3600.0
    #             if employee.contract_id.x_working_hours!= 0:
    #               if worked_hours > work_hours_day :
    #
    #                  attendance.over_time = worked_hours-work_hours_day
    #                 # over =
    #               else:
    #                 attendance.over_time = 0.0
    #             else:
    #                 attendance.over_time = 0.0
    #         else:
    #
    #             attendance.over_time = False


    def create_from_api_response(self,data_from,data_to):
        attendance=self.env['attendance.get.data'].search([('punch_time','>',data_from),('punch_time','<',data_to)])
        print(attendance)
        for item in attendance:
            
            employees = self.env['hr.employee'].search([('code_employee', '=', item.emp_code)])
            if employees:
                self.create_record(item)

    def create_record(self, data):
        
     
    

        if data.punch_state_display == 'Sign In':
            employees = self.env['hr.employee'].search([('code_employee', '=', data.emp_code)])
            employee_count = employees.search_count([])
            
            # print("Employee count:", employee_count)
            for emp in employees:
                if emp:
                    
                    last_attendance = self.search([
                        ('employee_id', '=', emp.id),
                        ('check_in', '!=', False),
                        ('date_day','=', data.punch_time.date()),
                        ('check_out', '=', False),
                        ('id_api', '!=', int(data.Attendance_id))
                    ], order='check_in desc', limit=1)
                    id_attendance = self.search([('id_api', '=', int(data.Attendance_id))])
                    if last_attendance:
                        print(last_attendance.check_in.date(),"@@@@@@@@"*20)
                        continue

                    if id_attendance:
                        # print("0" * 50)
                        continue
                    else:
                        vals = {
                            'id_api': int(data.Attendance_id),
                            'employee_id': emp.id,
                            'code_employee': emp.code_employee,
                            'check_in': data.punch_time,
                            'date_day': data.punch_time.date(),
                        }
                        print("HR Attendance Record created:", data)
                        self.create(vals)
                        break
                else:
                    print("Employee with code_employee '{}' not found.".format(data.emp_code))

        # elif data.get('punch_state_display') == 'Sign Out':
        #             print("Employee with code_employee '{}' not found.".format(data.get('emp_code')))

        elif data.punch_state_display == 'Sign Out':

            employees = self.env['hr.employee'].search([('code_employee', '=', data.emp_code)])
            for emp in employees:
                if emp:
                    attendance = self.search([
                        ('employee_id', '=', emp.id),
                        ('check_in', '!=', False),
                        ('check_out', '=', False),
                        ('check_in', '<', data.punch_time),
                        ('date_day', '=', data.punch_time.date())


                    ])
                    if attendance :
                        # punch_time = datetime.strptime(data.punch_time, '%Y-%m-%d %H:%M:%S')
                        punch_time = data.punch_time
                        for rec in attendance:
                            time_difference = punch_time - rec.check_in
                            max_time_difference = timedelta(days=1) 
                            if time_difference < max_time_difference:
                                rec.write({'check_out': data.punch_time})
                                # print("HR Attendance Record updated with Check Out:", data)

                            else:    
                               print("Time difference between Check In and punch_time should be less than 24 hours. ")
                    else:
                        print("No open attendance record found for employee '{}' to sign out.".format(emp.name))
                else:
                    print("Employee with code_employee '{}' not found.".format(data.emp_code))
        # return self.create_from_api_response_two()
   











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
