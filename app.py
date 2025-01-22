from flask import Flask, render_template
from api.endpoints import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

#uncomment these if necessary
# @app.route('/')
# def index():
#     return "Welcome to the CV Ranker API! Visit /api to explore the endpoints."

# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # Empty response to handle favicon.ico requests

if __name__ == '__main__':
    app.run(debug=True)
