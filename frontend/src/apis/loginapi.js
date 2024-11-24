import axios from "axios";


const apiClient = axios.create({
    baseURL:"http://localhost:8000/common/",
    headers:{
        "Content-Type":"application/json",
    },
});

// export const getData = async () => {
//     try{
//         const response = await apiClient.get("");
//         return response.data;
//     } catch (error){
//         console.error("Error fetching data:", error);
//         throw error;
//     }
// };


export const postData = async (data) => {
    try {
      const response = await apiClient.post("/login/", data);
      return response.data;
    } catch (error) {
      console.error("Error posting data:", error);
      throw error;
    }
  };
  