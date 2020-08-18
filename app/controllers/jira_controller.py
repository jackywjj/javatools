# coding=utf8
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

jira_controller = Blueprint('jira_controller', __name__, url_prefix='/jira')


@jira_controller.route('/')
def list_sprint():
    try:
        data = {"menuid": 7}

        return render_template("jira_sprint_list.html", data=data)
    except TemplateNotFound:
        abort(404)
