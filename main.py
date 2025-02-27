import sqlite3
from flask import Flask, render_template, request,redirect
from notes import get_notes
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def note():
    if request.method == "POST":
        note = request.form.get("note")
        if note:
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (note,))
            conn.commit()
            conn.close()
    return render_template("index.html", notes=get_notes())
@app.route("/note/delete/<int:note_id>", methods=['GET', 'POST'])
def delete_note(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)