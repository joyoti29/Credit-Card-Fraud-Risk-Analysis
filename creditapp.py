import streamlit as st
import pandas as pd
import plotly.express as px

# Page setting
st.set_page_config(
    page_title="Credit Card Fraud Risk Dashboard",
    layout="wide"
)

# Load data
df = pd.read_csv("Credit Card Fraud Risk Analysis.csv")

# Convert date column
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

# Create month column
df["Month"] = df["Transaction Date"].dt.to_period("M").astype(str)

# Create Fraud Status column
df["Fraud Status"] = df["IsFraud"].apply(
    lambda x: "Fraud" if x == 1 else "Non-Fraud"
)

# Dashboard title
st.title("Credit Card Fraud Risk Analysis Dashboard")
st.write("Monitoring fraud transactions, fraud amount, risky categories, states, card types, and merchants.")

# -----------------------------
# Slicers
# -----------------------------
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    selected_state = st.multiselect(
        "Select State",
        options=df["State"].unique(),
        default=df["State"].unique()
    )

with col_filter2:
    selected_category = st.multiselect(
        "Select Transaction Category",
        options=df["Transaction Category"].unique(),
        default=df["Transaction Category"].unique()
    )

# Filter data
filtered_df = df[
    (df["State"].isin(selected_state)) &
    (df["Transaction Category"].isin(selected_category))
]

# -----------------------------
# KPI Cards
# -----------------------------
total_transactions = filtered_df.shape[0]
fraud_transactions = filtered_df["IsFraud"].sum()
fraud_rate = fraud_transactions / total_transactions if total_transactions > 0 else 0
fraud_amount = filtered_df.loc[
    filtered_df["IsFraud"] == 1,
    "Transaction Amount (INR)"
].sum()
avg_fraud_score = filtered_df["Fraud Score"].mean()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("Total Transactions", f"{total_transactions:,}")
kpi2.metric("Fraud Transactions", f"{fraud_transactions:,}")
kpi3.metric("Fraud Rate", f"{fraud_rate:.2%}")
kpi4.metric("Fraud Amount", f"₹{fraud_amount:,.0f}")
kpi5.metric("Avg Fraud Score", f"{avg_fraud_score:.2f}")

st.divider()

# -----------------------------
# Chart 1: Monthly Fraud Rate Trend
# -----------------------------
monthly_fraud = filtered_df.groupby("Month").agg(
    total_transactions=("Transaction ID", "count"),
    fraud_transactions=("IsFraud", "sum")
).reset_index()

monthly_fraud["Fraud Rate"] = (
    monthly_fraud["fraud_transactions"] /
    monthly_fraud["total_transactions"]
) * 100

fig1 = px.line(
    monthly_fraud,
    x="Month",
    y="Fraud Rate",
    markers=True,
    title="Monthly Fraud Rate Trend"
)

# -----------------------------
# Chart 2: Fraud vs Non-Fraud Donut
# -----------------------------
fraud_status = filtered_df["Fraud Status"].value_counts().reset_index()
fraud_status.columns = ["Fraud Status", "Count"]

fig2 = px.pie(
    fraud_status,
    names="Fraud Status",
    values="Count",
    hole=0.5,
    title="Fraud vs Non-Fraud Transactions"
)

col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Chart 3: Fraud by Category
# -----------------------------
category_fraud = filtered_df.groupby("Transaction Category").agg(
    fraud_transactions=("IsFraud", "sum")
).reset_index()

fig3 = px.bar(
    category_fraud,
    x="Transaction Category",
    y="fraud_transactions",
    title="Fraud Transactions by Category"
)

# -----------------------------
# Chart 4: Top States by Fraud Rate
# -----------------------------
state_fraud = filtered_df.groupby("State").agg(
    total_transactions=("Transaction ID", "count"),
    fraud_transactions=("IsFraud", "sum")
).reset_index()

state_fraud["Fraud Rate"] = (
    state_fraud["fraud_transactions"] /
    state_fraud["total_transactions"]
) * 100

state_fraud = state_fraud.sort_values("Fraud Rate", ascending=False).head(10)

fig4 = px.bar(
    state_fraud,
    x="Fraud Rate",
    y="State",
    orientation="h",
    title="Top States by Fraud Rate"
)

col3, col4 = st.columns(2)
col3.plotly_chart(fig3, use_container_width=True)
col4.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Chart 5: Fraud Rate by Card Type
# -----------------------------
card_fraud = filtered_df.groupby("Card Type").agg(
    total_transactions=("Transaction ID", "count"),
    fraud_transactions=("IsFraud", "sum")
).reset_index()

card_fraud["Fraud Rate"] = (
    card_fraud["fraud_transactions"] /
    card_fraud["total_transactions"]
) * 100

fig5 = px.bar(
    card_fraud,
    x="Card Type",
    y="Fraud Rate",
    title="Fraud Rate by Card Type"
)

# -----------------------------
# Chart 6: Top Risky Merchants
# -----------------------------
merchant_fraud = filtered_df.groupby("Merchant Name").agg(
    total_transactions=("Transaction ID", "count"),
    fraud_transactions=("IsFraud", "sum")
).reset_index()

merchant_fraud["Fraud Rate"] = (
    merchant_fraud["fraud_transactions"] /
    merchant_fraud["total_transactions"]
) * 100

merchant_fraud = merchant_fraud.sort_values("Fraud Rate", ascending=False).head(10)

fig6 = px.bar(
    merchant_fraud,
    x="Fraud Rate",
    y="Merchant Name",
    orientation="h",
    title="Top Risky Merchants by Fraud Rate"
)

col5, col6 = st.columns(2)
col5.plotly_chart(fig5, use_container_width=True)
col6.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# Transaction Table
# -----------------------------
st.subheader("Transaction Details")

st.dataframe(
    filtered_df[
        [
            "Transaction ID",
            "Customer Name",
            "Merchant Name",
            "Transaction Date",
            "Transaction Amount (INR)",
            "State",
            "Card Type",
            "Bank",
            "Fraud Risk",
            "Fraud Score",
            "IsFraud"
        ]
    ],
    use_container_width=True
)
