from flask import request, jsonify, url_for, render_template, redirect
from project import app

@app.route('/v1/sanitized/input', methods=['POST'])
def check_input():
    api_request = request.get_json()
    
    if list(api_request.keys())[0] != 'payload' or len(api_request) > 1:
        raise ValueError('The API takes a JSON input with only 1 argument - "payload"')
    
    payload = api_request['payload'].lower()

    filter_characters = ['*', '+', '-', '/', 
                        '"', '\'', '=', '--', ';',
                        ' as ', ' drop ', ' or ']

    result = 'sanitized'
    for character in filter_characters:
        if character in payload:
            result = 'unsanitized'

    return jsonify({"result" : result})
