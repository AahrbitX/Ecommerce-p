import Select from 'react-select';
import { product } from '../api/product';
import { useEffect, useState } from 'react';

const options = [
    { value: "sofa", label: "Sofa" },
    { value: 1, label: "New products" },
    { value: "watch", label: "Watch" },
    { value: "mobile", label: "Mobile" },
    { value: "wireless", label: "Wireless" },
];

const customStyles = {
    control: (provided) => ({
        ...provided,
        backgroundColor: "#0f3460",
        color: "white",
        borderRadius: "5px",
        border: "none",
        boxShadow: "none",
        width: "200px",
        height: "40px",
    }),
    option: (provided, state) => ({
        ...provided,
        backgroundColor: state.isSelected ? "#0f3460" : "white",
        color: state.isSelected ? "white" : "#0f3460",
        "&:hover": {
        backgroundColor: "#0f3460",
        color: "white",
        },
    }),
    singleValue: (provided) => ({
        ...provided,
        color: "white",
    }),
};

const FilterSelect = ({setFilterList}) => {

    const [error, setError]=useState(null);
    const [products, setProducts] =useState([]);
  
    useEffect(()=>{

      const fetchProducts =async()=>{
  
      try {
        const response = await product();
        setProducts(response.data);
      }
      catch (error){
        console.error("Error",error);
        setError("Failed to fetch products");
      }
      };
      fetchProducts();
  
    },[]);

    const handleChange=(selectedOption) =>{
        const selectedCategory =selectedOption?.value||"";
        const filteredProducts = products.filter(
            (item)=>item.category === selectedCategory
        );
        setFilterList(filteredProducts);
    };
    
    return (
    <Select
    options={options}
    defaultValue={{ value: "", label: "Filter By Category" }}
    styles={customStyles}
    onChange={handleChange}
    />
    );
};

export default FilterSelect;
