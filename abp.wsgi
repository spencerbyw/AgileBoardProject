import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/abp/")
sys.path.insert(0,"/var/www/abp/abp")

from abp import app as application
application.secret_key = 'Add your secret key'
