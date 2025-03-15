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
       

if __name__ == '__main__':
    app.run(debug=True)


