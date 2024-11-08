import sys


def function_with_breakpoint():
    print('calling function with breakpoint')
    x = 5
    breakpoint()
    x = 7
    print('after breakpoint')


def function_with_exception():
    print('calling function with exception')
    x = 5
    raise RuntimeError('Some error occured')
    x = 7
    print('after exception')


def function_with_caught_exception():
    print('calling function with exception')
    x = 5
    try:
        raise RuntimeError('Some error occured')
    except RuntimeError:
        print('RuntimeError was caught')
    x = 7
    print('after exception')


def run_program():
    try:
        mode = sys.argv[1]
    except IndexError:
        print('Please specify mode')
        return        

    print('entering main program')
    if mode == '-b':
        function_with_breakpoint()
    elif mode == '-e':
        function_with_exception()
    elif mode == '-x':
        function_with_caught_exception()
    else:
        print(f'unknown mode {mode}')


if __name__ == '__main__':
    run_program()
