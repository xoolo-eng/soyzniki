import os
import sys
sys.path.append('/var/www/django/venv/lib/python3.5/site-packages')
sys.path.append('/var/www/django/soyzniki')
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soyzniki.settings")
application = get_wsgi_application()
