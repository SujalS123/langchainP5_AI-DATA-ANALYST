import axios from 'axios';

const axiosClient = axios.create({
  baseURL: 'https://langchainp5-ai-data-analyst.onrender.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosClient;
