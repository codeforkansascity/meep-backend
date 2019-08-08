import re
import os

import pandas as pd
import requests

#shamelessly copied from stack overflow
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={ 'id' : id }, stream=True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


ids = {
    'locations': '1-jn_oDi7zjP-R1NZlM7hLl1o7ZsYKxgB',
    'projects': '19eAtW6hcA3yE0WYK-cOr0UQG_AFaxNT2'
}

def download_to_df(sheet):
    id = ids.get(sheet)
    if id is None:
        raise ValueError('invalid sheet')
    if 'temp' not in os.listdir():
        os.mkdir('temp')
    try:
        filename = f'./temp/{sheet}.csv'
        download_file_from_google_drive(id, filename)
        df = pd.read_csv(filename)
    finally:
        os.remove(filename)
        os.rmdir('temp')
    return df




if __name__ == '__main__':
    locations = download_to_df('locations')
    projects = download_to_df('projects')
