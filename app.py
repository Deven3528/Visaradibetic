from flask import Flask, flash, jsonify, url_for, redirect, render_template, url_for, session, logging, request
import pyrebase
import PyPDF2
import requests
import firebase_admin
from firebase_admin import credentials, db, auth


URL = "https://api.meaningcloud.com/summarization-1.0"
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash message


@app.route('/summarise')
def summarise_form():
    return render_template("summarise.html")



firebaseConfig = {
    'apiKey': "AIzaSyAUuAFrWwrTtMGsfdtYdc-cPx2TDFqmvQM",
    'authDomain': "visara-health-management.firebaseapp.com",
    'projectId': "visara-health-management",
    'storageBucket': "visara-health-management.firebasestorage.app",
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
    if request.method == "POST":
        full_name = request.form.get("fullname")
        age = request.form.get("age")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phone_number = request.form.get("phoneNumber")
        password = request.form.get("password")
        user = auth.create_user_with_email_and_password(email, password)

        # Store patient data in Firebase Realtime Database
        patient_data = {
            "full_name": full_name,
            "age": age,
            "gender": gender,
            "email": email,
            "phone_number": phone_number,
            
        }
        db.child("patients").push(patient_data)

        # Return success message with popup
        return jsonify({"success": True})
       

       

if __name__ == '__main__':
    app.run(debug=True)


