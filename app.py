# Updated version: uses a real Bank Marketing CSV instead of synthetic data.
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import plotly.express as px
import plotly.graph_objects as go

MONTHS = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

st.set_page_config(page_title="Customer Conversion Intelligence", page_icon="🏦", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
[data-testid="stMetricValue"] {font-size: 2rem;}
.hero {padding: 1.2rem 1.5rem; border-radius: 14px; background: linear-gradient(90deg,#14324b,#1f4f70); color: white; margin-bottom: 1.5rem;}
.hero h1 {margin-bottom: 0.2rem;}
.section-card {padding: 1rem 1.2rem; border: 1px solid rgba(128,128,128,.25); border-radius: 12px; margin-bottom: .8rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def read_bank_csv(source):
    df = pd.read_csv(source, sep=None, engine="python")
    df.columns = [str(c).strip().lower().replace(".", "_").replace(" ", "_") for c in df.columns]
    if "y" in df.columns and "subscribed" not in df.columns:
        df = df.rename(columns={"y": "subscribed"})
    if "subscribed" not in df.columns:
        raise ValueError("CSV must contain target column 'y' or 'subscribed'.")
    if df["subscribed"].dtype == object:
        df["subscribed"] = df["subscribed"].astype(str).str.strip().str.lower().map(
            {"yes": 1, "no": 0, "1": 1, "0": 0}
        )
    df = df.dropna(subset=["subscribed"]).copy()
    df["subscribed"] = df["subscribed"].astype(int)
    return df.loc[:, ~df.columns.str.contains("^unnamed", case=False, regex=True)]

default_csv = Path(__file__).parent / "bank_marketing.csv"

with st.sidebar:
    st.header("Data Source")
    uploaded_csv = st.file_uploader("Upload Bank Marketing CSV", type=["csv"])
    st.caption("Without an upload, bank_marketing.csv in the project folder is used.")

try:
    if uploaded_csv is not None:
        df = read_bank_csv(uploaded_csv)
        data_source = "Uploaded CSV"
    elif default_csv.exists():
        df = read_bank_csv(default_csv)
        data_source = "bank_marketing.csv"
    else:
        st.error("No dataset found. Upload a CSV or add bank_marketing.csv to the project.")
        st.stop()
except Exception as e:
    st.error(f"Unable to load CSV: {e}")
    st.stop()

@st.cache_resource
def train_model(data):
    features = [c for c in data.columns if c != "subscribed"]
    X, y = data[features], data["subscribed"]
    categorical = X.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric = [c for c in features if c not in categorical]
    preprocessor = ColumnTransformer([
        ("num", Pipeline([
            ("fill", SimpleImputer(strategy="median")),
            ("scale", StandardScaler())
        ]), numeric),
        ("cat", Pipeline([
            ("fill", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical)
    ])
    model = Pipeline([
        ("prep", preprocessor),
        ("rf", RandomForestClassifier(
            n_estimators=250, max_depth=14, min_samples_leaf=4,
            random_state=42, class_weight="balanced"
        ))
    ])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.2, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    return model, features, accuracy_score(y_test, model.predict(X_test)), categorical

model, FEATURES, accuracy, CATEGORICAL = train_model(df)

def probability_band(p):
    if p >= .70:
        return "High Potential", "The customer appears highly suitable for a follow-up offer.", "🟢"
    if p >= .40:
        return "Moderate Potential", "A targeted follow-up may improve the chance of conversion.", "🟡"
    return "Low Potential", "Consider a different offer, channel, or timing before further contact.", "🔴"

def fmt_pct(x):
    return f"{x*100:.1f}%"

st.markdown("""
<div class="hero">
<h1>🏦 Customer Conversion Intelligence</h1>
<div>Support smarter campaign decisions using analysis and prediction from the Bank Marketing CSV dataset.</div>
</div>
""", unsafe_allow_html=True)

st.caption(f"Data source: **{data_source}** | Records: **{len(df):,}** | Validation accuracy: **{accuracy:.1%}**")

tabs = st.tabs(["📊 Campaign Overview", "💼 Customer Segments", "📈 Campaign Trends",
               "🎓 Customer Insights", "🤖 Customer Assessment"])

with tabs[0]:
    st.header("Campaign Overview")
    total = len(df)
    successful = int(df["subscribed"].sum())
    rate = successful / total
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers Reached", f"{total:,}")
    c2.metric("Positive Responses", f"{successful:,}")
    c3.metric("Overall Conversion Rate", fmt_pct(rate))
    c4.metric("Model Validation Accuracy", f"{accuracy:.1%}")
    left, right = st.columns(2)
    with left:
        outcome = pd.DataFrame({"Outcome":["No Positive Response","Positive Response"],
                                "Customers":[total-successful, successful]})
        st.plotly_chart(px.pie(outcome, values="Customers", names="Outcome", hole=.55),
                        use_container_width=True)
    with right:
        if "poutcome" in df.columns:
            s = df.groupby("poutcome", as_index=False)["subscribed"].mean()
            s["rate"] = s["subscribed"] * 100
            fig = px.bar(s, x="poutcome", y="rate", text=s["rate"].round(1),
                         labels={"poutcome":"Previous Campaign Result","rate":"Conversion Rate (%)"})
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.header("Customer Segments")
    if "job" in df.columns:
        s = df.groupby("job", as_index=False)["subscribed"].mean().sort_values("subscribed", ascending=False)
        s["Conversion Rate (%)"] = s["subscribed"] * 100
        st.plotly_chart(px.bar(s, x="job", y="Conversion Rate (%)",
                               labels={"job":"Employment Group"}),
                        use_container_width=True)
        top = s.head(3)[["job","Conversion Rate (%)"]].copy()
        top["Conversion Rate (%)"] = top["Conversion Rate (%)"].round(1).astype(str) + "%"
        st.dataframe(top.rename(columns={"job":"Customer Segment"}),
                     use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("Campaign Trends")
    if "month" in df.columns:
        monthly = df.groupby("month", as_index=False).agg(
            Customers=("subscribed","size"),
            Positive_Responses=("subscribed","sum")
        )
        monthly["month"] = pd.Categorical(monthly["month"].astype(str).str.lower(),
                                          categories=MONTHS, ordered=True)
        monthly = monthly.sort_values("month")
        monthly["Conversion Rate (%)"] = monthly["Positive_Responses"] / monthly["Customers"] * 100
        a, b = st.columns(2)
        with a:
            st.plotly_chart(px.line(monthly, x="month", y="Conversion Rate (%)", markers=True),
                            use_container_width=True)
        with b:
            fig = go.Figure()
            fig.add_bar(name="Customers Contacted", x=monthly["month"], y=monthly["Customers"])
            fig.add_bar(name="Positive Responses", x=monthly["month"], y=monthly["Positive_Responses"])
            fig.update_layout(barmode="group")
            st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.header("Customer Insights")
    if "education" in df.columns and "campaign" in df.columns:
        edu = df.groupby("education", as_index=False).agg(
            Conversion_Rate=("subscribed","mean"),
            Average_Contacts=("campaign","mean")
        )
        edu["Conversion Rate (%)"] = edu["Conversion_Rate"] * 100
        a, b = st.columns(2)
        with a:
            st.plotly_chart(px.bar(edu, x="education", y="Conversion Rate (%)"),
                            use_container_width=True)
        with b:
            st.plotly_chart(px.bar(edu, x="education", y="Average_Contacts"),
                            use_container_width=True)

with tabs[4]:
    st.header("🤖 Customer Conversion Assessment")
    st.write("The prediction model is trained from the real CSV currently loaded by the application.")
    with st.form("customer_assessment"):
        values = {}
        for col in FEATURES:
            label = col.replace("_", " ").title()
            if col in CATEGORICAL:
                values[col] = st.selectbox(label, sorted(df[col].dropna().astype(str).unique().tolist()))
            else:
                series = pd.to_numeric(df[col], errors="coerce").dropna()
                default = float(series.median())
                if pd.api.types.is_integer_dtype(df[col]):
                    values[col] = st.number_input(label, value=int(round(default)), step=1)
                else:
                    values[col] = st.number_input(label, value=default)
        submitted = st.form_submit_button("Assess Conversion Potential", type="primary",
                                         use_container_width=True)

    if submitted:
        row = pd.DataFrame([values])[FEATURES]
        probability = float(model.predict_proba(row)[0,1])
        label, guidance, icon = probability_band(probability)
        a, b, c = st.columns(3)
        a.metric("Conversion Potential", label)
        b.metric("Estimated Positive Response", fmt_pct(probability))
        c.metric("Suggested Action", "Prioritise Follow-up" if probability >= .40 else "Review Approach")
        st.markdown(f"<div class='section-card'><h3>{icon} Recommended Next Step</h3><p>{guidance}</p></div>",
                    unsafe_allow_html=True)
        score_data = pd.DataFrame({"Assessment":["Positive response potential"],
                                   "Probability":[probability*100]})
        fig = px.bar(score_data, x="Probability", y="Assessment", orientation="h",
                     range_x=[0,100], text=score_data["Probability"].round(1))
        fig.update_traces(texttemplate="%{text}%")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Customer Conversion Intelligence | CSV-based decision-support workspace")
