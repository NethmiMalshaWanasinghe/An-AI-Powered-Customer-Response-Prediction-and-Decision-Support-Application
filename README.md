# Customer Conversion Intelligence

An end-to-end AI-powered decision-support application that predicts the
likelihood of a customer responding positively to a banking marketing
campaign.

## Live Application

**Deployment:** https://customer-conversion-ai.onrender.com

## 1. Problem Statement

Bank marketing campaigns can involve contacting thousands of customers,
while only a relatively small proportion may respond positively.
Contacting every customer with the same priority can lead to inefficient
use of time and campaign resources.

This project uses machine learning to estimate a customer's probability
of giving a positive response to a banking offer. The prediction is
converted into a **High**, **Moderate**, or **Low** conversion potential
category and paired with a suggested follow-up action.

> **Note:** This is a decision-support prototype. Predictions are
> intended to support human decision-making and should not replace
> organisational policies, compliance requirements, or professional
> judgement.

## 2. Use Case

The application helps marketing and customer engagement teams to:

-   Identify customers with a higher estimated probability of positive
    response.
-   Explore customer segments and campaign outcomes.
-   Analyse campaign trends and customer characteristics.
-   Assess an individual customer using demographic, campaign, and
    economic information.
-   Prioritise follow-up activities using AI-generated probability
    estimates.

## 3. Solution Overview

``` text
Bank Marketing CSV Dataset
          |
          v
Data Loading and Validation
          |
          v
Data Cleaning and Feature Preparation
          |
          v
Train / Validation Split
          |
          v
Preprocessing Pipeline
(Numerical + Categorical Features)
          |
          v
Random Forest Classifier
          |
          v
Probability Prediction
          |
          +---------------------------+
          |                           |
          v                           v
Conversion Potential          Suggested Action
          |
          v
Streamlit Decision-Support Dashboard
```

The application loads the real CSV dataset, prepares the features,
trains the model, and uses the trained model to generate predictions for
individual customer assessments.

## 4. Dataset

The project uses the **Bank Marketing dataset** included in this
repository:

``` text
bank_marketing.csv
```

The current application dataset contains **41,184 records**.

The dataset includes:

-   **Customer profile:** age, job, marital status, education.
-   **Financial information:** default, housing loan, personal loan.
-   **Campaign information:** contact month, day of week, campaign
    contacts, duration.
-   **Previous campaign information:** previous contacts and previous
    outcome.
-   **Economic indicators:** employment variation rate, consumer price
    index, consumer confidence index, Euribor rate, and number of
    employees.
-   **Target variable:** positive or negative campaign response.

The dataset is based on the publicly available **Bank Marketing**
dataset. The CSV required by the application is included in this
repository.

## 5. AI/ML Approach

### Model

A **Random Forest Classifier** is used for binary classification.

### Preprocessing

The machine-learning workflow includes:

-   One-Hot Encoding for categorical variables.
-   Preparation of numerical variables for model input.
-   Training and validation of the classifier.
-   Probability prediction for individual customer assessments.

### Prediction Output

The application produces:

1.  **Estimated Positive Response** -- predicted probability as a
    percentage.
2.  **Conversion Potential** -- High, Moderate, or Low.
3.  **Suggested Action** -- a recommendation based on the estimated
    probability.

### Validation

The current application displays a model validation accuracy of
approximately **86.7%** for the dataset and validation configuration
used by the application.

> Validation performance can change if the dataset, random split, model
> configuration, or preprocessing is changed.

## 6. Application Features

### Campaign Overview

Provides:

-   Total customers reached.
-   Number of positive responses.
-   Overall conversion rate.
-   Model validation accuracy.
-   Campaign response distribution.
-   Response analysis based on previous campaign outcome.

### Customer Segments

Explores customer groups and response patterns.

### Campaign Trends

Provides visual analysis of campaign response patterns and trends.

### Customer Insights

Displays insights derived from the dataset.

### Customer Assessment

Allows users to enter customer and campaign attributes and receive:

-   Estimated positive response probability.
-   Conversion potential category.
-   Recommended next step.

Example output:

``` text
Conversion Potential: High Potential
Estimated Positive Response: 85.6%
Suggested Action: Prioritise Follow-up
```

## 7. Application Architecture

``` text
+-----------------------+
|       User            |
+-----------+-----------+
            |
            v
+-----------------------+
|  Streamlit Web App    |
|       app.py          |
+-----------+-----------+
            |
            v
+-----------------------+
| bank_marketing.csv    |
| Data Loading          |
+-----------+-----------+
            |
            v
+-----------------------+
| Preprocessing         |
| Feature Preparation   |
+-----------+-----------+
            |
            v
+-----------------------+
| Random Forest Model   |
+-----------+-----------+
            |
            v
+-----------------------+
| Prediction +          |
| Decision Support      |
+-----------------------+
```

## 8. Technology Stack

  -----------------------------------------------------------------------
  Technology                          Purpose
  ----------------------------------- -----------------------------------
  Python                              Application and machine-learning
                                      development

  Streamlit                           Interactive web application
                                      interface

  Pandas                              Data loading and processing

  NumPy                               Numerical operations

  Scikit-learn                        Preprocessing, model training,
                                      validation, and prediction

  Random Forest                       Classification model

  Plotly                              Interactive visualisation

  Docker                              Application containerisation

  Render                              Cloud deployment

  GitHub                              Source code repository and version
                                      control
  -----------------------------------------------------------------------

## 9. Project Structure

``` text
An-AI-Powered-Customer-Response-Prediction-and-Decision-Support-Application/
│
├── app.py
├── bank_marketing.csv
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## 10. Local Setup Instructions

### Prerequisites

-   Python 3.10 or later
-   pip

### Clone the Repository

``` bash
git clone https://github.com/NethmiMalshaWanasinghe/An-AI-Powered-Customer-Response-Prediction-and-Decision-Support-Application.git
cd An-AI-Powered-Customer-Response-Prediction-and-Decision-Support-Application
```

### Create a Virtual Environment

``` bash
python -m venv .venv
```

### Activate the Environment

**Windows PowerShell**

``` powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

``` cmd
.venv\Scripts\activate
```

### Install Dependencies

``` bash
pip install -r requirements.txt
```

### Run the Application

``` bash
streamlit run app.py
```

Open the local address displayed by Streamlit, normally:

``` text
http://localhost:8501
```

## 11. How to Use the Application

1.  Open the application.
2.  Review the **Campaign Overview** dashboard.
3.  Explore **Customer Segments**, **Campaign Trends**, and **Customer
    Insights**.
4.  Open **Customer Assessment**.
5.  Enter the required customer, campaign, previous-contact, and
    economic information.
6.  Click **Assess Conversion Potential**.
7.  Review the predicted positive-response probability.
8.  Review the conversion potential category and suggested action.

## 12. Cloud Deployment

The application is deployed on **Render**.

The deployed version is:

https://customer-conversion-ai.onrender.com

## 13. Docker Instructions

### Build the Docker Image

``` bash
docker build -t customer-conversion-intelligence .
```

### Run the Container

``` bash
docker run -p 8501:8501 customer-conversion-intelligence
```

Then open:

``` text
http://localhost:8501
```

### Run with Docker Compose

``` bash
docker compose up --build
```

To stop the application:

``` bash
docker compose down
```

## 14. Assignment Requirement Coverage

  -----------------------------------------------------------------------
  Assignment Requirement              Implementation
  ----------------------------------- -----------------------------------
  AI Use Case                         Banking customer response and
                                      conversion prediction

  End-to-End AI Application           Streamlit interface, CSV data
                                      loading, preprocessing, model
                                      training, prediction, and
                                      visualisation

  Cloud Deployment                    Application deployed on Render

  Containerisation                    Dockerfile and Docker Compose
                                      configuration included

  Public Source Repository            Project maintained in a public
                                      GitHub repository

  Dataset                             `bank_marketing.csv` included in
                                      the repository

  Documentation                       Comprehensive README with setup,
                                      architecture, AI approach, usage,
                                      deployment, and Docker instructions
  -----------------------------------------------------------------------

## 15. Limitations and Future Improvements

Current limitations:

-   The model is trained from the dataset available to the application.
-   The application is a prototype rather than a production banking
    system.
-   Prediction quality depends on the quality and representativeness of
    the dataset.
-   Production authentication, monitoring, and model-drift detection are
    not currently implemented.

Future improvements:

-   Model persistence and scheduled retraining.
-   Hyperparameter optimisation and comparison with additional models.
-   Explainable AI using techniques such as SHAP.
-   Model monitoring and drift detection.
-   Authentication and role-based access control.
-   Integration with approved enterprise data sources.
-   Audit logging and governance controls.
-   API-based separation of frontend and machine-learning services.

## 16. Responsible AI Considerations

A real-world banking implementation should include:

-   Data privacy and protection controls.
-   Access control and secure handling of customer information.
-   Fairness and bias testing.
-   Human oversight.
-   Ongoing model monitoring.
-   Compliance with applicable organisational and regulatory
    requirements.

The application should be used as a **decision-support tool**, not as an
uncontrolled automated decision-making system.

## 17. Author

**Nethmi Malsha Wanasinghe**

MSc Assignment -- End-to-End AI Application Development and Cloud
Deployment
