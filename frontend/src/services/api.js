import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 上传PDF文件
export const uploadPDF = async (formData) => {
  try {
    const response = await api.post('/papers/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

// 获取论文列表
export const getPapers = async () => {
  try {
    const response = await api.get('/papers/');
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

// 获取单个论文详情
export const getPaper = async (paperId) => {
  try {
    const response = await api.get(`/papers/${paperId}`);
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

// 获取实体列表
export const getEntities = async () => {
  try {
    const response = await api.get('/entities/');
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

// 搜索实体
export const searchEntities = async (query, type) => {
  try {
    const response = await api.get('/entities/search/', {
      params: { query, type },
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

// 获取知识图谱数据
export const getKnowledgeGraph = async () => {
  try {
    const response = await api.get('/graph/');
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

export const deletePaper = async (paperId) => {
  const response = await fetch(`${API_BASE_URL}/papers/${paperId}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '删除文档失败');
  }
  
  return response.json();
}; 