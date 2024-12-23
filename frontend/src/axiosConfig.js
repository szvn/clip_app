// axiosConfig.js
import axios from 'axios';

// Get the identity token from the browser's local storage, cookies, or use an authentication library to get it
const getIdentityToken = () => {
  return localStorage.getItem('id_token');  // Assuming you've stored it in local storage
}

const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8080/run/', // Update this to your Cloud Run service URL
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getIdentityToken()}`, // Attach the token here
  },
  withCredentials: true,
});

export default axiosInstance;
