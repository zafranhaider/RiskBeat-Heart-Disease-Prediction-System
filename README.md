# RiskBeat
A Django-based web application that predicts the risk of heart disease using Machine Learning algorithms like Xtreme Gradient Boosting. The system provides personalized insights for early diagnosis, enhanced treatment planning, and efficient healthcare management.

---

## Table of Contents
- [Introduction](#introduction)
- [Existing System](#existing-system)
- [Problem Statement](#problem-statement)
- [Proposed Solution](#proposed-solution)
- [Scope of the Project](#scope-of-the-project)
- [Project Features](#project-features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Screenshots](#screenshots)
- [Feedback and Contributions](#feedback-and-contributions)
- [License](#license)

---

## Introduction
The Heart Risk Disease Prediction System leverages advanced data mining and machine learning techniques to analyze medical parameters and predict the risk level of heart disease. It utilizes algorithms like Gradient Boosting and Logistic Regression along with a multilayer perceptron neural network for high-performance prediction accuracy. The system uses 13 medical parameters such as age, sex, blood pressure, cholesterol, and obesity for prediction.

---

## Existing System
Currently, heart disease diagnoses rely on:
- Expensive tests and consultations.
- Underutilized healthcare data.
- Limited accessibility for many individuals.

These challenges often delay early diagnosis, leading to costly treatments and severe health outcomes.

---

## Problem Statement
Heart disease remains one of the leading causes of death worldwide. Despite the abundance of healthcare data, it is often underutilized for predictive analysis. Current diagnostic methods are expensive, time-consuming, and inaccessible, highlighting the need for a cost-effective, efficient system for early detection of heart disease.

---

## Proposed Solution
The Heart Disease Risk Prediction System addresses these challenges by:
- Using patient profiles (e.g., age, blood pressure, cholesterol) to predict the likelihood of heart disease.
- Employing machine learning techniques for accurate risk classification.
- Enhancing healthcare decision-making through data-driven insights.
- Improving treatment affordability and outcomes.

---

## Scope of the Project
### Role-Based Logins
- **Admin**: Manages the system, user accounts, and data.
- **Doctor**: Views patient predictions and provides medical advice.
- **User**: Submits personal health data and views prediction results.

### Disease Prediction
- Predicts heart disease risk based on patient data.
- Classifies risk levels (low, medium, high) using Gradient Boosting and Logistic Regression.
- Provides personalized insights for early diagnosis.

### View Diseases
- Displays information about heart diseases, symptoms, causes, and treatments.
- Educates users and doctors for informed decision-making.

### Lifestyle Assessment
- Allows users to input lifestyle habits (gender, age, occupation, sleep duration, quality of sleep, physical activity level, stress levels, BMI category, blood pressure, heart rate, etc.) to predict the initial chances of risk.

### Doctor Appointment Module
- Allows users to search for doctors by name, specialization, or availability.
- Displays doctor profiles with qualifications, experience, and ratings.
- Facilitates in-person and virtual consultations.

### Search Your Doctor
- Enables users to find heart specialists by location or expertise.
- Displays contact details and availability for consultations.

### Health Deals and Checkup Alerts
- Notifies users about free health checkup events and medicine discounts.

### Community Module
- Provides a platform for users, doctors, and health professionals to interact.
- Users can share experiences, ask questions, and get peer support.

### Feedback System
- Collects feedback from users and doctors about system functionality.
- Gathers suggestions for improvements.

---

## Project Features
- **Role-Based Access Control**: Separate functionalities for Admin, Doctor, and User.
- **Machine Learning Models**: Gradient Boosting and Logistic Regression for accurate predictions.
- **User-Friendly Interface**: Easy navigation for health data submission and result viewing.
- **Doctor Search and Appointment Booking**: Integrated module for finding and booking doctors.
- **Feedback Collection**: System improvement based on user suggestions.

---

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Django Framework
- **Database**: SQLite/MySQL
- **Machine Learning**: Gradient Boosting, Logistic Regression
- **Other Tools**: Python libraries (e.g., Scikit-learn, Pandas, NumPy)

---

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RiskBeat.git
   ```
2. Navigate to the project directory:
   ```bash
   cd RiskBeat
   ```
3. Create a virtual environment:
   ```bash
   python -m venv env
   ```
4. Activate the virtual environment:
   - Windows:
     ```bash
     env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source env/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Apply migrations:
   ```bash
   python manage.py migrate
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```
8. Open the browser and go to `http://127.0.0.1:8000/` to access the application.

---




