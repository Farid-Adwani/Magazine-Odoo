# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class publish_command(models.Model):
    _name= 'publish_command'
    _inherit = 'mail.thread'
    _description='Commande de publication de page'
    page=fields.Many2one(comodel_name='product.template',required=True,domain=[('default_code','like','PAGE')])
    month=fields.Selection([('1','Janvier'),('2','Février'),('3','Mars'),('4','Avril'),('5','Mai'),
                            ('6','Juin'),('7','Juillet'),('8','Aout'),('9','Septembre'),('10','Octobre'),('11','Novembre'),
                            ('12','Décembre')],required=True)
    customer=fields.Many2one(comodel_name='res.partner',required=True)
    magazine_name=fields.Char('Nom De La Magazine',related='page.magazine.title')
    img_magazine=fields.Binary('Photo De La Magazine',related='page.magazine.image')
    img_page=fields.Binary('Photo',related='page.image_1920')
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

    @api.model
    def create(self, values):
        test=False;
        sold_pages = 0
        customer=self.env['res.partner'].browse(values['customer'])
        page=self.env['product.template'].browse(values['page'])
        sale_orders=self.env['sale.order.line'].search([('state','=','sale'),('order_partner_id','=',values['customer']),('product_id','=',page.id)])
        if(len(sale_orders)==0):
            raise ValidationError('This Record can not be created because the customer '+str(customer.name)+' did not buy yet '
                                    'this page: '+str(page.name))

        same_order=self.env['publish_command'].search(['&',('page','=',values['page']),('month','=',values['month'])])
        if len(same_order)==0:
            for order in sale_orders:
                sold_pages+=order.product_uom_qty
            consumed=self.env['publish_command'].search([('page','=',values['page']),('customer','=',values['customer'])])
            if(sold_pages<=len(consumed)):
                raise ValidationError("Désolé :(\n vous avez voulez publier la page n° "+str(len(consumed)+1)+" mais vous avez achetez que "+str(int(sold_pages))+" de : "+str(page.name))
            res = super(publish_command, self).create(values)
        else:
            month_string=dict(self._fields['month'].selection).get(values['month'])
            raise ValidationError('Désolé :( \n '+str(page.name)+' est réservée en mois de '+str(month_string)+' à Mr '+str(customer.name))
        # page1
        # page milieu
        return res;

    {'order_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {}, 'depends': (),
                  'domain': [], 'manual': False, 'readonly': False, 'relation': 'sale.order', 'required': True,
                  'searchable': True, 'sortable': True, 'store': True, 'string': 'Order Reference'},
     'name': {'type': 'text', 'change_default': False, 'company_dependent': False, 'depends': (), 'manual': False,
              'readonly': False, 'required': True, 'searchable': True, 'sortable': True, 'store': True,
              'string': 'Description', 'translate': False},
     'sequence': {'type': 'integer', 'change_default': False, 'company_dependent': False, 'depends': (),
                  'group_operator': 'sum', 'manual': False, 'readonly': False, 'required': False, 'searchable': True,
                  'sortable': True, 'store': True, 'string': 'Sequence'},
     'invoice_lines': {'type': 'many2many', 'change_default': False, 'company_dependent': False, 'context': {},
                       'depends': (), 'domain': [], 'manual': False, 'readonly': False, 'relation': 'account.move.line',
                       'required': False, 'searchable': True, 'sortable': False, 'store': True,
                       'string': 'Invoice Lines'},
     'invoice_status': {'type': 'selection', 'change_default': False, 'company_dependent': False, 'depends': (
     'order_id.state', 'state', 'product_uom_qty', 'qty_delivered', 'qty_to_invoice', 'qty_invoiced'), 'manual': False,
                        'readonly': True, 'required': False, 'searchable': True,
                        'selection': [('upselling', 'Upselling Opportunity'), ('invoiced', 'Fully Invoiced'),
                                      ('to invoice', 'To Invoice'), ('no', 'Nothing to Invoice')], 'sortable': True,
                        'store': True, 'string': 'Invoice Status'},
     'price_unit': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (),
                    'digits': (16, 2), 'group_operator': 'sum', 'manual': False, 'readonly': False, 'required': True,
                    'searchable': True, 'sortable': True, 'store': True, 'string': 'Unit Price'},
     'price_subtotal': {'type': 'monetary', 'change_default': False, 'company_dependent': False,
                        'currency_field': 'currency_id',
                        'depends': ('product_uom_qty', 'discount', 'price_unit', 'tax_id'), 'group_operator': 'sum',
                        'manual': False, 'readonly': True, 'required': False, 'searchable': True, 'sortable': True,
                        'store': True, 'string': 'Subtotal'},
     'price_tax': {'type': 'float', 'change_default': False, 'company_dependent': False,
                   'depends': ('product_uom_qty', 'discount', 'price_unit', 'tax_id'), 'group_operator': 'sum',
                   'manual': False, 'readonly': True, 'required': False, 'searchable': True, 'sortable': True,
                   'store': True, 'string': 'Total Tax'},
     'price_total': {'type': 'monetary', 'change_default': False, 'company_dependent': False,
                     'currency_field': 'currency_id',
                     'depends': ('product_uom_qty', 'discount', 'price_unit', 'tax_id'), 'group_operator': 'sum',
                     'manual': False, 'readonly': True, 'required': False, 'searchable': True, 'sortable': True,
                     'store': True, 'string': 'Total'},
     'price_reduce': {'type': 'float', 'change_default': False, 'company_dependent': False,
                      'depends': ('price_unit', 'discount'), 'digits': (16, 2), 'group_operator': 'sum',
                      'manual': False, 'readonly': True, 'required': False, 'searchable': True, 'sortable': True,
                      'store': True, 'string': 'Price Reduce'},
     'tax_id': {'type': 'many2many', 'change_default': False, 'company_dependent': False, 'context': {},
                'depends': ('tax_id.active',), 'domain': ['|', ('active', '=', False), ('active', '=', True)],
                'manual': False, 'readonly': False, 'relation': 'account.tax', 'required': False, 'searchable': True,
                'sortable': False, 'store': True, 'string': 'Taxes'},
     'price_reduce_taxinc': {'type': 'monetary', 'change_default': False, 'company_dependent': False,
                             'currency_field': 'currency_id', 'depends': ('price_total', 'product_uom_qty'),
                             'group_operator': 'sum', 'manual': False, 'readonly': True, 'required': False,
                             'searchable': True, 'sortable': True, 'store': True, 'string': 'Price Reduce Tax inc'},
     'price_reduce_taxexcl': {'type': 'monetary', 'change_default': False, 'company_dependent': False,
                              'currency_field': 'currency_id', 'depends': ('price_subtotal', 'product_uom_qty'),
                              'group_operator': 'sum', 'manual': False, 'readonly': True, 'required': False,
                              'searchable': True, 'sortable': True, 'store': True, 'string': 'Price Reduce Tax excl'},
     'discount': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (),
                  'digits': (16, 2), 'group_operator': 'sum', 'manual': False, 'readonly': False, 'required': False,
                  'searchable': True, 'sortable': True, 'store': True, 'string': 'Discount (%)'},
     'product_id': {'type': 'many2one', 'change_default': True, 'company_dependent': False, 'context': {},
                    'depends': (),
                    'domain': "[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                    'manual': False, 'readonly': False, 'relation': 'product.product', 'required': False,
                    'searchable': True, 'sortable': True, 'store': True, 'string': 'Product'},
     'product_template_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                             'depends': ('product_id.product_tmpl_id',), 'domain': [('sale_ok', '=', True)],
                             'manual': False, 'readonly': True, 'related': ('product_id', 'product_tmpl_id'),
                             'relation': 'product.template', 'required': False, 'searchable': True, 'sortable': False,
                             'store': False, 'string': 'Product Template'},
     'product_updatable': {'type': 'boolean', 'change_default': False, 'company_dependent': False,
                           'depends': ('move_ids', 'product_id', 'order_id.state', 'qty_invoiced', 'qty_delivered'),
                           'manual': False, 'readonly': True, 'required': False, 'searchable': False, 'sortable': False,
                           'store': False, 'string': 'Can Edit Product'},
     'product_uom_qty': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (),
                         'digits': (16, 2), 'group_operator': 'sum', 'manual': False, 'readonly': False,
                         'required': True, 'searchable': True, 'sortable': True, 'store': True, 'string': 'Quantity'},
     'product_uom': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                     'depends': (), 'domain': "[('category_id', '=', product_uom_category_id)]", 'manual': False,
                     'readonly': False, 'relation': 'uom.uom', 'required': False, 'searchable': True, 'sortable': True,
                     'store': True, 'string': 'Unit of Measure'},
     'product_uom_category_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                                 'depends': ('product_id.uom_id.category_id',), 'domain': [],
                                 'help': 'Conversion between Units of Measure can only occur if they belong to the same category. The conversion will be made based on the ratios.',
                                 'manual': False, 'readonly': True, 'related': ('product_id', 'uom_id', 'category_id'),
                                 'relation': 'uom.category', 'required': False, 'searchable': True, 'sortable': False,
                                 'store': False, 'string': 'Category'},
     'product_uom_readonly': {'type': 'boolean', 'change_default': False, 'company_dependent': False,
                              'depends': ('state',), 'manual': False, 'readonly': True, 'required': False,
                              'searchable': False, 'sortable': False, 'store': False, 'string': 'Product Uom Readonly'},
     'product_custom_attribute_value_ids': {'type': 'one2many', 'change_default': False, 'company_dependent': False,
                                            'context': {}, 'depends': (), 'domain': [], 'manual': False,
                                            'readonly': False, 'relation': 'product.attribute.custom.value',
                                            'relation_field': 'sale_order_line_id', 'required': False,
                                            'searchable': True, 'sortable': False, 'store': True,
                                            'string': 'Custom Values'},
     'product_no_variant_attribute_value_ids': {'type': 'many2many', 'change_default': False,
                                                'company_dependent': False, 'context': {}, 'depends': (), 'domain': [],
                                                'manual': False, 'readonly': False,
                                                'relation': 'product.template.attribute.value', 'required': False,
                                                'searchable': True, 'sortable': False, 'store': True,
                                                'string': 'Extra Values'},
     'qty_delivered': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (
     'move_ids.state', 'move_ids.scrapped', 'move_ids.product_uom_qty', 'move_ids.product_uom', 'qty_delivered_method',
     'qty_delivered_manual', 'analytic_line_ids.so_line', 'analytic_line_ids.unit_amount',
     'analytic_line_ids.product_uom_id'), 'digits': (16, 2), 'group_operator': 'sum', 'manual': False,
                       'readonly': False, 'required': False, 'searchable': True, 'sortable': True, 'store': True,
                       'string': 'Delivered Quantity'},
     'qty_delivered_manual': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (),
                              'digits': (16, 2), 'group_operator': 'sum', 'manual': False, 'readonly': False,
                              'required': False, 'searchable': True, 'sortable': True, 'store': True,
                              'string': 'Delivered Manually'},
     'qty_to_invoice': {'type': 'float', 'change_default': False, 'company_dependent': False,
                        'depends': ('qty_invoiced', 'qty_delivered', 'product_uom_qty', 'order_id.state'),
                        'digits': (16, 2), 'group_operator': 'sum', 'manual': False, 'readonly': True,
                        'required': False, 'searchable': True, 'sortable': True, 'store': True,
                        'string': 'To Invoice Quantity'},
     'qty_invoiced': {'type': 'float', 'change_default': False, 'company_dependent': False,
                      'depends': ('invoice_lines.move_id.state', 'invoice_lines.quantity', 'untaxed_amount_to_invoice'),
                      'digits': (16, 2), 'group_operator': 'sum', 'manual': False, 'readonly': True, 'required': False,
                      'searchable': True, 'sortable': True, 'store': True, 'string': 'Invoiced Quantity'},
     'untaxed_amount_invoiced': {'type': 'monetary', 'change_default': False, 'company_dependent': False,
                                 'currency_field': 'currency_id', 'depends': (
         'invoice_lines', 'invoice_lines.price_total', 'invoice_lines.move_id.state',
         'invoice_lines.move_id.move_type'), 'group_operator': 'sum', 'manual': False, 'readonly': True,
                                 'required': False, 'searchable': True, 'sortable': True, 'store': True,
                                 'string': 'Untaxed Invoiced Amount'},
     'untaxed_amount_to_invoice': {'type': 'monetary', 'change_default': False, 'company_dependent': False,
                                   'currency_field': 'currency_id', 'depends': (
         'state', 'price_reduce', 'product_id', 'untaxed_amount_invoiced', 'qty_delivered', 'product_uom_qty'),
                                   'group_operator': 'sum', 'manual': False, 'readonly': True, 'required': False,
                                   'searchable': True, 'sortable': True, 'store': True,
                                   'string': 'Untaxed Amount To Invoice'},
     'salesman_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                     'depends': ('order_id.user_id',), 'domain': [('groups_id', 'in', 20)], 'manual': False,
                     'readonly': True, 'related': ('order_id', 'user_id'), 'relation': 'res.users', 'required': False,
                     'searchable': True, 'sortable': True, 'store': True, 'string': 'Salesperson'},
     'currency_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                     'depends': ('order_id.currency_id',), 'domain': [], 'manual': False, 'readonly': True,
                     'related': ('order_id', 'currency_id'), 'relation': 'res.currency', 'required': False,
                     'searchable': True, 'sortable': True, 'store': True, 'string': 'Currency'},
     'company_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                    'depends': ('order_id.company_id',), 'domain': [], 'manual': False, 'readonly': True,
                    'related': ('order_id', 'company_id'), 'relation': 'res.company', 'required': False,
                    'searchable': True, 'sortable': True, 'store': True, 'string': 'Company'},
     'order_partner_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                          'depends': ('order_id.partner_id',),
                          'domain': "['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                          'manual': False, 'readonly': False, 'related': ('order_id', 'partner_id'),
                          'relation': 'res.partner', 'required': False, 'searchable': True, 'sortable': True,
                          'store': True, 'string': 'Customer'},
     'analytic_tag_ids': {'type': 'many2many', 'change_default': False, 'company_dependent': False, 'context': {},
                          'depends': (), 'domain': "['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                          'manual': False, 'readonly': False, 'relation': 'account.analytic.tag', 'required': False,
                          'searchable': True, 'sortable': False, 'store': True, 'string': 'Analytic Tags'},
     'analytic_line_ids': {'type': 'one2many', 'change_default': False, 'company_dependent': False, 'context': {},
                           'depends': (), 'domain': [], 'manual': False, 'readonly': False,
                           'relation': 'account.analytic.line', 'relation_field': 'so_line', 'required': False,
                           'searchable': True, 'sortable': False, 'store': True, 'string': 'Analytic lines'},
     'is_expense': {'type': 'boolean', 'change_default': False, 'company_dependent': False, 'depends': (),
                    'help': 'Is true if the sales order line comes from an expense or a vendor bills', 'manual': False,
                    'readonly': False, 'required': False, 'searchable': True, 'sortable': True, 'store': True,
                    'string': 'Is expense'},
     'is_downpayment': {'type': 'boolean', 'change_default': False, 'company_dependent': False, 'depends': (),
                        'help': 'Down payments are made when creating invoices from a sales order. They are not copied when duplicating a sales order.',
                        'manual': False, 'readonly': False, 'required': False, 'searchable': True, 'sortable': True,
                        'store': True, 'string': 'Is a down payment'},
     'state': {'type': 'selection', 'change_default': False, 'company_dependent': False, 'depends': ('order_id.state',),
               'manual': False, 'readonly': True, 'related': ('order_id', 'state'), 'required': False,
               'searchable': True,
               'selection': [('draft', 'Quotation'), ('sent', 'Quotation Sent'), ('sale', 'Sales Order'),
                             ('done', 'Locked'), ('cancel', 'Cancelled')], 'sortable': True, 'store': True,
               'string': 'Order Status'},
     'customer_lead': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (),
                       'group_operator': 'sum',
                       'help': 'Number of days between the order confirmation and the shipping of the products to the customer',
                       'manual': False, 'readonly': False, 'required': True, 'searchable': True, 'sortable': True,
                       'store': True, 'string': 'Lead Time'},
     'display_type': {'type': 'selection', 'change_default': False, 'company_dependent': False, 'depends': (),
                      'help': 'Technical field for UX purpose.', 'manual': False, 'readonly': False, 'required': False,
                      'searchable': True, 'selection': [('line_section', 'Section'), ('line_note', 'Note')],
                      'sortable': True, 'store': True, 'string': 'Display Type'},
     'sale_order_option_ids': {'type': 'one2many', 'change_default': False, 'company_dependent': False, 'context': {},
                               'depends': (), 'domain': [], 'manual': False, 'readonly': False,
                               'relation': 'sale.order.option', 'relation_field': 'line_id', 'required': False,
                               'searchable': True, 'sortable': False, 'store': True,
                               'string': 'Optional Products Lines'},
     'qty_delivered_method': {'type': 'selection', 'change_default': False, 'company_dependent': False,
                              'depends': ('product_id', 'state', 'is_expense'),
                              'help': 'According to product configuration, the delivered quantity can be automatically computed by mechanism :\n  - Manual: the quantity is set manually on the line\n  - Analytic From expenses: the quantity is the quantity sum from posted expenses\n  - Timesheet: the quantity is the sum of hours recorded on tasks linked to this sale line\n  - Stock Moves: the quantity comes from confirmed pickings\n',
                              'manual': False, 'readonly': True, 'required': False, 'searchable': True,
                              'selection': [('manual', 'Manual'), ('analytic', 'Analytic From Expenses'),
                                            ('stock_move', 'Stock Moves')], 'sortable': True, 'store': True,
                              'string': 'Method to update delivered qty'},
     'product_packaging': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                           'depends': (), 'domain': "[('company_id', 'in', [company_id, False])]", 'manual': False,
                           'readonly': False, 'relation': 'product.packaging', 'required': False, 'searchable': True,
                           'sortable': True, 'store': True, 'string': 'Package'},
     'route_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {}, 'depends': (),
                  'domain': [('sale_selectable', '=', True)], 'manual': False, 'readonly': False,
                  'relation': 'stock.location.route', 'required': False, 'searchable': True, 'sortable': True,
                  'store': True, 'string': 'Route'},
     'move_ids': {'type': 'one2many', 'change_default': False, 'company_dependent': False, 'context': {}, 'depends': (),
                  'domain': [], 'manual': False, 'readonly': False, 'relation': 'stock.move',
                  'relation_field': 'sale_line_id', 'required': False, 'searchable': True, 'sortable': False,
                  'store': True, 'string': 'Stock Moves'},
     'product_type': {'type': 'selection', 'change_default': False, 'company_dependent': False,
                      'depends': ('product_id.type',),
                      'help': 'A storable product is a product for which you manage stock. The Inventory app has to be installed.\nA consumable product is a product for which stock is not managed.\nA service is a non-material product you provide.',
                      'manual': False, 'readonly': True, 'related': ('product_id', 'type'), 'required': False,
                      'searchable': True,
                      'selection': [('consu', 'Consumable'), ('service', 'Service'), ('product', 'Storable Product')],
                      'sortable': False, 'store': False, 'string': 'Product Type'},
     'virtual_available_at_date': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (
     'product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.commitment_date', 'move_ids',
     'move_ids.forecast_expected_date', 'move_ids.forecast_availability'), 'digits': (16, 2), 'group_operator': 'sum',
                                   'manual': False, 'readonly': True, 'required': False, 'searchable': False,
                                   'sortable': False, 'store': False, 'string': 'Virtual Available At Date'},
     'scheduled_date': {'type': 'datetime', 'change_default': False, 'company_dependent': False, 'depends': (
     'product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.commitment_date', 'move_ids',
     'move_ids.forecast_expected_date', 'move_ids.forecast_availability'), 'manual': False, 'readonly': True,
                        'required': False, 'searchable': False, 'sortable': False, 'store': False,
                        'string': 'Scheduled Date'},
     'forecast_expected_date': {'type': 'datetime', 'change_default': False, 'company_dependent': False, 'depends': (
     'product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.commitment_date', 'move_ids',
     'move_ids.forecast_expected_date', 'move_ids.forecast_availability'), 'manual': False, 'readonly': True,
                                'required': False, 'searchable': False, 'sortable': False, 'store': False,
                                'string': 'Forecast Expected Date'},
     'free_qty_today': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (
     'product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.commitment_date', 'move_ids',
     'move_ids.forecast_expected_date', 'move_ids.forecast_availability'), 'digits': (16, 2), 'group_operator': 'sum',
                        'manual': False, 'readonly': True, 'required': False, 'searchable': False, 'sortable': False,
                        'store': False, 'string': 'Free Qty Today'},
     'qty_available_today': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (
     'product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.commitment_date', 'move_ids',
     'move_ids.forecast_expected_date', 'move_ids.forecast_availability'), 'group_operator': 'sum', 'manual': False,
                             'readonly': True, 'required': False, 'searchable': False, 'sortable': False,
                             'store': False, 'string': 'Qty Available Today'},
     'warehouse_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                      'depends': ('order_id.warehouse_id',), 'domain': [], 'manual': False, 'readonly': True,
                      'related': ('order_id', 'warehouse_id'), 'relation': 'stock.warehouse', 'required': False,
                      'searchable': True, 'sortable': False, 'store': False, 'string': 'Warehouse'},
     'qty_to_deliver': {'type': 'float', 'change_default': False, 'company_dependent': False, 'depends': (
     'product_type', 'product_uom_qty', 'qty_delivered', 'state', 'move_ids', 'product_uom'), 'digits': (16, 2),
                        'group_operator': 'sum', 'manual': False, 'readonly': True, 'required': False,
                        'searchable': False, 'sortable': False, 'store': False, 'string': 'Qty To Deliver'},
     'is_mto': {'type': 'boolean', 'change_default': False, 'company_dependent': False,
                'depends': ('product_id', 'route_id', 'order_id.warehouse_id', 'product_id.route_ids'), 'manual': False,
                'readonly': True, 'required': False, 'searchable': False, 'sortable': False, 'store': False,
                'string': 'Is Mto'},
     'display_qty_widget': {'type': 'boolean', 'change_default': False, 'company_dependent': False, 'depends': (
     'product_type', 'product_uom_qty', 'qty_delivered', 'state', 'move_ids', 'product_uom'), 'manual': False,
                            'readonly': True, 'required': False, 'searchable': False, 'sortable': False, 'store': False,
                            'string': 'Display Qty Widget'},
     'id': {'type': 'integer', 'change_default': False, 'company_dependent': False, 'depends': (), 'manual': False,
            'readonly': True, 'required': False, 'searchable': True, 'sortable': True, 'store': True, 'string': 'ID'},
     'display_name': {'type': 'char', 'change_default': False, 'company_dependent': False, 'depends': ('name',),
                      'manual': False, 'readonly': True, 'required': False, 'searchable': False, 'sortable': False,
                      'store': False, 'string': 'Display Name', 'translate': False, 'trim': True},
     'create_uid': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                    'depends': (), 'domain': [], 'manual': False, 'readonly': True, 'relation': 'res.users',
                    'required': False, 'searchable': True, 'sortable': True, 'store': True, 'string': 'Created by'},
     'create_date': {'type': 'datetime', 'change_default': False, 'company_dependent': False, 'depends': (),
                     'manual': False, 'readonly': True, 'required': False, 'searchable': True, 'sortable': True,
                     'store': True, 'string': 'Created on'},
     'write_uid': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                   'depends': (), 'domain': [], 'manual': False, 'readonly': True, 'relation': 'res.users',
                   'required': False, 'searchable': True, 'sortable': True, 'store': True, 'string': 'Last Updated by'},
     'write_date': {'type': 'datetime', 'change_default': False, 'company_dependent': False, 'depends': (),
                    'manual': False, 'readonly': True, 'required': False, 'searchable': True, 'sortable': True,
                    'store': True, 'string': 'Last Updated on'},
     '__last_update': {'type': 'datetime', 'change_default': False, 'company_dependent': False,
                       'depends': ('create_date', 'write_date'), 'manual': False, 'readonly': True, 'required': False,
                       'searchable': False, 'sortable': False, 'store': False, 'string': 'Last Modified on'}}
