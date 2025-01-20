import React, { useState, useEffect } from 'react';
import { Typography, Table, Card, Space, Tag, Tooltip } from 'antd';
import { getEntities } from '../services/api';

const { Title } = Typography;

function Entities() {
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(false);

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
      message.error('获取实体列表失败');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '实体名称',
      dataIndex: 'entity_name',
      key: 'entity_name',
    },
    {
      title: '实体类型',
      dataIndex: 'entity_type',
      key: 'entity_type',
      render: (type) => (
        <Tag color={
          type === 'PERSON' ? 'blue' :
          type === 'ORG' ? 'green' :
          type === 'LOC' ? 'gold' :
          'default'
        }>
          {type}
        </Tag>
      ),
    },
    {
      title: '出现次数',
      dataIndex: 'papers',
      key: 'total_count',
      render: (papers) => {
        const totalCount = papers.reduce((sum, p) => sum + p.count, 0);
        return totalCount;
      },
    },
    {
      title: '关联文档',
      dataIndex: 'papers',
      key: 'papers',
      render: (papers) => (
        <Space wrap>
          {papers.map(paper => (
            <Tooltip 
              key={paper.paper_id} 
              title={`出现 ${paper.count} 次`}
            >
              <Tag color="processing">
                {paper.paper_name}
              </Tag>
            </Tooltip>
          ))}
        </Space>
      ),
    },
  ];

  return (
    <Space direction="vertical" size="large" style={{ width: '100%' }}>
      <Title level={2}>实体列表</Title>
      
      <Card>
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
    </Space>
  );
}

export default Entities; 