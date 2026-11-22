
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Fraud Risk Analytics",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #152C4E;
}

.metric-card {
    background: #FFFFFF;
    padding: 20px 22px;
    border-radius: 14px;
    border: 1px solid #E6ECF3;
    box-shadow: 0 3px 12px rgba(20, 45, 80, 0.05);
    min-height: 125px;
}

.metric-title {
    font-size: 13px;
    color: #6B7C93;
    font-weight: 600;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 27px;
    font-weight: 700;
    color: #16365C;
}

.metric-subtitle {
    font-size: 12px;
    color: #8A9AAF;
    margin-top: 7px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #17365D;
    margin-top: 10px;
    margin-bottom: 15px;
}

div[data-testid="stSidebar"] {
    background-color: #FFFFFF;
}

div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    color: #18385E;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E6ECF3;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #6B7C93;
}

div[data-testid="stMetricValue"] {
    color: #16365C;
}

.stButton button {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    df = pd.read_csv("Credit Card Fraud Risk Analysis.csv")

    df["Transaction Date"] = pd.to_datetime(
        df["Transaction Date"],
        errors="coerce"
    )

    df["Month"] = df["Transaction Date"].dt.to_period("M").astype(str)

    df["Fraud Status"] = df["IsFraud"].apply(
        lambda x: "Fraud" if x == 1 else "Non-Fraud"
    )

    return df


df = load_data()

# =========================================================
# COLOR PALETTE
# =========================================================
NAVY = "#16365C"
BLUE = "#3678B8"
LIGHT_BLUE = "#7EB6E8"
RED = "#E45756"
GREEN = "#38A169"
GRAY = "#7D8CA3"
BACKGROUND = "#F4F7FB"

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div style="
    background: linear-gradient(90deg, #16365C, #24568A);
    padding: 28px 30px;
    border-radius: 15px;
    margin-bottom: 20px;
">
    <h1 style="color:white; margin:0; font-size:30px;">
        Credit Card Fraud Risk Analytics
    </h1>
    <p style="color:#DCE9F7; margin-top:8px; margin-bottom:0;">
        Monitor fraud performance, transaction patterns, and risk exposure
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.markdown("## Dashboard Filters")
st.sidebar.markdown("---")

states = sorted(df["State"].dropna().unique())
categories = sorted(df["Transaction Category"].dropna().unique())

selected_state = st.sidebar.multiselect(
    "Select State",
    options=states,
    default=states
)

selected_category = st.sidebar.multiselect(
    "Transaction Category",
    options=categories,
    default=categories
)

st.sidebar.markdown("---")

if st.sidebar.button("Reset Filters", use_container_width=True):
    st.rerun()

# =========================================================
# FILTER DATA
# =========================================================
filtered_df = df[
    df["State"].isin(selected_state) &
    df["Transaction Category"].isin(selected_category)
].copy()

# =========================================================
# EMPTY DATA CHECK
# =========================================================
if filtered_df.empty:

    st.warning("No transactions found for the selected filters.")

else:

    # =====================================================
    # KPI CALCULATIONS
    # =====================================================
    total_transactions = len(filtered_df)

    fraud_transactions = filtered_df["IsFraud"].sum()

    non_fraud_transactions = total_transactions - fraud_transactions

    fraud_rate = (
        fraud_transactions / total_transactions * 100
        if total_transactions > 0 else 0
    )

    fraud_amount = filtered_df.loc[
        filtered_df["IsFraud"] == 1,
        "Transaction Amount (INR)"
    ].sum()

    avg_fraud_score = filtered_df["Fraud Score"].mean()

    # =====================================================
    # KPI CARDS
    # =====================================================
    st.markdown("### Overall Performance")

    k1, k2, k3, k4, k5 = st.columns(5)

    def metric_card(column, title, value, subtitle):
        column.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    metric_card(
        k1,
        "Total Transactions",
        f"{total_transactions:,}",
        "Transactions analyzed"
    )

    metric_card(
        k2,
        "Fraud Transactions",
        f"{fraud_transactions:,}",
        "Confirmed fraud transactions"
    )

    metric_card(
        k3,
        "Fraud Rate",
        f"{fraud_rate:.2f}%",
        "Percentage of total transactions"
    )

    metric_card(
        k4,
        "Fraud Amount",
        f"₹{fraud_amount:,.0f}",
        "Total amount associated with fraud"
    )

    metric_card(
        k5,
        "Average Fraud Score",
        f"{avg_fraud_score:.2f}" if pd.notna(avg_fraud_score) else "N/A",
        "Average risk score"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # MATPLOTLIB DEFAULT STYLING
    # =====================================================
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["axes.edgecolor"] = "#E6ECF3"
    plt.rcParams["axes.labelcolor"] = NAVY
    plt.rcParams["xtick.color"] = GRAY
    plt.rcParams["ytick.color"] = GRAY
    plt.rcParams["text.color"] = NAVY
    plt.rcParams["font.size"] = 10

    # =====================================================
    # CHART 1 - MONTHLY FRAUD RATE TREND
    # =====================================================
    monthly_fraud = filtered_df.groupby("Month").agg(
        total_transactions=("Transaction ID", "count"),
        fraud_transactions=("IsFraud", "sum")
    ).reset_index()

    monthly_fraud["Fraud Rate"] = (
        monthly_fraud["fraud_transactions"] /
        monthly_fraud["total_transactions"]
    ) * 100

    monthly_fraud = monthly_fraud.sort_values("Month")

    fig1, ax1 = plt.subplots(figsize=(8, 4))

    ax1.plot(
        monthly_fraud["Month"],
        monthly_fraud["Fraud Rate"],
        marker="o",
        linewidth=2.5,
        markersize=6,
        color=BLUE
    )

    ax1.fill_between(
        range(len(monthly_fraud)),
        monthly_fraud["Fraud Rate"],
        alpha=0.10,
        color=BLUE
    )

    ax1.set_title("Monthly Fraud Rate Trend", fontweight="bold", pad=15)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Fraud Rate (%)")
    ax1.grid(axis="y", alpha=0.2)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.tick_params(axis="x", rotation=45)

    fig1.tight_layout()

    # =====================================================
    # CHART 2 - FRAUD DISTRIBUTION
    # =====================================================
    fraud_status = filtered_df["Fraud Status"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 4))

    pie_colors = [BLUE, RED]

    wedges, texts, autotexts = ax2.pie(
        fraud_status.values,
        labels=fraud_status.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=pie_colors[:len(fraud_status)],
        wedgeprops={"width": 0.45, "edgecolor": "white"},
        textprops={"color": NAVY, "fontsize": 9}
    )

    for autotext in autotexts:
        autotext.set_fontweight("bold")

    ax2.set_title("Fraud vs Non-Fraud Transactions", fontweight="bold", pad=15)

    # =====================================================
    # DISPLAY CHART 1 & 2
    # =====================================================
    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(fig1, use_container_width=True)

    with col2:
        st.pyplot(fig2, use_container_width=True)

    plt.close(fig1)
    plt.close(fig2)

    # =====================================================
    # CHART 3 - FRAUD BY CATEGORY
    # =====================================================
    category_fraud = filtered_df.groupby(
        "Transaction Category"
    )["IsFraud"].sum().reset_index()

    category_fraud = category_fraud.sort_values(
        "IsFraud", ascending=False
    )

    fig3, ax3 = plt.subplots(figsize=(8, 4))

    ax3.bar(
        category_fraud["Transaction Category"],
        category_fraud["IsFraud"],
        color=BLUE,
        width=0.65
    )

    ax3.set_title("Fraud Transactions by Category", fontweight="bold", pad=15)
    ax3.set_xlabel("Transaction Category")
    ax3.set_ylabel("Fraud Transactions")
    ax3.grid(axis="y", alpha=0.2)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.tick_params(axis="x", rotation=35)

    fig3.tight_layout()

    # =====================================================
    # CHART 4 - TOP STATES BY FRAUD RATE
    # =====================================================
    state_fraud = filtered_df.groupby("State").agg(
        total_transactions=("Transaction ID", "count"),
        fraud_transactions=("IsFraud", "sum")
    ).reset_index()

    state_fraud["Fraud Rate"] = (
        state_fraud["fraud_transactions"] /
        state_fraud["total_transactions"]
    ) * 100

    state_fraud = state_fraud.sort_values(
        "Fraud Rate", ascending=False
    ).head(10)

    fig4, ax4 = plt.subplots(figsize=(8, 4))

    ax4.barh(
        state_fraud["State"],
        state_fraud["Fraud Rate"],
        color=RED,
        height=0.65
    )

    ax4.set_title("Top 10 States by Fraud Rate", fontweight="bold", pad=15)
    ax4.set_xlabel("Fraud Rate (%)")
    ax4.invert_yaxis()
    ax4.grid(axis="x", alpha=0.2)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)

    fig4.tight_layout()

    # =====================================================
    # DISPLAY CHART 3 & 4
    # =====================================================
    col3, col4 = st.columns(2)

    with col3:
        st.pyplot(fig3, use_container_width=True)

    with col4:
        st.pyplot(fig4, use_container_width=True)

    plt.close(fig3)
    plt.close(fig4)

    # =====================================================
    # CHART 5 - FRAUD RATE BY CARD TYPE
    # =====================================================
    card_fraud = filtered_df.groupby("Card Type").agg(
        total_transactions=("Transaction ID", "count"),
        fraud_transactions=("IsFraud", "sum")
    ).reset_index()

    card_fraud["Fraud Rate"] = (
        card_fraud["fraud_transactions"] /
        card_fraud["total_transactions"]
    ) * 100

    card_fraud = card_fraud.sort_values(
        "Fraud Rate", ascending=False
    )

    fig5, ax5 = plt.subplots(figsize=(8, 4))

    ax5.bar(
        card_fraud["Card Type"],
        card_fraud["Fraud Rate"],
        color=LIGHT_BLUE,
        width=0.6
    )

    ax5.set_title("Fraud Rate by Card Type", fontweight="bold", pad=15)
    ax5.set_xlabel("Card Type")
    ax5.set_ylabel("Fraud Rate (%)")
    ax5.grid(axis="y", alpha=0.2)
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)

    fig5.tight_layout()

    # =====================================================
    # CHART 6 - TOP RISKY MERCHANTS
    # =====================================================
    merchant_fraud = filtered_df.groupby("Merchant Name").agg(
        total_transactions=("Transaction ID", "count"),
        fraud_transactions=("IsFraud", "sum")
    ).reset_index()

    merchant_fraud["Fraud Rate"] = (
        merchant_fraud["fraud_transactions"] /
        merchant_fraud["total_transactions"]
    ) * 100

    merchant_fraud = merchant_fraud.sort_values(
        "Fraud Rate", ascending=False
    ).head(10)

    fig6, ax6 = plt.subplots(figsize=(8, 4))

    ax6.barh(
        merchant_fraud["Merchant Name"],
        merchant_fraud["Fraud Rate"],
        color=RED,
        height=0.65
    )

    ax6.set_title("Top 10 Risky Merchants", fontweight="bold", pad=15)
    ax6.set_xlabel("Fraud Rate (%)")
    ax6.invert_yaxis()
    ax6.grid(axis="x", alpha=0.2)
    ax6.spines["top"].set_visible(False)
    ax6.spines["right"].set_visible(False)

    fig6.tight_layout()

    # =====================================================
    # DISPLAY CHART 5 & 6
    # =====================================================
    col5, col6 = st.columns(2)

    with col5:
        st.pyplot(fig5, use_container_width=True)

    with col6:
        st.pyplot(fig6, use_container_width=True)

    plt.close(fig5)
    plt.close(fig6)

    # =====================================================
    # TRANSACTION DETAILS
    # =====================================================
    st.markdown("## Transaction Details")

    display_columns = [
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

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # DOWNLOAD FILTERED DATA
    # =====================================================
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Transactions",
        data=csv,
        file_name="filtered_fraud_transactions.csv",
        mime="text/csv"
    )
