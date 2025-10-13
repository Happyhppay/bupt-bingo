// API 基础配置
const API_BASE_URL = 'http://localhost:8000'; // 根据实际后端地址修改

// 存储用户token
let userToken = localStorage.getItem('userToken');

// 通用请求函数
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // 如果有token，添加到请求头
    if (userToken) {
        defaultOptions.headers['Authorization'] = `Bearer ${userToken}`;
    }

    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, finalOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || `HTTP error! status: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API请求失败:', error);
        throw error;
    }
}

// 用户相关API
const UserAPI = {
    // 用户登录
    async login(studentId, name) {
        return await apiRequest('/users/login', {
            method: 'POST',
            body: JSON.stringify({
                student_id: studentId,
                name: name
            })
        });
    },

    // 验证邀请码
    async verifyInviteCode(inviteCode) {
        return await apiRequest('/users/verify', {
            method: 'POST',
            body: JSON.stringify({
                inviteCode: inviteCode
            })
        });
    }
};

// 社团相关API
const ClubAPI = {
    // 生成社团二维码
    async generateQrCode() {
        return await apiRequest('/clubs/qrcode', {
            method: 'GET'
        });
    },

    // 扫描社团二维码
    async scanQrCode(qrcodeToken) {
        return await apiRequest('/clubs/scan', {
            method: 'POST',
            body: JSON.stringify({
                qrcodeToken: qrcodeToken
            })
        });
    }
};

// Bingo相关API
const BingoAPI = {
    // 获取Bingo状态
    async getStatus() {
        return await apiRequest('/bingo/status', {
            method: 'GET'
        });
    },

    // 点亮Bingo格子
    async lightGrid(pointType, location = null) {
        const body = { pointType };
        if (location) {
            body.location = location;
        }
        
        return await apiRequest('/bingo/light', {
            method: 'POST',
            body: JSON.stringify(body)
        });
    }
};

// 奖励相关API
const RewardAPI = {
    // 生成领奖二维码
    async generateRewardQrCode(bingoType) {
        return await apiRequest('/reward/qrcode', {
            method: 'POST',
            body: JSON.stringify({
                bingoType: bingoType
            })
        });
    },

    // 验证领奖码
    async verifyRewardToken(rewardToken) {
        return await apiRequest('/reward/verify', {
            method: 'POST',
            body: JSON.stringify({
                rewardToken: rewardToken
            })
        });
    }
};

// 工具函数
const Utils = {
    // 显示消息提示
    showMessage(message, type = 'info') {
        const toast = document.getElementById('messageToast');
        const messageText = document.getElementById('messageText');
        
        messageText.textContent = message;
        toast.style.display = 'block';
        
        // 根据类型设置样式
        toast.className = `message-toast ${type}`;
        
        // 3秒后自动隐藏
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    },

    // 显示加载状态
    showLoading(show = true) {
        const loadingOverlay = document.getElementById('loadingOverlay');
        loadingOverlay.style.display = show ? 'flex' : 'none';
    },

    // 保存用户token
    saveToken(token) {
        userToken = token;
        localStorage.setItem('userToken', token);
    },

    // 清除用户token
    clearToken() {
        userToken = null;
        localStorage.removeItem('userToken');
    },

    // 检查用户是否已登录
    isLoggedIn() {
        return !!userToken;
    },

    // 格式化时间
    formatTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('zh-CN');
    }
};

// 导出API对象
window.UserAPI = UserAPI;
window.ClubAPI = ClubAPI;
window.BingoAPI = BingoAPI;
window.RewardAPI = RewardAPI;
window.Utils = Utils;
