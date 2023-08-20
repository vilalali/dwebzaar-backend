# #!/usr/bin/python

# activate_this_file="/home/vilal/venv/bin/activate_this.py"

# with open(activate_this_file) as file:
#     exec(file.read(), dict(__file__=activate_this_file))

# import sys
# sys.path.insert(0, "/home/vilal/ebslab/webzaar-backend")
# from run import app as application

import sys
import site
import os
import logging

venv_path = '/home/vilal/ebslab/webzaar-backend/venvDwebzaar'

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(os.path.join(venv_path, 'lib', 'python%s' % sys.version[:3], 'site-packages'))

sys.path.insert(0, venv_path)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
from run import app as application