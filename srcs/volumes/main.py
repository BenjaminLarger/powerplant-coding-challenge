import logging
from flask import Flask, request, jsonify
from algo import prduction_plan
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

@app.route('/')
def hello_world():
    app.logger.debug('Hello World endpoint was accessed')
    return 'Hello, World!'

@app.route('/productionplan', methods=['POST'])
def receive_load():
    data = request.get_json()  # Get the JSON data from the request

    if not data:
        return jsonify({"error": "No data provided"}), 400

    app.logger.debug(f"Received data: {data}")  # Log the received data

    json_response = prduction_plan(data)

    return jsonify({"message": "Data received successfully!", "data": data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
