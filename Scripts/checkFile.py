from os.path import isfile, abspath, basename


def checkFile(file_name, file_content=''):
    test_file_exist = isfile(file_name)
    if not test_file_exist:
        file = open(file_name, 'w')
        file.write(file_content)
        file.close()
        log = f'Created : {file_name}'
    else:
        log = f'Found   : {file_name}'
    return str(basename(abspath(__file__))), log


if __name__ == '__main__':
    checkFile(abspath(__file__))
