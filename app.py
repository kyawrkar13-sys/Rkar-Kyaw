from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solar")
def solar():
    return render_template("solar.html")

@app.route("/generator")
def generator():
    return render_template("generator.html")

if__kyawrkar13-sys/Rkar-Kyaw__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
