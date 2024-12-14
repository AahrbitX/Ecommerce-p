import { useEffect, useState } from "react";
import "./searchbar.css";
import { product } from "../../api/product";
// import { products } from "../../utils/products";
// import useDebounce from "../../hooks/useDebounce";
const SearchBar = ({ setFilterList }) => {
  const [searchWord, setSearchWord] = useState(null);
  const [products,setProduts] =useState([]);
  const [error,setError] = useState(null);

  // const debounceSearchWord = useDebounce(searchWord, 300);

  useEffect(()=>{
    const fetchProdutcs= async()=>{
      try{
        const response = await product();
        setProduts(response.data);
      }
      catch(error){
        console.error("Error",error);
        setError("Error Fetching Data");
      }
    }
    fetchProdutcs();
  },[]);
  const handelChange = (input) => {
    setSearchWord(input.target.value);
    setFilterList(
      products.filter((item) =>
        item.name?.toLowerCase().includes(searchWord?.toLowerCase())
      )
    );
  };
  return (
    <div className="search-container">
      <input type="text" placeholder="Search..." onChange={handelChange} />
      <ion-icon name="search-outline" className="search-icon"></ion-icon>
    </div>
  );
};

export default SearchBar;
