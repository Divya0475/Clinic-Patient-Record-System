# Clinic Patient Record System

## Project Overview

The Clinic Patient Record System is a web-based healthcare management application developed to help clinics and doctors efficiently manage patient information, consultation records, follow-ups, and medical history.

The system replaces manual record-keeping methods by providing a centralized platform where doctors can register patients, record visits, track diagnoses and prescriptions, monitor follow-up appointments, and analyze clinic statistics.

---

# Problem Statement

Many small clinics maintain patient records using paper files or spreadsheets. This makes it difficult to:

* Track patient history
* Manage follow-up appointments
* Search patient records quickly
* Analyze clinic performance
* Store consultation details securely

This project provides a digital solution for managing patient records efficiently.

---

# Objectives

* Register and manage patient information.
* Record patient consultations.
* Maintain complete patient medical history.
* Track follow-up appointments.
* Analyze clinic activities through dashboards.
* Provide a secure login system for doctors.

---

# Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript
* Font Awesome Icons
* Responsive Design

## Backend

* Python
* Flask Framework

## Database

* SQLite3

## Development Tools

* Visual Studio Code
* Python Virtual Environment (venv)

---

# Features Implemented

## Doctor Authentication

### Doctor Registration

Doctors can create a clinic account by providing:

* Doctor Name
* Clinic Name
* Clinic Phone Number
* Clinic Address
* Email
* Username
* Password

### Doctor Login

Registered doctors can log in using:

* Username
* Password

Validation includes:

* Doctor not registered
* Incorrect password
* Successful login session

### Logout

Doctors can securely log out of the system.

---

# Patient Registration

Doctors can register new patients with:

* Name
* Phone Number (Unique ID)
* Age
* Gender
* Blood Group

Validation:

* Duplicate patient prevention
* Mandatory fields
* Phone number validation

---

# Consultation Management

Doctors can record patient visits including:

* Visit Date
* Symptoms
* Additional Symptoms
* Diagnosis
* Prescription
* Dosage
* Duration
* Follow-Up Date
* Doctor Notes

---

# Patient Records

Doctors can:

* View all registered patients
* Search patients by:

  * Name
  * Phone Number
* Access patient history
* Add new consultation records

---

# Patient History

Displays complete medical history in reverse chronological order.

Includes:

* Patient Information
* Visit Date
* Symptoms
* Diagnosis
* Prescription
* Duration
* Doctor Notes
* Follow-Up Date

---

# Dashboard

The dashboard provides real-time clinic insights.

### Statistics

* Total Registered Patients
* Total Visits
* Visits Today
* Upcoming Follow-Ups

### Additional Information

* Recent Consultations
* Most Common Symptoms
* Top Symptoms Analysis

---

# Analytics

Provides clinic performance metrics:

* Total Patients
* Total Visits
* Visits Today
* Most Common Symptom
* Top Symptoms List

---

# Database Design

## Doctors Table

| Field          | Type    |
| -------------- | ------- |
| id             | INTEGER |
| doctor_name    | TEXT    |
| clinic_name    | TEXT    |
| clinic_phone   | TEXT    |
| clinic_address | TEXT    |
| email          | TEXT    |
| username       | TEXT    |
| password       | TEXT    |

---

## Patients Table

| Field       | Type    |
| ----------- | ------- |
| phone       | TEXT    |
| name        | TEXT    |
| age         | INTEGER |
| gender      | TEXT    |
| blood_group | TEXT    |

---

## Visits Table

| Field         | Type    |
| ------------- | ------- |
| id            | INTEGER |
| patient_phone | TEXT    |
| visit_date    | TEXT    |
| symptoms      | TEXT    |
| diagnosis     | TEXT    |
| prescription  | TEXT    |
| duration      | TEXT    |
| notes         | TEXT    |
| followup_date | TEXT    |

---

# System Architecture

```text
Doctor Login
      │
      ▼
 Dashboard
      │
      ├──────────────┐
      ▼              ▼
Register        Patient Records
Patient              │
      │              ▼
      │         Search Patient
      │              │
      ▼              ▼
 Consultation  Patient History
      │              │
      ▼              ▼
 Save Visit     View All Visits
      │
      ▼
 Follow-Up Tracking
      │
      ▼
 Analytics Dashboard
```

---

# Workflow

## Step 1

Doctor registers a clinic account.

## Step 2

Doctor logs into the system.

## Step 3

Doctor registers a patient.

## Step 4

Doctor records consultation details.

## Step 5

Patient visit information is stored in the database.

## Step 6

Doctor can search patient records.

## Step 7

Doctor can view complete patient history.

## Step 8

Dashboard and analytics are automatically updated.

---

# User Interface Design

The application uses a modern healthcare-inspired design featuring:

* Dark Theme Dashboard
* Responsive Layout
* Sidebar Navigation
* Interactive Cards
* Search Components
* Icons and Visual Indicators
* Mobile-Friendly Interface

Color palette inspired by professional healthcare management systems.

---

# Future Enhancements

* PDF Export of Patient History
* Edit Patient Details
* Delete Patient Records
* Follow-Up Management Module
* Email Notifications
* Appointment Scheduling
* Multi-Doctor Support
* Cloud Database Integration
* AI-Based Disease Prediction
* Electronic Prescription Generation

---

# How To Run

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install flask
```

## Create Database

```bash
python init_db.py
```

## Run Application

```bash
python app.py
```

## Open Browser

```text
http://127.0.0.1:5000
```

---

# Project Outcome

The Clinic Patient Record System successfully digitizes patient record management by providing secure doctor authentication, patient registration, consultation recording, follow-up tracking, medical history management, and analytical dashboards through a user-friendly web interface.
