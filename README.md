# keychain_utils

## This utils help

### Additionally, help to save passwords to Keychain using python or command line tool

### Usage

```
usage: secutil [-h] [-l PASS_LENGTH] [-p REPO_PATH] [-a REPO_ARG] [-rp REPLACE_ARG] [-c COMPLEXITY] [-g] [-s]

Utils

optional arguments:
  -h, --help       show this help message and exit
  -l PASS_LENGTH   Password length
  -p REPO_PATH     Repo path
  -a REPO_ARG      Repo arg
  -rp REPLACE_ARG  Repo replace arg
  -c COMPLEXITY    Password complexity: 1 - easy, 2 - medium, 3 - hard
  -g               Generate password
  -s               Find strings in repo
```

## Manual

### Installation

#### Prerequisites

- python3 and pip3
- bash

### Development

1) Install requirements

- pip install -r requirements.txt

2) Go to repo dir then `sec_util`. Compile tool:

`pip3 install -e . --upgrade`

#### How to set applications to automatically launch at boot up

```
Step 1: Open System Preferences.
Step 2: Click Users & Groups.
Step 3: Click Login Items. At the bottom left corner of the window,
click on the lock icon and enter your admin password.
Step 4: Click the ‘+‘ sign and find the Application that you wish to auto-start via the Finde
```

#### Standalone application on mac

[py2app Documentation](https://py2app.readthedocs.io/en/latest/tutorial.html)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](LICENSE)

## Help

[Read output from terminal - tutorial](https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/)


