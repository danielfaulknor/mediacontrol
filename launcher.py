#!/usr/bin/env python
"""
    SingularityHA Launcher
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
import modules_loader
import logging


def main():
    """ Fire up logger and then call the modules loader """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    modules_loader.main()

if __name__ == "__main__":
    main()
