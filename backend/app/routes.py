from flask import current_app as app

@app.route('/')
def index():
    return "Hello, World!"