from lib import summarizer
from flask import Flask, abort, jsonify, request
from multiprocessing import Process, Queue
import json
import queue
import uuid
import sys, traceback
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
job_queue = Queue()

def f_io(fn, mode, obj):
    if mode == "r":
        with open(fn, mode) as f:
            return json.loads(f.read())
    else:
        with open(fn, mode) as f:
            f.write(json.dumps(obj))

def rm_files():
    files = os.listdir("./data")
    for f in files:
        if f.endswith(".json"):
            os.remove("./data/{}".format(f))

def process_loop():
    try:
        while True:
            job = job_queue.get()
            top_5_sentences = summarizer.summarize(job["data"])[:5]
            summary = ' '.join(top_5_sentences)
            obj = {"uid": job["uid"], "summary": summary, "summarized": True}
            f_io("data/"+str(job["uid"])+".json", "w+", obj)
    except KeyboardInterrupt:
        rm_files()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

@app.route("/api/submit", methods=["POST"])
def submit():
    uid = uuid.uuid4().int
    data = str(request.get_data(), 'utf8')
    job = {"uid": uid, "data": data, "summarized": False}
    f_io("data/{}.json".format(job["uid"]), "w+", job)
    job_queue.put(job)
    return jsonify({"response": job["uid"]}), 201

@app.route("/api/query/<int:uid>", methods=["GET"])
def query(uid):
    try:
        data = f_io("data/{}.json".format(uid), "r", None)
    except FileNotFoundError:
        return jsonify({"status": "error"}), 404
    if data["summarized"]:
        return jsonify({"response": data["summary"], "status": "succeeded"}), 200
    else:
        return jsonify({"status": "pending"}), 200

if __name__ == "__main__":
    p = Process(target=process_loop)
    p.start()
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
    p.join()
