import sys

from kmk_keyboard_user import main

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
