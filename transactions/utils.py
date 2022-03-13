from typing import Iterable


def can_add_device_name(existing_device_names: Iterable[str], new_device_name: str):
    """
    Verify if the device with display_name `name` can be added to the session with 
    device names `existing_device_names`.
    Note that there shouldn't be two devices with names such as 'username1' and 'Username1'
    """
    device_names_dict_list = [
        {'lower_name': name.lower(), 'og_name': name} \
        for name in existing_device_names
    ]

    for entry in device_names_dict_list:
        # If name is already taken, return False and the conflicting name
        if new_device_name.lower() == entry['lower_name']:
            return False, entry['og_name']
    
    return True, ''

