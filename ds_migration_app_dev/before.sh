#!/bin/bash
sudo yum install python3.7
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip --version