#!/usr/bin/python3

import os.path
TOOLS_PATH = os.path.dirname(__file__)
UMLFRI2_PATH = os.path.join(TOOLS_PATH, "..", "..")
LOCALE_PATH = os.path.join(UMLFRI2_PATH, "data", "locale")


import sys
sys.path.append(os.path.join(TOOLS_PATH, '..', '..'))

import subprocess
from umlfri2.application import Application

xgettext = subprocess.Popen(['xgettext', '-f-', '-o', os.path.join(LOCALE_PATH, 'umlfri2.pot'), '-s', '--no-location',
                             '--package-name={0}'.format(Application().about.name),
                             '--package-version={0}'.format(Application().about.version),
                             '--from-code=UTF-8'],
                            stdin=subprocess.PIPE)

DIR = os.path.join(UMLFRI2_PATH, 'umlfri2')

for dirpath, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(dirpath, file)
            xgettext.stdin.write(path.encode(sys.getdefaultencoding()) + b'\n')

xgettext.stdin.close()
