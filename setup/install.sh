#!/bin/bash

# Update apt repository
apt update
# Install required packages
apt install unzip python3-pip python3-dev build-essential libssl-dev libffi-dev xvfb -y
# Upgrade pip and setuptools
pip3 install --upgrade pip setuptools
# Move to user's home folder
cd ~
# Clone chrome debian package
wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
# Install chrome
dpkg -i google-chrome-stable_current_amd64.deb
# Install chrome dependencies
apt install -y -f
# Delete installation file
rm google-chrome-stable_current_amd64.deb
# Fix pip3 error
echo -ne '#!/usr/bin/python3\nimport sys\nfrom pip import __main__\nif __name__ == "__main__":\n  sys.exit(__main__._main())\n' > /usr/bin/pip3
# Install instapy
pip3 install instapy --ignore-installed
