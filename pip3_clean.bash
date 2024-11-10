#!/bin/bash

pip3 freeze | grep -v "^\(pip\|setuptools\|wheel\)" | xargs pip3 uninstall -y
