import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="IFRS Question Generator", page_icon="📊", layout="wide")

def generate_sopl():
    revenue = random.randint(500000, 2000000)
    cos = int(revenue * random.uniform(0.45, 0.70))
    distribution = int(revenue * random.uniform(0.03, 0.08))
    admin = int(revenue * random.uniform(0.05, 0.12))
    finance_cost = int(revenue * random.uniform(0.01, 0.03))
    profit_before_tax = revenue - cos - distribution - admin - finance_cost
    tax = int(profit_before_tax * 0.20)
    profit_after_tax = profit_before_tax - tax
    return {
        'Revenue': revenue,
        'Cost of Sales': cos,
        'Distribution Expenses': distribution,
        'Administrative Expenses': admin,
        'Finance Cost': finance_cost,
        'Tax Expense': tax,
        'Profit Before Tax': profit_before_tax,
        'Profit After Tax': profit_after_tax
    }


def generate_sofp():
    ppe = random.randint(250000, 800000)
    inventory = random.randint(50000, 250000)
    receivables = random.randint(40000, 150000)
    cash = random.randint(20000, 100000)
    total_assets = ppe + inventory + receivables + cash
    share_capital = int(total_assets * random.uniform(0.35, 0.50))
    long_term_loan = int(total_assets * random.uniform(0.15, 0.25))
    trade_payables = int(total_assets * random.uniform(0.08, 0.15))
    retained_earnings = total_assets - share_capital - long_term_loan - trade_payables
    return {
        'PPE': ppe,
        'Inventory': inventory,
        'Receivables': receivables,
        'Cash': cash,
        'Total Assets': total_assets,
        'Share Capital': share_capital,
        'Retained Earnings': retained_earnings,
        'Long-term Loan': long_term_loan,
        'Trade Payables': trade_payables
    }


def generate_trial_balance():
    sopl = generate_sopl()
    sofp = generate_sofp()
    return pd.DataFrame({
        'Account':['Revenue','Cost of Sales','Distribution Expenses','Administrative Expenses','Finance Cost','Property, Plant & Equipment','Inventory','Trade Receivables','Cash','Share Capital','Trade Payables','Long-term Loan'],
        'Amount (£)':[sopl['Revenue'],sopl['Cost of Sales'],sopl['Distribution Expenses'],sopl['Administrative Expenses'],sopl['Finance Cost'],sofp['PPE'],sofp['Inventory'],sofp['Receivables'],sofp['Cash'],sofp['Share Capital'],sofp['Trade Payables'],sofp['Long-term Loan']]
    })


def calculate_ratios(sopl, sofp):
    gross_profit = sopl['Revenue'] - sopl['Cost of Sales']
    current_assets = sofp['Inventory'] + sofp['Receivables'] + sofp['Cash']
    equity = sofp['Share Capital'] + sofp['Retained Earnings']
    return pd.DataFrame({
        'Ratio':['Gross Profit Margin %','Net Profit Margin %','Current Ratio','Return on Equity %'],
        'Value':[
            round(gross_profit/sopl['Revenue']*100,2),
            round(sopl['Profit After Tax']/sopl['Revenue']*100,2),
            round(current_assets/sofp['Trade Payables'],2),
            round(sopl['Profit After Tax']/equity*100,2)
        ]
    })

st.title('📊 IFRS Undergraduate Question Generator')
question_type = st.sidebar.selectbox('Select Question Type',['Statement of Profit or Loss','Statement of Financial Position','Trial Balance','Integrated Exercise'])
generate = st.sidebar.button('Generate Question')

if generate:
    if question_type == 'Statement of Profit or Loss':
        st.dataframe(pd.DataFrame(generate_sopl().items(), columns=['Item','£']))
    elif question_type == 'Statement of Financial Position':
        st.dataframe(pd.DataFrame(generate_sofp().items(), columns=['Item','£']))
    elif question_type == 'Trial Balance':
        st.dataframe(generate_trial_balance())
    else:
        sopl = generate_sopl(); sofp = generate_sofp()
        st.dataframe(pd.DataFrame(sopl.items(), columns=['Item','£']))
        st.dataframe(pd.DataFrame(sofp.items(), columns=['Item','£']))
        st.dataframe(calculate_ratios(sopl, sofp))
