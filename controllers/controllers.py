# -*- coding: utf-8 -*-
# from odoo import http


# class Magasine(http.Controller):
#     @http.route('/magasine/magasine/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/magasine/magasine/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('magasine.listing', {
#             'root': '/magasine/magasine',
#             'objects': http.request.env['magasine.magasine'].search([]),
#         })

#     @http.route('/magasine/magasine/objects/<model("magasine.magasine"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('magasine.object', {
#             'object': obj
#         })
