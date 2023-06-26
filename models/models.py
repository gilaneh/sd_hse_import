# -*- coding: utf-8 -*-
import datetime
from datetime import  timedelta
# import random

from odoo import models, fields, api

from colorama import Fore


class SdHseImpoertData(models.Model):
    _name = 'sd_hse_import.data'
    _description = 'sd_hse_import.data'

    active = fields.Boolean(default=True)
    project = fields.Many2one('sd_hse.project')
    data_date = fields.Date(string="date")
    data_file = fields.Char(string="file")
    data_sheet = fields.Char(string="sheet")
    data_sheet_date = fields.Char(string="sheet_date")
    data_weather = fields.Char(string="weather")
    data_max_temp = fields.Char(string="max_temp")
    data_min_temp = fields.Char(string="min_temp")
    data_wind = fields.Char(string="wind")
    data_subcontractor = fields.Char(string="subcontractor")
    data_suncontractor = fields.Char(string="suncontractor")
    data_contractor = fields.Char(string="contractor")
    data_local = fields.Char(string="local")
    data_client = fields.Char(string="client")
    data_visitor = fields.Char(string="visitor")
    data_Fatality = fields.Char(string="Fatality")
    data_PTD_PPD = fields.Char(string="PTD_PPD")
    data_LTI = fields.Char(string="LTI")
    data_MTC = fields.Char(string="MTC")
    data_Audits = fields.Char(string="Audits")
    data_UC_UA = fields.Char(string="UC_UA")
    data_Near_Miss = fields.Char(string="Near_Miss")
    data_meetings = fields.Char(string="meetings")
    data_training = fields.Char(string="training")
    data_FAC = fields.Char(string="FAC")
    data_RVA = fields.Char(string="RVA")
    data_Fire = fields.Char(string="Fire")
    data_prdc = fields.Char(string="prdc")
    data_medical_rest = fields.Char(string="medical_rest")
    data_tbm = fields.Char(string="tbm")
    data_anomaly = fields.Char(string="anomaly")
    data_drill = fields.Char(string="drill")
    data_induction = fields.Char(string="induction")
    data_ptw = fields.Char(string="ptw")
    description = fields.Text()

    def process_records(self):
        active_ids = self.env.context.get('active_ids')
        records = self.browse(active_ids)
        personnel_model = self.env['sd_hse.personnel']
        weather_model = self.env['sd_hse.weather']
        weather_types_model = self.env['sd_hse.weather.types']
        weather_types = list([rec.name.lower() for rec in weather_types_model.search([])])
        print(weather_types)
        incident_model = self.env['sd_hse.incident']
        training_model = self.env['sd_hse.training']
        drill_model = self.env['sd_hse.drill']
        anomaly_model = self.env['sd_hse.anomaly']
        permit_model = self.env['sd_hse.permit']


        int_field_names = [
                     'data_max_temp',
                     'data_min_temp',
                     'data_wind',
                     'data_subcontractor',
                     'data_contractor',
                     'data_local',
                     'data_client',
                     'data_visitor',
                     'data_Fatality',
                     'data_PTD_PPD',
                     'data_LTI',
                     'data_MTC',
                     'data_Audits',
                     'data_UC_UA',
                     'data_Near_Miss',
                     'data_meetings',
                     'data_training',
                     'data_FAC',
                     'data_RVA',
                     'data_Fire',
                     'data_prdc',
                     'data_medical_rest',
                     'data_tbm',
                     'data_anomaly',
                     'data_drill',
                     'data_induction',
                     'data_ptw']
        # int_fields = filter(lambda name: name in int_field_names, self._fields)
        # for f in int_fields:
        #     print(f, type(f))

        for record in records:
            description = ''
            personnel = personnel_model.search([('record_date', '=', record.data_date),
                                                ('project', '=', record.project.id),])
            # check for old personnel or weather. If exists, it means this record cannot be imported
            if personnel:
                record.write({'description': 'Record already in sd_hse.personnel'})
                continue
            weather = weather_model.search([('record_date', '=', record.data_date),
                                            ('project', '=', record.project.id),])
            if weather:
                record.write({'description': 'Record already in sd_hse.weather'})
                continue
            if not personnel and not weather:
                record.write({'description': ''})
            # Remove old records. If there is no  personnel and weather but others, it means that there are some
            #   old records which needed to be removed.
            old_records = incident_model.search([('record_date', '=', record.data_date),
                                               ('project', '=', record.project.id), ])
            old_records.unlink() if old_records else ''
            old_records = training_model.search([('record_date', '=', record.data_date),
                                               ('project', '=', record.project.id), ])
            old_records.unlink() if old_records else ''
            old_records = drill_model.search([('record_date', '=', record.data_date),
                                               ('project', '=', record.project.id), ])
            old_records.unlink() if old_records else ''
            old_records = anomaly_model.search([('record_date', '=', record.data_date),
                                               ('project', '=', record.project.id), ])
            old_records.unlink() if old_records else ''
            old_records = permit_model.search([('record_date', '=', record.data_date),
                                               ('project', '=', record.project.id), ])
            old_records.unlink() if old_records else ''

            # check for record validity
            if record.data_weather.lower() not in weather_types:
                description += 'Weather type mismatch.\n'
            ints = [(rec_name.split('_', 1)[1], record[rec_name])
                    for rec_name in int_field_names
                    if not record[rec_name] or not record[rec_name].isdigit()]
            if ints:
                description += f'{ints}\n'
                record.write({'description': description})
                continue

            # Everything seams ok! Write the data to the models
            personnel_model.create({
                'record_date': record.data_date,
                'project': record.project,
                'subcontractor': record.data_subcontractor,
                'contractor': record.data_contractor,
                'local': record.data_local,
                'client': record.data_client,
                'visitor': record.data_visitor,
            })




