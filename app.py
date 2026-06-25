import psycopg2
from psycopg2.extras import DictCursor
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
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=DB_URL,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    return g.db


# this decorator manages tearing down connections after requests finish
@app.teardown_appcontext
def tear_down_db(exception=None):
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
    db_cursor = db_con.cursor(cursor_factory=DictCursor)
    db_cursor.execute('SELECT * FROM questions')
    res = db_cursor.fetchall()
    return {"Got Data": res}, 200


@app.route('/get-questions', methods=['GET'])
def get_questions():
    db_con = get_db()
    db_cursor = db_con.cursor(cursor_factory=DictCursor)
    try:
        q_data = DB_DRIVER.get_questions(db_cursor)
        if q_data:
            return jsonify(q_data), 200
        else:
            return "Error retrieving the question data!", 500
    except Exception as e:
        app.logger.error(e)
        return f"Error retrieving the question data!", 500


@app.route('/checkuser', methods=['POST'])
def check_user():
    signee_email = request.get_json(silent=True)
    if signee_email is not (None or "") and "email" in signee_email:
        cleared = signee_email in PermittedUsers
        return {"cleared": cleared}, 200
    else:
        return "Must provide email address", 400


@app.route('/get-answers', methods=['POST'])
def get_answers():
    db_con = get_db()
    q_ids = request.get_json(silent=True)
    print(f"Question IDs: {q_ids}")
    if q_ids is not None and "ids" in q_ids:
        try:
            db_cursor = db_con.cursor(cursor_factory=DictCursor)
            a_data = DB_DRIVER.get_answers(q_ids["ids"], db_cursor)
            print(f"Answer data: {a_data}")
            if a_data:
                return jsonify(a_data), 200
            else:
                return "Error parsing the answer data!", 500
        except Exception as e:
            app.logger.error(e)
            return f"Error retrieving the answer data!", 500
    return {"Bad request": None}, 400


if __name__ == '__main__':
    # App is run using Gunicorn in Prod, by running: gunicorn -w 4 app:app
    app.run(host="0.0.0.0", port=8000)
