from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solar", methods=["GET", "POST"])
def solar():

    result = None

    if request.method == "POST":

        solar_cost = float(request.form["solar_cost"])

        electricity_before = float(
            request.form["electricity_before"]
        )

        electricity_after = float(
            request.form["electricity_after"]
        )

        generator_before = float(
            request.form["generator_before"]
        )

        generator_after = float(
            request.form["generator_after"]
        )


        monthly_electricity_saving = max(
            electricity_before - electricity_after,
            0
        )

        monthly_generator_saving = max(
            generator_before - generator_after,
            0
        )

        total_monthly_saving = (
            monthly_electricity_saving
            + monthly_generator_saving
        )

        total_annual_saving = (
            total_monthly_saving * 12
        )


        if solar_cost > 0:

            roi = (
                total_annual_saving
                / solar_cost
            ) * 100

        else:
            roi = 0


        if total_annual_saving > 0:

            payback = (
                solar_cost
                / total_annual_saving
            )

        else:
            payback = 0


        result = {

            "monthly_electricity_saving":
                monthly_electricity_saving,

            "monthly_generator_saving":
                monthly_generator_saving,

            "total_monthly_saving":
                total_monthly_saving,

            "total_annual_saving":
                total_annual_saving,

            "roi":
                round(roi, 2),

            "payback":
                round(payback, 2)
        }


    return render_template(
        "solar.html",
        result=result
    )


@app.route("/generator")
def generator():

    return render_template(
        "generator.html"
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )