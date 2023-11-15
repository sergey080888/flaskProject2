import os
import re
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, jsonify, Response
from pymongo.errors import OperationFailure
from schema import data_convert

DB_URI = os.getenv('DB_URI')

app = Flask(__name__)

client = MongoClient(DB_URI)
db = client["test-database"]
collection = db['forms']


@app.route('/get_form', methods=['POST'])
def get_form_handler():
    # form = {
    #     "name": "Form template name",
    #     "field_1": "email",
    #     "field_2": "phone",
    # }
    # insert_result = collection.insert_one(form)

    args = dict(request.args)

    pattern = re.compile('.')

    docs = {}
    list_docs = list(collection.find())
    for doc in list_docs:
        docs.update(doc)
    fields_of_collection = set(list(docs.keys()))

    intersect_set = fields_of_collection & set(list(args.keys()))

    for key in intersect_set:
        collection.create_index({key: 1})

    filter_ = {'$or': [{key: {'$regex': pattern} for key in intersect_set}]}

    new_args_converted = data_convert(args)

    if not intersect_set:
        return Response(json_util.dumps(new_args_converted), mimetype="application/json", status=400)

    try:
        some_templates = list(collection.find(filter_))
    except OperationFailure:
        return Response(json_util.dumps(new_args_converted), mimetype="application/json", status=400)

    if not some_templates:
        return Response(json_util.dumps(new_args_converted), mimetype="application/json", status=400)

    for template in some_templates:
        try:
            _id = template.pop('_id')
            name = template.pop('name')
        except AttributeError:
            return Response(json_util.dumps(new_args_converted), mimetype="application/json", status=400)

        # сверяем ключ и значение шаблона с формой
        for key, val in template.items():
            if new_args_converted.get(key) != val:
                return Response(json_util.dumps(new_args_converted), mimetype="application/json", status=400)

        # если шаблон найден возвращаем имя шаблона
        return jsonify({"name": name})


if __name__ == '__main__':
    app.run(debug=True)
