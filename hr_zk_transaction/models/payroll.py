from odoo import fields ,api , models 

class Payslip_attendance(models.Model):
    _inherit = 'hr.payslip'

    def attendance(self):
        for pay in self:
            attendance=self.env['hr.attendance'].search_count([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id)])
            # pay.contract_id.x_day_vacation=pay.contract_id.x_day_attendance-attendance
            # over_time=self.env['hr.attendance'].search([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id)])
            print(attendance)
            # amount_time=0.0
            # for time in over_time:
            #     amount_time += time.over_time
            # pay.contract_id.x_over_time=amount_time
            # # print("Total Overtime:", amount_time)


