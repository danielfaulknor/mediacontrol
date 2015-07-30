"""
    SingularityHA Config
    ~~~~~~~~~~~~~~~~~~~~

    Imports configuration file and makes it available to modules that import
    this file

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
import ConfigParser
import os

config = ConfigParser.RawConfigParser()
config.read(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/config.ini')
