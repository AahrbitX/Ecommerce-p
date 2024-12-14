import { Col, Container, Row } from "react-bootstrap";
import { useEffect } from "react";
import FilterSelect from "../components/FilterSelect";
import SearchBar from "../components/SeachBar/SearchBar";
import { Fragment, useState } from "react";
import { product } from "../api/product";
import ShopList from "../components/ShopList";
import Banner from "../components/Banner/Banner";
import useWindowScrollToTop from "../hooks/useWindowScrollToTop";

const Shop = () => {
  const [filterList, setFilterList] = useState([]);
  const [error, setError]=useState(null)

  useEffect(()=>{
    const fetchData =async()=>{

    try {
      const response = await product();
      console.log(response.data)
      setFilterList(response.data.filter((item)=>item.category===1))
    }
    catch (error){
      console.error("Error")
      setError("Failed to fetch products")
    }
    };

    fetchData();

  },[]);


  useWindowScrollToTop();

  return (
    <Fragment>
      <Banner title="product" />
      <section className="filter-bar">
        <Container className="filter-bar-contianer">
          <Row className="justify-content-center">
            <Col md={4}>
              <FilterSelect setFilterList={setFilterList} />
            </Col>
            <Col md={8}>
              <SearchBar setFilterList={setFilterList} />
            </Col>
          </Row>
        </Container>
        <Container>
          
        {error ? (<p>{error}</p>):(<ShopList productItems={filterList} />)}
          
        </Container>
      </section>
    </Fragment>
  );
};

export default Shop;
