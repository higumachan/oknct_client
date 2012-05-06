import sys
sys.path.append('/home/dotcloud/current')

from app import app as application
from flask import *

#application = Flask(__name__);
#app = application;

#@app.route("/")
#def index():
#    return ("Hello");

if __name__ == "__main__":
    application.debug = True;
    application.run()
