import json
import os


def _get_settings_dir():
    current_dir = os.path.abspath(__file__).split('/')
    relativ_dir = 'settings/io_devices.json'
    current_dir = current_dir[:-2]
    current_dir.append(relativ_dir)
    settings_dir = '/'.join(current_dir)
    return settings_dir


class DevicesIO:
    path = _get_settings_dir()

    def __init__(self):
        with open(self.path, "r") as read_file:
            self.data = json.load(read_file)

    def __str__(self):
        return str(self.data)

    def write_to_disc(self):
        with open(self.path, "w") as write_file:
            json.dump(self.data, write_file)

    def set_input(self, value):
        self.data['input'] = value
        self.write_to_disc()

    def set_output(self, value):
        self.data['output'] = value
        self.write_to_disc()

    def get_input(self):
        return self.data['input']

    def get_output(self):
        return self.data['output']

    def set_default(self):
        for key in self.data.keys():
            self.data[key] = None
            self.write_to_disc()
