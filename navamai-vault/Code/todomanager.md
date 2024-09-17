## Todo Manager

Create a todo manager with add, remove, update, save, and load features.

## Instructions

Add search. Editing should be in-place.

## Install script

```bash
#!/bin/bash
mkdir todo-manager && cd todo-manager
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @radix-ui/react-dialog @radix-ui/react-checkbox
npm install @radix-ui/react-icons
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

## File: src/App.jsx

```jsx
import { useState, useEffect } from 'react';
import * as Checkbox from '@radix-ui/react-checkbox';
import { CheckIcon, Cross2Icon, Pencil1Icon } from '@radix-ui/react-icons';

export default function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const storedTodos = JSON.parse(localStorage.getItem('todos'));
    if (storedTodos) setTodos(storedTodos);
  }, []);

  useEffect(() => {
    localStorage.setItem('todos', JSON.stringify(todos));
  }, [todos]);

  const addTodo = () => {
    if (newTodo.trim()) {
      setTodos([...todos, { id: Date.now(), text: newTodo, completed: false }]);
      setNewTodo('');
    }
  };

  const removeTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  const updateTodo = (id, newText) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, text: newText } : todo
    ));
    setEditingId(null);
  };

  const filteredTodos = todos.filter(todo =>
    todo.text.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl">
      <h1 className="text-2xl font-bold mb-4">Todo Manager</h1>
      <div className="flex mb-4">
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          className="flex-grow mr-2 p-2 border rounded"
          placeholder="Add new todo"
        />
        <button onClick={addTodo} className="bg-blue-500 text-white px-4 py-2 rounded">Add</button>
      </div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full p-2 border rounded mb-4"
        placeholder="Search todos"
      />
      <ul>
        {filteredTodos.map(todo => (
          <li key={todo.id} className="flex items-center mb-2">
            <Checkbox.Root
              checked={todo.completed}
              onCheckedChange={() => toggleTodo(todo.id)}
              className="mr-2 w-5 h-5 border rounded"
            >
              <Checkbox.Indicator>
                <CheckIcon />
              </Checkbox.Indicator>
            </Checkbox.Root>
            {editingId === todo.id ? (
              <input
                type="text"
                value={todo.text}
                onChange={(e) => updateTodo(todo.id, e.target.value)}
                onBlur={() => setEditingId(null)}
                autoFocus
                className="flex-grow p-1 border rounded"
              />
            ) : (
              <span className={`flex-grow ${todo.completed ? 'line-through' : ''}`}>{todo.text}</span>
            )}
            <button onClick={() => setEditingId(todo.id)} className="mr-2 text-blue-500"><Pencil1Icon /></button>
            <button onClick={() => removeTodo(todo.id)} className="text-red-500"><Cross2Icon /></button>
          </li>
        ))}
      </ul>
    </div>
  );
}
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

## Updates

1. Added a search input field and functionality to filter todos based on the search term.
2. Implemented in-place editing by replacing the Dialog component with an input field that appears when the edit button is clicked.
3. Removed the editTodo state and Dialog-related code, replacing it with an editingId state to track which todo is being edited.
4. Updated the updateTodo function to work with the new in-place editing system.
5. Added autoFocus to the edit input for better user experience.