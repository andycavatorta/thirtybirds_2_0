#!/bin/bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install git
brew install wget
brew install python
sudo pip install pyyaml
wget https://pypi.python.org/packages/a7/4c/8e0771a59fd6e55aac993a7cc1b6a0db993f299514c464ae6a1ecf83b31d/netifaces-0.10.5.tar.gz#md5=5b4d1f1310ed279e6df27ef3a9b71519 --no-check-certificate
tar xvzf netifaces-0.10.5.tar.gz
cd netifaces-0.10.5
python setup.py install
cd
sudo pip install mido
brew instal portmidi
sudo pip install python-rtmidi
sudo pip install pyzmq