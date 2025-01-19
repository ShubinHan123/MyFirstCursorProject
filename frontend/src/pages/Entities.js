import React, { useState, useEffect } from 'react';
import { Table, Typography, Card, Space, Input, Select, List } from 'antd';
import { getEntities, searchEntities } from '../services/api';

const { Title } = Typography;
const { Search } = Input;
const { Option } = Select;

function Entities() {
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [entityType, setEntityType] = useState(null);

  useEffect(() => {
    fetchEntities();
  }, []);

  const fetchEntities = async () => {
    setLoading(true);
    try {
      const data = await getEntities();
      setEntities(data);
    } catch (error) {
      console.error('获取实体列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (value) => {
    setLoading(true);
    try {
      const data = await searchEntities(value, entityType);
      setEntities(data);
    } catch (error) {
      console.error('搜索实体失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'entity_id',
      key: 'entity_id',
    },
    {
      title: '实体名称',
      dataIndex: 'entity_name',
      key: 'entity_name',
    },
    {
      title: '实体类型',
      dataIndex: 'entity_type',
      key: 'entity_type',
    },
    {
      title: '出现次数',
      key: 'occurrence',
      render: (_, record) => {
        const papers = record.papers || [];
        return papers.length;
      },
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <Title level={2}>实体列表</Title>
      
      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Select
            style={{ width: 200 }}
            placeholder="选择实体类型"
            allowClear
            onChange={setEntityType}
          >
            <Option value="PERSON">人物</Option>
            <Option value="ORG">组织</Option>
            <Option value="WORK_OF_ART">作品</Option>
          </Select>
          
          <Search
            placeholder="搜索实体"
            allowClear
            enterButton="搜索"
            onSearch={handleSearch}
            style={{ width: 300 }}
          />
        </Space>

        <Table
          columns={columns}
          dataSource={entities}
          rowKey="entity_id"
          loading={loading}
          pagination={{
            total: entities.length,
            pageSize: 10,
            showTotal: (total) => `共 ${total} 个实体`,
          }}
        />
      </Card>

      <List
        bordered
        dataSource={[]}
        renderItem={(item) => (
          <List.Item>{item}</List.Item>
        )}
      />
    </Space>
  );
}

export default Entities; 