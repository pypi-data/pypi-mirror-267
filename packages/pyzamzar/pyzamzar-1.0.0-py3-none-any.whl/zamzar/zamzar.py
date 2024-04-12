import requests
from requests.auth import HTTPBasicAuth


class ZamzarClient:
    def __init__(self, api_key, sandbox=False) -> None:
        self.api_key = api_key
        if sandbox:
            self.BASE_URL = "https://sandbox.zamzar.com/v1"
        else:
            self.BASE_URL = "https://api.zamzar.com/v1"

    def start_conversion_job(self, source_file, target_format):
        endpoint = f'{self.BASE_URL}/jobs'
        file_content = {'source_file': open(source_file, 'rb')}
        data_content = {'target_format': target_format}
        response = requests.post(
            endpoint, files=file_content, data=data_content,
            auth=HTTPBasicAuth(self.api_key, ''))
        return response.json()

    def get_job_status(self, job_id):
        endpoint = f'{self.BASE_URL}/jobs/{job_id}'
        response = requests.get(endpoint, auth=HTTPBasicAuth(self.api_key, ''))
        return response.json()

    def download_converted_file(self, file_id, save_as):
        endpoint = f'{self.BASE_URL}/files/{file_id}/content'
        response = requests.get(
            endpoint, stream=True, auth=HTTPBasicAuth(self.api_key, ''))
        with open(save_as, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
                f.flush()
        endpoint = f'{self.BASE_URL}/files/{file_id}'
        requests.delete(endpoint, auth=HTTPBasicAuth(self.api_key, ''))
