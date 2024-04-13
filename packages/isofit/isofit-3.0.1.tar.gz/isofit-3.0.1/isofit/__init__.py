#! /usr/bin/env python
#
#  Copyright 2018 California Institute of Technology
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# ISOFIT: Imaging Spectrometer Optimal FITting
# Author: David R Thompson, david.r.thompson@jpl.nasa.gov
#         Philip G Brodrick, philip.brodrick@jpl.nasa.gov
#


### Variables ###
import importlib.metadata

__version__ = importlib.metadata.version(__package__ or __name__)

warnings_enabled = False

import atexit
import logging
import os
import signal

Logger = logging.getLogger("isofit")

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get("ISOFIT_DEBUG"):
    Logger.info("Using ISOFIT internal ray")
    from .wrappers import ray
else:
    import ray


def shutdown_ray():
    try:
        ray.shutdown()
    except:
        pass


# Auto call ray.shutdown when the python interpreter exits
# ray itself also implements this, but there's no harm in calling it twice
atexit.register(shutdown_ray)
try:
    signal.signal(signal.SIGINT, shutdown_ray)  # ctrl
    signal.signal(signal.SIGTERM, shutdown_ray)  # kill
except:
    pass
