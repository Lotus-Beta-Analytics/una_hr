# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeePayslip(http.Controller):
#     @http.route('/employee_payslip/employee_payslip', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_payslip/employee_payslip/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_payslip.listing', {
#             'root': '/employee_payslip/employee_payslip',
#             'objects': http.request.env['employee_payslip.employee_payslip'].search([]),
#         })

#     @http.route('/employee_payslip/employee_payslip/objects/<model("employee_payslip.employee_payslip"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_payslip.object', {
#             'object': obj
#         })

