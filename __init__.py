import os
import site
os.system('sudo cp -ru ./rpi '+site.getsitepackages()[0])

import os
import subprocess
cwd = os.getcwd()

try:
    with open('/sys/firmware/devicetree/base/model', 'r') as file:
        info = file.read()
        if "Raspberry" in info:
            is_rpi = True
        else:
            raise
except Exception:
    raise
