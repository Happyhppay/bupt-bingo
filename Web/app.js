// 应用主逻辑
class BingoApp {
    constructor() {
        this.currentUser = null;
        this.bingoGrid = null;
        this.selectedLocation = null;
        this.qrScanner = null;
        
        this.init();
    }

    // 初始化应用
    init() {
        this.bindEvents();
        this.checkLoginStatus();
    }

    // 绑定事件
    bindEvents() {
        // 登录表单
        document.getElementById('loginForm').addEventListener('submit', this.handleLogin.bind(this));
        
        // 游戏页面按钮
        document.getElementById('scanBtn').addEventListener('click', this.showScanPage.bind(this));
        document.getElementById('useNormalBtn').addEventListener('click', this.useNormalPoints.bind(this));
        document.getElementById('useSpecialBtn').addEventListener('click', this.showSpecialSelect.bind(this));
        document.getElementById('generateRewardBtn').addEventListener('click', this.generateReward.bind(this));
        
        // 后台管理按钮
        document.getElementById('adminBtn').addEventListener('click', this.showAdminPage.bind(this));
        
        // 返回按钮
        document.getElementById('backToGameBtn').addEventListener('click', this.showGamePage.bind(this));
        document.getElementById('backToGameFromAdminBtn').addEventListener('click', this.showGamePage.bind(this));
        document.getElementById('backToGameFromSelectBtn').addEventListener('click', this.showGamePage.bind(this));
        
        // 后台管理功能
        document.getElementById('generateClubQrBtn').addEventListener('click', this.generateClubQr.bind(this));
        document.getElementById('verifyRewardBtn').addEventListener('click', this.verifyReward.bind(this));
        
        // 特殊积分选择
        document.getElementById('confirmSelectBtn').addEventListener('click', this.confirmSpecialSelect.bind(this));
    }

    // 检查登录状态
    checkLoginStatus() {
        if (Utils.isLoggedIn()) {
            this.showGamePage();
            this.loadGameData();
        } else {
            this.showLoginPage();
        }
    }

    // 显示页面
    showPage(pageId) {
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        document.getElementById(pageId).classList.add('active');
    }

    showLoginPage() {
        this.showPage('loginPage');
    }

    showGamePage() {
        this.showPage('gamePage');
        if (this.currentUser) {
            this.loadGameData();
        }
    }

    showScanPage() {
        this.showPage('scanPage');
        this.initQrScanner();
    }

    showAdminPage() {
        this.showPage('adminPage');
        this.updateAdminSections();
    }

    showSpecialSelect() {
        this.showPage('specialSelectPage');
        this.initSelectGrid();
    }

    // 处理登录
    async handleLogin(event) {
        event.preventDefault();
        
        const studentId = document.getElementById('studentId').value;
        const name = document.getElementById('name').value;
        
        if (!studentId || !name) {
            Utils.showMessage('请填写完整信息', 'error');
            return;
        }

        try {
            Utils.showLoading(true);
            const response = await UserAPI.login(parseInt(studentId), name);
            
            if (response.code === 200) {
                Utils.saveToken(response.data.userToken);
                this.currentUser = response.data.userInfo;
                this.updateUserInfo();
                this.showGamePage();
                this.loadGameData();
                Utils.showMessage('登录成功！', 'success');
            }
        } catch (error) {
            Utils.showMessage(`登录失败: ${error.message}`, 'error');
        } finally {
            Utils.showLoading(false);
        }
    }

    // 更新用户信息显示
    updateUserInfo() {
        if (!this.currentUser) return;
        
        document.getElementById('userName').textContent = this.currentUser.name;
        document.getElementById('userRole').textContent = this.getRoleText(this.currentUser.role);
        
        // 根据角色显示/隐藏后台按钮
        const adminBtn = document.getElementById('adminBtn');
        if (this.currentUser.role === 'club' || this.currentUser.role === 'admin') {
            adminBtn.style.display = 'block';
        } else {
            adminBtn.style.display = 'none';
        }
    }

    // 获取角色文本
    getRoleText(role) {
        const roleMap = {
            'normal': '普通用户',
            'club': '社团成员',
            'admin': '管理员'
        };
        return roleMap[role] || '未知';
    }

    // 加载游戏数据
    async loadGameData() {
        try {
            const response = await BingoAPI.getStatus();
            if (response.code === 200) {
                this.updateGameData(response.data);
            }
        } catch (error) {
            Utils.showMessage(`加载游戏数据失败: ${error.message}`, 'error');
        }
    }

    // 更新游戏数据显示
    updateGameData(data) {
        // 更新积分显示
        document.getElementById('normalPoints').textContent = data.point;
        document.getElementById('specialPoints').textContent = data.specialPoint;
        
        // 更新Bingo格子
        this.updateBingoGrid(data.bingoGrid);
        
        // 更新奖励显示
        this.updateRewards(data.bingoType);
        
        // 更新按钮状态
        this.updateButtonStates(data.point, data.specialPoint);
    }

    // 更新Bingo格子
    updateBingoGrid(grid) {
        const bingoGrid = document.getElementById('bingoGrid');
        bingoGrid.innerHTML = '';
        
        for (let i = 0; i < 5; i++) {
            for (let j = 0; j < 5; j++) {
                const cell = document.createElement('div');
                cell.className = 'bingo-cell';
                cell.dataset.row = i;
                cell.dataset.col = j;
                
                if (grid[i][j] === 1) {
                    cell.classList.add('lit');
                }
                
                bingoGrid.appendChild(cell);
            }
        }
        
        this.bingoGrid = grid;
    }

    // 更新奖励显示
    updateRewards(bingoTypes) {
        const rewardsSection = document.getElementById('rewardsSection');
        const rewardsList = document.getElementById('rewardsList');
        const generateBtn = document.getElementById('generateRewardBtn');
        
        if (bingoTypes && bingoTypes.length > 0) {
            rewardsSection.style.display = 'block';
            rewardsList.innerHTML = '';
            
            bingoTypes.forEach(type => {
                const rewardItem = document.createElement('div');
                rewardItem.className = 'reward-item';
                rewardItem.textContent = type;
                rewardsList.appendChild(rewardItem);
            });
            
            generateBtn.style.display = 'block';
        } else {
            rewardsSection.style.display = 'none';
        }
    }

    // 更新按钮状态
    updateButtonStates(normalPoints, specialPoints) {
        const useNormalBtn = document.getElementById('useNormalBtn');
        const useSpecialBtn = document.getElementById('useSpecialBtn');
        
        useNormalBtn.disabled = normalPoints < 1;
        useSpecialBtn.disabled = specialPoints < 1;
    }

    // 使用普通积分
    async useNormalPoints() {
        try {
            Utils.showLoading(true);
            const response = await BingoAPI.lightGrid('normal');
            
            if (response.code === 200) {
                this.updateGameData(response.data);
                Utils.showMessage('成功点亮一个格子！', 'success');
            }
        } catch (error) {
            Utils.showMessage(`操作失败: ${error.message}`, 'error');
        } finally {
            Utils.showLoading(false);
        }
    }

    // 显示特殊积分选择
    showSpecialSelect() {
        this.showSpecialSelect();
    }

    // 初始化选择格子
    initSelectGrid() {
        const selectGrid = document.getElementById('selectGrid');
        selectGrid.innerHTML = '';
        
        for (let i = 0; i < 5; i++) {
            for (let j = 0; j < 5; j++) {
                const cell = document.createElement('div');
                cell.className = 'select-cell';
                cell.dataset.row = i;
                cell.dataset.col = j;
                
                // 如果格子已点亮，显示为已点亮状态
                if (this.bingoGrid && this.bingoGrid[i][j] === 1) {
                    cell.classList.add('lit');
                } else {
                    cell.classList.add('selectable');
                    cell.addEventListener('click', () => this.selectLocation(i, j));
                }
                
                selectGrid.appendChild(cell);
            }
        }
    }

    // 选择位置
    selectLocation(row, col) {
        // 清除之前的选择
        document.querySelectorAll('.select-cell.selected').forEach(cell => {
            cell.classList.remove('selected');
        });
        
        // 选择新位置
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        cell.classList.add('selected');
        
        this.selectedLocation = [row, col];
        
        // 启用确认按钮
        document.getElementById('confirmSelectBtn').disabled = false;
    }

    // 确认特殊积分选择
    async confirmSpecialSelect() {
        if (!this.selectedLocation) return;
        
        try {
            Utils.showLoading(true);
            const response = await BingoAPI.lightGrid('special', this.selectedLocation);
            
            if (response.code === 200) {
                this.updateGameData(response.data);
                Utils.showMessage('成功点亮指定格子！', 'success');
                this.showGamePage();
            }
        } catch (error) {
            Utils.showMessage(`操作失败: ${error.message}`, 'error');
        } finally {
            Utils.showLoading(false);
        }
    }

    // 初始化二维码扫描器
    initQrScanner() {
        if (this.qrScanner) {
            this.qrScanner.clear();
        }
        
        this.qrScanner = new Html5QrcodeScanner("qr-reader", {
            qrbox: { width: 250, height: 250 },
            fps: 5
        });
        
        this.qrScanner.render(this.onScanSuccess.bind(this), this.onScanFailure.bind(this));
    }

    // 扫描成功回调
    async onScanSuccess(decodedText) {
        try {
            Utils.showLoading(true);
            const response = await ClubAPI.scanQrCode(decodedText);
            
            if (response.code === 200) {
                Utils.showMessage(`扫描成功！获得 ${response.data.addedPoint} 普通积分，${response.data.addedSpecialPoint} 特殊积分`, 'success');
                this.showGamePage();
                this.loadGameData();
            }
        } catch (error) {
            Utils.showMessage(`扫描失败: ${error.message}`, 'error');
        } finally {
            Utils.showLoading(false);
        }
    }

    // 扫描失败回调
    onScanFailure(error) {
        // 静默处理扫描失败，避免过多错误提示
    }

    // 生成奖励
    async generateReward() {
        const bingoTypes = this.getAvailableBingoTypes();
        if (bingoTypes.length === 0) {
            Utils.showMessage('暂无可兑换的奖励', 'error');
            return;
        }
        
        // 这里简化处理，选择第一个可用的Bingo类型
        const bingoType = bingoTypes[0];
        
        try {
            Utils.showLoading(true);
            const response = await RewardAPI.generateRewardQrCode(bingoType);
            
            if (response.code === 200) {
                Utils.showMessage(`领奖码已生成: ${response.data.rewardToken}`, 'success');
                // 这里可以显示二维码或复制到剪贴板
                this.copyToClipboard(response.data.rewardToken);
            }
        } catch (error) {
            Utils.showMessage(`生成领奖码失败: ${error.message}`, 'error');
        } finally {
            Utils.showLoading(false);
        }
    }

    // 获取可用的Bingo类型
    getAvailableBingoTypes() {
        const rewardsList = document.getElementById('rewardsList');
        const rewardItems = rewardsList.querySelectorAll('.reward-item');
        return Array.from(rewardItems).map(item => item.textContent);
    }

    // 复制到剪贴板
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            Utils.showMessage('领奖码已复制到剪贴板', 'success');
        } catch (error) {
            Utils.showMessage('复制失败，请手动复制', 'error');
        }
    }

    // 更新后台管理区域
    updateAdminSections() {
        const clubSection = document.getElementById('clubMemberSection');
        const adminSection = document.getElementById('adminSection');
        
        if (this.currentUser.role === 'club') {
            clubSection.style.display = 'block';
        } else {
            clubSection.style.display = 'none';
        }
        
        if (this.currentUser.role === 'admin') {
            adminSection.style.display = 'block';
        } else {
            adminSection.style.display = 'none';
        }
    }

    // 生成社团二维码
    async generateClubQr() {
        try {
            Utils.showLoading(true);
            const response = await ClubAPI.generateQrCode();
            
            if (response.code === 200) {
                const qrDisplay = document.getElementById('clubQrDisplay');
                const qrCode = document.getElementById('clubQrCode');
                
                qrDisplay.style.display = 'block';
                qrCode.textContent = response.data.qrcodeToken;
                
                Utils.showMessage('社团二维码已生成', 'success');
            }
        } catch (error) {
            Utils.showMessage(`生成二维码失败: ${error.message}`, 'error');
        } finally {
            Utils.showLoading(false);
        }
    }

    // 验证领奖码
    async verifyReward() {
        const rewardToken = document.getElementById('rewardTokenInput').value.trim();
        if (!rewardToken) {
            Utils.showMessage('请输入领奖码', 'error');
            return;
        }
        
        try {
            Utils.showLoading(true);
            const response = await RewardAPI.verifyRewardToken(rewardToken);
            
            if (response.code === 200) {
                const verifyResult = document.getElementById('verifyResult');
                const verifyInfo = document.getElementById('verifyInfo');
                
                verifyInfo.innerHTML = `
                    <p><strong>用户信息:</strong></p>
                    <p>学号: ${response.data.userInfo.studentId}</p>
                    <p>姓名: ${response.data.userInfo.name}</p>
                    <p><strong>Bingo类型:</strong> ${response.data.bingoType}</p>
                `;
                
                verifyResult.style.display = 'block';
                Utils.showMessage('领奖码验证成功', 'success');
            }
        } catch (error) {
            Utils.showMessage(`验证失败: ${error.message}`, 'error');
        } finally {
            Utils.showLoading(false);
        }
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    window.bingoApp = new BingoApp();
});
