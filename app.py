from flask import Flask
import os
from supabase import create_client, Client



# Defining the supabase client
# SUPABASE DOCS: https://supabase.com/docs/reference/python/rpc
SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
supabase_client = create_client(SUPA_URL, SUPA_KEY)


# TODO: Add the connection strings to connect to supabase
app = Flask(__name__)
# Dev config, change in Prod
app.config['DEV'] = True
app.debug = True
# app.config['SUPABASE_CLIENT'] = supabase_client

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/get-questions')
def get_questions():
    return ""



if __name__ == '__main__':
    app.run()
