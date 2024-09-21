## Todo Manager

Create a todo manager

## Install script

```bash
#!/bin/bash
mkdir todo_manager
cd todo_manager
python3 -m venv venv
source venv/bin/activate
pip install streamlit plotly pandas
```

## Run script

```bash
#!/bin/bash
cd todo_manager
source venv/bin/activate
streamlit run app.py
```

## File: app.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def load_todos():
    try:
        return pd.read_csv('todos.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['task', 'due_date', 'status'])

def save_todos(df):
    df.to_csv('todos.csv', index=False)

st.set_page_config(page_title="Todo Manager", layout="wide")
st.title("Todo Manager")

if 'todos' not in st.session_state:
    st.session_state.todos = load_todos()

col1, col2 = st.columns(2)

with col1:
    task = st.text_input("Task")
    due_date = st.date_input("Due Date")
    if st.button("Add Task"):
        new_task = pd.DataFrame({'task': [task], 'due_date': [due_date], 'status': ['Pending']})
        st.session_state.todos = pd.concat([st.session_state.todos, new_task], ignore_index=True)
        save_todos(st.session_state.todos)

with col2:
    st.subheader("Tasks")
    for i, row in st.session_state.todos.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"{row['task']} (Due: {row['due_date']})")
        if col2.button("Complete", key=f"complete_{i}"):
            st.session_state.todos.at[i, 'status'] = 'Completed'
            save_todos(st.session_state.todos)
        if col3.button("Delete", key=f"delete_{i}"):
            st.session_state.todos = st.session_state.todos.drop(i)
            save_todos(st.session_state.todos)
            st.experimental_rerun()

st.subheader("Task Statistics")
completed = len(st.session_state.todos[st.session_state.todos['status'] == 'Completed'])
pending = len(st.session_state.todos[st.session_state.todos['status'] == 'Pending'])
fig = px.pie(values=[completed, pending], names=['Completed', 'Pending'], title='Task Status')
st.plotly_chart(fig)

st.subheader("Upcoming Tasks")
upcoming = st.session_state.todos[st.session_state.todos['due_date'] >= str(datetime.now().date())]
upcoming = upcoming.sort_values('due_date')
st.dataframe(upcoming[['task', 'due_date', 'status']])
```