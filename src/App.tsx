import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import CoachSchedule from "./pages/CoachSchedule";
import './App.sass';

const App: React.FC = () => {
  return (
    <div className="app">
      <BrowserRouter>
        <Sidebar />
        <div className="main">
          <Routes>
            <Route path="/coach" element={<CoachSchedule />} />
          </Routes>      
        </div>
      </BrowserRouter>
    </div>
  )
};

export default App;
