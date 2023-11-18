import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import CoachSchedule from "./pages/CoachSchedule";
import './App.sass';

const App: React.FC = () => {
  return (
    <div className="app">
      <BrowserRouter>
        <Sidebar />
        <div className="rightside">
          <Header />
          <div className="main">
            <Routes>
              <Route path="/coach" element={<CoachSchedule />} />
            </Routes>      
          </div>
        </div>
      </BrowserRouter>
    </div>
  )
};

export default App;
