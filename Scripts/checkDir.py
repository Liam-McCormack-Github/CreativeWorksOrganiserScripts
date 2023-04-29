from os.path import isdir, abspath, dirname, basename
from os import makedirs


def checkDir(dir_name):
    test_dir_exist = isdir(dir_name)
    if not test_dir_exist:
        makedirs(dir_name)
        log = f'Created : {dir_name}'
    else:
        log = f'Found   : {dir_name}'
    return str(basename(abspath(__file__))), log


if __name__ == '__main__':
    checkDir(dirname(abspath(__file__)))
