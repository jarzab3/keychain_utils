import csv
import re
import os

csv_path = "path_passwords.csv"


def read_data_from_csv():
    data = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            addr = row[5]
            comm = row[6]
            user = row[1]
            password = row[2]
            dat = [addr, user, password, comm]
            data.append(dat)
    return data


def get_generic_password(service, account):
    def decode_hex(s):
        s = eval('"' + re.sub(r"(..)", r"\x\1", s) + '"')
        if "" in s: s = s[:s.index("")]
        return s

    cmd = ' '.join([
        "/usr/bin/security",
        " find-generic-password",
        "-g -s '%s' -a '%s'" % (service, account),
        "2>&1 >/dev/null"
    ])
    p = os.popen(cmd)
    s = p.read()
    p.close()
    m = re.match(r"password: (?:0x([0-9A-F]+)\s*)?\"(.*)\"$", s)
    if m:
        hexform, stringform = m.groups()
        if hexform:
            return decode_hex(hexform)
        else:
            return stringform


def get_internet_password(service, account):
    def decode_hex(s):
        s = eval('"' + re.sub(r"(..)", r"\x\1", s) + '"')
        if "" in s: s = s[:s.index("")]
        return s

    cmd = ' '.join([
        "/usr/bin/security",
        " find-internet-password",
        "-g -s '%s' -a '%s'" % (service, account),
        "2>&1 >/dev/null"
    ])
    p = os.popen(cmd)
    s = p.read()
    p.close()
    m = re.match(r"password: (?:0x([0-9A-F]+)\s*)?\"(.*)\"$", s)
    if m:
        hexform, stringform = m.groups()
        if hexform:
            return decode_hex(hexform)
        else:
            return stringform


def set_generic_password(service, account, password):
    cmd = 'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()


def set_internet_password(service, account, password, comment=""):
    cmd = "security add-internet-password -U -a '%s' -s '%s' -w '%s' -r http -j 'LastPass   ---  %s'" % (
        account, service, password, comment)
    p = os.popen(cmd)
    s = p.read()
    p.close()


def import_from_csv_to_keychain():
    data = read_data_from_csv()

    for i, entry in enumerate(data):
        set_internet_password(*entry)


if __name__ == '__main__':
    import_from_csv_to_keychain()
    # print(get_internet_password("", ""))
