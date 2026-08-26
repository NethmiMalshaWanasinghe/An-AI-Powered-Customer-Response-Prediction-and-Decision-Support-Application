# Customer Conversion Intelligence

## 1. Project Overview
Customer Conversion Intelligence is an end-to-end AI decision-support application designed for banking marketing and customer engagement teams. The application analyzes customer and campaign characteristics and estimates the likelihood that a customer will respond positively to a banking offer.

The application provides:
- Campaign-level performance overview
- Customer segment analysis
- Monthly campaign trend analysis
- Customer insight analysis
- Individual customer conversion assessment
- A recommended follow-up action based on the predicted probability

> **Important:** The application is a decision-support prototype. Predictions should support, not replace, approved banking policies, compliance requirements, and staff judgment.

---

# 2. Assignment Requirement Mapping

| Requirement | Implementation in this project |
|---|---|
| 1. Identify an AI Use Case | Predict customer conversion potential for banking campaign follow-up |
| 2. End-to-End AI Application | Streamlit interface + data generation + preprocessing + Random Forest training + prediction + visualization |
| 3. Cloud Deployment | Docker-ready application with deployment instructions for Streamlit Community Cloud or any Docker-compatible cloud platform |
| 4. Containerization | Dockerfile, .dockerignore and docker-compose.yml |
| 5. Source Code Repository | Project structure ready for GitHub/GitLab |
| 6. README Documentation | This document |

---

# 3. AI Use Case

## Business Problem
Bank marketing teams often contact many customers during campaigns, but customer response rates can be low. A decision-support system can help staff prioritize customers who show a higher estimated probability of responding positively.

## AI Objective
Build a binary classification model that estimates whether a customer is likely to provide a positive response.

## Input Categories
The application uses customer profile, campaign history, previous campaign outcomes, and selected market indicators.

## Output
- Estimated positive-response probability
- Conversion potential category: High, Moderate, or Low
- Suggested next action for follow-up planning

## Selected AI Model
A **Random Forest Classifier** is used because it can handle nonlinear relationships and a mixture of numerical and categorical features when combined with a preprocessing pipeline.

---

# 4. End-to-End Application Architecture

```text
User Input
    |
    v
Streamlit Web Interface
    |
    v
Input Validation and Feature Preparation
    |
    v
Preprocessing Pipeline
(Standard Scaling + One-Hot Encoding)
    |
    v
Random Forest Classification Model
    |
    v
Probability Prediction
    |
    +-------------------------+
    |                         |
    v                         v
Conversion Potential     Recommended Action
    |
    v
Decision-Support Dashboard
```

---

# 5. Project Structure

```text
Customer_Conversion_Intelligence_Assignment/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

---

# 6. Local Installation and Execution

## Prerequisites
- Python 3.10 or later
- pip

## Steps

```bash
git clone <YOUR-REPOSITORY-URL>
cd Customer_Conversion_Intelligence_Assignment
python -m venv .venv
```

Activate the virtual environment:

### Windows PowerShell
```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt
```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit, normally `http://localhost:8501`.

---

# 7. Containerization

## Build the Docker Image

```bash
docker build -t customer-conversion-intelligence .
```

## Run the Container

```bash
docker run -p 8501:8501 customer-conversion-intelligence
```

Then open `http://localhost:8501`.

## Run with Docker Compose

```bash
docker compose up --build
```

To stop the application:

```bash
docker compose down
```

---

# 8. Cloud Deployment Options

## Option A: Streamlit Community Cloud
1. Create a GitHub repository and push this project.
2. Sign in to Streamlit Community Cloud.
3. Select **Create app**.
4. Select the GitHub repository and branch.
5. Set the main file path to `app.py`.
6. Deploy.

## Option B: Docker-Compatible Cloud Platform
Use the included Dockerfile with a cloud provider that supports container deployment. The container exposes port `8501` and starts the application with:

```text
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
```

For production deployment, configure platform-specific authentication, HTTPS, secrets management, logging, and access controls.

---

# 9. Source Code Repository Setup

Create an empty repository on GitHub, then run:

```bash
git init
git add .
git commit -m "Initial commit - Customer Conversion Intelligence AI application"
git branch -M main
git remote add origin <YOUR-REPOSITORY-URL>
git push -u origin main
```

Do not commit passwords, API keys, customer data, or other sensitive information.

---

# 10. Technology Stack

- **Python** – application development
- **Streamlit** – interactive web interface
- **Pandas and NumPy** – data processing
- **Scikit-learn** – preprocessing, model training, and prediction
- **Random Forest Classifier** – machine learning model
- **Plotly** – interactive visualizations
- **Docker** – containerization
- **Git/GitHub** – source code management

---

# 11. Model Workflow

1. Customer and campaign features are collected through the web interface.
2. Categorical features are transformed using One-Hot Encoding.
3. Numerical features are standardized.
4. The processed features are passed to the Random Forest model.
5. The model produces a probability of positive response.
6. The probability is converted into a High, Moderate, or Low potential category.
7. The application displays a suggested follow-up action.

---

# 12. Limitations and Future Improvements

Current prototype limitations:
- The application uses generated demonstration data for the included standalone version.
- The model is trained when the application starts and is not connected to a production banking data source.
- Predictions are decision-support indicators rather than automated decisions.

Possible future improvements:
- Secure integration with approved bank data sources
- Model persistence and scheduled retraining
- Model monitoring and drift detection
- Authentication and role-based access control
- Explainable AI features such as SHAP
- API-based architecture for separating frontend and model services
- Audit logging and compliance controls

---

# 13. Responsible AI Considerations

A banking deployment should include data protection, access control, fairness testing, human oversight, monitoring, and compliance review. The system should not make fully automated high-impact decisions without appropriate governance and approval.

---

# 14. Demonstration Checklist

For the assignment demonstration:

1. Run the application locally.
2. Show the campaign dashboard tabs.
3. Open **Customer Assessment**.
4. Enter customer and campaign information.
5. Click **Assess Conversion Potential**.
6. Explain the prediction probability, potential category, and recommended action.
7. Build and run the application using Docker.
8. Show the GitHub repository.
9. Deploy the same application to a cloud platform and demonstrate the public application URL.
