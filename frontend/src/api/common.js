import apiClient from "./apiClients";

export const login = async (email, password) =>{
   try {
      const response = await apiClient.post('/common/login/', { email, password }); // Replace the endpoint with the actual one
      return response; // Return the full response object
    } catch (error) {
      console.error("Error in login API:", error);
      throw error; // Rethrow the error to be caught in the calling code
    }
};

export const SignUp = async(email,password) =>{
   const response = await apiClient.post("/common/signup/",{email,password})
   return response.data;
};

export const CurrentUser = async (access) => {
   try {
     const response = await apiClient.post("/common/currentuser/", { access }); // Await the API response
     return response.data; // Return the `data` property from the response
   } catch (error) {
     console.error("Error fetching current user:", error); // Log errors for debugging
     throw error; // Rethrow the error so the calling code can handle it
   }
 };
 