#! /usr/bin/python3.8

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/Yogapose/')
from run import app as application

