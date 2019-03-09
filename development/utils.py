from os import listdir
from os.path import isfile, join

def list_all_files(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print(onlyfiles)
    return onlyfiles

def is_machine_generated(pdf_path: str) -> bool:
    return False
