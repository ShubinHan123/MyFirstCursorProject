import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';

const { Header } = Layout;

function Navbar() {
  const location = useLocation();
  
  const items = [
    { key: '/', label: <Link to="/">首页</Link> },
    { key: '/papers', label: <Link to="/papers">文档管理</Link> },
    { key: '/entities', label: <Link to="/entities">实体列表</Link> },
    { key: '/graph', label: <Link to="/graph">关系图谱</Link> },
  ];

  return (
    <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
      <div className="logo" />
      <Menu
        theme="dark"
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={items}
      />
    </Header>
  );
}

export default Navbar; 