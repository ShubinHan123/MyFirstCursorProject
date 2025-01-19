import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 上传PDF文件
export const uploadPDF = (formData) => {
  return api.post('/papers/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// 获取论文列表
export const getPapers = () => {
  return api.get('/papers').then(response => response.data);
};

// 获取单个论文详情
export const getPaper = async (paperId) => {
  const response = await api.get(`/papers/${paperId}`);
  return response.data;
};

// 获取实体列表
export const getEntities = () => {
  return api.get('/entities').then(response => response.data);
};

// 搜索实体
export const searchEntities = (query, type) => {
  return api.get('/entities/search', {
    params: { query, type },
  }).then(response => response.data);
};

// 获取知识图谱数据
export const getKnowledgeGraph = () => {
  return api.get('/graph').then(response => response.data);
}; 