# flask server reciving mail and direct message from client
from flask import Flask, request, jsonify
from ai import run
app = Flask(__name__)



@app.route('/mail', methods=['POST'])
def mail():
    data = request.json
    data = data['data']
    response = run(data,True)
    return jsonify({'response': response})

@app.route('/direct_message', methods=['POST'])
def direct_message():
    data = request.json
    msg = data['msg']
    response = run(msg,True)
    return jsonify({'response': response})

app.run(port=5000, debug=True)