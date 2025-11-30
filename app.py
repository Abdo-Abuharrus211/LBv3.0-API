from http.client import responses
from flask import Flask, request
import os
from supabase import create_client, Client

from src.questions import DbDriver

# Defining the supabase client
# SUPABASE DOCS: https://supabase.com/docs/reference/python/rpc
SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
supabase_client = create_client(SUPA_URL, SUPA_KEY)

db_driver = DbDriver(supabase_client)
app = Flask(__name__)
# Dev config, change in Prod
app.config['DEV'] = True
app.debug = True

# app.config['SUPABASE_CLIENT'] = supabase_client
# TODO: set up the PROD config using WSGI server
# TODO: test the data fetching (using postman)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
@app.route('/testdb')
def test_db_connection():
    res = supabase_client.table("questions").select("*").execute()
    print("retrieved")
    print(f"res is: {res}")
    return "Completed test"

@app.route('/get-questions')
def get_questions():
    return ""

@app.route('/checkuser', methods=['GET'])
def check_user():
    signee_email = request.form['email']
    print(signee_email)

if __name__ == '__main__':
    # This method is only for Dev environments, in Prod need a WSGI server and its config
    app.run()
