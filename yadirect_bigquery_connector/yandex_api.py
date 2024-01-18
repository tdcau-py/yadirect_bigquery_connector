import json
from time import time
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from requests import Response
from bigquery_api import BigQuery


load_dotenv('.env')


class YaDirectApi:
    API_TOKEN = os.getenv('YA_DIRECT_TOKEN')
    AGENCY_CLIENTS = 'https://api.direct.yandex.com/json/v5/agencyclients'
    REPORTS = 'https://api.direct.yandex.com/json/v5/reports'
    RESULT_CSV = 'ClientLogin;Impressions;Clicks;Ctr;Conversions\n'

    @property
    def header(self):
        return {
            'Authorization': f'Bearer {self.API_TOKEN}',
            'Accept-Language': 'ru',
        }

    @property
    def agency_body(self):
        return {
                'method': 'get',
                'params': {
                    'SelectionCriteria': {
                        'Archived': 'NO'
                    },
                    'FieldNames': ['Login'],
                    'Page': {
                        'Limit': 10000,
                        'Offset': 0
                    }
                }
            }

    @property
    def reports_body(self):
        return {
            'params': {
                'SelectionCriteria': {
                    'DateFrom': '2022-01-01',
                    'DateTo': '2023-12-28'
                },
                'FieldNames': [
                    'ClientLogin',
                    'Impressions',
                    'Clicks',
                    'Ctr',
                    'Conversions',
                    'Cost',
                ],

                'ReportName': 'ACCOUNT_PERFORMANCE_test',
                'ReportType': 'ACCOUNT_PERFORMANCE_REPORT',
                'Format': 'TSV',
                'DateRangeType': 'CUSTOM_DATE',
                'IncludeVAT': 'NO',
                'IncludeDiscount': 'NO'
            }
        }

    def get_clients(self):
        agency_body = self.agency_body
        has_all_client_logins_received = False
        client_list = []
        clients = None

        while not has_all_client_logins_received:
            response: Response = requests.post(self.AGENCY_CLIENTS, data=json.dumps(agency_body), headers=self.header)

            if response.json():
                clients = response.json()['result']

            for client in clients['Clients']:
                client_list.append(client['Login'])

            if response.json()['result'].get('LimitedBy', False):
                agency_body['Page']['Offset'] = clients['LimitedBy']

            else:
                has_all_client_logins_received = True

        return client_list

    def get_client_statistics(self):
        clients = self.get_clients()
        headers = self.header

        headers['skipReportHeader'] = 'true'
        headers['skipColumnHeader'] = 'true'
        headers['skipReportSummary'] = 'true'
        headers['returnMoneyInMicros'] = 'false'

        filename = 'TestReport_{}.tsv'.format(str(time()))

        for client in clients:
            headers['Client-Login'] = client
            body = json.dumps(self.reports_body, indent=4)
            response = requests.post(self.REPORTS, data=body, headers=headers)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                if response.text != '':
                    tempresult = response.text.split('\t')
                    self.RESULT_CSV += '{};{};{};{};{}\n'.format(
                        tempresult[0], tempresult[1], tempresult[2], tempresult[3], tempresult[4]
                    )

                else:
                    self.RESULT_CSV += '{};0;0;0;0\n'.format(client)

            else:
                print(response.text)

        with open(filename, 'a', encoding='utf-8') as resultfile:
            resultfile.write(self.RESULT_CSV)

        return pd.read_csv(filename, sep='\t')


def main():
    api = YaDirectApi()
    df_origin = api.get_client_statistics()
    bigquery_upload = BigQuery(df_origin)
    bigquery_upload.bigquery_uploader()


if __name__ == '__main__':
    main()
