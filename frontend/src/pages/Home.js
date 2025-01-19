import React from 'react';
import { Typography } from 'antd';

const { Title, Paragraph } = Typography;

function Home() {
  return (
    <Typography>
      <Title>欢迎使用PDF文档实体识别与关系可视化平台</Title>
      <Paragraph>
        本平台可以帮助您：
        - 上传并管理PDF文档
        - 自动识别文档中的实体
        - 可视化展示实体之间的关系
      </Paragraph>
    </Typography>
  );
}

export default Home; 