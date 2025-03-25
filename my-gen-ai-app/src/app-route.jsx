import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import WebSocketComponent from "./connect";
import './App.css'
import ViewDetail from "./ViewDetail"; // Ensure this component is imported
import Banner from "./Banner"; // Ensure this component is imported
import Dashboard from "./Dashboard";

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
          {/* <Route path="/details/:id" element={<ViewDetail />} />
          <Route path="/email-classifications" element={<WebSocketComponent />} />
          <Route exact path="/" element={<Dashboard />} /> */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />}>
            <Route path="configuration" element={<div style={{'position': 'absolute', 'top': '50%', 'left': '50%'}}>Feature enhancement will be added here.</div>}></Route>
            <Route path="email-classifications" element={<WebSocketComponent />} />
            <Route path="email-classifications/details/:id" element={<ViewDetail />} />
        </Route>
        </Routes>
      </Router>
    </MyProvider>
  );
};

export default AppRoute;
