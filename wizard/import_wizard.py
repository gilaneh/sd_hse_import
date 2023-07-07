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
# from tabulate import tabulate
# from prettytable import PrettyTable


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
    file_date = fields.Date(required=True)
    log_field = fields.Text()


    # start_date = fields.Date(required=True, default=lambda self: date.today() )
    calendar = fields.Selection([('fa_IR', 'Persian'), ('en_US', 'Gregorian')],
                                default=lambda self: 'fa_IR' if self.env.context.get('lang') == 'fa_IR' else 'en_US')

    # #############################################################################
    def hse_test_import(self):
        self.log_field = ''
        error_log = ''
        log_result = ''
        read_form = self.read()[0]
        data = {'form_data': read_form}

        if read_form.get('excel_file'):
            data_list = {
                #     'date': (1, 'Unnamed: 6'),
                'weather': (1, 'Unnamed: 14'),
                'max_temp': (2, 'Unnamed: 15'),
                'min_temp': (3, 'Unnamed: 15'),
                'wind': (4, 'Unnamed: 15'),
                'subcontractor': (6, 'Unnamed: 2'),
                'contractor': (6, 'Unnamed: 6'),
                'local': (6, 'Unnamed: 10'),
                'client': (6, 'Unnamed: 13'),
                'visitor': (6, 'Unnamed: 16'),
                'Fatality': (16, 'Unnamed: 1'),
                'PTD_PPD': (16, 'Unnamed: 2'),
                'LTI': (16, 'Unnamed: 3'),
                'RWC': (16, 'Unnamed: 4'),
                'illness': (16, 'Unnamed: 5'),
                'MTC': (16, 'Unnamed: 6'),
                'Audits': (16, 'Unnamed: 7'),
                'UC_UA': (16, 'Unnamed: 8'),
                'Near_Miss': (16, 'Unnamed: 9'),
                'meetings': (16, 'Unnamed: 10'),
                'training': (16, 'Unnamed: 11'),
                'FAC': (16, 'Unnamed: 12'),
                'RVA': (16, 'Unnamed: 13'),
                'Fire': (16, 'Unnamed: 14'),
                'prdc': (16, 'Unnamed: 15'),
                'medical_rest': (16, 'Unnamed: 16'),
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
                    # sheet_data = [rec.sheet for rec in import_data]
                    excel_file = base64.b64decode(self.excel_file)
                    bytestream = io.BytesIO(excel_file)
                    bytestream.seek(0)
                    wb = openpyxl.load_workbook(bytestream)
                    sheets = wb.sheetnames
                    # return

                    excel_data = pd.read_excel(excel_file, sheet_name=sheets)
                    if self.calendar == 'fa_IR':
                        month_first_day = jdatetime.date.fromgregorian(date=self.file_date).replace(day=1)
                        next_month = month_first_day.replace(day=28) + timedelta(days=5)
                        month_last_day = next_month - timedelta(days=next_month.day)
                        last_day = month_last_day.day
                        self.log_field += month_first_day.strftime('%Y/%m/%d') + '   ' + month_last_day.strftime('%Y/%m/%d') + '\n'
                        month_first_day = month_first_day.togregorian()
                        month_last_day = month_last_day.togregorian()

                    else:
                        month_first_day = self.file_date.replace(day=1)
                        next_month = month_first_day.replace(day=28) + timedelta(days=5)
                        month_last_day = (next_month - timedelta(days=next_month.day))
                        last_day = month_last_day.day
                        self.log_field += month_first_day.strftime('%Y/%m/%d') + ' ' + month_last_day.strftime('%Y/%m/%d') + '\n'

                    import_data = self.env['sd_hse_import.data'].search([
                                                                         '|',
                                                                         ('active', '=', True),
                                                                         ('active', '=', False),
                                                                        ('data_date', '>=', month_first_day),
                                                                         ('data_date', '<=', month_last_day),
                                                                         ('project', '<=', self.project.id),
                                                                         ],)
                    import_data_date = [rec.data_date for rec in import_data]
                    print(f'\n{import_data}\n')

                    data_all = []
                    for sheet in sheets:
                        if sheet == '00':
                            continue
                        sheet_day = int(sheet) if sheet.isdigit() else False
                        if not sheet_day and sheet_day < 1 or sheet_day > last_day:
                            error_log += _(f'{sheet:<4}')
                            log_result += _(f'{sheet:<4}Ignored\n')
                            continue


                        # print(sheet, sheet_day, last_day)

                        if self.calendar == 'fa_IR':
                            data_date = jdatetime.date.fromgregorian(date=self.file_date).replace(day=sheet_day)
                            log_result_date = data_date.strftime('%Y-%m-%d')
                            data_date = data_date.togregorian()
                        else:
                            data_date = self.file_date.replace(day=sheet_day)
                            log_result_date = data_date.strftime('%Y-%m-%d')
                        if data_date in import_data_date:
                            error_log += _(f'{sheet:<4}')
                            log_result += _(f'{sheet:<4}Date record already exists\n')
                            continue

                        row_items = [self.project, data_date, self.excel_file_name, sheet, ]
                        new_rec_data = {'project': self.project.id, 'data_date': data_date, 'data_file': self.excel_file_name, 'data_sheet': sheet}
                        # log_result.append([self.project.name, log_result_date, self.excel_file_name, sheet])
                        log_result += f'{sheet:<4}{log_result_date:<12}{self.project.name:<30}{self.excel_file_name:<30}\n'
                        df = excel_data[sheet]
                        for key, value in data_list.items():
                            row_items.append(df.loc[value] if df.loc[value] != 'nan' else 0)
                            new_rec_data[f'data_{key}'] = df.loc[value]
                        self.env['sd_hse_import.data'].create(new_rec_data)
                        data_all.append(row_items)
                    # for data in data_all:
                    #     print(data)
                except Exception as e:
                    logging.error(f'hse_test_import: {e}')
                    raise UserError(_(f'File read Error: {e}'))
            elif self.excel_file_name:
                self.excel_file = ''
                self.excel_file_name = ''
                raise UserError(_(f'Try again! select a .xlsx file '))
        # self.log_field += tabulate(log_result, headers=['Project', 'Date', 'File', 'Sheet'],tablefmt='orgtbl')
        # t = PrettyTable(['Project', 'Date', 'File', 'Sheet'])
        # t.add_rows(log_result)
        # print(t)
        # self.log_field += str(t)
        self.log_field += 'Ignored Sheets:\n' + error_log
        self.log_field += '\n----------------------------------------------------\n'
        self.log_field += log_result

        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'sd_hse_import.import.wizard',
                'target': 'new',
                'res_id': self.id,
                }

    def hse_close(self):
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