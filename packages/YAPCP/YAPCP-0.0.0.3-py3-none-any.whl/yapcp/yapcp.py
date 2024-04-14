import subprocess
import platform

def setupdevtools():
    plf = platform.system()
    if plf == 'Linux':
        subprocess.call(['bash', './instsyspkg.sh'])
    else:
        print(plf, "is not supported")

def setupothertools():
    plf = platform.system()
    if plf == 'Linux':
        subprocess.call(['bash', './instotherpkg.sh'])
    else:
        print(plf, "is not supported")
