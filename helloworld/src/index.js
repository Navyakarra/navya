import React from 'react';
import ReactDOM from 'react-dom/client'; // Change import
import './index.css';
import Header from './components/header';
import App from './App.jsx'
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(<Header/>)
root.render(<App/>);

