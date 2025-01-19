import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Papers from './pages/Papers';
import Entities from './pages/Entities';
import Graph from './pages/Graph';
import 'antd/dist/antd.css';
import './App.css';

const { Content } = Layout;

function App() {
  return (
    <Router>
      <Layout className="layout">
        <Navbar />
        <Content style={{ padding: '0 50px', marginTop: 64 }}>
          <div className="site-layout-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/papers" element={<Papers />} />
              <Route path="/entities" element={<Entities />} />
              <Route path="/graph" element={<Graph />} />
            </Routes>
          </div>
        </Content>
      </Layout>
    </Router>
  );
}

export default App; 