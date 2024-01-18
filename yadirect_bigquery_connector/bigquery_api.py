from google.cloud import bigquery
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BigQuery:
    SERVICE_KEY = 'braided-tracker-408113-cdf2eba3dbf1.json'
    PATH_SERVICE_KEY = os.path.join(BASE_DIR, SERVICE_KEY)

    def __init__(self, df_origin):
        self.df_origin = df_origin

    def bigquery_uploader(self):
        client = bigquery.Client.from_service_account_json(self.PATH_SERVICE_KEY)
        dataset_ref = client.dataset('DirectClients')
        dataset = bigquery.Dataset(dataset_ref)

        try:
            dataset_create = client.create_dataset(dataset)

        except Exception as error:
            print('Датасет уже существует.')

        finally:
            table_ref = dataset_ref.table('Report')
            result = client.load_table_from_dataframe(self.df_origin, table_ref).result()
            print('Данные загружены')

