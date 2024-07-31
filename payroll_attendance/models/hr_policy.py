# -*- coding:utf-8 -*-

from odoo import api, fields, models, _


class HrPolicy(models.Model):
    _name = 'hr.policy'
    _description = 'Hr Policy'


    ATTENDANCE_STATUS = [('1_late', "Late 0:16 to 0:30"), 
                         ('2_late', "Late 0:31 to 1:00"),
                         ('3_late', "Late more than 1H"),
                         ('1_early', "Early out 0:15 to 0:30"),
                         ('absent', "Absent"),
                         ('leave', "Leave")]
    
    policy_name = fields.Char(string="Policy Name")
    name = fields.Char(string='Policy Code', required=True, readonly=True, default=lambda self: 'New')
    line_ids = fields.One2many('hr.policy.line', 'policy_id', string='Policy Lines')
    attendance_status = fields.Selection(ATTENDANCE_STATUS,string="Status")


    @api.model_create_multi
    def create(self, vals):
        if not vals[0].get('name') or vals['name'] ==  'New':
            vals[0]['name'] = self.env['ir.sequence'].next_by_code('hr.policy.seq') or 'New'
        return super(HrPolicy, self).create(vals)




class HrPolicyLine(models.Model):
    _name = 'hr.policy.line'
    _description = 'Hr Policy Line'

    policy_id = fields.Many2one("hr.policy", string="Policy")
    no = fields.Char(string='Policy Name')
    policy = fields.Float(string="Policy")
    actual_policy = fields.Float("Actual Policy") 
