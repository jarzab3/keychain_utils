################################################################################
# Author: Adam Jarzębak adam@jarzebak.eu
#
# Go to dir where are src files type "sh install.sh"
#
################################################################################

git clone https://github.com/jarzab3/keychain_utils.git

# Install pip package
cd sec_utils && pip3 install -e . --upgrade

cd .. & rm -r sec_utils

echo ""
echo ""
echo "Package secutil installed"
echo ""
echo ""
echo ""

secutil -h
