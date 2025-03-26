import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import WebSocketComponent from "./connect";
import './App.css'
import ViewDetail from "./ViewDetail"; // Ensure this component is imported
import Banner from "./Banner"; // Ensure this component is imported

export const MyContext = React.createContext();

const MyProvider = ({ children }) => {
  const [contextData, setContextData] = React.useState();

  return (
    <MyContext.Provider value={{ contextData, setContextData }}>
      {children}
    </MyContext.Provider>
  );
};

const AppRoute = () => {
  return (
    <MyProvider>
      <Banner />
      <Router>
        <Routes>
          <Route path="/details/:id" element={<ViewDetail />} />
          <Route exact path="/" element={<WebSocketComponent />} />
        </Routes>
      </Router>
    </MyProvider>
  );
};

export default AppRoute;
