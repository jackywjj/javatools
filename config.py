# coding=utf8
# Debug enviroment
DEBUG = True
# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Define the database
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0401cy@127.0.0.1/cy_qydb'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://cyuser:0831tscy@106.14.94.150/cy_qydb'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0401cy@192.168.1.106/cy_qydb'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0401cy@58.246.116.82/cy_tools'

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "mkoiujnbhyt"

# Secret key for signing cookies
SECRET_KEY = "adfljojweo82s93479hf"

RECORD_PER_PAGE = 30

PAGE_TITLE = "Java Tools"
PAGE_KEYWORKDS = "Java Tools"
