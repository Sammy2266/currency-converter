from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://open.er-api.com/v6/latest/USD"

@app.route("/", methods=["GET", "POST"])
def currency_converter():
    rates = {}
    error = None
    result = None

    # Fetch exchange rates
    try:
        response = requests.get(API_URL)
        rates = response.json()["rates"]
    except Exception:
        error = "❌ Error: Couldn't connect to exchange rate API"

    # Handle conversion logic
    if request.method == "POST":
        from_currency = request.form.get("from_currency", "").upper()
        to_currency = request.form.get("to_currency", "").upper()
        amount = request.form.get("amount", "")

        if from_currency not in rates:
            error = f"❌ Invalid code: {from_currency}"
        elif to_currency not in rates:
            error = f"❌ Invalid code: {to_currency}"
        else:
            try:
                amount = float(amount)
                amount_in_usd = amount / rates[from_currency]
                result = {
                    "from": from_currency,
                    "to": to_currency,
                    "amount": amount,
                    "converted": amount_in_usd * rates[to_currency],
                    "rate": rates[to_currency] / rates[from_currency],
                }
            except ValueError:
                error = "❌ Please enter a valid number"

    return render_template("index.html", rates=rates, error=error, result=result)


if __name__ == "__main__":
    app.run(debug=True)