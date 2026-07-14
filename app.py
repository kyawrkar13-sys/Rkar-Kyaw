from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solar", methods=["GET", "POST"])
def solar():
    result = None

    if request.method == "POST":

        monthly_kwh = float(request.form["monthly_kwh"])
        rate = float(request.form["rate"])
        solar_kw = float(request.form["solar_kw"])
        cost = float(request.form["cost"])

        # Annual electricity
        annual_kwh = monthly_kwh * 12

        # Solar generation estimation
        annual_generation = solar_kw * 4 * 365 * 0.8

        # Electricity saving
        saving = annual_generation * rate

        # Payback
        payback = cost / saving if saving > 0 else 0

        # ROI
        roi = (saving / cost) * 100 if cost > 0 else 0

        result = {
            "annual_kwh": round(annual_kwh, 2),
            "saving": round(saving, 0),
            "payback": round(payback, 2),
            "roi": round(roi, 2)
        }

    return render_template("solar.html", result=result)



@app.route("/generator", methods=["GET", "POST"])
def generator():

    result = None

    if request.method == "POST":

        capacity = float(request.form["capacity"])
        hours = float(request.form["hours"])
        fuel_rate = float(request.form["fuel_rate"])
        fuel_price = float(request.form["fuel_price"])
        days = float(request.form["days"])

        daily_fuel = hours * fuel_rate

        monthly_fuel = daily_fuel * days

        monthly_cost = monthly_fuel * fuel_price

        annual_cost = monthly_cost * 12


        result = {
            "daily_fuel": round(daily_fuel, 2),
            "monthly_fuel": round(monthly_fuel, 2),
            "monthly_cost": round(monthly_cost, 0),
            "annual_cost": round(annual_cost, 0)
        }


    return render_template("generator.html", result=result)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)