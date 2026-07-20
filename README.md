# Credit Card Fraud Risk Analysis Dashboard

## Project Overview

This project analyzes credit card transaction data to identify fraud patterns, high-risk merchants, risky transaction categories, fraud-prone locations, affected card types, and bank-level fraud exposure.

The project was built using **Python, SQL Server, and Power BI**. Python was used for data cleaning and exploratory analysis, SQL Server was used for data storage and business queries, and Power BI was used to create an interactive fraud risk monitoring dashboard.

## Business Problem

Banks, fintech companies, and payment processing platforms handle thousands of credit card transactions every day. Some of these transactions may be fraudulent, causing financial loss, customer dissatisfaction, and operational risk.

The main business problem is:

> How can a fraud risk team monitor credit card fraud patterns and identify high-risk transactions, merchants, locations, banks, and card types?

This dashboard helps stakeholders quickly understand where fraud is happening and which areas need immediate attention.

## Stakeholder

**Primary Stakeholder:** Fraud Risk Management Team

Since the dataset contains transactions from multiple banks, this project is designed for a:

- FinTech payment gateway
- Multi-bank transaction monitoring company
- Centralized fraud analytics team
- Card transaction monitoring platform

The dashboard allows the stakeholder to compare fraud risk across banks, merchants, card types, states, and transaction categories.

## Dataset Description

The dataset contains **1,000 credit card transactions** with fraud-related attributes.

### Key Columns

| Column Name | Description |
|---|---|
| Transaction ID | Unique ID for each transaction |
| Customer Name | Name of the customer |
| Merchant Name | Merchant where transaction happened |
| Transaction Date | Date of transaction |
| Transaction Amount (INR) | Transaction value in Indian Rupees |
| Fraud Risk | Risk level such as Low, Medium, High, Critical |
| Fraud Type | Type of fraud such as Phishing, Card Skimming, Account Takeover |
| State | State where transaction/customer belongs |
| Card Type | Card network/type such as Visa, Mastercard, Amex, Rupay |
| Bank | Bank associated with the transaction |
| IsFraud | Target column: 1 = Fraud, 0 = Non-Fraud |
| Fraud Score | Numerical fraud risk score |
| Transaction Category | Category such as E-commerce, Electronics, Food Delivery |
| Merchant Location | Merchant city/location |

## Tools and Technologies Used

- **Python**: Data cleaning, preprocessing, EDA
- **Pandas**: Data manipulation
- **NumPy**: Conditional column creation
- **SQL Server**: Data storage and querying
- **Power BI**: Dashboard development and visualization
- **DAX**: KPI and measure creation

## Project Workflow

```text
Raw CSV Dataset
        ↓
Python Data Cleaning and EDA
        ↓
Cleaned Dataset
        ↓
SQL Server Database
        ↓
SQL Business Queries
        ↓
Power BI Dashboard
        ↓
Business Insights and Recommendations
```

## Data Cleaning Performed

The following cleaning and transformation steps were performed:

- Checked missing values and duplicate records
- Converted transaction date into proper date format
- Created month and year columns for trend analysis
- Created fraud status column using `IsFraud`
- Created clean fraud type column:
  - If `IsFraud = 1`, keep actual fraud type
  - If `IsFraud = 0`, mark as `Not Fraud`
- Created fraud KPIs and risk-based summary metrics

## Key KPI Measures

### Total Transactions

```DAX
Total Transactions =
COUNTROWS('credit_card_transactions')
```

### Fraud Transactions

```DAX
Fraud Transactions =
CALCULATE(
    [Total Transactions],
    'credit_card_transactions'[IsFraud] = 1
)
```

### Fraud Rate

```DAX
Fraud Rate =
DIVIDE(
    [Fraud Transactions],
    [Total Transactions],
    0
)
```

### Fraud Amount

```DAX
Fraud Amount =
CALCULATE(
    SUM('credit_card_transactions'[Transaction Amount (INR)]),
    'credit_card_transactions'[IsFraud] = 1
)
```

### Average Fraud Score

```DAX
Average Fraud Score =
AVERAGE('credit_card_transactions'[Fraud Score])
```

## Dashboard Features

The Power BI dashboard is designed as a **one-page fraud risk overview dashboard**.

### KPI Cards

The dashboard includes 5 KPI cards:

1. Total Transactions
2. Fraud Transactions
3. Fraud Rate
4. Fraud Amount
5. Average Fraud Score

### Slicers

The dashboard includes slicers for:

- State
- Transaction Category
- Bank

### Visuals Created

| Visual | Purpose |
|---|---|
| Monthly Fraud Rate Trend | Shows fraud trend over time |
| Fraud Transactions by Category | Identifies high-risk transaction categories |
| Fraud vs Non-Fraud Donut Chart | Shows fraud share out of total transactions |
| Top States by Fraud Rate | Highlights fraud-prone states |
| Fraud Rate by Card Type | Compares fraud exposure across card types |
| Top 5 Risky Merchants | Identifies merchants with high fraud rate |

## Dashboard Preview

```markdown
![Credit Card Fraud Risk Dashboard](E:\Project1\Credit Card Risk\Images\Credit Card Fraud Dashboard.png)
```

## Key Findings

- Total transactions analyzed: **1,000**
- Fraud transactions identified: **286**
- Overall fraud rate: **28.6%**
- Fraud amount: approximately **₹33.07 lakh**
- E-commerce, Electronics, and Food Delivery show high fraud activity
- Karnataka, Maharashtra, and West Bengal show higher fraud rates
- Visa card transactions show the highest fraud rate among card types
- Top risky merchants include Zomato, Big Bazaar, Reliance Digital, Tata Cliq, and Flipkart

## Business Problems Solved

### 1. High Fraud Rate

The dataset shows a fraud rate of **28.6%**, which indicates a significant fraud risk.

**Solution:** Built a dashboard to monitor fraud transactions, fraud rate, fraud amount, and high-risk segments.

### 2. Financial Loss Due to Fraud

Fraudulent transactions contribute around **₹33.07 lakh**.

**Solution:** Created fraud amount KPIs and category-wise fraud analysis to identify where financial exposure is high.

### 3. Risky Transaction Categories

Some categories show higher fraud transactions.

**Solution:** Used category-level analysis to identify high-risk categories such as E-commerce, Electronics, and Food Delivery.

### 4. Location-Based Fraud Risk

Fraud is not evenly distributed across all states.

**Solution:** Created state-wise fraud rate analysis to highlight high-risk states.

### 5. Merchant-Level Fraud Concentration

Some merchants show higher fraud risk.

**Solution:** Built a Top 5 Risky Merchants chart based on fraud rate.

## Business Recommendations

1. **Monitor high-risk categories** such as E-commerce, Electronics, and Food Delivery more closely.
2. **Apply stronger verification rules** for transactions from high-risk states.
3. **Review risky merchants** with consistently high fraud rates.
4. **Monitor Visa card transactions** more carefully due to higher fraud exposure in the dataset.
5. **Create automated fraud alerts** for high-value and high-risk transactions.

## Fraud Types in Dataset

| Fraud Type | Meaning |
|---|---|
| Card Not Present | Fraud using card details without physical card, usually online |
| Phishing | Fraudster tricks customer into sharing OTP, CVV, or card details |
| Card Skimming | Card details are copied using illegal devices at ATM/POS |
| Account Takeover | Fraudster gains access to customer account |
| Identity Theft | Fraudster uses someone else's identity for financial transactions |

## SQL Analysis Examples

### Overall Fraud KPI

```sql
SELECT
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
    CAST(
        SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS fraud_rate_percentage,
    SUM(transaction_amount_inr) AS total_transaction_amount,
    SUM(CASE WHEN isfraud = 1 THEN transaction_amount_inr ELSE 0 END) AS fraud_transaction_amount,
    AVG(CAST(fraud_score AS FLOAT)) AS avg_fraud_score
FROM dbo.clean_credit_card_fraud_analysis;
```

### Fraud by Transaction Category

```sql
SELECT
    transaction_category,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
    CAST(
        SUM(CASE WHEN isfraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
        AS DECIMAL(10,2)
    ) AS fraud_rate_percentage
FROM dbo.clean_credit_card_fraud_analysis
GROUP BY transaction_category
ORDER BY fraud_rate_percentage DESC;
```

## Limitations

- Dataset contains only 1,000 records
- Fraud rate is higher than typical real-world fraud datasets
- No transaction time is available
- No customer ID is available; customer name is present instead
- No device ID, IP address, channel, or login history is available
- Fraud Type is available for all rows, so a cleaned fraud type column was needed

## Future Scope

- Add machine learning model to predict fraud probability
- Add real-time fraud monitoring
- Include customer behavior and transaction time analysis
- Add alert system for high-risk transactions
- Add more advanced fields like IP address, device ID, payment channel, and location mismatch

## Skills Demonstrated

- Data cleaning using Python
- Business KPI creation
- SQL querying and aggregation
- Power BI dashboard design
- DAX measure creation
- Fraud risk analysis
- Business storytelling with data
- Insight generation and recommendation building

## Conclusion

This project demonstrates how credit card fraud data can be analyzed using Python, SQL Server, and Power BI. The dashboard helps fraud risk teams monitor fraud KPIs, identify risky merchants, analyze location-based fraud, compare card type exposure, and make data-driven decisions to reduce fraud losses.

