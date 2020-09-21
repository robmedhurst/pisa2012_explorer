"""."""

import pickle

from os.path import isfile

from graphics.graphics import close_figures
from main.interface.helpers import multi_responses_from_list


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
