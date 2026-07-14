from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solar", methods=["GET", "POST"])
def solar():
    result = None

    if request.method == "POST":
        pv_size = float(request.form["pv_size"])
        sun_hours = float(request.form["sun_hours"])
        performance_ratio = float(request.form["performance_ratio"]) / 100
        monthly_load = float(request.form["monthly_load"])

        battery_kwh = float(request.form["battery_kwh"])
        battery_dod = float(request.form["battery_dod"]) / 100
        efficiency = float(request.form["efficiency"]) / 100

        tariff = float(request.form["tariff"])
        capex = float(request.form["capex"])
        om_year = float(request.form["om_year"])
        project_life = int(request.form["project_life"])
        discount_rate = float(request.form["discount_rate"]) / 100

        generator_annual_saving = float(
            request.form.get("generator_annual_saving", 0)
        )

        # PV generation
        daily_pv_generation = (
            pv_size * sun_hours * performance_ratio
        )

        annual_pv_generation = (
            daily_pv_generation * 365
        )

        # Annual load
        annual_load = monthly_load * 12

        # Solar energy actually used
        usable_solar_energy = min(
            annual_pv_generation,
            annual_load
        )

        # Battery usable capacity
        usable_battery = (
            battery_kwh
            * battery_dod
            * efficiency
        )

        # Electricity saving
        annual_electricity_saving = (
            usable_solar_energy * tariff
        )

        # Solar net annual saving
        solar_net_annual_saving = (
            annual_electricity_saving
            - om_year
        )

        # Total saving including generator
        total_annual_saving = (
            solar_net_annual_saving
            + generator_annual_saving
        )

        # Solar payback
        solar_payback = (
            capex / solar_net_annual_saving
            if solar_net_annual_saving > 0
            else 0
        )

        # Solar ROI over project life
        solar_roi = (
            (
                solar_net_annual_saving
                * project_life
                - capex
            )
            / capex
            * 100
            if capex > 0
            else 0
        )

        # Solar NPV
        solar_npv = -capex

        for year in range(1, project_life + 1):
            solar_npv += (
                solar_net_annual_saving
                / ((1 + discount_rate) ** year)
            )

        # Total payback
        total_payback = (
            capex / total_annual_saving
            if total_annual_saving > 0
            else 0
        )

        # Total ROI
        total_roi = (
            (
                total_annual_saving
                * project_life
                - capex
            )
            / capex
            * 100
            if capex > 0
            else 0
        )

        # Total NPV
        total_npv = -capex

        for year in range(1, project_life + 1):
            total_npv += (
                total_annual_saving
                / ((1 + discount_rate) ** year)
            )

        result = {
            "pv_generation": round(annual_pv_generation, 2),
            "usable_battery": round(usable_battery, 2),

            "solar_payback": round(solar_payback, 2),
            "solar_roi": round(solar_roi, 2),
            "solar_npv": round(solar_npv, 0),

            "electricity_saving": round(
                annual_electricity_saving, 0
            ),

            "generator_saving": round(
                generator_annual_saving, 0
            ),

            "total_annual_saving": round(
                total_annual_saving, 0
            ),

            "total_payback": round(total_payback, 2),
            "total_roi": round(total_roi, 2),
            "total_npv": round(total_npv, 0)
        }

    return render_template(
        "solar.html",
        result=result
    )


@app.route("/generator")
def generator():
    return render_template("generator.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )