import { useState } from 'react'
import { useNavigate } from "react-router-dom";

export default function ProductForm(){
  const [url, setUrl] = useState("");
  const [name, setName] = useState("");
  const navigateTo = useNavigate();

  function handleUrlChange(event){
    setUrl(event.target.value);
  }
  function handleNameChange(event){
    setName(event.target.value);
  }

  function handleFormSubmit(event){
    event.preventDefault();
    navigateTo(`/product-dashboard/${encodeURIComponent(name)}/${encodeURIComponent(url)}`);
  }
  return (
      <form onSubmit={handleFormSubmit} className="flex flex-col w-64">
        <label htmlFor="input-url" hidden={true}>Product URL:</label>
        <input type="text" id="input-name" name="text" placeholder="Your product name" value={name} onChange={handleNameChange} autoFocus={true} className="my-2 mx-4 px-1 py-1 rounded-md"/>
        <input type="url" id="input-url" name="url" placeholder="Your product URL" value={url} onChange={handleUrlChange} autoFocus={false} className="my-2 mx-4 px-1 py-1 rounded-md"/>
        <button type="submit" className="my-2 mx-4 text-xl border-2 rounded-md border-black hover:bg-green-200">SUBMIT</button>
      </form>
  );
}