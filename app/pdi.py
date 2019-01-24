import os
import subprocess

PDI_PATH = '/root/8.1/data-integration'
PENTAHO_SCRIPTS = '/pentaho'


def run_trafo(name):
    os.system('{}/pan.sh -file="{}/{}.ktr"'.format(PDI_PATH, PENTAHO_SCRIPTS, name))
    return True


def run_job(name, _param=None):
    if _param:
        os.system(('{}/kitchen.sh -file="{}/{}.kjb" -param:{}')
            .format(PDI_PATH, PENTAHO_SCRIPTS, name, _param))
    else:
        os.system('{}/kitchen.sh -file="{}/{}.kjb"'.format(PDI_PATH, PENTAHO_SCRIPTS, name))
    return True
