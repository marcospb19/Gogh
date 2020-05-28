import argparse


def run_argparse() -> argparse.Namespace:
    """ wrap argparse configuration """
    parser = argparse.ArgumentParser()
    return parser.parse_args()


def main():
    """ main function """
    args: argparse.Namespace = run_argparse()


if __name__ == '__main__':
    main()

