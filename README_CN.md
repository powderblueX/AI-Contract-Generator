# 合同生成系统

[English](README.md) | [中文](README_CN.md)

## 项目简介
合同生成系统是一个基于人工智能的自动化合同创建平台，旨在通过模板推荐、智能信息提取和自动文档生成，提高合同起草的效率和准确性。该系统采用模块化设计，结合前端图形界面、后端业务逻辑和AI模型服务，实现从用户需求到最终合同文档的端到端自动化。

## 功能特点
- **智能模板推荐**：基于用户需求描述，自动推荐最匹配的合同模板
- **信息自动提取**：利用大语言模型从用户输入中提取关键合同信息
- **合同自动生成**：将提取的信息自动填充到模板中，生成完整合同文档
- **知识库检索**：集成向量检索技术，提供合同相关知识支持

## 系统要求
- Python 3.9.21
- Conda 环境管理工具
- 网络连接（用于模型下载和API调用）

## 安装步骤
1. **创建并激活虚拟环境**
   ```bash
   conda env create -f demo/environment.yml
   conda activate contract_generator
   ```

2. **配置API密钥**
   编辑 `demo/core/config.py` 文件，设置通义千问 API 密钥：
   ```python
   API_KEY = "your_api_key_here"
   ```

3. **启动应用程序**
   ```bash
   cd demo
   python demo.py
   ```

## 使用方法
1. 在主界面输入合同需求描述
2. 系统自动推荐相关合同模板
3. 选择合适的模板并补充必要信息
4. 点击"生成合同"按钮
5. 查看并下载生成的合同文档

## 项目结构
```
AI-Contract-Generator/
├── README.md                   # 英文项目说明文档
├── README_CN.md                # 中文项目说明文档
├── demo/                       # 应用程序主目录
│   ├── __init__.py
│   ├── contracts/              # 合同模板和资源
│   │   ├── generated/          # 生成的合同文件
│   │   ├── template/           # 合同模板文件
│   │   └── tran_template/      # 翻译模板
│   ├── core/                   # 核心配置模块
│   │   ├── __init__.py
│   │   └── config.py           # 系统配置文件
│   ├── demo.py                 # 应用程序入口
│   ├── embed_model/            # 嵌入模型和向量数据
│   ├── environment.yml         # 环境依赖配置
│   ├── run.bat                 # 环境配置脚本（Windows）
│   └── services/               # 业务服务模块
│       ├── __init__.py
│       ├── contract.py         # 合同服务核心逻辑
│       ├── GenerationWorker.py # 合同生成工作线程
│       └── RecommendationWorker.py # 模板推荐工作线程
├── documentation/              # 项目文档
│   ├── Technical Documentation.md # 英文技术文档
│   ├── User Manual.md          # 英文用户手册
│   ├── 技术文档.md             # 中文技术文档
│   └── 用户手册.md             # 中文用户手册
└── script/                     # 辅助脚本
```

## 核心技术栈
- **前端框架**：PyQt5 5.15.11
- **后端语言**：Python 3.9.21
- **自然语言处理**：
  - SentenceTransformers 2.2.2（文本嵌入）
  - FAISS 1.10.0（向量检索）
- **文档处理**：
  - python-docx 1.1.0（Word文档操作）
  - docxtpl 0.16.7（Word模板渲染）
- **AI模型**：通义千问（qwen-turbo）
- **依赖管理**：Conda
