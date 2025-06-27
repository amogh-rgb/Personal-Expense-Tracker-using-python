from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime

app = Flask(__name__)
FILENAME = os.path.join(os.path.dirname(__file__), "expenses.json")

def load_expenses():
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, PermissionError):
        return []

def save_expenses(expenses):
    try:
        with open(FILENAME, "w") as f:
            json.dump(expenses, f, indent=4)
    except PermissionError:
        print("🚫 Cannot write to expenses.json")

@app.route("/")
def index():
    expenses = load_expenses()
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
        except ValueError:
            amount = 0.0
        category = request.form["category"]
        date = request.form["date"] or datetime.now().strftime("%Y-%m-%d")
        
        expenses = load_expenses()
        expenses.append({"amount": amount, "category": category, "date": date})
        save_expenses(expenses)
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/summary")
def summary():
    expenses = load_expenses()
    summary_data = {}
    total = 0

    for item in expenses:
        cat = item["category"]
        amt = item["amount"]
        summary_data[cat] = summary_data.get(cat, 0) + amt
        total += amt

    return render_template("summary.html", summary=summary_data, total=total)

if __name__ == "__main__":
    app.run(debug=True)