from odoo import fields , models , api




class Contract_Registry(models.Model):
    _inherit = 'hr.contract'
    regulations_id=fields.Many2one('regulations', string="Regulation")
    
   