import sys, os

def dispatch(arguments=None):
    if arguments is None or len(arguments) != 2:
        raise Exception('Must have 2 parameters')
    
    if arguments[0] == 'script':
        run_script(arguments[1])
    else:
        raise Exception('Unknown command')

def run_script(name):
    try:
        exec(f'from scripts import {name}')
    except ImportError:
        raise Exception(f'Unknown script "{name}"')
        
    exec(f'{name}.main()')

if __name__ == '__main__':
    dispatch(sys.argv[1:])