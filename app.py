from flask import send_from_directory
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os
import requests

# Your API key (replace with your real one)
url = f"https://v6.exchangerate-api.com/v6/bf0f546991c9b3e4393b40a1/latest/USD"

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- Login Page ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        age = int(request.form["age"])
        if age >= 16:
            session["user"] = f"{surname} {name}"
            return redirect(url_for("converter"))
        else:
            return "❌ Sorry, you must be at least 16 to use this app."
    return render_template("login.html")


# ---------------- Dashboard Converter ----------------
@app.route("/converter", methods=["GET", "POST"])
def converter():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    conversion_rates = {}

    
    try:
        response = requests.get(url)
        data = response.json()
        conversion_rates = data["conversion_rates"]  
    except:
        return "⚠️ Error fetching live currency data."

    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from_curr = request.form["from_curr"]
            to_curr = request.form["to_curr"]

            if from_curr in conversion_rates and to_curr in conversion_rates:
                # relational conversion (any → any)
                rate = conversion_rates[to_curr] / conversion_rates[from_curr]
                result = round(amount * rate, 2)
        except:
            result = "⚠️ Invalid input."

    return render_template(
        "index.html",
        result=result,
        rates=conversion_rates,
        user=session["user"],
        now=datetime.now().strftime("%A, %d %B %Y — %I:%M %p")
    )


# ---------------- Logout ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- Main Runner ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ---------------- Error Page ----------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("login.html"), 404


# ---------------- Google Verification ----------------
@app.route('/google902b615e57984f03.html')
def google_verification():
    return send_from_directory('static', 'google902b615e57984f03.html')


# ---------------- Sitemap ----------------
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')
