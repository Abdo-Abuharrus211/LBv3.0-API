from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from supabase import create_client

from src.permitted_users import PermittedUsers
from src.db_driver import DbDriver

# Defining the supabase client
# SUPABASE DOCS: https://supabase.com/docs/reference/python/rpc
SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
supabase_client = create_client(SUPA_URL, SUPA_KEY)

DB_DRIVER = DbDriver(supabase_client)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Dev config, change in Prod
app.config['DEV'] = True
app.config['DEBUG'] = True

# app.config['SUPABASE_CLIENT'] = supabase_client
# TODO: set up the PROD config using WSGI server
# TODO: test the data fetching (using postman)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/testdb')
def test_db_connection():
    res = supabase_client.table("questions").select("*").execute()
    return {"Got Data": res}, 200


@app.route('/get-questions', methods=['GET'])
def get_questions():
    q_data = DB_DRIVER.get_questions()
    if q_data:
        return jsonify(q_data), 200
    else:
        return "Error retrieving the question data!", 400


@app.route('/checkuser', methods=['POST'])
def check_user():
    signee_email = request.get_json()['email']
    if signee_email is not None and not "":
        cleared = signee_email in PermittedUsers
        return {"cleared": cleared}, 200
    else:
        return "Must provide email address", 400


@app.route('/get-answers', methods=['POST'])
def get_answers():
    q_ids = request.get_json()['ids']
    print(q_ids)
    if q_ids is not None and len(q_ids) > 0:
        a_data = DB_DRIVER.get_answers(q_ids)
        print(a_data)
        if a_data:
            return jsonify(a_data), 200
        else:
            return "Error retrieving the answer data!", 400
    return {"Bad request": None}, 400


if __name__ == '__main__':
    # This method is only for Dev environments, in Prod need a WSGI server and its config
    app.run()
