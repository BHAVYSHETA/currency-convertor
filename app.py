from flask import send_from_directory
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "secret123"

# Currency conversion rates
conversion_rates = {
    "USD": 85.60, "AUD": 55.81, "CAD": 63.14, "EUR": 99.70, "GBP": 116.40,
    "AED": 23.40, "CNY": 11.986, "NZD": 51.70, "BRL": 15.50, "SGD": 67.07,
    "IDR": 0.05, "JPY": 0.60, "EGP": 1.85, "ZAR": 4.80, "KES": 0.70,
    "NGN": 0.11, "BDT": 0.70, "PKR": 0.30, "NPR": 0.63, "BTN": 1.00,
    "LKR": 0.29, "RUB": 1.08, "UAH": 2.08, "HKD": 11.00, "KZT": 1.70,
    "TRY": 2.38, "THB": 2.53, "KPW": 0.10, "KRW": 0.06
}

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
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            currency = request.form["currency"]
            rate = conversion_rates.get(currency)
            if rate:
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("login.html"), 404

@app.route('/google902b615e57984f03.html')
def google_verification():
    return send_from_directory('static', 'google902b615e57984f03.html')

from flask import send_from_directory

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')
