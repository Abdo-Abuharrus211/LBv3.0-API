from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy

from src.permitted_users import PermittedUsers
from src.db_driver import DbDriver

CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN")
# Defining the supabase client
# SUPABASE DOCS: https://supabase.com/docs/reference/python/rpc
# SUPA_URL = os.getenv("SUPA_URL")
# SUPA_KEY = os.getenv("SUPA_KEY")
# supabase_client = create_client(SUPA_URL, SUPA_KEY)

DB_URI = os.getenv("DB_URL")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
database = SQLAlchemy()

# define flask config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# this saves memory and resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEV'] = False
app.config['PROD'] = not app.config['DEV']
app.config['DEBUG'] = False

DB_DRIVER = DbDriver(database)
database.init_app(app)
CORS(app, resources={r"/*": {"origins": CLIENT_ORIGIN}}, supports_credentials=True)

@app.route('/')
def we_are_live():
    return 'If you see this, then the Flask server is up and running!', 200


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
    # App is run using Gunicorn in Prod, by running: gunicorn -w 4 app:app
    app.run(host="0.0.0.0", port=8000)
