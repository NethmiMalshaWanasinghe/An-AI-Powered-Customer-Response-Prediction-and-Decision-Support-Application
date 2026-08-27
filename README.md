# 🏦 Customer Conversion Intelligence

An end-to-end AI-powered customer response prediction and decision-support application that analyses bank marketing campaign data and helps identify customers with a higher probability of a positive response.

The application combines **data exploration, customer segmentation, campaign analysis, machine learning prediction, and decision-support recommendations** in an interactive Streamlit dashboard.

---

## 📌 Project Overview

Marketing campaigns often involve contacting a large number of customers with limited resources. This project uses machine learning to estimate the likelihood that a customer will provide a positive response and presents the results through an interactive decision-support interface.

The application enables users to:

- Explore campaign-level performance
- Analyse customer segments
- Identify trends in marketing campaigns
- Generate customer insights
- Enter customer and campaign characteristics
- Predict the estimated probability of a positive response
- Categorise conversion potential
- Receive a recommended next action based on the prediction

---

## ✨ Key Features

### 📊 Campaign Overview
Provides a high-level view of the dataset and campaign performance, including:

- Total customers reached
- Number of positive responses
- Overall conversion rate
- Model validation accuracy
- Response distribution
- Campaign performance visualisations
<img width="1905" height="952" alt="image" src="https://github.com/user-attachments/assets/ca8fe61f-fc0b-4c7e-bfbe-20a350d099a4" />

### 👥 Customer Segments
Allows users to explore how customer characteristics relate to campaign outcomes.
<img width="1916" height="967" alt="image" src="https://github.com/user-attachments/assets/71f71eea-2d16-4bfe-b577-e09e961609c3" />

### 📈 Campaign Trends
Visualises campaign-related patterns and response behaviour to support marketing analysis.
<img width="1862" height="942" alt="image" src="https://github.com/user-attachments/assets/07ad9a76-0d24-4aa6-b462-723ebc70f089" />

### 🎓 Customer Insights
Provides data-driven insights from the available customer and campaign information.
<img width="1887" height="951" alt="image" src="https://github.com/user-attachments/assets/f6c44c56-7999-4c57-bf6f-40351fb65e5c" />

### 🎯 Customer Conversion Assessment
Users can enter customer and campaign attributes such as:

- Age
- Job
- Marital status
- Education
- Default status
- Housing loan
- Personal loan
- Month
- Day of week
- Contact duration
- Campaign contacts
- Previous campaign contacts
- Previous outcome
- Employment variation rate
- Consumer price index
- Consumer confidence index
- Euribor 3-month rate
- Number of employees

The application then generates:

- **Estimated Positive Response Probability**
- **Conversion Potential Classification**
- **Suggested Action**
- **Recommended Next Step**
- A visual representation of the prediction result
<img width="1912" height="962" alt="image" src="https://github.com/user-attachments/assets/f7cbd5c0-6822-48d6-9dde-f8e1bfc3bf17" />

---

## 🧠 Machine Learning Approach

The prediction component is trained using the Bank Marketing dataset currently loaded by the application.

The workflow includes:

1. Loading the dataset
2. Preparing numerical and categorical features
3. Applying preprocessing and feature transformation
4. Training the classification model
5. Evaluating model performance using validation data
6. Using the trained model to generate predictions for new customer inputs
7. Converting the prediction probability into an interpretable conversion potential level

The application displays a validation accuracy of approximately **86.7%** for the model configuration currently deployed.

> **Note:** Model performance can change if the dataset, preprocessing steps, train/test split, random state, or model configuration is modified.

---

## 🚦 Decision-Support Logic

The predicted probability is translated into an actionable recommendation.

### High Potential
Customers with a high estimated probability of responding positively are prioritised for follow-up.

**Suggested action:** `Prioritise Follow-up`

### Moderate Potential
Customers with a medium estimated probability may require a more targeted approach.

**Suggested action:** `Optimise Approach`

### Low Potential
Customers with a low estimated probability may benefit from a different offer, channel, or timing.

**Suggested action:** `Review Approach`

This layer helps transform a machine learning prediction into information that can support practical marketing decisions.

---

## 📂 Dataset

This project uses the **Bank Marketing** dataset from the UCI Machine Learning Repository.

The dataset is related to direct marketing campaigns of a Portuguese banking institution. The classification objective is to predict whether a client will subscribe to a term deposit.

### Dataset used in this project

- **File:** `bank_marketing.csv`
- **Records used by the application:** 41,184
- **Features:** Customer, campaign, and socio-economic attributes
- **Target:** Campaign outcome / positive response

### Dataset source

UCI Machine Learning Repository – Bank Marketing Dataset:

https://archive.ics.uci.edu/dataset/222/bank-marketing

### Dataset citation

Moro, S., Rita, P., & Cortez, P. (2014). *Bank Marketing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application and dashboard |
| Pandas | Data loading and manipulation |
| NumPy | Numerical processing |
| Scikit-learn | Machine learning and preprocessing |
| Matplotlib / Plotly | Data visualisation |
| Docker | Application containerisation |
| Render | Cloud deployment |
| GitHub | Source code version control |

---

## 📁 Project Structure

```text
An-AI-Powered-Customer-Response-Prediction-and-Decision-Support-Application/
│
├── app.py                 # Main Streamlit application
├── bank_marketing.csv     # Dataset used by the application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore rules
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

---

## 🚀 Running the Application Locally

### 1. Clone the repository

```bash
git clone https://github.com/NethmiMalshaWanasinghe/An-AI-Powered-Customer-Response-Prediction-and-Decision-Support-Application.git
```

### 2. Move into the project directory

```bash
cd An-AI-Powered-Customer-Response-Prediction-and-Decision-Support-Application
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Or on macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## 🐳 Running with Docker

### Build the Docker image

```bash
docker build -t customer-conversion-intelligence .
```

### Run the container

```bash
docker run -p 8501:8501 customer-conversion-intelligence
```

Then open:

```text
http://localhost:8501
```

### Using Docker Compose

If Docker Compose is configured for the project, run:

```bash
docker-compose up --build
```

---

## ☁️ Deployment

The application has been deployed using Render.

### Live Application

https://customer-conversion-ai.onrender.com

> The deployed service may take some time to respond after a period of inactivity because it is hosted on a free-tier service.

### Docker Image

https://hub.docker.com/r/wanasinghe/customer-conversion-intelligence

---

## 🖥️ Application Workflow

```text
Bank Marketing Dataset
        │
        ▼
Data Loading & Preparation
        │
        ▼
Exploratory Analysis & Visualisation
        │
        ▼
Feature Preprocessing
        │
        ▼
Machine Learning Classification Model
        │
        ▼
Positive Response Probability
        │
        ▼
Conversion Potential Classification
        │
        ▼
Decision-Support Recommendation
```

---

## 📊 Example Output

For each customer assessment, the application provides an estimated probability of a positive response.

Example result:

```text
Conversion Potential: High Potential
Estimated Positive Response: 85.6%
Suggested Action: Prioritise Follow-up

Recommended Next Step:
The customer appears highly suitable for a follow-up offer.
```

The recommendation changes according to the model's estimated response probability.

---

## 🎯 Project Contribution

This project demonstrates how a machine learning model can be integrated into a practical decision-support application.

Rather than presenting only a prediction, the system also:

- Communicates the predicted probability
- Converts the result into understandable potential categories
- Provides an actionable recommendation
- Supports exploratory analysis through interactive dashboard sections
- Packages the application for reproducible deployment using Docker

The focus is therefore on connecting **data analysis → machine learning prediction → decision support → user-facing application**.

---

## ⚠️ Limitations

- The application is trained on a historical bank marketing dataset.
- The prediction represents patterns learned from the available dataset and should not be treated as a guaranteed real-world outcome.
- Model performance may vary with different preprocessing, model parameters, validation strategies, or datasets.
- The decision-support recommendations are based on probability thresholds implemented in the application.
- The system is intended as an analytical and educational decision-support tool.

---

## 🔮 Future Improvements

Possible future enhancements include:

- Comparing multiple machine learning algorithms
- Adding precision, recall, F1-score, ROC-AUC, and confusion matrix reporting
- Hyperparameter optimisation
- Feature importance and explainability using SHAP or similar methods
- Model persistence and versioning
- Real-time or API-based prediction
- User authentication
- Prediction history
- Exporting assessment reports
- Automated model retraining
- More advanced recommendation strategies

---

## 👩‍💻 Author

**Nethmi Malsha Wanasinghe**

GitHub:  
https://github.com/NethmiMalshaWanasinghe

---

## 📄 License

This project is intended for educational and academic purposes unless a separate license is added to the repository.

---

## 🙏 Acknowledgements

- UCI Machine Learning Repository for providing the Bank Marketing dataset
- The dataset creators: S. Moro, P. Rita, and P. Cortez
- Streamlit, Scikit-learn, Docker, Render, and the Python open-source community
