# coding=utf8
import json

from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from app.helpers.java_helper import *

dbdoc_controller = Blueprint('dbdoc_controller', __name__, url_prefix='/dbdoc')


@dbdoc_controller.route('/', methods=['GET', 'POST'])
def dbdoc_list():
    try:
        table_prefix = request.args.get('table_prefix')
        if not table_prefix:
            table_prefix = 'agt_'
        tables = get_doc_tables(table_prefix)
        data = {"menuid": 5}

        return render_template("dbdoc.html", data=data, table_prefix=table_prefix, tables=tables)
    except TemplateNotFound:
        abort(404)


@dbdoc_controller.route('/content', methods=['GET'])
def dbdoc_content():
    table_prefix = request.args.get('table_prefix')
    tables = get_doc_tables(table_prefix)
    html = ''
    for table in tables:
        html += '- [' + table + '](#archor_' + table + ')' + "\n"

    data = {"contentHtml": html}
    return json.dumps(data, ensure_ascii=False)


@dbdoc_controller.route('/table', methods=['GET'])
def dbdoc_table():
    table_name = request.args.get('table_name')
    fields = get_table_field('cy_qydb.' + table_name)
    html = generate_db_doc(table_name, fields)

    data = {"contentHtml": html}
    return json.dumps(data, ensure_ascii=False)


@dbdoc_controller.route('/table/all', methods=['GET'])
def dbdoc_table_all():
    table_prefix = request.args.get('table_prefix')
    tables = get_doc_tables(table_prefix)
    html = ''
    for table in tables:
        fields = get_table_field('cy_qydb.' + table)
        html += generate_db_doc(table, fields)

    htmlSrc = html.replace('&lt;', '<')
    htmlSrc = htmlSrc.replace('&gt;', '>')

    data = {"contentHtml": html, "contentHtmlSrc": htmlSrc}
    return json.dumps(data, ensure_ascii=False)
