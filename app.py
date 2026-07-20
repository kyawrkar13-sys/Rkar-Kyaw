from flask import Flask, render_template

app =Flask(__name__, static_folder=".", static_url_path="")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solar", methods=["GET", "POST"])
def solar():
    result = None

    if request.method == "POST":
        # SOLAR INPUT
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

        # GENERATOR INPUT
        fuel_price = float(request.form["fuel_price"])
        fuel_consumption = float(request.form["fuel_consumption"])
        gen_hours_before = float(request.form["gen_hours_before"])
        gen_hours_after = float(request.form["gen_hours_after"])
        operating_days = float(request.form["operating_days"])

        # SOLAR CALCULATION
        daily_pv_generation = (
            pv_size * sun_hours * performance_ratio
        )

        annual_pv_generation = (
            daily_pv_generation * 365
        )

        annual_load = monthly_load * 12

        usable_solar_energy = min(
            annual_pv_generation,
            annual_load
        )

        usable_battery = (
            battery_kwh *
            battery_dod *
            efficiency
        )

        annual_electricity_saving = (
            usable_solar_energy * tariff
        )

        solar_net_annual_saving = (
            annual_electricity_saving - om_year
        )

        # GENERATOR CALCULATION
        hours_saved = max(
            gen_hours_before - gen_hours_after,
            0
        )

        annual_fuel_saved = (
            hours_saved *
            fuel_consumption *
            operating_days
        )

        annual_generator_saving = (
            annual_fuel_saved * fuel_price
        )

        # SOLAR RESULT
        solar_payback = (
            capex / solar_net_annual_saving
            if solar_net_annual_saving > 0
            else 0
        )

        solar_roi = (
            (
                solar_net_annual_saving *
                project_life - capex
            ) / capex * 100
            if capex > 0
            else 0
        )

        solar_npv = -capex

        for year in range(1, project_life + 1):
            solar_npv += (
                solar_net_annual_saving /
                ((1 + discount_rate) ** year)
            )

        # TOTAL SOLAR + GENERATOR SAVING
        total_annual_saving = (
            solar_net_annual_saving +
            annual_generator_saving
        )

        total_payback = (
            capex / total_annual_saving
            if total_annual_saving > 0
            else 0
        )

        total_roi = (
            (
                total_annual_saving *
                project_life - capex
            ) / capex * 100
            if capex > 0
            else 0
        )

        total_npv = -capex

        for year in range(1, project_life + 1):
            total_npv += (
                total_annual_saving /
                ((1 + discount_rate) ** year)
            )

        result = {
            "pv_generation":
                round(annual_pv_generation, 2),

            "usable_battery":
                round(usable_battery, 2),

            "electricity_saving":
                round(annual_electricity_saving, 0),

            "solar_payback":
                round(solar_payback, 2),

            "solar_roi":
                round(solar_roi, 2),

            "solar_npv":
                round(solar_npv, 0),

            "hours_saved":
                round(hours_saved, 2),

            "annual_fuel_saved":
                round(annual_fuel_saved, 2),

            "generator_saving":
                round(annual_generator_saving, 0),

            "total_annual_saving":
                round(total_annual_saving, 0),

            "total_payback":
                round(total_payback, 2),

            "total_roi":
                round(total_roi, 2),

            "total_npv":
                round(total_npv, 0)
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
