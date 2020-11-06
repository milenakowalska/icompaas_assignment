from flask import render_template, url_for, redirect, request, jsonify
from app import app

@app.route('/v1/sanitized/input', methods=['POST'])
def check_input():
    api_request = request.get_json()
    payload = api_request['payload'].lower()

    filter_characters = ['*', '+', '-', '/', 
                        '"', '\'', '=', '--', ';',
                        ' as ', ' drop ', ' or ']

    result = 'sanitized'
    for character in filter_characters:
        if character in payload:
            result = 'unsanitized'

    return jsonify({"result" : result})
