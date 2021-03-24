import sys
import os
import argparse
import string
import random

homedir = os.environ['HOME']


class UserNamespace(object):
    pass


user_namespace = UserNamespace()
parser = argparse.ArgumentParser(description='Utils')
parser.add_argument('-l', dest='pass_length', type=int, required=False, help="Password length")
parser.parse_known_args(namespace=user_namespace)


def generate_password():
    pass_length = user_namespace.pass_length
    if not pass_length:
        pass_length = 20

    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(pass_length))
    print("Pass is: ", password)


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


parser.add_argument('-g', dest='generate', action=GeneratePassword, type=str, required=False, help="Generate password")
args = parser.parse_args(namespace=user_namespace)


def main():
    # Default behaviour, if not arg passed then display help
    if len(sys.argv) == 1:
        print(parser.format_help())
