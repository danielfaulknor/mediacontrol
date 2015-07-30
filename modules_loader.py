"""
    SingularityHA Modules Loader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
import os
import signal
import sys
import time
from multiprocessing import Process
import logging


def main():
    """
        Start up logger for this module and then loop through
            all the modules and fire them up in a multi-threaded
            fashion.
    """
    logger = logging.getLogger(__name__)
    logger.info("Loading modules...")
    jobs = []
    for root, dirs, files in os.walk('modules'):
        for dir in dirs:
            logger.debug("Loading module: " + dir)
            module = getattr(__import__("modules." + dir), dir)
            func = getattr(module, "main", None)
            if func:
                p = Process(target=func)
                jobs.append(p)
                p.start()
        dirs[:] = []  # don't recurse into directories.

    def signal_handler(signal, frame):
        logger.info("Got CTL+C")
        for job in jobs:
            job.terminate()
            job.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

