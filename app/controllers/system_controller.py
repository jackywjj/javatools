# coding=utf8
import json

from flask import Blueprint, request

from app.models.agent import *
from app.models.city import *

system_controller = Blueprint('system_controller', __name__, url_prefix='/system')


@system_controller.route('/city')
def get_city():
    province_code = request.args.get('province_code')
    city_list = City.query.filter_by(province_code=province_code)
    cities = []
    for city in city_list:
        cities.append(city.toJson())
    data = {"cities": cities}
    return json.dumps(data, ensure_ascii=False)


@system_controller.route('/agent')
def get_agent():
    grade_code = request.args.get('grade_code')
    province_code = request.args.get('province_code')
    city_code = request.args.get('city_code')

    filters = {}
    if not grade_code == "":
        filters['grade_code'] = grade_code
        print filters
    if not province_code == "":
        filters['province_code'] = province_code
    if not city_code == "":
        filters['city_code'] = city_code

    agent_list = Agent.query.filter_by(**filters)
    agents = []
    for agent in agent_list:
        agents.append(agent.toJson())
    data = {"agents": agents}
    return json.dumps(data, ensure_ascii=False)
