import sys, os

def run(arguments=None):
    if arguments is None or len(arguments) <2:
        raise Exception('Must have 2 parameters')
    
    if arguments[0] != 'script':
        raise Exception('Uknow command')
    else:
        run_script(arguments[1])

def run_script(name):
    exec(f'from scripts import {name}')
    exec(f'{name}.main()')

if __name__ == '__main__':
    run(sys.argv[1:])