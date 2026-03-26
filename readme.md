# Disease Detection & Drug Recommendation System

## Project Overview
This Machine Learning and Django-based web application provides a comprehensive healthcare solution. It allows patients to input their symptoms to predict potential diseases and provides doctors with AI-powered drug recommendations tailored to the patient's predicted disease, age, and gender.

## Features
- **Patient Dashboard**: Patients can register, create a profile, and predict diseases based on a wide selection of symptoms.
- **Doctor Dashboard**: Doctors can review patient predictions, recommend drugs using AI, and schedule/approve appointments.
- **Machine Learning Integration**: Real-time integration of AI models that load on application start for fast and optimized inference.

## Machine Learning Model Details
The system utilizes two primary Machine Learning models:
1. **Disease Prediction Model (`decision_tree.pkl`)**
   - **Type**: Decision Tree Classifier
   - **Usage**: Takes in patient symptoms to predict the underlying disease.
   - **Training**: Trained on generic disease symptom datasets mapping occurrences of 130+ symptoms to 40+ diseases.
2. **Drug Recommendation Model (`medical_nb.pkl`)**
   - **Type**: Naive Bayes Classifier
   - **Usage**: Takes the predicted disease, along with patient age and gender, to recommend the appropriate drug.
   - **Training**: Replaced an extremely large Random Forest model (1.4GB) with this lightweight alternative (~9.9MB) to ensure the application could be deployed securely and cost-effectively without crashing cloud servers.

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript (Provides the user interface for patients and doctors).
- **Backend Framework**: Python / Django (Handles secure routing, user authentication, and API endpoints).
- **Machine Learning**: `scikit-learn`, `numpy`, `joblib` (For building, serializing, and serving the predictive models).
- **Database**: SQLite (Local Dev) / PostgreSQL (Production via `dj-database-url`).
- **Production Tools**: `gunicorn` (WSGI server), `whitenoise` (Static file serving on platforms like Render).

---

## Installation & How to Run Locally

Follow these beginner-friendly steps to get the project running on your local machine:

1. **Clone or Open the Project**:
   Open a terminal and navigate to the `healthcare` folder:
   ```bash
   cd path/to/disease-detection-and-drug-recommendation-master/healthcare
   ```

2. **Install Dependencies**:
   Install all the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Database Database Migrations**:
   Set up your local SQLite database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the Development Server**:
   Start the Django server locally:
   ```bash
   python manage.py runserver
   ```
   Open your browser and go to `http://127.0.0.1:8000`.

## How to Run the ML Models
You do not need to run the ML models manually! The Django backend automatically preloads the models (`decision_tree.pkl` and `medical_nb.pkl`) when the server starts. When you submit symptoms via the "Diagnosis" page as a patient, or click "Recommend Drug" as a doctor, the predictions are made seamlessly in the background.

## Deployment Steps (Render)
This project is configured perfectly for a free **Render.com** deployment!
1. Push this entire project repository to your GitHub account.
2. Go to [Render](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the following settings:
   - **Build Command**: `./build.sh` (or `bash build.sh`)
   - **Start Command**: `gunicorn healthcare.wsgi:application`
5. Render will automatically detect the Python environment and install `requirements.txt`.
6. Click **Deploy**. Your app will be live and your models will run without memory errors!

## Environment Variables Required (Production)
If you add a PostgreSQL database on Render, it will expose:
- `DATABASE_URL`: Add this to your Render environment variables (Render often handles this automatically if you attach a database to the web service).

## Folder Structure
```
disease-detection-and-drug-recommendation-master/
├── healthcare/                 # Main Django Project Folder
│   ├── build.sh               # Render Deployment build script
│   ├── requirements.txt       # Dependencies
│   ├── manage.py              # Django execution script
│   ├── healthcare/            # Project Settings (urls, settings.py, wsgi)
│   ├── core/                  # Main App (views, models, routes)
│   │   ├── static/            # CSS/JS Assets
│   │   ├── templates/         # HTML Files
│   ├── model/                 # Contains the .pkl Machine Learning models
```
