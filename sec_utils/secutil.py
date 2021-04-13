import subprocess
import sys
import os
import argparse
import string
import random

homedir = os.environ['HOME']

from keychain_utils import set_internet_password, get_internet_password


class UserNamespace(object):
    pass


user_namespace = UserNamespace()
parser = argparse.ArgumentParser(description='Utils')
parser.add_argument('-l', dest='pass_length', type=int, required=False, help="Password length")
parser.add_argument('-p', dest='repo_path', type=str, required=False, help="Repo path")
parser.add_argument('-a', dest='repo_arg', type=str, required=False, help="Repo arg")
parser.add_argument('-rp', dest='replace_arg', type=str, required=False, help="Repo replace arg")
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
        user_input = input("Do you want to save this pass in keychain: y/n\n")
        if user_input.lower() == "y":
            user_name = input("Please add user name: \n")
            service = input("Please add service name: \n")
            set_internet_password(service, user_name, password)
            print("Password saved to keychain")

        elif user_input.lower() == "n":
            print("Password: ", password)
    else:
        print("Could not generate password")


def check_repo_dir():
    proc = subprocess.Popen(
        ['git', 'rev-parse', "--is-inside-work-tree"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    line = proc.stdout.readline()
    print(line.decode("utf-8").rstrip('\r\n')) if type(line) == bytes else print(line)


def get_pass_password():
    """
    Functions that gets passwords from the keychain
    :return:
    """
    service = input("Please enter service\n")
    account = input("Please enter account\n")
    print(get_internet_password(service, account))


def find_str_in_repo():
    """
    Functions checks first if given dir is correct then find string in that repo
    :return:
    """
    repo_path = user_namespace.repo_path
    repo_args = user_namespace.repo_arg
    replace_arg = user_namespace.replace_arg

    if repo_path is None:
        print("Please provide repo directory")
        sys.exit()
    else:
        if not os.path.isdir(repo_path):
            print("-p Incorrect directory")
            sys.exit()
        else:
            if repo_args is None:
                print("Please provide strings to scan in the repo")
                sys.exit()

            os.chdir(repo_path)

            if replace_arg is not None:
                print("Replacing repo: {} for '{}' with '{}\n".format(repo_path, repo_args, replace_arg))
                cmd = "git filter-branch --tree-filter \"find . -type f -not -path '*/\.git/*' -exec sed -i -e 's/{}/{}/g' {{}} \;\"".format(
                    repo_args, replace_arg)

                stream = os.popen(cmd)
                output = stream.read()
                print(output)

                sys.exit()

            print("Scanning repo: {} for '{}'".format(repo_path, repo_args))

            print("")
            stream = os.popen('git --no-pager grep ' + repo_args + ' $(git rev-list --all)')
            output = stream.read()
            print(output)
            if output == "":
                print("Nothing there")
            else:
                print("please add '-rp <replace arg>' at the end of previous command")


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


class FindInRepo(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=None,
                 nargs=0,
                 default=None,
                 required=False,
                 type=None,
                 metavar=None,
                 help=None):
        super(FindInRepo, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help)

    def __call__(self, parser, args, values, option_string=None):
        find_str_in_repo()


class GetFromKeychain(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=None,
                 nargs=0,
                 default=None,
                 required=False,
                 type=None,
                 metavar=None,
                 help=None):
        super(GetFromKeychain, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help)

    def __call__(self, parser, args, values, option_string=None):
        get_pass_password()


parser.add_argument('-g', dest='generate', action=GeneratePassword, type=str, required=False, help="Generate password")
parser.add_argument('-s', dest='scan', action=FindInRepo, type=str, required=False, help="Find strings in repo")
parser.add_argument('-gp', dest='get_pass', action=GetFromKeychain, type=str, required=False,
                    help="Get pass from keychain")

args = parser.parse_args(namespace=user_namespace)


def main():
    # Default behaviour, if not arg passed then display help
    if len(sys.argv) == 1:
        print(parser.format_help())
