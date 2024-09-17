## Bird Swarm Life Simulator

Create an app to simulate the game of life on a swarm of birds with sliders for changing randomness, number of birds, depth perspective of the animation, colors.

## Install script

```bash
#!/bin/bash
mkdir bird-swarm-life-simulator && cd bird-swarm-life-simulator
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @radix-ui/react-slider
npm install @radix-ui/react-select
npm install three
```

## Run script

```bash
#!/bin/bash
npm run dev
```

## File: src/App.jsx

```jsx
import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import * as Slider from '@radix-ui/react-slider';
import * as Select from '@radix-ui/react-select';

const App = () => {
  const [settings, setSettings] = useState({
    randomness: 0.5,
    birdCount: 100,
    depth: 50,
    color: '#ffffff',
  });

  const canvasRef = useRef(null);
  const sceneRef = useRef(null);
  const birdsRef = useRef([]);

  useEffect(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current });
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.position.z = 5;
    sceneRef.current = scene;

    const animate = () => {
      requestAnimationFrame(animate);
      updateBirds();
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      scene.clear();
      renderer.dispose();
    };
  }, []);

  useEffect(() => {
    updateBirdSwarm();
  }, [settings]);

  const updateBirdSwarm = () => {
    const scene = sceneRef.current;
    scene.clear();
    birdsRef.current = [];

    for (let i = 0; i < settings.birdCount; i++) {
      const geometry = new THREE.BoxGeometry(0.1, 0.1, 0.1);
      const material = new THREE.MeshBasicMaterial({ color: settings.color });
      const bird = new THREE.Mesh(geometry, material);
      bird.position.set(
        Math.random() * settings.depth - settings.depth / 2,
        Math.random() * settings.depth - settings.depth / 2,
        Math.random() * settings.depth - settings.depth / 2
      );
      scene.add(bird);
      birdsRef.current.push(bird);
    }
  };

  const updateBirds = () => {
    birdsRef.current.forEach(bird => {
      bird.position.x += (Math.random() - 0.5) * settings.randomness;
      bird.position.y += (Math.random() - 0.5) * settings.randomness;
      bird.position.z += (Math.random() - 0.5) * settings.randomness;
    });
  };

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    localStorage.setItem('birdSwarmSettings', JSON.stringify({ ...settings, [key]: value }));
  };

  useEffect(() => {
    const savedSettings = localStorage.getItem('birdSwarmSettings');
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  }, []);

  return (
    <div className="h-screen w-screen overflow-hidden">
      <canvas ref={canvasRef} className="absolute inset-0" />
      <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 p-4 text-white">
        <Slider.Root
          className="relative flex items-center select-none touch-none w-full h-5"
          value={[settings.randomness]}
          max={1}
          step={0.01}
          onValueChange={([value]) => handleSettingChange('randomness', value)}
        >
          <Slider.Track className="bg-white bg-opacity-20 relative grow rounded-full h-1">
            <Slider.Range className="absolute bg-white rounded-full h-full" />
          </Slider.Track>
          <Slider.Thumb className="block w-5 h-5 bg-white rounded-full" />
        </Slider.Root>
        <Slider.Root
          className="relative flex items-center select-none touch-none w-full h-5 mt-4"
          value={[settings.birdCount]}
          max={1000}
          step={1}
          onValueChange={([value]) => handleSettingChange('birdCount', value)}
        >
          <Slider.Track className="bg-white bg-opacity-20 relative grow rounded-full h-1">
            <Slider.Range className="absolute bg-white rounded-full h-full" />
          </Slider.Track>
          <Slider.Thumb className="block w-5 h-5 bg-white rounded-full" />
        </Slider.Root>
        <Slider.Root
          className="relative flex items-center select-none touch-none w-full h-5 mt-4"
          value={[settings.depth]}
          max={100}
          step={1}
          onValueChange={([value]) => handleSettingChange('depth', value)}
        >
          <Slider.Track className="bg-white bg-opacity-20 relative grow rounded-full h-1">
            <Slider.Range className="absolute bg-white rounded-full h-full" />
          </Slider.Track>
          <Slider.Thumb className="block w-5 h-5 bg-white rounded-full" />
        </Slider.Root>
        <Select.Root value={settings.color} onValueChange={(value) => handleSettingChange('color', value)}>
          <Select.Trigger className="inline-flex items-center justify-center rounded px-4 py-2 text-sm leading-none bg-white text-black mt-4">
            <Select.Value />
          </Select.Trigger>
          <Select.Portal>
            <Select.Content className="overflow-hidden bg-white rounded-md shadow-lg">
              <Select.Viewport className="p-2">
                {['#ffffff', '#ff0000', '#00ff00', '#0000ff'].map((color) => (
                  <Select.Item key={color} value={color} className="relative flex items-center px-8 py-2 text-sm text-black">
                    <Select.ItemText>{color}</Select.ItemText>
                  </Select.Item>
                ))}
              </Select.Viewport>
            </Select.Content>
          </Select.Portal>
        </Select.Root>
      </div>
    </div>
  );
};

export default App;
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

## File: vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
```