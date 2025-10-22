import axios from 'axios';

const axiosClient = axios.create({
  baseURL: 'https://langchainp5-ai-data-analyst.onrender.com',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
});

// Add response interceptor to handle CORS issues
axiosClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'ERR_NETWORK' || error.message.includes('Network Error')) {
      console.error('CORS or Network Error - This might be a CORS issue');
    }
    return Promise.reject(error);
  }
);

export default axiosClient;
