import os
from datetime import datetime


def name_generate():
    now = datetime.now()
    str_date = now.strftime('%m-%d-%Y_%H:%M:%S')
    return f'record_{str_date}.flac'


def default_path():
    current_dir = os.path.abspath(__file__).split('/')
    relativ_dir = 'records/' + name_generate()
    current_dir = current_dir[:-2]
    current_dir.append(relativ_dir)
    settings_dir = '/'.join(current_dir)
    return settings_dir
