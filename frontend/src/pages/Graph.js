import React from 'react';
import { Typography } from 'antd';

const { Title } = Typography;

function Graph() {
  return (
    <div>
      <Title level={2}>关系图谱</Title>
      <div style={{ height: '500px', background: '#f0f2f5', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        知识图谱展示区域（开发中）
      </div>
    </div>
  );
}

export default Graph; 