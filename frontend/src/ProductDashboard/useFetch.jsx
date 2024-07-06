import { useEffect, useState } from "react";

export default function useFetch(url, shouldFetch) {
    const [res, setRes] = useState(null);
    const [err, setErr] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!shouldFetch) {
            return;
        }
        fetch(url)
            .then(r => r.json())
            .then(d => setRes(d))
            .catch(e => setErr(e))
            .finally(() => setLoading(false));
    }, [url, shouldFetch]);

    return { res, err, loading };
}