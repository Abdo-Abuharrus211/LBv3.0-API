import psycopg2
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import os

from src.permitted_users import PermittedUsers
from src.db_driver import DbDriver

CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN")
DB_URL = os.getenv("DB_URL")
DB_PORT = int(os.getenv("DB_PORT", 8000))
DB_NAME = os.getenv("DB_NAME", "lbv3")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# database = psycopg2.connect(
#     host=DB_URL,
#     port=DB_PORT,
#     dbname=DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD
# )
# db_cursor = database.cursor()

# define flask config
app = Flask(__name__)
app.config['DEV'] = False
app.config['PROD'] = not app.config['DEV']
app.config['DEBUG'] = False

DB_DRIVER = DbDriver()
CORS(app, resources={r"/*": {"origins": CLIENT_ORIGIN}}, supports_credentials=True)


def get_db():
    """
    Retrieve the db connection stored in the Flask context or create it if DNE
    :return: psycopg2.connection instance to the PostgreSQL database
    """
    if not g.db:
        g.db = psycopg2.connect(
        host=DB_URL,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return g.db

@app.teardown_appcontext
def tear_down_db():
    """
    Close the db connection when app shutdown
    :return:
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def we_are_live():
    return 'If you see this, then the Flask server is up and running!', 200

@app.route('/testdb')
def test_db_connection():
    db_con = get_db()
    db_cursor = db_con.cursor()
    db_cursor.execute('SELECT * FROM questions')
    res = db_cursor.fetchall()
    return {"Got Data": res}, 200


@app.route('/get-questions', methods=['GET'])
def get_questions():
    db_con = get_db()
    q_data = DB_DRIVER.get_questions(db_con)
    tear_down_db()
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
    db_con = get_db()
    q_ids = request.get_json()['ids']
    print(q_ids)
    if q_ids is not None and len(q_ids) > 0:
        a_data = DB_DRIVER.get_answers(q_ids, db_con)
        print(a_data)
        tear_down_db()
        if a_data:
            return jsonify(a_data), 200
        else:
            return "Error retrieving the answer data!", 400
    tear_down_db()
    return {"Bad request": None}, 400

if __name__ == '__main__':
    # App is run using Gunicorn in Prod, by running: gunicorn -w 4 app:app
    app.run(host="0.0.0.0", port=8000)
