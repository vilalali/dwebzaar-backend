# #!/usr/bin/python
# import sys
# import os
# import logging

# venv_path = '/var/www/html/public_html/webzaar-server'
# activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

# with open(activate_this) as file_:
#     exec(file_.read(), {'__file__': activate_this})

# sys.path.insert(0, "/var/www/html/public_html/webzaar-server")
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
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