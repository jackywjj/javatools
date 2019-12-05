# coding=utf8
from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from app.models.agent_grade import *
from app.models.city import *
from app.models.province import *

json_controller = Blueprint('json_controller', __name__, url_prefix='/json')


@json_controller.route('/')
def convert_to_json():
    try:
        data = {"menuid": 6}
        

        return render_template("json_tools.html",data=data)
    except TemplateNotFound:
        abort(404)

@json_controller.route('/generate/json', methods=['GET','POST'])
def generate_json():
  data =  '{"status": "OK", "total_used": 63330648, "total_space": 125604864, "total_avail": 62274216}'
  return data