import {BrowserRouter, Routes, Route} from "react-router-dom";

import ProductForm from './ProductForm';
import ProductDashboardWrapper from './ProductDashboard';

import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="h-screen w-screen flex items-center justify-center bg-gradient-to-tr from-white via-blue-200 to-white ">
        <Routes>
          <Route path="/" element={<ProductForm />} />
          <Route path="/product-dashboard/:name/:url" element={<ProductDashboardWrapper />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App;