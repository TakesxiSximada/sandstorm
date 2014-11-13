# -*- coding: utf-8 -*-
import sys
import argparse


def main(argv=sys.argv[1:]):  # pragma: no cover
    parser = argparse.ArgumentParser()
    opts = parser.parse_args(argv)
    if opts:
        return


if __name__ == '__main__':  # pragma: no cover
    main()
