from flask import abort, jsonify, make_response, render_template, request
from web_app import app
from lib import summarizer

#configs - TODO: Move these to a configuration file.
api_uri_base = "/api/v0.0.0/"

# WEB UI COMPONENT
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",
                           title="flywheel, I guess")

# API
@app.route(api_uri_base+"submit", methods=["POST"])
def submit_job():
    if not request.json or not "data" in request.json:
        abort(400)
    job = {"data": request.json["data"]}
    result = summarizer.summarize(request.json["data"])
    return jsonify({'response': result}), 201

# ERROR HANDLING
@app.errorhandler(404)
def not_found(error):
    obj = {"Error": "Not Found"}
    return make_response(jsonify(obj), 404)
