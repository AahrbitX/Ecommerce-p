import axios from 'axios';
import { getToken } from '../utils/auth';

const apiClient = axios.create({
    baseURL: "http://localhost:8000",
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});

apiClient.interceptors.request.use(
    (config) => {
        const token = getToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        console.debug("Outgoing request:", config);
        return config;
    },
    (error) => {
        console.error("Request error:", error);
        return Promise.reject(error);
    }
);

apiClient.interceptors.response.use(
    (response) => {
        console.debug("Response received:", response);
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            console.error("Unauthorized - redirecting to login");
            window.location.href = "/login"; // Adjust the route as needed
        }
        console.error("Response error:", error.response);
        return Promise.reject(error);
    }
);

export default apiClient;
