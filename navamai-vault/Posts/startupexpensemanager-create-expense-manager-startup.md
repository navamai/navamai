## StartupExpenseManager

Create an expense manager app for a startup with categories for expenses and a chart to visualize expense by categories.

## Install script

```bash
#!/bin/bash
mkdir StartupExpenseManager && cd StartupExpenseManager
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material
npm install react-chartjs-2 chart.js
npm install dexie react-dexie
```

## Run script

```bash
#!/bin/bash
npm run dev
```

## File: index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Startup Expense Manager</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## File: src/main.jsx

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## File: src/index.css

```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
```

## File: src/App.jsx

```jsx
import React, { useState, useEffect } from 'react';
import { Container, Typography, Box } from '@mui/material';
import ExpenseForm