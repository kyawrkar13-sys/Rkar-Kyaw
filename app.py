[14/07/2026 00:33] Rkar Kyaw: from flask import Flask, render_template, request
import math

app = Flask(__name__)


def solar_energy(pv_kw, psh, pr, degradation, year):
    return pv_kw * psh * 365 * pr * ((1 - degradation) ** (year - 1))


def generator_saving(fuel_l_hr, hours_day, diesel_price, offset):
    fuel_year = fuel_l_hr * hours_day * 365
    saved_fuel = fuel_year * (offset / 100)
    saving = saved_fuel * diesel_price

    return saved_fuel, saving


def financial_model(capex, yearly_saving, om, lifetime, discount):

    cashflow = []
    cumulative = -capex
    npv = -capex
    payback = None

    for year in range(1, lifetime + 1):

        om_cost = capex * (om / 100)

        net = yearly_saving - om_cost

        cumulative += net

        npv += net / ((1 + discount / 100) ** year)

        if payback is None and cumulative >= 0:
            payback = year

        cashflow.append({
            "year": year,
            "cash": round(net,2),
            "total": round(cumulative,2)
        })

    total_return = sum(x["cash"] for x in cashflow)

    roi = ((total_return - capex) / capex) * 100

    return {
        "payback": payback,
        "roi": round(roi,2),
        "npv": round(npv,2),
        "cashflow": cashflow
    }


@app.route("/", methods=["GET","POST"])
def index():

    result = None

    if request.method == "POST":

        pv_kw = float(request.form["pv_kw"])
        psh = float(request.form["psh"])
        pr = float(request.form["pr"]) / 100

        degradation = float(request.form["degradation"]) / 100

        fuel = float(request.form["fuel"])
        hours = float(request.form["hours"])
        diesel = float(request.form["diesel"])
        offset = float(request.form["offset"])

        capex = float(request.form["capex"])
        om = float(request.form["om"])

        lifetime = int(request.form["lifetime"])

        discount = float(request.form["discount"])


        solar_year = solar_energy(
            pv_kw,
            psh,
            pr,
            degradation,
            1
        )


        fuel_saved, money_saved = generator_saving(
            fuel,
            hours,
            diesel,
            offset
        )


        finance = financial_model(
            capex,
            money_saved,
            om,
            lifetime,
            discount
        )


        result = {
            "solar": round(solar_year,2),
            "fuel": round(fuel_saved,2),
            "saving": round(money_saved,2),
            "finance": finance
        }


    return render_template(
        "index.html",
        result=result
    )


if name == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
[14/07/2026 13:01] Rkar Kyaw: from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Solar & Generator Analyzer is working!"

if name == "__main__":
    app.run(host="0.0.0.0", port=5000)
