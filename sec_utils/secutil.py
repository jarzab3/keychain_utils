import sys
import os
import argparse
import secrets
import string

homedir = os.environ['HOME']


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    print(password)


class GeneratePassword(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=None,
                 nargs=0,
                 default=None,
                 required=False,
                 type=None,
                 metavar=None,
                 help=None):
        super(GeneratePassword, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help)

    def __call__(self, parser, args, values, option_string=None):
        generate_password()


class UserNamespace(object):
    pass


user_namespace = UserNamespace()
parser = argparse.ArgumentParser(description='Utils')

parser.add_argument('-g', dest='generate', action=GeneratePassword, type=str, required=False, help="Generate password")
args = parser.parse_args(namespace=user_namespace)


def main():
    # Default behaviour, if not arg passed then display help
    if len(sys.argv) == 1:
        print(parser.format_help())
