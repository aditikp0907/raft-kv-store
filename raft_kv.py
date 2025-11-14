import json
import os

class RaftKV:
    def __init__(self, is_leader=False):
        self.is_leader = is_leader
        self.log = []
        self.store = {}

        # load previous state if exists (for crash recovery)
        self.load_state()

    def load_state(self):
        if os.path.exists("state.json"):
            try:
                data = json.load(open("state.json"))
                self.log = data.get("log", [])
                self.store = data.get("store", {})
                print("State loaded:", data)
            except:
                print("State file corrupted, starting fresh.")

    def save_state(self):
        data = {
            "log": self.log,
            "store": self.store
        }
        json.dump(data, open("state.json", "w"))
        print("State saved:", data)

    def redirect_to_leader(self):
        print("Not leader. Redirecting request...")

    def append_log(self, entry):
        self.log.append(entry)
        print("Log appended:", entry)

    def replicate(self):
        print("Replicating log to followers... (stub)")

    def put(self, key, value):
        if not self.is_leader:
            self.redirect_to_leader()
            return

        entry = {"op": "put", "k": key, "v": value}
        self.append_log(entry)
        self.replicate()

        # commit to store
        self.store[key] = value

        # persist state for crash survival
        self.save_state()

    def get(self, key):
        return self.store.get(key)
