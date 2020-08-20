'''This is the main file. Ensure that this is set as the FLASK_APP environment variable'''

import atexit
from flask import Flask
from flask_cors import CORS
from queenroxxanes.router.users import users
from queenroxxanes.router.appointments import appointments


#Initialize Flask
app = Flask(__name__)

#initialize CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# , resources={r"/*": {"origins": "*"}}, supports_credentials=True


# Blueprints
app.register_blueprint(users)
app.register_blueprint(appointments)

@app.route('/')
def entry_page():
    '''Route to main page of application'''
    return {}, 200
