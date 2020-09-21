"""."""

import zipfile
import pickle

from os.path import isfile
from os import listdir

import pandas as pd

from main.interface.helpers import single_response_from_list


def original_from_file():
    """."""
    def load_pisa_csv():
        return pd.read_csv(
            'pisa2012.csv',
            sep=',', encoding='latin-1', error_bad_lines=False,
            dtype='unicode', index_col=False)

    def load_pisa_zip():
        return pd.read_csv(
            zipfile.ZipFile(
                'pisa2012.csv.zip', 'r').open('pisa2012.csv'),
            sep=',', encoding='latin-1', error_bad_lines=False,
            dtype='unicode', index_col=False)

    def do_load(file_type, function_name):
        print("Reading pisa2012 from", file_type, "file.\n",
              "This may take a few minutes...")
        # pisa = locals()[function_name]()
        pisa = function_name()
        print("Finished loading from", file_type, "file.\n\n")
        return pisa

    if isfile('pisa2012.csv'):
        return do_load('csv', load_pisa_csv)
    if isfile('pisa2012.csv.zip'):
        return do_load('zip', load_pisa_zip)
    raise Exception('Could not load from local csv or zip file.')


def retrieve_save(save_keys=None):
    """."""
    save_keys = ['saved_user_data_', 'saved_user_selections_']

    def pickled_objects_from_file(filename):
        extracted_objects = []
        with (open(filename, "rb")) as open_file:
            while True:
                try:
                    extracted_objects .append(pickle.load(open_file))
                except EOFError:
                    break
        return extracted_objects

    def detect_save_files():
        detected_save_files = []
        for file_name in listdir():
            for base_name in save_keys:
                if base_name in file_name:
                    detected_save_files.append(file_name)
        return detected_save_files

    return pickled_objects_from_file(
        single_response_from_list(detect_save_files()))[0]
