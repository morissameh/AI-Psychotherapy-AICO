from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
from FB_AUTH import log_in, sign_up
from ML_MODEL import Model
# To-DO Deployment
import warnings

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure server-side sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key'
Session(app)

# model = None

@app.route('/chat', methods=['POST'])
def chat():
    if 'history' not in session:
        session['history'] = []

    text = request.data.decode('utf-8')
    print(f"Received text: {text}")

    session['history'].append(text)
    response = model.Chain(text)
#    return jsonify({'response': response, 'history': session['history']})
    return response

@app.route('/signin', methods=['POST'])
def signin():
    json_data = request.get_json()
    print(json_data)
    email = json_data.get("email", "")
    password = json_data.get("password", "")
    result = log_in(email, password)
    print(result)
    return result

@app.route('/signup', methods=['POST'])
def signup():
    json_data = request.get_json()
    email = json_data.get('email')
    password = json_data.get('password')
    fullName = json_data.get('fullName')
    userName = json_data.get('userName')

    result = sign_up(email, password, fullName)
    return result

if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=UserWarning)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
        model = Model()
        model.load_pretrained()
    app.run(debug=True, port=8090)
