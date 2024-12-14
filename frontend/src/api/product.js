import apiClient from './apiClients';


export const product = async () => {
  try {
    const response = await apiClient.get('/api/products/'); // Or apiClient.get('/api/products/')
    console.log(response); // Verify the structure of the data
    return response; // Return the array of products
  } catch (error) {
    console.error("Error fetching products:", error);
    return []; // Return an empty array in case of an error
  }
};
