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
     const response = await apiClient.post("/common/currentuser/"); // Await the API response
     return response.data; // Return the `data` property from the response
   } catch (error) {
     console.error("Error fetching current user:", error); // Log errors for debugging
     throw error; // Rethrow the error so the calling code can handle it
   }
 };

 export const Logout = async () => { 
  try{
    const response =await apiClient.post("/common/logout/");
    return response.data
  } catch (error){ 
    console.error("Error While Logout user: ", error);
    throw error;
  }
 };
 export const SendOtp = async (email) =>{
  try {
    const response = await apiClient.post("/common/forgot-password/",{email});
    return response.data;
  }
  catch(error) {
    console.error("Error Finding user: ", error)
    throw error;
  }
 };
 export const VerifyOTP = async (otp,newpassword) =>{
  try {
    const response = await apiClient.post("common/verify-otp/",{otp, newpassword});
    return response.data
  }
  catch(error){
    console.error("Wrong otp:", error);
    throw error;
  }
 }