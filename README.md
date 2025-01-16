# Gauge Python 自动化测试项目

这是一个使用 Gauge 框架和 Python 语言实现的自动化测试项目，包含了 API、Web 和移动端的测试用例。

## 项目结构

```
gauge-python-automation/
├── specs/                    # 测试规范文件目录
│   ├── api_test.spec        # API 测试规范
│   ├── web_test.spec        # Web 测试规范
│   └── mobile_test.spec     # 移动端测试规范
├── step_impl/               # 步骤实现目录
│   ├── api_test.py         # API 测试步骤实现
│   ├── web_test.py         # Web 测试步骤实现
│   └── mobile_test.py      # 移动端测试步骤实现
├── env/                     # 环境配置目录
├── logs/                    # 日志目录
├── reports/                 # 测试报告目录
├── requirements.txt         # Python 依赖文件
└── manifest.json           # Gauge 项目配置文件
```

## 环境要求

- Python 3.11+
- Gauge 1.6.10+
- Chrome 浏览器（Web 测试）
- Edge 浏览器（Web 测试）
- Android SDK 和 adb（移动测试）
- Appium 2.0+（移动测试）
- SwagLabs 移动应用（移动测试）

## 安装步骤

1. 安装 Gauge
```bash
brew install gauge
```

2. 安装 Gauge Python 插件
```bash
gauge install python
```

3. 创建并激活 Python 虚拟环境
```bash
python -m venv venv
source venv/bin/activate
```

4. 安装项目依赖
```bash
pip install -r requirements.txt
```

5. 安装 Appium（用于移动测试）
```bash
npm install -g appium
```

## 测试用例说明

### API 测试
- 位置：`specs/api_test.spec`
- 测试内容：使用 JSONPlaceholder API 进行 POST 操作测试
- 运行命令：`gauge run specs/api_test.spec`

### Web 测试
- 位置：`specs/web_test.spec`
- 测试内容：百度搜索功能测试，支持 Chrome 和 Edge 浏览器
- 运行命令：`gauge run specs/web_test.spec`

### 移动测试
- 位置：`specs/mobile_test.spec`
- 测试内容：SwagLabs 移动应用登录功能测试
- 前置条件：
  - Appium 服务器已启动（`appium`）
  - Android 设备已连接（`adb devices`）
  - SwagLabs 应用已安装
- 运行命令：`gauge run specs/mobile_test.spec`

## 运行测试

### 运行所有测试
```bash
gauge run specs/
```

### 运行特定测试
```bash
gauge run specs/api_test.spec    # 运行 API 测试
gauge run specs/web_test.spec    # 运行 Web 测试
gauge run specs/mobile_test.spec # 运行移动测试
```

### 查看测试报告
测试执行完成后，可以在 `reports/html-report` 目录下查看 HTML 格式的测试报告。

## 常见问题解决

### 移动测试相关

1. Appium 连接问题
   - 确保 Appium 服务器已启动
   - 检查设备连接状态：`adb devices`
   - 验证应用包名：`adb shell pm list packages | grep swaglabs`

2. 应用未正常关闭
   - 使用强制停止命令：`adb shell am force-stop com.swaglabsmobileapp`

### Web 测试相关

1. 浏览器驱动问题
   - Chrome 和 Edge 浏览器驱动会自动下载和管理
   - 确保浏览器版本与驱动版本匹配

### API 测试相关

1. 网络连接问题
   - 确保能够访问 JSONPlaceholder API
   - 检查网络连接状态

## 维护和贡献

- 添加新的测试规范时，请在 `specs` 目录下创建相应的 .spec 文件
- 实现步骤时，请在 `step_impl` 目录下创建或修改相应的 Python 文件
- 保持良好的代码风格和注释
- 定期更新依赖版本

## 许可证

MIT License
