## SaaSy Dashboard

Create a mock dashboard for a SaaS startup. Use dummy data to run animated and cool infographics and analytics. Use appropriate icons. The dashboard should cover all aspects of a business of a typical SaaS startup.

## Install script

```bash
#!/bin/bash
mkdir saasy-dashboard && cd saasy-dashboard
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @radix-ui/react-dropdown-menu @radix-ui/react-avatar @radix-ui/react-progress
npm install @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/react-fontawesome
npm install recharts
```

## Run script

```bash
#!/bin/bash
npm run dev
```

## File: src/index.css

```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
```

## File: src/App.jsx

```jsx
import React from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200">
          <Dashboard />
        </main>
      </div>
    </div>
  );
}

export default App;
```

## File: src/components/Header.jsx

```jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBell, faUser } from '@fortawesome/free-solid-svg-icons';
import * as Avatar from '@radix-ui/react-avatar';

function Header() {
  return (
    <header className="bg-white shadow-md py-4 px-6 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-gray-800">SaaSy Dashboard</h1>
      <div className="flex items-center space-x-4">
        <FontAwesomeIcon icon={faBell} className="text-gray-600 text-xl" />
        <Avatar.Root className="inline-flex items-center justify-center align-middle overflow-hidden select-none w-10 h-10 rounded-full bg-gray-300">
          <Avatar.Image
            className="w-full h-full object-cover"
            src="https://github.com/shadcn.png"
            alt="User avatar"
          />
          <Avatar.Fallback className="w-full h-full flex items-center justify-center bg-gray-300 text-gray-600" delayMs={600}>
            <FontAwesomeIcon icon={faUser} />
          </Avatar.Fallback>
        </Avatar.Root>
      </div>
    </header>
  );
}

export default Header;
```

## File: src/components/Sidebar.jsx

```jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faUsers, faCog, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

function Sidebar() {
  return (
    <aside className="bg-gray-800 text-white w-64 min-h-screen p-4">
      <nav>
        <ul className="space-y-2">
          <li>
            <a href="#" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
              <FontAwesomeIcon icon={faChartLine} />
              <span>Dashboard</span>
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
              <FontAwesomeIcon icon={faUsers} />
              <span>Customers</span>
            </a>
          </li>
          <li>
            <a href="#" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
              <FontAwesomeIcon icon={faCog} />
              <span>Settings</span>
            </a>
          </li>
        </ul>
      </nav>
      <div className="absolute bottom-4 left-4">
        <a href="#" className="flex items-center space-x-2 p-2 hover:bg-gray-700 rounded">
          <FontAwesomeIcon icon={faSignOutAlt} />
          <span>Logout</span>
        </a>
      </div>
    </aside>
  );
}

export default Sidebar;
```

## File: src/components/Dashboard.jsx

```jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUsers, faDollarSign, faChartLine } from '@fortawesome/free-solid-svg-icons';
import * as Progress from '@radix-ui/react-progress';

const data = [
  { name: 'Jan', value: 400 },
  { name: 'Feb', value: 300 },
  { name: 'Mar', value: 600 },
  { name: 'Apr', value: 800 },
  { name: 'May', value: 500 },
  { name: 'Jun', value: 700 },
];

function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard icon={faUsers} title="Total Users" value="10,234" />
        <StatCard icon={faDollarSign} title="Revenue" value="$54,321" />
        <StatCard icon={faChartLine} title="Growth" value="23%" />
      </div>
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Monthly Revenue</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">User Engagement</h2>
        <div className="space-y-4">
          <ProgressBar label="Daily Active Users" value={75} />
          <ProgressBar label="Weekly Active Users" value={60} />
          <ProgressBar label="Monthly Active Users" value={85} />
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow flex items-center space-x-4">
      <div className="bg-blue-500 p-3 rounded-full">
        <FontAwesomeIcon icon={icon} className="text-white text-2xl" />
      </div>
      <div>
        <h3 className="text-lg font-semibold">{title}</h3>
        <p className="text-2xl font-bold">{value}</p>
      </div>
    </div>
  );
}

function ProgressBar({ label, value }) {
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-medium text-gray-700">{value}%</span>
      </div>
      <Progress.Root className="h-4 bg-gray-200 rounded-full overflow-hidden" value={value}>
        <Progress.Indicator
          className="h-full bg-blue-500 transition-all duration-300 ease-in-out"
          style={{ width: `${value}%` }}
        />
      </Progress.Root>
    </div>
  );
}

export default Dashboard;
```

## File: tailwind.config.js

```javascript
module.exports = {
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