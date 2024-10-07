## AI Startup Expense Manager

An expense manager app for a startup. Use dropdown for selecting category of expense using categories relevant for an AI startup. As user enters the expenses these should be listed by category with sub totals and overall total as a professional looking expense report. Add a chart in appropriaa of the app to visualize the expenses by category.

## Install script

```bash
#!/bin/bash
mkdir ai_startup_expense_manager
cd ai_startup_expense_manager
python3 -m venv venv
source venv/bin/activate
pip install streamlit pandas plotly
```

## Run script

```bash
#!/bin/bash
cd ai_startup_expense_manager
source venv/bin/activate
streamlit run app.py
```

## File: app.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Category', 'Amount'])

# App title
st.title('AI Startup Expense Manager')

# Expense categories
categories = [
    'Cloud Computing',
    'Data Acquisition',
    'Hardware',
    'Software Licenses',
    'Salaries',
    'Office Rent',
    'Marketing',
    'Travel',
    'Research & Development',
    'Miscellaneous'
]

# Input form
with st.form('expense_form'):
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox('Expense Category', categories)
    with col2:
        amount = st.number_input('Amount', min_value=0.01, step=0.01, format='%.2f')
    submitted = st.form_submit_button('Add Expense')

    if submitted:
        new_expense = pd.DataFrame({'Category': [category], 'Amount': [amount]})
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

# Display expense report
if not st.session_state.expenses.empty:
    st.subheader('Expense Report')
    
    # Group expenses by category and calculate subtotals
    expense_summary = st.session_state.expenses.groupby('Category')['Amount'].sum().reset_index()
    expense_summary = expense_summary.sort_values('Amount', ascending=False)
    
    # Display expense table
    st.table(expense_summary.style.format({'Amount': '${:.2f}'}))
    
    # Calculate and display total
    total = expense_summary['Amount'].sum()
    st.markdown(f"**Total Expenses: ${total:.2f}**")
    
    # Create and display pie chart
    fig = px.pie(expense_summary, values='Amount', names='Category', title='Expenses by Category')
    st.plotly_chart(fig)
else:
    st.info('No expenses added yet. Use the form above to add expenses.')
```