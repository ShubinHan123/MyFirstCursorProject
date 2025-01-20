import React, { useState, useEffect } from 'react';
import { Typography, Upload, Button, Table, Card, Space, message, Tag, Popconfirm } from 'antd';
import { UploadOutlined, DeleteOutlined } from '@ant-design/icons';
import { uploadPDF, getPapers, deletePaper } from '../services/api';

const { Title } = Typography;

function Papers() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPapers();
  }, []);

  const fetchPapers = async () => {
    setLoading(true);
    try {
      const data = await getPapers();
      setPapers(data);
    } catch (error) {
      console.error('获取文档列表失败:', error);
      message.error('获取文档列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (paperId) => {
    try {
      await deletePaper(paperId);
      message.success('文档已成功删除');
      fetchPapers(); // 刷新文档列表
    } catch (error) {
      console.error('删除文档时出错:', error);
      message.error(error.message || '删除文档时发生错误');
    }
  };

  const columns = [
    {
      title: '文档名称',
      dataIndex: 'paper_name',
      key: 'paper_name',
    },
    {
      title: '文件类型',
      key: 'file_types',
      render: () => (
        <Space>
          <Tag color="blue">PDF</Tag>
          <Tag color="green">DOCX</Tag>
          <Tag color="gold">JSON</Tag>
          <Tag color="purple">实体</Tag>
        </Space>
      ),
    },
    {
      title: '实体数量',
      dataIndex: 'entity_count',
      key: 'entity_count',
      render: (_, record) => {
        const entities = record.entities || [];
        return entities.length;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Popconfirm
          title="确定要删除这个文档吗？"
          description="删除后将无法恢复，相关的实体关系也会被删除。"
          onConfirm={() => handleDelete(record.paper_id)}
          okText="确定"
          cancelText="取消"
        >
          <Button type="link" danger icon={<DeleteOutlined />}>
            删除
          </Button>
        </Popconfirm>
      ),
    },
  ];

  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await uploadPDF(formData);
      message.success(`${file.name} 上传成功`);
      fetchPapers(); // 刷新文档列表
      return true;
    } catch (error) {
      console.error('上传失败:', error);
      message.error(`${file.name} 上传失败`);
      return false;
    }
  };

  const uploadProps = {
    name: 'file',
    accept: '.pdf',
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        await handleUpload(file);
        onSuccess();
      } catch (error) {
        onError(error);
      }
    },
  };

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <Title level={2}>文档管理</Title>
      
      <Card title="上传文档">
        <Upload {...uploadProps}>
          <Button icon={<UploadOutlined />}>选择PDF文件</Button>
        </Upload>
      </Card>

      <Card title="文档列表">
        <Table
          columns={columns}
          dataSource={papers}
          rowKey="paper_id"
          loading={loading}
          pagination={{
            total: papers.length,
            pageSize: 10,
            showTotal: (total) => `共 ${total} 篇文档`,
          }}
        />
      </Card>
    </Space>
  );
}

export default Papers; 