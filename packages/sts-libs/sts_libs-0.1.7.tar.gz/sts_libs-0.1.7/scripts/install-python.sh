#!/bin/bash

python3_version=$(python3 -V | cut -d . -f 2)
required_version=9


if [[ $python3_version -lt $required_version ]]; then
    dnf install -y python39-pip
    alternatives --set python3 /usr/bin/python3.9
fi
