import sqlite3
import datetime
from flask import Flask, render_template, request,redirect
from notes import get_notes
app = Flask(__name__)

@app.route('/note', methods=['GET', 'POST'])
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

@app.route('/', methods=['GET', 'POST'])
def time():
    today = datetime.date.today()
    days = None
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        if title and year and month and day and year.isdigit() and month.isdigit() and day.isdigit():
            try:
                test_day = datetime.date(int(year), int(month), int(day))
                days = (test_day - today).days
                if days < 0:
                    days = 0
                    
                conn = sqlite3.connect("day.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO time_events (title, date) VALUES (?, ?)", (title, test_day.strftime("%Y-%m-%d")))
                conn.commit()
                return redirect("/")
            except ValueError:
                pass
            finally:
                conn.close() 
            conn = sqlite3.connect("day.db")
    conn = sqlite3.connect("day.db") 
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, date FROM time_events ORDER BY date ASC")
    events = []
    for time_events_id, title, date_str in cursor.fetchall():
        event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        days = (event_date - today).days
        if days >= 0:
            events.append((title, date_str, days, time_events_id))
        else:
            conn = sqlite3.connect("day.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM time_events WHERE date = ?", (date_str,))
            conn.commit()
    conn.close()

    return render_template("time.html", events=events)

@app.route("/delete/<int:time_events_id>", methods=['GET', 'POST'])
def delete(time_events_id):
    conn = sqlite3.connect("day.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM time_events WHERE id = ?", (time_events_id,))
    conn.commit()
    conn.close()
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True)