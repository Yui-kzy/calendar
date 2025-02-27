import sqlite3
import datetime
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

@app.route('/time', methods=['GET', 'POST'])
def time():
    today = datetime.date.today()
    days = None
    if request.method == "POST":
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        if year and month and day and year.isdigit() and month.isdigit() and day.isdigit():
            try:
                test_day = datetime.date(int(year), int(month), int(day))
                days = (test_day - today).days
                if days < 0:
                    days = 0
            except ValueError:
                days = 0
    return render_template("time.html", days=days)
if __name__ == '__main__':
    app.run(debug=True)