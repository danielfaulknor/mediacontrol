#!/usr/bin/env python
"""
    SingularityHA Setup
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014- by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
from git import Repo
import json
import os
import requests
import shutil
import socket
import sys
from lib import state
from lib.config import config

root = config.get("general", "path")

""" Pull in list of modules from the config server """
payload = {'format': 'json', 'server__name': socket.gethostname()}  # Generate payload for request
r = json.loads(requests.get("http://" + config.get("general", "confighost") + "/api/v1/module/", params=payload).text)

""" Loop through returned results and grab core module data """
modules = {}
for module in r['objects']:  # Loop through modules the server says we should have
    payload = {'format': 'json', 'name': module['name']}
    moduleData = json.loads(
        requests.get("http://" + config.get("general", "confighost") + "/api/v1/module_list/", params=payload).text)[
        'objects'][0]  # Pull config options and build a modules list
    modules[module['id']] = {"name": module['name'], "package": moduleData["package"], "config": module["config"]}

""" Get list of currently installed modules so we can remove ones that have been removed """
module_dir = []
for root, dirs, files in os.walk('modules'):
    for dir in dirs:
        module_dir.append(dir)
    dirs[:] = []  # don't recurse into directories.

""" Run various operations to install modules """
modules_list = ""
for moduleID, moduleInfo in modules.iteritems():
    try:
        Repo.clone_from(moduleInfo['package'], "modules/" + str(moduleInfo['name']))  # Install the module from git
    except:
        print "Error cloning " + str(moduleInfo['name'])
    module = str(moduleInfo['name'])

    """ Import config for the module if it exists """
    if moduleInfo['config']:
        configSplit = moduleInfo['config'].split("\r\n")
	print configSplit
        try:
            config.add_section(module)
        except:
            pass
	for configLine in configSplit:
		configSplitNow = configLine.split("=")
	        config.set(module, str(configSplitNow[0]).strip(), configSplitNow[1])

    """ Write out an ID to the module folder for it's own setup to use """
    target = open("modules/" + module + "/id.txt", 'w')
    target.write(str(moduleID))
    target.close()

    """ Exec the module's own setup file """
    script = os.path.join(root, module, "setup.py")
    if os.path.isfile(script):
        g = globals().copy()
        g['__file__'] = script
        execfile(script, g)

    """ Remove from "to be removed" list """
    try:
	module_dir.remove(moduleInfo['name'])
    except:
        pass

""" Drop old modules """
for path in module_dir:
	shutil.rmtree("modules/" + path)

""" Write out config file with new module options """
with open(os.path.dirname(os.path.realpath(__file__)) + '/config.ini', 'wb') as configfile:
    config.write(configfile)

