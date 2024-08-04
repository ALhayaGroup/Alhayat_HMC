from odoo import fields, api, models, exceptions, _
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from datetime import datetime
import requests

class Hr_Zk(models.Model):
    _inherit = "hr.attendance"
    id_api = fields.Integer()
    code_employee = fields.Char(string="Code")

    _sql_constraints = [
        ('unique_id_api', 'unique(id_api)', 'ID API must be unique!'),
    ]
    





    
    def create_from_api_response(self):
        attendance=self.env['attendance.get.data'].search([])
        print(attendance)
        for item in attendance:
            
            employees = self.env['hr.employee'].search([('pin', '=', item.emp_code)])
            if employees:
                print(employees)
            #    self.create_record(it)
    # @api.model
    # def create_record(self, record):
    #     url2 = f"http://142.132.129.24:8080/iclock/api/transactions/{record}/"
    #     payload = ""
    #     headers = {
    #         'Authorization': 'Token f32eafa83433b8e0769025b4d879f074b943fe65',
    #         'Cookie': 'session_id=dbd2801052514f476db379fd8702b9c26ae40ece'
    #     }
    #     response = requests.request("GET", url2, headers=headers, data=payload)
    #     data = response.json()

    #     if data.get('punch_state_display') == 'Sign In':
    #         employees = self.env['hr.employee'].search([('code_employee', '=', data.get('emp_code'))])
    #         employee_count = employees.search_count([])
    #         print("Employee count:", employee_count)
    #         for emp in employees:
    #             if emp:
    #                 last_attendance = self.search([
    #                     ('employee_id', '=', emp.id),
    #                     ('check_in', '!=', False),
    #                     ('check_out', '=', False),
    #                     ('id_api', '!=', int(data.get('id')))
    #                 ], order='check_in desc', limit=1)
    #                 id_attendance = self.search([('id_api', '=', int(data.get('id')))])
    #                 if last_attendance and id_attendance==False:
    #                     last_attendance.write({'check_out': last_attendance.check_in})
    #                 elif id_attendance:
    #                     print("0" * 50)
    #                     continue
    #                 else:
    #                     vals = {
    #                         'id_api': int(data.get('id')),
    #                         'employee_id': emp.id,
    #                         'code_employee': emp.code_employee,
    #                         'check_in': data.get('punch_time'),
    #                     }
    #                     print("HR Attendance Record created:", data)
    #                     self.create(vals)
    #                     break
    #             else:
    #                 print("Employee with code_employee '{}' not found.".format(data.get('emp_code')))

    #     elif data.get('punch_state_display') == 'Sign Out':
    #         employees = self.env['hr.employee'].search([('code_employee', '=', data.get('emp_code'))])
    #         for emp in employees:
    #             if emp:
    #                 attendance = self.search([
    #                     ('employee_id', '=', emp.id),
    #                     ('check_in', '!=', False),
    #                     ('check_out', '=', False),
    #                     ('check_in', '<', data.get('punch_time'))

    #                 ])
    #                 if attendance :
    #                     attendance.write({'check_out': data.get('punch_time')})
    #                     print("HR Attendance Record updated with Check Out:", data)
    #                 else:
    #                     print("No open attendance record found for employee '{}' to sign out.".format(emp.name))
    #             else:
    #                 print("Employee with code_employee '{}' not found.".format(data.get('emp_code')))                        

    


    @api.depends('check_in','check_out')
    def _onchange_(self):
        self.ensure_one()
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            
        else:
            self.worked_hours = False



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





    # @api.constrains('check_in', 'check_out', 'employee_id')
    # def _check_validity(self):
    #     """ Verifies the validity of the attendance record compared to the others from the same employee.
    #         For the same employee we must have :
    #             * maximum 1 "open" attendance record (without check_out)
    #             * no overlapping time slices with previous employee records
    #     """
    #     pass
    #     # for attendance in self:
    #     #     # we take the latest attendance before our check_in time and check it doesn't overlap with ours
    #     #     last_attendance_before_check_in = self.env['hr.attendance'].search([
    #     #         ('employee_id', '=', attendance.employee_id.id),
    #     #         ('check_in', '<=', attendance.check_in),
    #     #         ('id', '!=', attendance.id),
    #     #     ], order='check_in desc', limit=1)
    #     #     if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
    #     #         raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
    #     #             'empl_name': attendance.employee_id.name,
    #     #             'datetime': format_datetime(self.env, attendance.check_in, dt_format=False),
    #     #         })

    #     #     if not attendance.check_out:
    #     #         # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
    #     #         no_check_out_attendances = self.env['hr.attendance'].search([
    #     #             ('employee_id', '=', attendance.employee_id.id),
    #     #             ('check_out', '=', False),
    #     #             ('id', '!=', attendance.id),
    #     #         ], order='check_in desc', limit=1)
    #     #         if no_check_out_attendances:
    #     #             raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
    #     #                 'empl_name': attendance.employee_id.name,
    #     #                 'datetime': format_datetime(self.env, no_check_out_attendances.check_in, dt_format=False),
    #     #             })
    #     #     else:
    #     #         # we verify that the latest attendance with check_in time before our check_out time
    #     #         # is the same as the one before our check_in time computed before, otherwise it overlaps
    #     #         last_attendance_before_check_out = self.env['hr.attendance'].search([
    #     #             ('employee_id', '=', attendance.employee_id.id),
    #     #             ('check_in', '<', attendance.check_out),
    #     #             ('id', '!=', attendance.id),
    #     #         ], order='check_in desc', limit=1)
    #     #         if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
    #     #             raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
    #     #                 'empl_name': attendance.employee_id.name,
    #     #                 'datetime': format_datetime(self.env, last_attendance_before_check_out.check_in, dt_format=False),
    #     #             })

