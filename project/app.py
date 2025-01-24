from flask import Flask, jsonify, render_template
from database import retrieve_all_data

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    """Fetch the latest logged data."""
    data = retrieve_all_data()
    response = [
        {'timestamp': record.timestamp.isoformat(), 'variable': record.variable, 'value': record.value}
        for record in data
    ]
    return jsonify(response)

@app.route('/latest-data', methods=['GET'])
def get_latest_data():
    """Fetch the latest logged data for each variable."""
    data = retrieve_all_data()[-10:]  # Fetch the latest 10 records (adjust as needed)
    response = [
        {'timestamp': record.timestamp.isoformat(), 'variable': record.variable, 'value': record.value}
        for record in data
    ]
    return jsonify(response)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
