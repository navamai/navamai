#!/bin/bash
mkdir todomaster && cd todomaster
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @radix-ui/react-dialog @radix-ui/react-checkbox
npm install @radix-ui/react-icons
npm install idb