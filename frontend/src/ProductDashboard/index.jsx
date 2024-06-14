import ProductDashboard from "./ProductDashboard";
import useWs from "./useWs";

export default function ProductDashboardWrapper(){
    // const { name, url } = useParams();
    // const { data, error, loading } = useWs(
    //     "similar_products_request",
    //     {"name": name, "url": url},
    //     "similar_products_response",
    //     "similar_products_error"
    // );
    // if (loading){
    //     return <div>LOADING...</div>
    // }
    // if (error){
    //     return <div>ERROR</div>
    // }
    // if (data){
    const data = {
        score: 55,
        neighbors: ["shit", "ass", "nigga"]
    }
        return <ProductDashboard data={data}></ProductDashboard>
    // }
}