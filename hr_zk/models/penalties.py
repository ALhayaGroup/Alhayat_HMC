from odoo import models, fields

class Regulation(models.Model):
    _name = 'regulations'  # This should match the model name in XML
    _description = 'Regulations'

    name = fields.Char(required=True)
    hour_per_day = fields.Float( string="Hours per day",required=True)
    regulations_id = fields.One2many('regulations.line', 'regulation_id', string='Regulation Lines')

class RegulationsLine(models.Model):
    _name = 'regulations.line'  # This should match the model name in XML
    _description = 'Regulations Line'
    number = fields.Integer(string= "number")
    # sign_in = fields.Float(string="Check In")
    # sign_out = fields.Float(string="Check Out")
    late_from = fields.Float(string="Late from")
    late_to = fields.Float(string="Late to")
    work_hours = fields.Float(required=True, string="Work Hours")
    regulation_id = fields.Many2one('regulations', string="Regulation")



