#!/usr/bin/env python3

import argparse
from havamal.core import format, default_mapping
from os.path import exists

def handle_cmd():
    parser = argparse.ArgumentParser(description="LDIF to CSV formatter... \n(CSV fully double-quotted, comma separated, UTF-8 encoded, with header)")
    parser.add_argument("infile_path", help="Infile LDIF path")
    parser.add_argument("outfile_path", help="Outfile CSV path")
    parser.add_argument("mapper_file", help="Path to mapper file")

    args = parser.parse_args()

    try:
        verify_path_exists(args.infile_path)
        verify_path_exists(args.mapper_file)
    except CMDException as e:
        print(e.message)

    try:
        protect_existent_path(args.outfile_path)
    except CMDException as e:
        print(e.message)
        overwrite_cli()

    format(args.infile_path, args.outfile_path, args.mapper_file)

def generate_default_mapping():
    parser = argparse.ArgumentParser(description="LDIF to CSV formatter... \nDefault Mapper file generator")
    parser.add_argument("infile_path", help="Infile LDIF path")
    parser.add_argument("mapper_file", help="Path to mapper file")

    args = parser.parse_args()

    try:
        verify_path_exists(args.infile_path)
    except CMDException as e:
        print(e.message)

    try:
        protect_existent_path(args.mapper_file)
    except CMDException as e:
        print(e.message)
        overwrite_cli()

    default_mapping(args.infile_path, args.mapper_file)


def overwrite_cli():
    resp = input("Do you want to overwrite ? (Y/N)")
    if resp == "Y":
        pass
    elif resp == "N":
        exit()
    else:
        overwrite_cli()


def protect_existent_path(path_to_protect):
    if exists(path_to_protect):
        raise CMDException("File already existant : {}".format(path_to_protect))


def verify_path_exists(path_to_verify):
    if not exists(path_to_verify):
        raise CMDException("Invalid Path : {}".format(path_to_verify))


class CMDException(Exception):
    pass


if __name__ == '__main__':
    handle_cmd()
