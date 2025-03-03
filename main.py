import sqlite3
import datetime
import os
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = os.urandom(24)
@app.route("/sign", methods=['GET', 'POST'])
def sign():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        if user_id and password:
            hashed_password = generate_password_hash(password)
            conn = sqlite3.connect("day.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (user_id, password) VALUES (?, ?)", (user_id, hashed_password))
                conn.commit()
            except sqlite3.IntegrityError:
                return "這個帳號已被註冊！"
            finally:
                conn.close()
            return redirect("/") 
    return render_template("sign.html")

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        conn = sqlite3.connect("day.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            session["user_id"] = user_id
            return redirect(f"/{user_id}")          
        else:
            return "帳號或密碼錯誤！"

    return render_template("login.html")
@app.route('/<string:user_id>', methods=['GET', 'POST'])
def time(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login")) 
    
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
                cursor.execute("INSERT INTO time_events (user_id,title, date) VALUES (?,?, ?)", (user_id,title, test_day.strftime("%Y-%m-%d")))
                conn.commit()
                return redirect(f"/{user_id}")
            except ValueError:
                pass
           
    conn = sqlite3.connect("day.db") 
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, date FROM time_events WHERE user_id = ? ORDER BY date ASC", (user_id,))
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

    return render_template("time.html", events=events,user_id=user_id)
@app.route("/delete/<int:time_events_id>/<user_id>", methods=['POST'])
def delete(time_events_id, user_id):
    conn = sqlite3.connect("day.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM time_events WHERE id = ? AND user_id = ?", (time_events_id, user_id))
    conn.commit()
    conn.close()
    return redirect(f"/{user_id}")
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)ss