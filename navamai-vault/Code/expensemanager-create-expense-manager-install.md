## ExpenseManager

Create an expense manager app

## Install script

```bash
#!/bin/bash
mkdir ExpenseManager && cd ExpenseManager
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material
npm install @mui/x-data-grid
npm install date-fns
```

## Run script

```bash
#!/bin/bash
npm run dev
```

## File: src/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## File: tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## File: src/App.jsx

```jsx
import { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ExpenseForm from './components/ExpenseForm';
import ExpenseList from './components/ExpenseList';
import { Container, Typography, Box } from '@mui/material';

const theme = createTheme();

export default function App() {
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    const storedExpenses = JSON.parse(localStorage.getItem('expenses')) || [];
    setExpenses(storedExpenses);
  }, []);

  useEffect(() => {
    localStorage.setItem('expenses', JSON.stringify(expenses));
  }, [expenses]);

  const addExpense = (expense) => {
    setExpenses([...expenses, { ...expense, id: Date.now() }]);
  };

  const deleteExpense = (id) => {
    setExpenses(expenses.filter(expense => expense.id !== id));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" className="mt-8">
        <Typography variant="h4" component="h1" gutterBottom className="text-center">
          Expense Manager
        </Typography>
        <Box className="mb-8">
          <ExpenseForm onAddExpense={addExpense} />
        </Box>
        <ExpenseList expenses={expenses} onDeleteExpense={deleteExpense} />
      </Container>
    </ThemeProvider>
  );
}
```

## File: src/components/ExpenseForm.jsx

```jsx
import { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';

export default function ExpenseForm({ onAddExpense }) {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (description && amount) {
      onAddExpense({ description, amount: parseFloat(amount) });
      setDescription('');
      setAmount('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <TextField
        fullWidth
        label="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <TextField
        fullWidth
        label="Amount"
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <Box className="text-right">
        <Button type="submit" variant="contained" color="primary">
          Add Expense
        </Button>
      </Box>
    </form>
  );
}
```

## File: src/components/ExpenseList.jsx

```jsx
import { DataGrid } from '@mui/x-data-grid';
import { IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { format } from 'date-fns';

export default function ExpenseList({ expenses, onDeleteExpense }) {
  const columns = [
    { field: 'date', headerName: 'Date', width: 120, valueGetter: (params) => format(new Date(params.row.id), 'yyyy-MM-dd') },
    { field: 'description', headerName: 'Description', flex: 1 },
    { field: 'amount', headerName: 'Amount', width: 120, valueFormatter: ({ value }) => `$${value.toFixed(2)}` },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 100,
      renderCell: (params) => (
        <IconButton onClick={() => onDeleteExpense(params.row.id)} color="error">
          <DeleteIcon />
        </IconButton>
      ),
    },
  ];

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={expenses}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        disableSelectionOnClick
      />
    </div>
  );
}
```