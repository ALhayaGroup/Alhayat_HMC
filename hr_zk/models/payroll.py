from odoo import fields ,api , models 

class Payslip_attendance(models.Model):
    _inherit = 'hr.payslip'

    def attendance(self):
        for pay in self:
            pay.onchange_employee_id(pay.date_from , pay.date_to )
            pay.onchange_employee()
            # pay.onchange_contract()
            pay.contract_id.amount_day_in_month= pay.worked_days_line_ids.number_of_days

            attendance=self.env['hr.attendance'].search_count([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id),('check_out','!=',False)])
            # pay.contract_id.x_day_vacation=pay.contract_id.x_day_attendance-attendance
            over_time=self.env['hr.attendance'].search([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id)])
            amount_days=self.env['hr.attendance'].search_count([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id)])
            print(attendance)
            amount_time=0.0
            for time in over_time:
                amount_time += time.worked_hours
            pay.contract_id.amount_hour=amount_time
            pay.contract_id.amount_day=amount_days
            reg = pay.contract_id.regulations_id.regulations_id
            pay.contract_id.dis_hours = 0
            for line in reg:
                # print(line)
                if line.number == 1:
                   late_one = self.env['hr.attendance'].search_count([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id),('worked_hours','>=',line.late_to),('worked_hours','<=',line.late_from)])
                   print(late_one,"#"*5)
                   if late_one >= 3:
                      dis= pay.contract_id.regulations_id.hour_per_day * 0.10
                      pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                      print(dis)
                   elif late_one >= 4:
                       all_dis= late_one -3
                       
                       dis2=all_dis * (pay.contract_id.regulations_id.hour_per_day * 0.15)
                       pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                       print(dis2)    

                         
                elif line.number == 2:
                    late_two = self.env['hr.attendance'].search_count([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id),('worked_hours','>=',line.late_to),('worked_hours','<=',line.late_from)])
                    print(late_two)
                    if late_two >= 2:
                      dis= pay.contract_id.regulations_id.hour_per_day * 0.10
                      pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                      print(dis)
                    if late_two >= 3:
                      dis= pay.contract_id.regulations_id.hour_per_day * 0.15
                      pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                      print(dis)
                    elif late_two >= 4:
                       all_dis= late_one -3
                       
                       dis2=all_dis * (pay.contract_id.regulations_id.hour_per_day * 0.20)
                       pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                       print(dis2)   
                elif line.number == 3:
                    late_three = self.env['hr.attendance'].search_count([('check_in','>=',pay.date_from),('check_in','<=',pay.date_to),('employee_id','=',pay.employee_id.id),('worked_hours','<=',line.late_from)])
                    print(late_three)
                    if late_three >= 1:
                      dis= pay.contract_id.regulations_id.hour_per_day * 0.20
                      pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                      print(dis)
                    if late_three >= 2:
                      dis= pay.contract_id.regulations_id.hour_per_day * 0.25
                      pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                      print(dis)  
                    if late_three >= 3:
                      dis= pay.contract_id.regulations_id.hour_per_day * 0.35
                      pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis
                      print(dis)
                    if late_three >= 4:
                       all_dis= late_three -3
                       
                       dis2=all_dis * (pay.contract_id.regulations_id.hour_per_day * 0.50)
                       pay.contract_id.dis_hours = pay.contract_id.dis_hours + dis2
                       print(dis2)  
                    # print(3)
                

            # print(reg)
            # count_late= 0
            

            # print(count_late)
            # if count_late > 2:
            #     print(count_late-2) 
            #     if count_late == 3:
                    