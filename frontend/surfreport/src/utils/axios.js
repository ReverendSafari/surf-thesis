import axios from 'axios';
import axiosRetry from 'axios-retry';

// Configure axios to retry on failure
axiosRetry(axios, {
  retries: 3, // Number of retry attempts
  retryDelay: (retryCount) => retryCount * 1000, // Delay between retries in milliseconds
  retryCondition: (error) => {
    // Retry only for server errors (status code 500)
    return error.response && error.response.status >= 500;
  },
});

export default axios;
