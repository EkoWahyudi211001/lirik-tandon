from flask import Flask, render_template, jsonify, request
from datetime import datetime
import random
from collections import defaultdict

app = Flask(__name__)

# Simulasi Data
daily_usage = defaultdict(int)
status_keran = "ON"
last_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "water_level": 75,
    "water_usage": 120,
    "status_keran": status_keran
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data")
def get_data():
    global last_data
    # Simulasi update
    last_data["water_level"] = random.randint(40, 90)
    last_data["water_usage"] += random.randint(1, 5)
    last_data["timestamp"] = datetime.now().strftime('%H:%M:%S')
    last_data["status_keran"] = "ON" if random.choice([True, False]) else "OFF"
    return jsonify(last_data)

@app.route("/get_daily_usage")
def get_daily_usage():
    # Simulasi data per tanggal
    return jsonify({
        "2025-05-10": 80,
        "2025-05-11": 95,
        "2025-05-12": 100,
        "2025-05-13": 90,
        "2025-05-14": last_data["water_usage"]
    })

@app.route("/update_data", methods=["POST"])
def update_data():
    global last_data
    data = request.get_json()
    if not data:
        return "No JSON received", 400
    
    try:
        last_data["water_level"] = int(data["w"])
        last_data["water_usage"] += int(data["u"])
        last_data["status_keran"] = data["s"]
        last_data["timestamp"] = datetime.now().strftime('%H:%M:%S')
        return "", 204  # No Content (berhasil tanpa body)
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(debug=True)
