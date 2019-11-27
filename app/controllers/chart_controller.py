# coding=utf8

import csv

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

chart_controller = Blueprint('chart_controller', __name__, url_prefix='/')

'''
Dashboard
'''


@chart_controller.route('/chart/329', methods=['GET'])
def chart329():
    try:
        data = {"menuid": 4}
        csv_file = csv.reader(open('/workdisk/workspace-python/javatools/app/record.csv', 'r'))
        label_list = []
        value_list = []
        for line in csv_file:
            created_hour = line[0]
            amount = line[1]
            label_list.append(created_hour)
            value_list.append(amount)
        return render_template("chart_329.html", data=data, value_list=value_list, label_list=label_list)
    except TemplateNotFound:
        abort(404)
