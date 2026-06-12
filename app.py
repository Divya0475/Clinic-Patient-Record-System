from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

import sqlite3
import json
from datetime import date
from flask import session

app = Flask(__name__)
app.secret_key = "clinic_secret_key"

DB_PATH = "database/database.db"

@app.route("/login", methods=["GET","POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM doctors
        WHERE username=?
        """,(username,))

        doctor = cursor.fetchone()

        conn.close()

        if doctor is None:

            message = "Doctor not registered"

        elif doctor[7] != password:

            message = "Incorrect password. Please re-enter."

        else:

            session["doctor"] = doctor[1]
            session["clinic"] = doctor[2]

            return redirect("/")

    return render_template(
        "login.html",
        message=message
    )


@app.route(
"/register_doctor",
methods=["GET","POST"]
)
def register_doctor():

    message = ""

    if request.method == "POST":

        doctor_name = request.form["doctor_name"]
        clinic_name = request.form["clinic_name"]
        clinic_phone = request.form["clinic_phone"]
        clinic_address = request.form["clinic_address"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            message = (
                "Passwords do not match"
            )

            return render_template(
                "register_doctor.html",
                message=message
            )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM doctors
        WHERE username=?
        """,(username,))

        existing = cursor.fetchone()

        if existing:

            message = (
                "Username already exists"
            )

        else:

            cursor.execute("""
            INSERT INTO doctors(
                doctor_name,
                clinic_name,
                clinic_phone,
                clinic_address,
                email,
                username,
                password
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                doctor_name,
                clinic_name,
                clinic_phone,
                clinic_address,
                email,
                username,
                password
            ))

            conn.commit()

            message = (
                "Registration Successful. "
                "Please Login."
            )

        conn.close()

    return render_template(
        "register_doctor.html",
        message=message
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/")
def dashboard():

    if "doctor" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total Patients
    cursor.execute(
    "SELECT COUNT(*) FROM patients"
    )

    total_patients = cursor.fetchone()[0]

    # Total Visits
    cursor.execute(
    "SELECT COUNT(*) FROM visits"
    )

    total_visits = cursor.fetchone()[0]

    # Visits Today
    today = date.today().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT COUNT(*)
    FROM visits
    WHERE visit_date=?
    """, (today,))

    visits_today = cursor.fetchone()[0]

    # Recent Consultations
    cursor.execute("""
    SELECT patients.name,
           visits.diagnosis,
           visits.visit_date
    FROM visits
    JOIN patients
    ON visits.patient_phone = patients.phone
    ORDER BY visits.id DESC
    LIMIT 5
    """)

    recent_visits = cursor.fetchall()

    # Symptom Analysis
    cursor.execute("""
    SELECT symptoms
    FROM visits
    """)

    rows = cursor.fetchall()

    symptom_count = {}

    for row in rows:

        if row[0]:

            symptoms = row[0].split(",")

            for symptom in symptoms:

                symptom = symptom.strip()

                if symptom:

                    symptom_count[symptom] = (
                        symptom_count.get(symptom, 0) + 1
                    )

    most_common_symptom = "None"

    if symptom_count:

        most_common_symptom = max(
            symptom_count,
            key=symptom_count.get
        )

    top_symptoms = sorted(
        symptom_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    cursor.execute("""
    SELECT COUNT(*)
    FROM visits
    WHERE followup_date >= date('now')
    """)

    upcoming_followups = cursor.fetchone()[0]
    conn.close()


    return render_template(
    "dashboard.html",
    total_patients=total_patients,
    total_visits=total_visits,
    visits_today=visits_today,
    most_common_symptom=most_common_symptom,
    recent_visits=recent_visits,
    top_symptoms=top_symptoms,
    upcoming_followups=upcoming_followups
)


# ==========================================
# REGISTER PATIENT
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        age = request.form["age"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT phone FROM patients WHERE phone=?",
            (phone,)
        )

        existing = cursor.fetchone()

        if existing:

            message = "Patient already exists"

        else:

            cursor.execute("""
            INSERT INTO patients
            (
                phone,
                name,
                age,
                gender,
                blood_group
            )
            VALUES(?,?,?,?,?)
            """,
            (
                phone,
                name,
                age,
                gender,
                blood_group
            ))

            conn.commit()

            message = (
                "Patient Registered Successfully"
            )

        conn.close()

    return render_template(
        "register_patient.html",
        message=message
    )


# ==========================================
# PATIENT RECORDS
# ==========================================

@app.route("/records")
def records():

    search = request.args.get("search", "")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if search:

        cursor.execute("""
        SELECT *
        FROM patients
        WHERE name LIKE ?
        OR phone LIKE ?
        ORDER BY name
        """,
        (
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("""
        SELECT *
        FROM patients
        ORDER BY name
        """)

    patients = cursor.fetchall()

    conn.close()

    return render_template(
        "patient_records.html",
        patients=patients,
        search=search
    )


# ==========================================
# CONSULTATION
# ==========================================

@app.route(
    "/consultation",
    methods=["GET", "POST"]
)
def consultation():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    selected_phone = request.args.get(
        "phone",
        ""
    )

    if request.method == "POST":

        patient_phone = request.form[
            "patient_phone"
        ]

        visit_date = request.form[
            "visit_date"
        ]

        symptoms = request.form.getlist(
            "symptoms"
        )

        additional_symptoms = request.form[
            "additional_symptoms"
        ]

        diagnosis = request.form[
            "diagnosis"
        ]

        medicine = request.form[
            "medicine"
        ]

        dosage = request.form[
            "dosage"
        ]

        duration = request.form[
            "duration"
        ]

        followup_date = request.form[
            "followup_date"
        ]

        notes = request.form[
            "notes"
        ]

        all_symptoms = ", ".join(symptoms)

        if additional_symptoms:

            if all_symptoms:
                all_symptoms += (
                    ", " + additional_symptoms
                )
            else:
                all_symptoms = (
                    additional_symptoms
                )

        prescription = (
            f"{medicine} - {dosage}"
        )

        cursor.execute("""
        INSERT INTO visits
        (
            patient_phone,
            visit_date,
            symptoms,
            diagnosis,
            prescription,
            duration,
            notes,
            followup_date
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            patient_phone,
            visit_date,
            all_symptoms,
            diagnosis,
            prescription,
            duration,
            notes,
            followup_date
        ))

        conn.commit()
        conn.close()

        return redirect(
            url_for(
                "history",
                phone=patient_phone
            )
        )

    cursor.execute("""
    SELECT phone,name
    FROM patients
    ORDER BY name
    """)

    patients = cursor.fetchall()

    with open(
        "data/symptoms.json",
        "r"
    ) as f:

        symptoms_list = json.load(f)

    with open(
        "data/medicines.json",
        "r"
    ) as f:

        medicines = json.load(f)

    conn.close()

    return render_template(
        "consultation.html",
        patients=patients,
        symptoms_list=symptoms_list,
        medicines=medicines,
        selected_phone=selected_phone
    )


# ==========================================
# PATIENT HISTORY
# ==========================================

@app.route("/history/<phone>")
def history(phone):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM patients
    WHERE phone=?
    """, (phone,))

    patient = cursor.fetchone()

    cursor.execute("""
    SELECT *
    FROM visits
    WHERE patient_phone=?
    ORDER BY visit_date DESC
    """, (phone,))

    visits = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        patient=patient,
        visits=visits,
        phone=phone
    )


# ==========================================
# ANALYTICS
# ==========================================

@app.route("/analytics")
def analytics():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total Patients
    cursor.execute(
        "SELECT COUNT(*) FROM patients"
    )

    total_patients = cursor.fetchone()[0]

    # Total Visits
    cursor.execute(
        "SELECT COUNT(*) FROM visits"
    )

    total_visits = cursor.fetchone()[0]

    # Visits Today

    today = date.today().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT COUNT(*)
    FROM visits
    WHERE visit_date=?
    """,(today,))

    visits_today = cursor.fetchone()[0]

    # Symptom Analysis

    cursor.execute("""
    SELECT symptoms
    FROM visits
    """)

    rows = cursor.fetchall()

    symptom_count = {}

    for row in rows:

        if row[0]:

            symptoms = row[0].split(",")

            for symptom in symptoms:

                symptom = symptom.strip()

                if symptom:

                    symptom_count[symptom] = (
                        symptom_count.get(symptom,0)+1
                    )

    most_common_symptom = "None"

    if symptom_count:

        most_common_symptom = max(
            symptom_count,
            key=symptom_count.get
        )

    top_symptoms = sorted(
        symptom_count.items(),
        key=lambda x:x[1],
        reverse=True
    )[:5]

    conn.close()

    return render_template(
        "analytics.html",
        total_patients=total_patients,
        total_visits=total_visits,
        visits_today=visits_today,
        most_common_symptom=most_common_symptom,
        top_symptoms=top_symptoms
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)





