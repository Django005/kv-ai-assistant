from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Load response JSON files from 'responses' directory
def load_response(file_name):
    file_path = os.path.join(os.path.dirname(__file__), 'responses', file_name)
    with open(file_path, 'r') as file:
        return json.load(file)

@app.route('/service/catalog/plm/createProject', methods=['POST'])
def create_project():
    response_data = load_response('create_project.json')
    return jsonify(response_data)

@app.route('/service/system/service/serviceCall', methods=['POST'])
def get_product_details():
    response_data = load_response('get_product_details.json')
    return jsonify(response_data)

@app.route('/service/catalog/plm/createItemVersion', methods=['POST'])
def create_item_version():
    response_data = load_response('create_item_version.json')
    return jsonify(response_data)

@app.route('/service/catalog/plm/updateProjectItem', methods=['POST'])
def update_project_item():
    response_data = load_response('update_project_item.json')
    return jsonify(response_data)

@app.route('/service/catalog/plm/getProjectItem', methods=['POST'])
def get_project_item():
    response_data = load_response('get_project_item.json')
    return jsonify(response_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))  # Allow PORT customization with env variable, default to 5000
    app.run(host='0.0.0.0', port=port)