# -*- coding: utf-8 -*-

import os
import sys

current_dir = os.path.join(os.getcwd(), "python")
sys.path.append(current_dir)

from FlightRadar24 import __version__ as version
from FlightRadar24 import FlightRadar24API
from FlightRadar24.errors import CloudflareError
