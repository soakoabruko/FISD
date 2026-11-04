import itertools
import json
import os
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

notes = []
note_ids = itertools.count(1)
authors_cache = {}

DATA_FILE = "guestbook.json"

def save_data():
    global note_ids
    next_note_id = next(note_ids)
    note_ids = itertools.count(next_note_id)
    data = {
        "notes": notes,
        "authors_cache": authors_cache,
        "next_note_id": next_note_id, 
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        global notes, authors_cache, note_ids
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                notes = data.get("notes", [])
                authors_cache = data.get("authors_cache", {})
                next_note_id = data.get("next_note_id", 1)
                note_ids = itertools.count(next_note_id)
        except (json.JSONDecodeError, KeyError):
            notes = []
            note_ids = itertools.count(1)
            authors_cache = {}

def find_note(note_id):
    return next((n for n in notes if n["id"] == note_id), None)

@app.get("/")
def index():
    return "<h1>Гостевая книга</h1>"

@app.get("/notes")
def get_notes():
    author = request.args.get("author", "").strip()
    limit_raw = request.args.get("limit", "10")
    offset_raw = request.args.get("offset", "0")
    sort_raw = request.args.get("sort", "id")
    order_raw = request.args.get("order", "asc")
    try:
        limit = int(limit_raw)
        if not 1 <= limit <= 100:
            raise ValueError
    except ValueError:
        return jsonify(error="parameter 'limit' is invalid. it must be an integer from 1 to 100"), 400
    try:
        offset = int(offset_raw)
        if not offset >= 0:
            raise ValueError
    except ValueError:
        return jsonify(error="parameter 'offset' is invalid. it must be a non-negative integer"), 400
    if sort_raw not in ("id", "likes"):
        return jsonify(error="parameter 'sort' is invalid. it must be 'id' or 'likes'"), 400
    sort = sort_raw
    if order_raw not in ("asc", "desc"):
        return jsonify(error="parameter 'order' is invalid. it must be 'asc' or 'desc'"), 400
    order = order_raw
    filtered_notes = notes
    if author:
        filtered_notes = [note for note in notes if note["author"] == author.strip()]
    filtered_notes.sort(key=lambda note: note[sort], reverse=order == "desc")
    paginated_notes = filtered_notes[offset : offset + limit]
    return jsonify(paginated_notes), 200

@app.post("/notes")
def create_note():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="bad request"), 400
    elif not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400
    elif not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    note = {
        "id": next(note_ids),
        "author": data["author"].strip(),
        "text": data["text"].strip(),
        "likes": 0,
    }
    notes.append(note)
    author = data["author"].strip()
    if author not in authors_cache:
        authors_cache[author] = {"notes": 0, "likes": 0}
    authors_cache[author]["notes"] += 1
    save_data()
    return jsonify(note), 201

@app.delete("/notes")
def delete_author():
    author = request.args.get("author", "").strip()
    if not author:
        return jsonify(error="parameter 'author' (non-empty string) is required"), 400
    global notes
    notes = [note for note in notes if note["author"] != author]
    notes_num = 0
    if author in authors_cache:
        notes_num = authors_cache[author]["notes"]
        del authors_cache[author]
    save_data()
    return jsonify(deleted=notes_num), 200

@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    return jsonify(note)

@app.put("/notes/<int:note_id>")
def put_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="bad request"), 400
    elif not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400
    elif not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    old_author, new_author = note["author"], data["author"].strip()
    authors_cache[old_author]["notes"] -= 1
    authors_cache[old_author]["likes"] -= note["likes"]
    if authors_cache[old_author]["notes"] == 0:
        del authors_cache[old_author]
    if new_author not in authors_cache:
        authors_cache[new_author] = {"notes": 0, "likes": 0}
    authors_cache[new_author]["notes"] += 1
    authors_cache[new_author]["likes"] += note["likes"]
    note["author"] = data["author"].strip()
    note["text"] = data["text"].strip()
    save_data()
    return jsonify(note), 200

@app.patch("/notes/<int:note_id>")
def patch_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="bad request"), 400
    elif not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    note["text"] = data["text"].strip()
    save_data()
    return jsonify(note), 200

@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    notes.remove(note)
    author = note["author"]
    authors_cache[author]["notes"] -= 1
    authors_cache[author]["likes"] -= note["likes"]
    if authors_cache[author]["notes"] == 0:
        del authors_cache[author]
    save_data()
    return "", 204

@app.post("/notes/<int:note_id>/like")
def like_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    note["likes"] += 1
    author = note["author"]
    authors_cache[author]["likes"] += 1
    save_data()
    return jsonify(note), 200

@app.get("/authors")
def get_authors():
    result = [
        {"author": author, "notes": stat["notes"], "likes": stat["likes"]}
        for author, stat in authors_cache.items()
    ]
    result.sort(key=lambda x: x["author"])
    return jsonify(result), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not found"), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="method not allowed"), 405

if __name__ == "__main__":
    load_data()
    app.run(debug=True)