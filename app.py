from flask import Flask, request, jsonify, render_template
from database import init_db, insert_reading, get_all_readings, get_latest_reading

app = Flask(__name__)

@app.route('/readings', methods=['POST'])
def receive_reading():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    temp_c  = data.get('temperature_c')
    temp_f  = data.get('temperature_f')
    humidity = data.get('humidity')

    if None in (temp_c, temp_f, humidity):
        return jsonify({'error': 'Missing fields'}), 400

    rssi   = data.get('rssi')
    vcc    = data.get('vcc')
    uptime = data.get('uptime')

    insert_reading(temp_c, temp_f, humidity, rssi, vcc, uptime)
    print(f"Reading saved — {temp_f:.1f}°F, {humidity:.1f}% RH, RSSI: {rssi} dBm")

    return jsonify({'status': 'ok'}), 201

@app.route('/readings', methods=['GET'])
def get_readings():
    rows = get_all_readings()
    readings = [
        {
            'id':            r[0],
            'temperature_c': r[1],
            'temperature_f': r[2],
            'humidity':      r[3],
            'rssi':          r[4],
            'vcc':           r[5],
            'uptime':        r[6],
            'timestamp':     r[7]
        }
        for r in rows
    ]
    return jsonify(readings)

@app.route('/latest', methods=['GET'])
def get_latest():
    row = get_latest_reading()
    if not row:
        return jsonify({'error': 'No readings yet'}), 404
    return jsonify({
        'id':            row[0],
        'temperature_c': row[1],
        'temperature_f': row[2],
        'humidity':      row[3],
        'rssi':          row[4],
        'vcc':           row[5],
        'uptime':        row[6],
        'timestamp':     row[7]
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)