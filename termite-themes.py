import argparse
import sys


def run_argparse() -> argparse.Namespace:
    """ wrap argparse configuration """
    parser = argparse.ArgumentParser()
    return parser.parse_args()


def printerr(*args, **kwargs):
    """ print() but to stderr """
    print(*args, file=sys.stderr, **kwargs)


def main():
    """ main function """
    args: argparse.Namespace = run_argparse()


if __name__ == '__main__':
    main()

