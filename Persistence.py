import json
import os

# app data that must survive a restart lives in <project_root>/persisted
PERSIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persisted")

def load_json(filename, default):
    # a missing file just means nothing was saved yet; a corrupted one fails loudly
    # instead of starting empty and overwriting it on the next save
    if not os.path.exists(filename):
        return default

    with open(filename, encoding='utf-8') as jsonFile:
        return json.load(jsonFile)

def save_json(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # write to a temp file and swap it in, so a crash mid-write cannot leave a truncated file
    tmp_filename = filename + ".tmp"
    with open(tmp_filename, 'w', encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False, indent=2)
    os.replace(tmp_filename, filename)
