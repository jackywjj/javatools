# coding=utf8
from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from app.models.agent_grade import *
from app.models.city import *
from app.models.province import *

redeem_controller = Blueprint('redeem_controller', __name__, url_prefix='/redeem')


@redeem_controller.route('/')
def redeem():
    try:
        data = {"menuid": 3}
        start_redeem_code_number = request.args.get('start_redeem_code_number')
        if not start_redeem_code_number:
            start_redeem_code_number = 1000000
        redeem_code_amount = request.args.get('redeem_code_amount')
        if not redeem_code_amount:
            redeem_code_amount = 10
        else:
            redeem_code_amount = int(redeem_code_amount)

        amount_list = []
        for i in range(0, redeem_code_amount):
            amount_list.append(i)

        grade_list = AgentGrade.query.all()
        province_list = Province.query.all()
        city_list = City.query.all()

        return render_template("redeem_tools.html",
                               data=data, amount_list=amount_list,
                               redeem_code_amount=redeem_code_amount,
                               start_redeem_code_number=start_redeem_code_number,
                               grade_list=grade_list,
                               province_list=province_list,
                               city_list=city_list)
    except TemplateNotFound:
        abort(404)
