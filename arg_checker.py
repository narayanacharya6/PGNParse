import os

def dir_path(string):
    script_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(script_dir, string))