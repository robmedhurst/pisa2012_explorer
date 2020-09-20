"""."""

import zipfile
import pickle

from os.path import isfile
from os import listdir

import pandas as pd

from ui.ui import multi_responses_from_list
from ui.ui import single_response_from_list
from graphics.graphics import close_figures


def load_original_from_file():
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


def request_delivery(user_data):
    """."""
    # Helper functions
    #
    def rip_lanes(application):
        for key in user_data.keys():
            if 'graphic_objects' in key:
                for group in user_data[key].values():
                    for graphic in group.values():
                        if graphic is not None:
                            application(graphic)

    def save_pickle_next_location(selection, base_name):
        def get_next_save_location():
            save_num = 0
            while isfile(base_name + "_" + str(save_num).zfill(3)):
                save_num += 1
            return base_name + "_" + str(save_num).zfill(3)

        with open(get_next_save_location(), "wb") as open_file:
            pickle.dump(selection, open_file)

    # Delivery functions
    #
    def do_display_figures():
        def do_display_figure(graphic):
            graphic.seek(0)
            pickle.load(graphic)
            # graphic.show()
        rip_lanes(do_display_figure)

    # def do_store_pickles():
    #     def do_store_pickle(graphic):
    #         file_name = str(graphic)[-9:-1]
    #         with open(file_name, "wb") as open_file:
    #             open_file.write(graphic.getbuffer())
    #     rip_lanes(do_store_pickle)

    # def do_store_images():
    #     def do_store_image(graphic):
    #         graphic.seek(0)
    #         pickle.load(graphic).savefig(str(graphic)[-9:-1] + ".png")
    #     rip_lanes(do_store_image)

    # def do_display_images():
    #     # TODO: OS display
    #     from PIL import Image

    #     def do_display_image(graphic):
    #         file_name = str(graphic)[-9:-1] + ".png"
    #         graphic.seek(0)
    #         pickle.load(graphic).savefig(file_name)
    #         image = Image.open(file_name)
    #         image.show()
    #     rip_lanes(do_display_image)

    def do_big_pickle():
        selection = user_data
        save_pickle_next_location(selection, "saved_user_data")

    def do_little_pickle():
        desired_keys = [
            'dependent_groups',
            'group_category_matches',
            'independent_groups',
            'response_trackers',
            'sample_size']
        selection = {
            k: user_data[k] for k in user_data.keys() if k in desired_keys}
        save_pickle_next_location(selection, "saved_user_selections")

    def do_statistics():
        def do_description(target):
            for group_name, variables in user_data[target].items():
                print("\n")
                print("Group name: ", group_name)
                print("Group category: ",
                      user_data['group_category_matches'][target][group_name])
                print(user_data['pisa_sample'][variables].describe())

        print("\n\n")
        print("'Independent Groups:'")
        do_description('independent_groups')
        print("\n\n")
        print("'Dependent Groups:'")
        do_description('dependent_groups')

    # User selection options and corresponding functions
    #
    delivery_options = [
        'Display figures through backend',
        # 'Save all figures to file as BytesIO Objects',
        # 'Save all figures to file as images',
        # 'Display figures as images through OS.',
        'Pickle and save all user_data to a single file',
        'Pickle and save user selections to a single file',
        'Display pandas descriptive statistics'
        ]
    delivery_functions = [
        do_display_figures,
        # do_store_pickles,
        # do_store_images,
        # do_display_images,
        do_big_pickle,
        do_little_pickle,
        do_statistics
        ]

    # Action
    #
    print("\n-Delivery Options-")
    for user_request in multi_responses_from_list(delivery_options):
        delivery_functions[delivery_options.index(user_request)]()
    close_figures()
    return user_data
