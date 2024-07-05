import { useSearchParams } from "react-router-dom";
import ProductDashboard from "./ProductDashboard";
import useFetch from "./useFetch";

export default function ProductDashboardWrapper(){
    const [searchParams, setSearchParams] = useSearchParams()
    const name = searchParams.get("name")
    const url = searchParams.get("url")
    
    const fetchUrl = `http://127.0.0.1/products?` + new URLSearchParams({
        "name": name,
        "url": url,
    }).toString();
    const { data, error, loading } = useFetch(fetchUrl, name && url);
    
    if (loading){
        return <div>LOADING...</div>
    }
    if (error){
        return <div>ERROR</div>
    }
    if (data){
        const data = {
            score: 55,
            neighbors: ["shit", "ass", "nigga"]
        }
        return <ProductDashboard data={data}></ProductDashboard>
    }
}