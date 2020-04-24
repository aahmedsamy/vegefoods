import os
import shutil

from django.conf import settings

BASE_DIR = settings.BASE_DIR


def check_file_existance(path):
    return os.path.isfile(path)


def check_directory_existance(path):
    return os.path.isdir(path)


def delete_file(paths):
    for path in paths:
        if check_file_existance(path):
            os.remove(path)
        elif check_directory_existance(path):
            shutil.rmtree(path)
        else:
            print("{} is not file or directory!".format(path))
