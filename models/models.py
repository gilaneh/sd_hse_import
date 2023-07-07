# -*- coding: utf-8 -*-
import datetime
from datetime import  timedelta
# import random

from odoo import models, fields, api
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError

from colorama import Fore
import random
import logging
import traceback

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
    data_contractor = fields.Char(string="contractor")
    data_local = fields.Char(string="local")
    data_client = fields.Char(string="client")
    data_visitor = fields.Char(string="visitor")
    data_Fatality = fields.Char(string="Fatality")
    data_PTD_PPD = fields.Char(string="PTD_PPD")
    data_LTI = fields.Char(string="LTI")
    data_RWC = fields.Char(string="RWC")
    data_illness = fields.Char(string="illness")
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

    def records_statistics(self):
        active_ids = self.env.context.get('active_ids')
        records = self.browse(active_ids)
        subcontrators = 0
        print(f'records\n {records}')
        subcontractor = 0
        contractor = 0
        local = 0
        client = 0
        visitor = 0
        fatality = 0
        ptd_ppd = 0
        lti = 0
        rwc = 0
        mtc = 0
        fac = 0
        rva = 0
        fire = 0
        near_miss = 0
        training = 0
        tbm = 0
        induction = 0
        anomaly = 0
        drill = 0
        ptw = 0
        records_info = ((r.data_subcontractor, 
                         r.data_contractor, 
                         r.data_local, 
                         r.data_client,
                         r.data_visitor,
                         r.data_Fatality,
                         r.data_PTD_PPD,
                         r.data_LTI,
                         r.data_RWC,
                         r.data_MTC,
                         r.data_FAC,
                         r.data_RVA,
                         r.data_Fire,
                         r.data_Near_Miss,
                         r.data_training,
                         r.data_tbm,
                         r.data_induction,
                         r.data_anomaly,
                         r.data_drill,
                         r.data_ptw,
                         ) for r in records)
        for item in records_info:
            subcontractor += int(item[0])
            contractor += int(item[1])
            local += int(item[2])
            client += int(item[3])
            visitor += int(item[4])
            fatality += int(item[5])
            ptd_ppd += int(item[6])
            lti += int(item[7])
            rwc += int(item[8])
            mtc += int(item[9])
            fac += int(item[10])
            rva += int(item[11])
            fire += int(item[12])
            near_miss += int(item[13])
            training += int(item[14])
            tbm += int(item[15])
            induction += int(item[16])
            anomaly += int(item[17])
            drill += int(item[18])
            ptw += int(item[19])
        raise UserError(f'subcontractor: {subcontractor}\n'
                        f'contractor: {contractor}\n'
                                f'local: {local}\n'
        f'client: {client}\n'
        f'fatality: {fatality}\n'
        f'ptd_ppd: {ptd_ppd}\n'
        f'lti: {lti}\n'
        f'rwc: {rwc}\n'
        f'mtc: {mtc}\n'
        f'fac: {fac}\n'
        f'rva: {rva}\n'
        f'fire: {fire}\n'
        f'near_miss: {near_miss}\n'
        f'training: {training}\n'
        f'tbm: {tbm}\n'
        f'induction: {induction}\n'
        f'anomaly: {anomaly}\n'
        f'drill: {drill}\n'
        f'ptw: {ptw}\n'
                        f'')

    def process_records(self):
        active_ids = self.env.context.get('active_ids')
        records = self.browse(active_ids)
        personnel_model = self.env['sd_hse.personnel']
        weather_model = self.env['sd_hse.weather']

        weather_types_model = self.env['sd_hse.weather.types']
        weather_types = dict([(rec.name.lower(), rec.id) for rec in weather_types_model.search([])])

        incident_types_model = self.env['sd_hse.incident.types']
        incident_types = dict([(rec.name.lower(), rec.id) for rec in incident_types_model.search([])])
        training_types_model = self.env['sd_hse.training.types']
        training_types = dict([(rec.name.lower(), rec.id) for rec in training_types_model.search([])])

        drill_types_model = self.env['sd_hse.drill.types']
        drill_types = dict([(rec.name.lower(), rec.id) for rec in drill_types_model.search([])])
        anomaly_types_model = self.env['sd_hse.anomaly.types']
        anomaly_types = dict([(rec.name.lower(), rec.id) for rec in anomaly_types_model.search([])])
        permit_types_model = self.env['sd_hse.permit.types']
        permit_types = dict([(rec.name.lower(), rec.id) for rec in permit_types_model.search([])])
        print('FFFFFFFFFFFFFFFF\n', 'incident_types', incident_types)
        print(incident_types.get('fatality', False))
        # print('training_types', training_types)
        # print('drill_types', drill_types)
        # print('anomaly_types', anomaly_types)
        # print('permit_types', permit_types)

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
                     'data_RWC',
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

        for record in records:
            try:
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
                if not weather_types.get(record.data_weather.lower(), False):
                    record.write({'description': 'Weather type mismatch.\n'})
                    continue
                ints = [(rec_name.split('_', 1)[1], record[rec_name])
                        for rec_name in int_field_names
                        if not record[rec_name] or not record[rec_name].isdigit()]
                if ints:
                    description += f'{ints}\n'
                    record.write({'description': description})
                    continue
                weather_type = weather_types_model. search([('name', '=', record.data_weather)])
                if len(weather_type) > 1:
                    record.write({'description': f'multiple weather{" ".join(list([r.name for r in weather_type]))}'})
                    continue
                data_Fatality = int(record.data_Fatality)
                data_PTD_PPD = int(record.data_PTD_PPD)
                data_LTI = int(record.data_LTI)
                data_RWC = int(record.data_RWC)
                data_MTC = int(record.data_MTC)
                data_FAC = int(record.data_FAC)
                data_RVA = int(record.data_RVA)
                data_Fire = int(record.data_Fire)
                data_Near_Miss =int(record.data_Near_Miss)
                total_incidents = int(data_Fatality) + int(data_PTD_PPD) + int(data_LTI) + int(data_RWC) + int(data_MTC)
                total_incidents = total_incidents  + int(data_FAC) + int(data_RVA) + int(data_Fire) + int(data_Near_Miss)
                print(f'>>>>>>>>>>>>>>>>\n {total_incidents}')
                # if int(record.data_medical_rest) > 0 and total_incidents == 0:
                #     record.write({'description': f'Mediacl Rest needed at least one incident'})
                #     continue


                # Everything seams ok! Write the data to the models
                personnel_model.create({
                    'record_date': record.data_date,
                    'project': record.project.id,
                    'subcontractor': record.data_subcontractor,
                    'contractor': record.data_contractor,
                    'local': record.data_local,
                    'client': record.data_client,
                    'visitor': record.data_visitor,
                })

                weather_model.create({
                    'record_date': record.data_date,
                    'project': record.project.id,
                    'record_type': int(weather_types.get(record.data_weather.lower())),
                    'max_temperature': record.data_max_temp,
                    'min_temperature': record.data_min_temp,
                    'wind_speed': record.data_wind,
                })

                for _ in range(int(record.data_anomaly)):
                    anomaly_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'anomaly_no': 'AN_NO_' + str(int(random.random() * 10000000000000)),
                    })

                for _ in range(int(record.data_drill)):
                    drill_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'name': 'CONTRACTOR',
                    })
                for _ in range(int(record.data_training)):
                    training_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(training_types.get('special')),
                    })
                for _ in range(int(record.data_tbm)):
                    training_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(training_types.get('tbm')),
                    })
                for _ in range(int(record.data_induction)):
                    training_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(training_types.get('induction')),
                    })
                for _ in range(int(record.data_ptw)):
                    new_permit = permit_model.create({
                                'record_date': record.data_date,
                                'project': record.project.id,
                                'permit_state': 'close',
                                'permit_no': 'PR_NO_' + str(int(random.random() * 10000000000000)),
                            })
                    new_permit.write({'due_date': record.data_date + timedelta(days=3)})
                for _ in range(int(record.data_Fatality)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('fatality', False)),
                    })
                for _ in range(int(record.data_PTD_PPD)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('ptd&ppd', False)),
                    })
                for _ in range(int(record.data_LTI)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('lti', False)),
                    })
                for _ in range(int(record.data_RWC)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('rwc', False)),
                    })
                for _ in range(int(record.data_MTC)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('fatality', False)),
                    })

                for _ in range(int(record.data_FAC)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('fac', False)),
                    })
                for _ in range(int(record.data_RVA)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('rva', False)),
                    })
                for _ in range(int(record.data_Fire)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('fire', False)),
                    })
                for _ in range(int(record.data_Near_Miss)):
                    incident_model.create({
                        'record_date': record.data_date,
                        'project': record.project.id,
                        'record_type': int(incident_types.get('near miss', False)),
                    })
                record.write({'active': False})

            except Exception as e:
                logging.error(f'sd_hse_import:\n{traceback.format_exc()}')
                print(f'sd_hse_import:\n{traceback.format_exc()}')
                record.write({'description': traceback.format_exc()})

                # raise ValueError(f'sd_hse_import:{e}')
