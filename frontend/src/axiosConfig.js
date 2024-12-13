import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000/run', // Adjust the baseURL to your server endpoint
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true, // If your server requires credentials like cookies, sessions, etc.
});

export default axiosInstance;