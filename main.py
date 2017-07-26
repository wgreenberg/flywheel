# Need to go back to file implementation...

from lib import summarizer
from flask import Flask, abort, jsonify, request
from multiprocessing import Process, Queue, Array, Value
import random
import queue
import json
import os

app = Flask(__name__)
job_queue = Queue()

def process_loop():
    while True:
        try:
            job = job_queue.get()
        except queue.Empty:
            print("waiting...")
            continue
        summary = summarizer.summarize(job["data"])
        fname="data/"+str(job["uid"])+".json"
        with open(fname, "w+") as f:
            f.write(json.dumps({"uid": job["uid"], "summary": summary, "summarized": True}))

@app.route("/api/submit", methods=["POST"])
def submit():
    if not request.json or not "data" in request.json:
        abort(400)
    uid = int("".join(str(random.choice(range(10))) for _ in range(10)))
    job = {"uid": uid, "data": request.json["data"], "summarized": False}
    fname = "data/"+str(uid)+".json"
    with open(fname, "w+") as f:
        f.write(json.dumps(job))
    job_queue.put(job)
    return jsonify({"response": job["uid"]}), 201

@app.route("/api/query/<int:uid>", methods=["GET"])
def query(uid):
    try:
        fname = "data/"+str(uid)+".json"
        with open(fname, "r") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        return jsonify({"response": "Invalid Key"}), 404
    if data["summarized"]:
        return jsonify({"response": data["summary"]}), 200
    else:
        return jsonify({"response": "Summarization has yet to complete"}), 203

if __name__ == "__main__":
    p = Process(target=process_loop)
    p.start()
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
    p.join()
