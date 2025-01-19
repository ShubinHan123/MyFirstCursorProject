import React from 'react';
import { Typography, Upload, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const { Title } = Typography;

function Papers() {
  return (
    <div>
      <Title level={2}>文档管理</Title>
      <Upload>
        <Button icon={<UploadOutlined />}>上传PDF文件</Button>
      </Upload>
    </div>
  );
}

export default Papers; 