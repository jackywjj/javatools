# Import flask and libs
from flask import Flask, render_template
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('config')
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# HTTP 404
# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.controllers.dashboard_controller import dashboard_controller as dashboard_controller_module
from app.controllers.java_controller import java_controller as java_controller_module
from app.controllers.redeem_controller import redeem_controller as redeem_controller_module
from app.controllers.system_controller import system_controller as system_controller_module
from app.controllers.chart_controller import chart_controller as chart_controller_module
from app.controllers.dbdoc_controller import dbdoc_controller as dbdoc_controller_module
from app.controllers.json_controller import json_controller as json_controller_module
from app.controllers.jira_controller import jira_controller as jira_controller_module

# Register blueprint(s)
app.register_blueprint(dashboard_controller_module)
app.register_blueprint(java_controller_module)
app.register_blueprint(redeem_controller_module)
app.register_blueprint(system_controller_module)
app.register_blueprint(chart_controller_module)
app.register_blueprint(dbdoc_controller_module)
app.register_blueprint(json_controller_module)
app.register_blueprint(jira_controller_module)
