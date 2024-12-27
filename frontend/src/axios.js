// src/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000/api/',  // Flask API URL
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',  // Ensure the Content-Type is set to JSON
    'Access-Control-Allow-Origin': 'http://localhost:8000'  // Allow requests from your frontend's origin
  },
});

export default instance;
