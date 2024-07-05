import { useEffect, useState } from "react";

export default function useFetch(url){
    const [res, setRes] = useState(null);
    const [err, setErr] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(()=>{
        fetch(url)
        .then(r => {
            setRes(r.json());
            setLoading(false);
        })
        .catch(e => {
            setErr(e);
            setLoading(false);
        });
    }, []);
    
    return {res, err, loading};
}