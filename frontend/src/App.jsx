import React from 'react';
import { RouterProvider } from 'react-router-dom';
import router from './routes'; // Assuming your router is exported as default from index.jsx
import './styles/App.css'; // Keep existing App.css for general styling

function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
