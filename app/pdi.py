import os
import subprocess

PDI_PATH = '/root/8.1/data-integration'
PENTAHO_SCRIPTS = '/pentaho'


def run_trafo(name):
#    return subprocess.run([
#        '{}/pan.sh'.format(PDI_PATH),
#        '-file="{}/{}"'.format(PENTAHO_SCRIPTS, name)])

    os.system('{}/pan.sh -file="{}/{}"'.format(PDI_PATH, PENTAHO_SCRIPTS, name))
    return "success"
