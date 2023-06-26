# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo import Command
from colorama import Fore
from datetime import datetime, date
import jdatetime
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
import pandas as pd
import base64
from lxml import etree
import openpyxl
import io
# #############################################################################
class SdHseImportImportWizard(models.TransientModel):
    _name = 'sd_hse_import.import.wizard'
    _description = 'HSE Database Import Wizard'

    def _project_domain(self):
        partner_id = self.env.user.partner_id
        projects = self.env['sd_hse.project'].search(['|',
                                                      ('hse_managers', 'in', partner_id.id),
                                                      ('hse_officers', 'in', partner_id.id),])
        return [('id', 'in', projects.ids)]

    project = fields.Many2one('sd_hse.project', required=True,
                              domain=lambda self: self._project_domain(), tracking=True,
                              default=lambda self: self.project.search(
                                  ['|', ('hse_managers', 'in', self.env.user.partner_id.id),
                                   ('hse_officers', 'in', self.env.user.partner_id.id)], limit=1))
    excel_file = fields.Binary(required=True)
    excel_file_name = fields.Char()
    # sheet_names = fields.Selection(selection=sheet_list, string='Sheet Names', default='0')
    sheet_list = fields.Char()
    file_date = fields.Date()


    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')




    # @api.onchange('excel_file')
    def excel_file_changed(self):
        data_list = {'date': (1, 'Unnamed: 6'),
                     'weather': (1, 'Unnamed: 14'),
                     'max_temp': (2, 'Unnamed: 15'),
                     'min_temp': (3, 'Unnamed: 15'),
                     'wind': (4, 'Unnamed: 15'),
                     'subcontractor': (6, 'Unnamed: 2'),
                     'contractor': (6, 'Unnamed: 6'),
                     'local': (6, 'Unnamed: 10'),
                     'client': (6, 'Unnamed: 13'),
                     'visitor': (6, 'Unnamed: 16'),
                     'Fatality': (6, 'Unnamed: 16'),
                     'PTD_PPD': (16, 'Unnamed: 1'),
                     'LTI': (16, 'Unnamed: 2'),
                     'MTC': (16, 'Unnamed: 3'),
                     'Audits': (16, 'Unnamed: 4'),
                     'UC_UA': (16, 'Unnamed: 5'),
                     'Near_Miss': (16, 'Unnamed: 6'),
                     'meetings': (16, 'Unnamed: 7'),
                     'training': (16, 'Unnamed: 8'),
                     'FAC': (16, 'Unnamed: 9'),
                     'RVA': (16, 'Unnamed: 10'),
                     'Fire': (16, 'Unnamed: 11'),
                     'prdc': (16, 'Unnamed: 12'),
                     'medical_rest': (16, 'Unnamed: 13'),
                     'tbm': (21, 'Unnamed: 2'),
                     'anomaly': (21, 'Unnamed: 6'),
                     'drill': (21, 'Unnamed: 10'),
                     'induction': (21, 'Unnamed: 13'),
                     'ptw': (21, 'Unnamed: 16'),

                     }
        if self.excel_file and self.excel_file_name and (self.excel_file_name.split('.')[-1]).lower() == 'xlsx':
            try:
                # todo: persian and grogerian month
                #   projec name
                import_data = self.env['sd_hse_import.data'].search([('data_date', '>=', self.file_date)])
                sheet_data = [rec.sheet for rec in import_data]
                excel_file = base64.b64decode(self.excel_file)
                bytestream = io.BytesIO(excel_file)
                bytestream.seek(0)
                wb = openpyxl.load_workbook(bytestream)
                sheets = wb.sheetnames

                excel_data = pd.read_excel(excel_file)
                print(f'---------------------\n {sheets}')
                data_all = []
                for sheet in sheets:
                    if sheet == '00' or sheet in sheet_data or not sheet.isdigit():
                        continue

                    row_items = [self.project, self.excel_file_name, sheet, self.file_date.replace(days=int(sheet))]
                    new_rec_data = {'data_file': self.excel_file_name, 'data_sheet': sheet}

                    df = pd.read_excel(excel_file, sheet_name=sheet)
                    for key, value in data_list.items():
                        row_items.append(df.loc[value])
                        new_rec_data[f'data_{key}'] = df.loc[value]
                    self.env['sd_hse_import.data'].create(new_rec_data)
                    data_all.append(row_items)
                for data in data_all:
                    print(data)
            except Exception as e:
                logging.error(f'hse_test_import: {e}')
                raise UserError(_(f'File read Error: {e}'))
        elif self.excel_file_name:
            self.excel_file = ''
            self.excel_file_name = ''
            raise UserError(_(f'Try again! select a .xlsx file '))

    # #############################################################################
    def hse_test_import(self):
        read_form = self.read()[0]
        data = {'form_data': read_form}

        if read_form.get('excel_file'):
            data_list = {
                # 'date': (1, 'Unnamed: 6'),
                         'weather': (1, 'Unnamed: 14'),
                         'max_temp': (2, 'Unnamed: 15'),
                         'min_temp': (3, 'Unnamed: 15'),
                         'wind': (4, 'Unnamed: 15'),
                         'subcontractor': (6, 'Unnamed: 2'),
                         'contractor': (6, 'Unnamed: 6'),
                         'local': (6, 'Unnamed: 10'),
                         'client': (6, 'Unnamed: 13'),
                         'Fatality': (6, 'Unnamed: 16'),
                         'PTD_PPD': (16, 'Unnamed: 1'),
                         'LTI': (16, 'Unnamed: 2'),
                         'MTC': (16, 'Unnamed: 3'),
                         'Audits': (16, 'Unnamed: 4'),
                         'UC_UA': (16, 'Unnamed: 5'),
                         'Near_Miss': (16, 'Unnamed: 6'),
                         'meetings': (16, 'Unnamed: 7'),
                         'training': (16, 'Unnamed: 8'),
                         'FAC': (16, 'Unnamed: 9'),
                         'RVA': (16, 'Unnamed: 10'),
                         'Fire': (16, 'Unnamed: 11'),
                         'prdc': (16, 'Unnamed: 12'),
                         'medical_rest': (16, 'Unnamed: 13'),
                         'tbm': (21, 'Unnamed: 2'),
                         'anomaly': (21, 'Unnamed: 6'),
                         'drill': (21, 'Unnamed: 10'),
                         'induction': (21, 'Unnamed: 13'),
                         'ptw': (21, 'Unnamed: 16'),

                         }
            if self.excel_file and self.excel_file_name and (self.excel_file_name.split('.')[-1]).lower() == 'xlsx':
                try:
                    # todo: persian and grogerian month
                    #   projec name
                    import_data = self.env['sd_hse_import.data'].search([('data_date', '>=', self.file_date)])
                    sheet_data = [rec.sheet for rec in import_data]
                    excel_file = base64.b64decode(self.excel_file)
                    bytestream = io.BytesIO(excel_file)
                    bytestream.seek(0)
                    wb = openpyxl.load_workbook(bytestream)
                    sheets = wb.sheetnames

                    excel_data = pd.read_excel(excel_file)
                    print(f'---------------------\n {sheets}')
                    data_all = []
                    for sheet in sheets:
                        if sheet == '00' or sheet in sheet_data or not sheet.isdigit():
                            continue

                        row_items = [self.project, self.file_date.replace(day=int(sheet)), self.excel_file_name, sheet, ]

                        if self.calendar == 'fa_IR':
                            data_date = jdatetime.date.fromgregorian(date=self.file_date).replace(day=int(sheet))
                            data_date = data_date.togregorian()
                        else:
                            data_date = self.file_date.replace(day=int(sheet))
                        new_rec_data = {'project': self.project.id, 'data_date': data_date, 'data_file': self.excel_file_name, 'data_sheet': sheet}
                        print('FFFFFFFFFFFFFFFF\n', new_rec_data)

                        df = pd.read_excel(excel_file, sheet_name=sheet)
                        for key, value in data_list.items():
                            row_items.append(df.loc[value])
                            new_rec_data[f'data_{key}'] = df.loc[value]
                        self.env['sd_hse_import.data'].create(new_rec_data)
                        data_all.append(row_items)
                    for data in data_all:
                        print(data)
                except Exception as e:
                    logging.error(f'hse_test_import: {e}')
                    raise UserError(_(f'File read Error: {e}'))
            elif self.excel_file_name:
                self.excel_file = ''
                self.excel_file_name = ''
                raise UserError(_(f'Try again! select a .xlsx file '))

        # return self.env.ref('sd_hse.daily_report').report_action(self, data=data)

        return {'type': 'ir.actions.client', 'tag': 'reload'}

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False, selection=[]):
    #     result = super(SdHseImportImportWizard, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #
    #     if view_type == 'form':
    #         doc = etree.XML(result['arch'])
    #         sheet_names = result['fields']['sheet_names']
    #         print('NNNNNNNNNNNNNNNN\n', result, '\n', sheet_names)
    #         result['fields']['sheet_names']['selection'] = selection
    #
    #
    #         # if True:
    #             # Update the selection options dynamically based on conditions
    #             # sheet_names_node = doc.xpath("//field[@name='sheet_names']")[0]
    #             # sheet_names_node.set('selection', "('0', 'Option 1'), ('1', 'Option 2')")  # New selection options
    #
    #             # print(sheet_names_node, etree.tostring(doc))
    #         # result['arch'] = etree.tostring(doc, encoding='unicode')
    #
    #     return result