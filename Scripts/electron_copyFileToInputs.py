from shutil import copy
from os.path import isfile, basename, join
from constants import input_dir
from sys import argv, stdout


def copyFileToInputs():
    file = argv[1]
    if isfile(file):
        copy(file, join(input_dir, basename(file)))
        print('File Copied')
    else:
        print('Error File not found!')
    stdout.flush()


if __name__ == '__main__':
    copyFileToInputs()
