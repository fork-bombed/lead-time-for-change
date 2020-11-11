"""
Very bad python code used for setup testing
"""

__author__ = "Testing"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    """ Main entry point of the app """
    print("hello world")
    if 1:
        try:
            print(int("hello"))
        except:
            pass
        print(3)
    else:
        pass


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()