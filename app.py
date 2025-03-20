import os
from pickletools import pydict
import time
from tkinter import Image
import cv2
from PIL import Image, ImageOps
from flask import Flask, flash, jsonify, url_for, redirect, render_template, url_for, session, logging, request
import h5py
from werkzeug.utils import secure_filename
import numpy as np
import pyrebase
import PyPDF2
import requests
import firebase_admin
from firebase_admin import credentials, db, auth
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, Add, MaxPooling2D, GlobalAveragePooling2D, Reshape, LSTM, Dense, Input
from tensorflow.keras.models import Model, load_model

URL = "https://api.meaningcloud.com/summarization-1.0"
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash message

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print(tf.config.list_physical_devices('GPU'))

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define CNN + LSTM Model
def build_model(input_shape):
    X_input = Input(shape=input_shape)
    
    # Initial Conv Layer
    X = Conv2D(32, (3, 3), padding='same')(X_input)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((2, 2))(X)
    
    # Branch 1 - ResNet Inspired Block
    Y = Conv2D(32, (3, 3), padding='same')(X)
    Y = BatchNormalization()(Y)
    Y = Activation('relu')(Y)
    Y = GlobalAveragePooling2D()(Y)
    Y = Reshape((1, -1))(Y)
    
    # Branch 2 - Another ResNet Inspired Block
    Z = Conv2D(32, (3, 3), padding='same')(X)
    Z = BatchNormalization()(Z)
    Z = Activation('relu')(Z)
    Z = GlobalAveragePooling2D()(Z)
    Z = Reshape((1, -1))(Z)
    
    # Merge both branches and pass through LSTM
    combined = tf.keras.layers.concatenate([Y, Z], axis=-1)
    T = LSTM(64)(combined)
    
    # Fully Connected Layers
    T = Dense(128, activation='relu')(T)
    T = Dense(5, activation='softmax')(T)  # Assuming 5 DR severity levels
    
    model = Model(inputs=X_input, outputs=T)
    return model

# Initialize Model
input_shape = (224, 224, 3)
model = build_model(input_shape)
print("✅ Model built successfully!")

# Load Model Weights
weights_path = "D:/Visara/modal/modal.weights.h5"
model_path = "D:/Visara/modal/drmodel.h5"

if os.path.exists(model_path):
    try:
        model = load_model(model_path)  # Load full model if available
        print("✅ Full model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading full model: {e}")
elif os.path.exists(weights_path):
    try:
        model.load_weights(weights_path)  # Load only weights
        print("✅ Weights loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading weights: {e}")
else:
    print("❌ Model file not found! Please train and save the model.")

@app.route('/summarise')
def summarise_form():
    return render_template("summarise.html")



firebaseConfig = {
    'apiKey': "AIzaSyAUuAFrWwrTtMGsfdtYdc-cPx2TDFqmvQM",
    'authDomain': "visara-health-management.firebaseapp.com",
    'projectId': "visara-health-management",
    'storageBucket': "visara-health-management.appspot.com",
    'messagingSenderId': "185911663002",
    'appId': "1:185911663002:web:17927fd2fa98902a4bc223",
    'measurementId': "G-CPLGMRRNGZ",
    "databaseURL" : "https://visara-health-management-default-rtdb.firebaseio.com"
    }
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db=firebase.database()

@app.route('/')
def index():
    return render_template('visaara.html')

@app.route('/aianalysis.html')
def aianalysis():
    return render_template("aianalysis.html")

@app.route('/Dlogin.html')
def Dlogin():
    return render_template('Dlogin.html')


@app.route('/Plogin.html')
def Plogin():
    return render_template('Plogin.html')

@app.route('/contact.html')
def contact ():
    return render_template("contact.html")

@app.route('/Dregistration.html')
def Dregistration():
    return render_template('Dregistration.html')

@app.route('/Ddash.html')
def Ddash():
    return render_template('Ddash.html')

@app.route('/Dappointment.html')
def Dappointment():
    return render_template('Dappointment.html')

@app.route('/Danalysis.html')
def Danalysis():
    return render_template('Danalysis.html')

@app.route('/Dsetting.html')
def Dsetting():
    return render_template('Dsetting.html')

@app.route('/DReport.html')
def DReport():
    return render_template('DReport.html')

@app.route('/Dpatientmanagement.html')
def Dpatientmanagement():
      return render_template('Dpatientmanagement.html')

@app.route('/Pregistration.html')
def Pregistration():
    return render_template('Pregistration.html')

@app.route('/Pdash.html')
def Pdash():
    return render_template('Pdash.html')

@app.route('/appoint section.html')
def appoint_section():
    return render_template('appoint section.html')

@app.route('/Paianalysis.html')
def Paianalysis():
    return render_template('Paianalysis.html')

@app.route('/report(Pdash).html')
def report():
    return render_template('report(Pdash).html')

@app.route('/yogabot.html')
def yogabot():
    return render_template('yogabot.html')

@app.route('/setting.html')
def setting():
    return render_template('setting.html')



@app.route("/Dregistration", methods=["POST"])
def doctor_registration():
    if request.method == "POST":
        full_name = request.form.get("fullName")
        hospital_name = request.form.get("hospitalName")
        email = request.form.get("email")
        specialization = request.form.get("specialization")
        password = request.form.get("password")
        user = auth.create_user_with_email_and_password(email, password)

        # Store in Firebase
        doctor_data = {
            "full_name": full_name,
            "hospital_name": hospital_name,
            "email": email,
            "specialization": specialization
        }
        db.child("doctors").push(doctor_data)

        # Return success message with popup
        return jsonify({"success": True})


@app.route("/Pregistration", methods=["POST"])
def patient_registration():
    try:
        # Get data from the form
        full_name = request.form.get("fullname")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        password = request.form.get("password")
        diabetes_history = request.form.get("diabetes-history")
        eye_conditions = request.form.getlist("eye_conditions[]")

        # Data to push to Firebase
        patient_data = {
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
            "email": email,
            "phone": phone,
            "address": address,
            "password": password,
            "diabetes_history": diabetes_history,
            "eye_conditions": eye_conditions
        }

        # Push data to Firebase Database
        db.child("patients").push(patient_data)

        return jsonify({"message": "Patient registration successful"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    name = request.form.get('name', '')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'dcm'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)  # Save the uploaded file

        try:
            start_time = time.time()

            # Handle DICOM file
            if filename.lower().endswith('.dcm'):
                import pydicom
                dicom_data = pydicom.dcmread(filepath)
                image_array = dicom_data.pixel_array

                # Convert grayscale to RGB
                if len(image_array.shape) == 2:  # Grayscale image
                    image_rgb = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
                else:
                    image_rgb = image_array  # Already RGB

                image_data = Image.fromarray(cv2.resize(image_rgb, (224, 224)))
            else:
                image_data = Image.open(filepath).convert("RGB")  # Ensure RGB format

            # ✅ Use the pre-built model
            global model  # Use the globally defined model

            if model is None:
                return jsonify({'error': 'Model is not loaded'}), 500

            # ✅ Define the import_and_predict function
            def import_and_predict(image, model):
                image = ImageOps.fit(image, (224, 224), Image.LANCZOS)  # Fixed deprecated method
                image_array = np.asarray(image)
                image_array = np.expand_dims(image_array, axis=0)
                image_array = image_array / 255.0  # Normalize
                return model.predict(image_array)

            prediction = import_and_predict(image_data, model)

            class_names = ["NO DR", "Mild DR", "Moderate DR", "Severe DR", "Proliferative DR"]
            result_index = np.argmax(prediction)
            result = class_names[result_index]
            probability = float(prediction[0][result_index])

            # ✅ Save to Firebase if name provided
            if name:
                db.child("Patient").child(name).update({
                    "dr": result,
                    "probability": probability
                })

            end_time = time.time()
            processing_time = round(end_time - start_time, 2)

            return jsonify({
                'severity_score': probability,
                'diagnosis': result,
                'processing_time': processing_time
            })

        except Exception as e:
            print(f"❌ Error processing image: {str(e)}")
            return jsonify({'error': 'Error processing image'}), 500

    return jsonify({'error': 'Invalid file type'}), 400
    
if __name__ == '__main__':
    app.run(debug=True)


