import os, sys

print('Initializating scripts')

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from package.module import foo

def main():
    print(foo())

if __name__ == '__main__':
    main()


