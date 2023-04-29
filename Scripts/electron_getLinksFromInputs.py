from sys import argv, stdout
from getLinksFromInputs import getLinksFromInputs
from insertLinksIntoDB import insertLinksIntoDB


def electron_getLinksFromInputs():
    for x in argv:
        print(f'Python : {x}')
    func1 = getLinksFromInputs()
    func2 = insertLinksIntoDB()
    print(f'Python : input file found : {func1}')
    print(f'Python : temp file found : {func2}')
    stdout.flush()


if __name__ == '__main__':
    electron_getLinksFromInputs()
