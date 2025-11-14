from flask import Flask, request
from raft_kv import RaftKV
import os

app = Flask(__name__)

# determine leader using docker-compose environment variable
is_leader = os.getenv("IS_LEADER", "false").lower() == "true"
node = RaftKV(is_leader=is_leader)

@app.route("/kv/<key>", methods=["PUT"])
def kv_put(key):
    value = request.get_data(as_text=True)

    if not value:
        value = request.form.get(None) or ""

    node.put(key, value)
    return {"status": "ok", "key": key, "value": value}

@app.route("/kv/<key>", methods=["GET"])
def kv_get(key):
    value = node.get(key)
    return {"key": key, "value": value}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
