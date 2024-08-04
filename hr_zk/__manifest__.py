# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'ZK',
    'version': '2.0',
    'category': 'Human Resources/Attendances',
    # 'sequence': 240,
    'summary': 'ZK employee attendance',
    'description': """
This module aims to manage employee's attendances.
==================================================

Keeps account of the attendances of the employees on the basis of the
actions(Check in/Check out) performed by them.
       """,
    'website': 'https://www.odoo.com/app/employees',
    'depends': ['base','hr', 'hr_attendance','om_hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/date.xml',
        'views/hr_zk.xml',
        'views/payrol.xml',
        'views/attendance.xml',
        
      
    
    ],
   
    'installable': True,
    'auto_install': False,
    'application': True,

    'license': 'LGPL-3',
}
