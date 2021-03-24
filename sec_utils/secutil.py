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
parser.add_argument('-c', dest='complexity', type=int, required=False,
                    help="Password complexity: 1 - easy, 2 - medium, 3 - hard")
parser.parse_known_args(namespace=user_namespace)


def generate_easy_pass(pass_length):
    return ''.join(random.sample(string.ascii_lowercase, pass_length))


def generate_medium_pass(pass_length):
    source = string.ascii_letters + string.digits
    return ''.join((random.choice(source) for i in range(pass_length)))


def generate_hard_pass(pass_length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(pass_length))


def validate_complexity_arg():
    pass_complexity = user_namespace.complexity
    if pass_complexity is not None:
        if pass_complexity not in [1, 2, 3]:
            print("Bad complexity argument\n")
            print(parser.format_help())
            sys.exit()
        return pass_complexity
    return False


def generate_password():
    pass_complexity = validate_complexity_arg()
    pass_length = user_namespace.pass_length
    password = None
    if not pass_length:
        pass_length = 20

    if pass_complexity == 1:
        password = generate_easy_pass(pass_length)
    elif pass_complexity == 2:
        password = generate_medium_pass(pass_length)
    elif pass_complexity == 3:
        password = generate_hard_pass(pass_length)

    else:
        password = generate_medium_pass(pass_length)

    if password:
        print("Password: ", password)
    else:
        print("Could not generate password")


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
