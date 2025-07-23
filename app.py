from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = joblib.load('model.pkl')
scaler = joblib.load('std_scaler.pkl')

def water_quality_prediction(data):
    scaled_data = scaler.transform([data])
    prediction = model.predict(scaled_data)
    if prediction == 1:
        return "Water is safe for consumption."
    else:
        return "Water is not safe for consumption."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        pH = float(request.form['pH-Mean'])
        conductivity = float(request.form['CONDUCTIVITY (µmhos/cm)-Mean'])
        BOD = float(request.form['Biochemical oxygen demand (B.O.D.) (mg/l)-Mean'])
        nitrate = float(request.form['NITRATE- N (mg/l)-Mean'])

        # Create data array
        data = np.array([pH, conductivity, BOD, nitrate])

        # Predict using model
        result = water_quality_prediction(data)

        return render_template('index.html', prediction_text=result)
    except ValueError:
        return "Invalid input, please enter numeric values."

if __name__ == "__main__":
    app.run(debug=True)
