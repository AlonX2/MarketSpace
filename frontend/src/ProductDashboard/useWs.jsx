import { useEffect, useState } from "react";
import socket from "../socket.js";

export default function useWs(eventName, data, resEvent, errEvent){
    const [res, setRes] = useState(null);
    const [err, setErr] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(()=>{
        socket.on(resEvent, (message)=>{
            setRes(message);
            setLoading(false);
        });
        socket.on(errEvent, (message)=>{
            setErr(message);
            setLoading(false);
        });
        socket.emit(eventName, data);
        return  () => {
            socket.off(resEvent);
            socket.off(errEvent);
        }
    },[data, eventName]);
    
    return {res, err, loading};
}