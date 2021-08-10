# -*- coding: utf-8 -*-

from odoo import models, fields, api

class page(models.Model):
    _inherit = 'product.template'
    magazine=fields.Many2one(comodel_name='mymagazine')
    published_pages=fields.Integer("Publiées ",compute="published",readonly=True)
    # statut = fields.Selection([('s1','mpi'),('s2','2eme'),('s3','3eme'),('s4','4eme'),('s5','5eme')], default='s1', clickable=True)
    # def next_state(self):
    #     if self.statut=='s1':
    #         return self.write({'statut':'s2'})
    #     elif self.statut=='s2':
    #         return self.write({'statut':'s3'})
    #     elif self.statut=='s3':
    #         return self.write({'statut':'s4'})
    #     elif self.statut=='s4':
    #         return self.write({'statut':'s5'})
    #     else:
    #         return {'warning': {'title': 'Warning',
    #                             'message': 'Where are you going , you finished your study...'}}

    def published(self):
        for rec in self:
            self.published_pages=len(self.env['publish_command'].search([('page','=',rec.id)]))

