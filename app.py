
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import plotly.express as px
import plotly.graph_objects as go


# Shared option lists used throughout the application
MONTHS = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
DAYS = ["mon","tue","wed","thu","fri"]

st.set_page_config(
    page_title="Customer Conversion Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Styling ----------
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
[data-testid="stMetricValue"] {font-size: 2rem;}
.hero {padding: 1.2rem 1.5rem; border-radius: 14px; background: linear-gradient(90deg,#14324b,#1f4f70); color: white; margin-bottom: 1.5rem;}
.hero h1 {margin-bottom: 0.2rem;}
.section-card {padding: 1rem 1.2rem; border: 1px solid rgba(128,128,128,.25); border-radius: 12px; margin-bottom: .8rem;}
.small-note {opacity: .78; font-size: .92rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def create_bank_data(n=12000, seed=42):
    rng = np.random.default_rng(seed)
    jobs = ["management","technician","admin.","services","retired","blue-collar",
            "entrepreneur","self-employed","housemaid","student","unemployed"]
    education = ["primary","secondary","tertiary"]
    months = MONTHS
    days = DAYS
    df = pd.DataFrame({
        "age": rng.integers(18, 76, n),
        "job": rng.choice(jobs, n),
        "marital": rng.choice(["single","married","divorced"], n, p=[.30,.58,.12]),
        "education": rng.choice(education, n, p=[.18,.50,.32]),
        "default": rng.choice(["no","yes"], n, p=[.985,.015]),
        "housing": rng.choice(["no","yes"], n, p=[.46,.54]),
        "loan": rng.choice(["no","yes"], n, p=[.84,.16]),
        "month": rng.choice(months, n),
        "day_of_week": rng.choice(days, n),
        "duration": rng.integers(30, 1200, n),
        "campaign": rng.integers(1, 12, n),
        "pdays": rng.choice([999,1,2,3,4,5,7,10], n, p=[.72,.04,.04,.04,.04,.04,.04,.04]),
        "previous": rng.integers(0, 8, n),
        "poutcome": rng.choice(["nonexistent","failure","success"], n, p=[.78,.14,.08]),
        "emp_var_rate": rng.normal(0.5, 1.7, n),
        "cons_price_idx": rng.normal(93.5, .55, n),
        "cons_conf_idx": rng.normal(-40, 4.5, n),
        "euribor3m": rng.uniform(.6, 5.2, n),
        "nr_employed": rng.normal(5190, 80, n)
    })
    logit = (
        -2.0
        + .018*(df["age"]-40)
        + .0025*(df["duration"]-300)
        - .13*(df["campaign"]-1)
        + .45*(df["poutcome"]=="success").astype(int)
        + .22*(df["job"]=="student").astype(int)
        + .18*(df["job"]=="retired").astype(int)
        + .25*(df["education"]=="tertiary").astype(int)
        - .28*(df["housing"]=="yes").astype(int)
        - .32*(df["loan"]=="yes").astype(int)
        - .65*(df["default"]=="yes").astype(int)
        - .18*(df["previous"]==0).astype(int)
    )
    p = 1/(1+np.exp(-logit))
    df["subscribed"] = (rng.random(n) < p).astype(int)
    return df

@st.cache_resource
def train_model(df):
    features = [c for c in df.columns if c != "subscribed"]
    X, y = df[features], df["subscribed"]
    categorical = X.select_dtypes(include="object").columns.tolist()
    numeric = [c for c in features if c not in categorical]
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
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
    score = accuracy_score(y_test, model.predict(X_test))
    return model, features, score

df = create_bank_data()
model, FEATURES, accuracy = train_model(df)

def probability_band(p):
    if p >= .70: return "High Potential", "The customer appears highly suitable for a follow-up offer.", "🟢"
    if p >= .40: return "Moderate Potential", "A targeted follow-up may improve the chance of conversion.", "🟡"
    return "Low Potential", "Consider a different offer, channel, or timing before further contact.", "🔴"

def fmt_pct(x): return f"{x*100:.1f}%"

# ---------- Header ----------
st.markdown("""
<div class="hero">
<h1>🏦 Customer Conversion Intelligence</h1>
<div>Support smarter campaign decisions by identifying customers who may respond positively to a banking offer.</div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "📊 Campaign Overview",
    "💼 Customer Segments",
    "📈 Campaign Trends",
    "🎓 Customer Insights",
    "🤖 Customer Assessment"
])

# ---------- Overview ----------
with tabs[0]:
    st.header("Campaign Overview")
    total = len(df)
    successful = int(df["subscribed"].sum())
    rate = successful / total
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Customers Reached", f"{total:,}")
    c2.metric("Positive Responses", f"{successful:,}")
    c3.metric("Overall Conversion Rate", fmt_pct(rate))
    c4.metric("Assessment Readiness", "Available")

    left,right = st.columns(2)
    with left:
        st.subheader("Campaign Response")
        outcome = pd.DataFrame({
            "Outcome":["No Positive Response","Positive Response"],
            "Customers":[total-successful, successful]
        })
        fig = px.pie(outcome, values="Customers", names="Outcome", hole=.55)
        fig.update_layout(margin=dict(l=0,r=0,t=20,b=0), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Response by Previous Campaign Outcome")
        s = df.groupby("poutcome", as_index=False)["subscribed"].mean()
        s["rate"] = s["subscribed"]*100
        fig = px.bar(s, x="poutcome", y="rate", text=s["rate"].round(1),
                     labels={"poutcome":"Previous Campaign Result","rate":"Conversion Rate (%)"})
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ---------- Job ----------
with tabs[1]:
    st.header("Customer Segments")
    st.caption("Compare campaign response across customer employment groups.")
    s = df.groupby("job", as_index=False)["subscribed"].mean().sort_values("subscribed", ascending=False)
    s["Conversion Rate (%)"] = s["subscribed"]*100
    fig = px.bar(s, x="job", y="Conversion Rate (%)",
                 labels={"job":"Employment Group"})
    fig.update_layout(xaxis_tickangle=-35, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recommended Segment Focus")
    top = s.head(3)[["job","Conversion Rate (%)"]].copy()
    top["Conversion Rate (%)"] = top["Conversion Rate (%)"].round(1).astype(str)+"%"
    st.dataframe(top.rename(columns={"job":"Customer Segment"}), use_container_width=True, hide_index=True)

# ---------- Monthly ----------
with tabs[2]:
    st.header("Campaign Trends")
    st.caption("Review changes in campaign activity and customer response over time.")
    month_order = MONTHS
    monthly = df.groupby("month", as_index=False).agg(
        Customers=("subscribed","size"),
        Positive_Responses=("subscribed","sum")
    )
    monthly["month"] = pd.Categorical(monthly["month"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("month")
    monthly["Conversion Rate (%)"] = monthly["Positive_Responses"]/monthly["Customers"]*100

    a,b = st.columns(2)
    with a:
        fig = px.line(monthly, x="month", y="Conversion Rate (%)", markers=True,
                      labels={"month":"Month"})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = go.Figure()
        fig.add_bar(name="Customers Contacted", x=monthly["month"], y=monthly["Customers"])
        fig.add_bar(name="Positive Responses", x=monthly["month"], y=monthly["Positive_Responses"])
        fig.update_layout(barmode="group", legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

# ---------- Education ----------
with tabs[3]:
    st.header("Customer Insights")
    st.caption("Understand response patterns using customer profile characteristics.")
    left,right = st.columns(2)
    edu = df.groupby("education", as_index=False).agg(
        Conversion_Rate=("subscribed","mean"),
        Average_Contacts=("campaign","mean")
    )
    edu["Conversion Rate (%)"] = edu["Conversion_Rate"]*100
    with left:
        fig = px.bar(edu, x="education", y="Conversion Rate (%)",
                     labels={"education":"Education Level"})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(edu, x="education", y="Average_Contacts",
                     labels={"education":"Education Level","Average_Contacts":"Average Contacts"})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ---------- Prediction ----------
with tabs[4]:
    st.header("🤖 Customer Conversion Assessment")
    st.write("Enter the available customer and campaign information to receive a decision-support assessment for follow-up planning.")
    st.info("Use information already available through approved customer and campaign records. The result is a decision-support indicator and should be considered together with normal banking policies and staff judgment.")

    with st.form("customer_assessment"):
        st.subheader("Customer Profile")
        c1,c2,c3 = st.columns(3)
        age = c1.number_input("Customer age", min_value=18, max_value=100, value=40)
        job = c2.selectbox("Employment category", sorted(df.job.unique()))
        marital = c3.selectbox("Marital status", ["single","married","divorced"])

        c1,c2,c3 = st.columns(3)
        education = c1.selectbox("Education level", ["primary","secondary","tertiary"])
        default = c2.selectbox("Known credit default status", ["no","yes"])
        housing = c3.selectbox("Housing loan", ["no","yes"])

        c1,c2,c3 = st.columns(3)
        loan = c1.selectbox("Personal loan", ["no","yes"])
        month = c2.selectbox("Planned contact month", MONTHS)
        day_of_week = c3.selectbox("Planned contact day", DAYS)

        st.subheader("Campaign History")
        c1,c2,c3 = st.columns(3)
        duration = c1.number_input("Expected or recorded interaction duration (seconds)", min_value=0, max_value=7200, value=300)
        campaign = c2.number_input("Contacts in the current campaign", min_value=1, max_value=50, value=1)
        pdays = c3.number_input("Days since previous contact (999 = no previous contact)", min_value=0, max_value=999, value=999)

        c1,c2,c3 = st.columns(3)
        previous = c1.number_input("Previous contacts before this campaign", min_value=0, max_value=50, value=0)
        poutcome = c2.selectbox("Previous campaign result", ["nonexistent","failure","success"])
        st.caption("Use the closest available campaign information. Fields can be aligned with your bank's internal customer management process.")

        st.subheader("Current Market Indicators")
        c1,c2,c3,c4,c5 = st.columns(5)
        emp_var_rate = c1.number_input("Employment variation indicator", value=1.1, format="%.2f")
        cons_price_idx = c2.number_input("Consumer price indicator", value=93.75, format="%.3f")
        cons_conf_idx = c3.number_input("Consumer confidence indicator", value=-41.8, format="%.1f")
        euribor3m = c4.number_input("Interest rate indicator", value=4.86, format="%.3f")
        nr_employed = c5.number_input("Employment indicator", value=5191.0, format="%.1f")

        submitted = st.form_submit_button("Assess Conversion Potential", type="primary", use_container_width=True)

    if submitted:
        row = pd.DataFrame([{
            "age":age,"job":job,"marital":marital,"education":education,
            "default":default,"housing":housing,"loan":loan,"month":month,
            "day_of_week":day_of_week,"duration":duration,"campaign":campaign,
            "pdays":pdays,"previous":previous,"poutcome":poutcome,
            "emp_var_rate":emp_var_rate,"cons_price_idx":cons_price_idx,
            "cons_conf_idx":cons_conf_idx,"euribor3m":euribor3m,
            "nr_employed":nr_employed
        }])[FEATURES]
        probability = float(model.predict_proba(row)[0,1])
        label, guidance, icon = probability_band(probability)

        st.divider()
        st.subheader("Assessment Result")
        a,b,c = st.columns([1,1,1])
        a.metric("Conversion Potential", label)
        b.metric("Estimated Positive Response", fmt_pct(probability))
        c.metric("Suggested Action", "Prioritise Follow-up" if probability >= .40 else "Review Approach")

        st.markdown(f"""
        <div class="section-card">
        <h3>{icon} Recommended Next Step</h3>
        <p>{guidance}</p>
        </div>
        """, unsafe_allow_html=True)

        score_data = pd.DataFrame({"Assessment":["Positive response potential"],"Probability":[probability*100]})
        fig = px.bar(score_data, x="Probability", y="Assessment", orientation="h",
                     range_x=[0,100], text=score_data["Probability"].round(1),
                     labels={"Probability":"Estimated probability (%)"})
        fig.update_traces(texttemplate="%{text}%")
        fig.update_layout(showlegend=False, height=180)
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Assessment input summary"):
            summary = row.copy()
            summary.columns = [x.replace("_"," ").title() for x in summary.columns]
            st.dataframe(summary, use_container_width=True, hide_index=True)

st.divider()
st.caption("Customer Conversion Intelligence | Decision-support workspace for campaign planning and customer follow-up")
