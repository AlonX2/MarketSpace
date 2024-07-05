import { useEffect, useState } from "react";

export default function useFetch(url, shouldFetch){
    const [res, setRes] = useState(null);
    const [err, setErr] = useState(null);
    const [loading, setLoading] = useState(true);

    console.log("NIBBER")
    useEffect(() => {
        if (!shouldFetch){
            console.log("doesn't fetch")
            return;
        }
        console.log("FETCHING")
        fetch(url)
        .then(r => {
            result = r.json();
            console.log(`GOT THIS RESULT:\n\n${result}\n\n`)
            setRes(r.json());
        })
        .catch(e => {
            console.log("BITCH")
            setErr(e);
        })
        .finally(() => {
            setLoading(false);
        })
    }, [url, shouldFetch]);
    
    return {res, err, loading};
}