{
    'name': 'Odoo 17 HR Payroll Attendance',
    'category': 'Generic Modules/Human Resources',
    'version': '17.0.1.0.4',
    'sequence': 1,
    'author': 'Manahil Gamal',
    'summary': 'Payroll Attendance Data',
    'description': "Odoo 17 Payroll Attendance",
    'license': 'LGPL-3',
    'depends': [
        'om_hr_payroll',
        'hr_holidays',
    ],
    'data': [
        # 'security/hr_payroll_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        
        'views/shift_shift_views.xml',
        'wizard/hr_payroll_attendance_views.xml',
        'views/hr_policy_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_leave_type_view.xml',
        'views/payroll_atendance_view.xml',
    ],
    'application': True,
}
