#!/usr/bin/env python


import yaml
import sys
import json
import os
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
nginx_dir = "/etc/nginx/sites-enabled/"


# Function defs
def remove_php_fpm_pool(user_name):
    """Remove the php-fpm pools of deleted accounts"""
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for php_path in list(php_backends_dict.values()):
            phppool_file = php_path + "/etc/fpm.d/" + user_name + ".conf"
            if os.path.isfile(phppool_file):
                fhandle.write(phppool_file)
                subprocess.call("kill -USR2 `cat " + php_path + "/var/run/php-fpm.pid`", shell=True)
    return



cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]
if os.path.isfile(installation_path+"/lock/todel_"+cpaneluser):
    fhandle = open(installation_path+"/lock/todel_"+cpaneluser,'r')
    mylines = fhandle.read().splitlines()
    for line in mylines:
        os.remove(line)
    fhandle.close()
    os.remove(installation_path+"/lock/todel_"+cpaneluser)
if cpaneluser != cpanelnewuser:    
    remove_php_fpm_pool(cpaneluser)
subprocess.call("/usr/sbin/nginx -s reload", shell=True)
subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
print(("1 nDeploy:postmodify:"+cpanelnewuser))
