## House Price Prediction

Predict house prices based on a given historical data

## Environment Setup

```bash
#!/bin/bash

# Create and navigate to project directory
mkdir house_price_prediction
cd house_price_prediction

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install jupyter pandas numpy matplotlib seaborn plotly scikit-learn

# Create Jupyter Notebook
touch house_price_prediction.ipynb
```

## Run Notebook

```bash
#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start Jupyter Notebook
jupyter notebook house_price_prediction.ipynb
```

## Cell: 1

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
```

## Cell: 2

```python
data = pd.read_csv('house_prices.csv')
data.head()
```

## Cell: 3

```python
data.info()
```

## Cell: 4

```python
data.describe()
```

## Cell: 5

```python
plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
```

## Cell: 6

```python
fig = px.scatter(data, x='SquareFeet', y='Price', title='Square Feet vs Price')
fig.show()
```

## Cell: 7

```python
X = data.drop('Price', axis=1)
y = data['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

## Cell: 8

```python
model = LinearRegression()
model.fit(X_train_scaled, y_train)
```

## Cell: 9

```python
y_pred = model.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared Score: {r2}')
```

## Cell: 10

```python
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('Actual vs Predicted House Prices')
plt.show()
```

## Cell: 11

```python
feature_importance = pd.DataFrame({'feature': X.columns, 'importance': model.coef_})
feature_importance = feature_importance.sort_values('importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance)
plt.title('Feature Importance')
plt.show()
```