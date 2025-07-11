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

以下是系统主要目录的详细说明：

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
│   ├── 技术文档.md              # 中文技术文档
│   └── 用户手册.md              # 中文用户手册
└── script/                     # 辅助脚本
    ├── getPlaceholder.py       # 占位符提取工具
    ├── rag.py                  # 向量检索实现
    ├── scrap.md                # 合同抓取说明
    ├── tranDocx.py             # 文档格式转换工具
    ├── tranKeywords.py         # 关键词提取工具
    └── tranTemplate.py         # 模板占位符生成工具

```

## 应用程序主目录 (demo/)

应用程序的核心功能实现目录，包含以下子模块：

- **contracts/**：合同相关资源存储
  - `generated/`：存放自动生成的合同文件
  - `template/`：原始合同模板文件
  - `tran_template/`：经过转换的带占位符的模板

- **core/**：系统核心配置
  - `config.py`：全局配置参数，包括API密钥管理

- **embed_model/**：文本嵌入模型及向量数据
  - `all-MiniLM-L6-v2/`：SentenceTransformer预训练模型
  - `template_embeddings.pt`：模板向量数据

- **services/**：业务逻辑服务
  - `contract.py`：合同处理核心逻辑
  - `GenerationWorker.py`：合同生成工作线程
  - `RecommendationWorker.py`：模板推荐工作线程

- **environment.yml**：Conda环境依赖配置
- **run.bat**：Windows环境启动脚本
- **demo.py**：应用程序入口文件

## 文档目录 (documentation/)

项目文档存储目录，包含中英文技术文档和用户手册：

- **Technical Documentation.md**：英文技术文档
- **User Manual.md**：英文用户手册
- **技术文档.md**：中文技术文档
- **用户手册.md**：中文用户手册

## 辅助脚本说明

script目录包含多个辅助脚本，用于合同处理的各个环节：

- **getPlaceholder.py**：从合同模板中提取占位符并保存为JSON文件。用于识别模板中需要用户填写的部分，为自动生成合同提供支持。

- **rag.py**：实现基于SentenceTransformer和FAISS的向量检索功能，构建合同知识库并支持相似性查询。用于合同相关知识的快速检索和推荐。

- **scrap.md**：提供使用Web Scraper插件抓取部委和地方合同的步骤说明，包括配置导入和执行方法。用于批量获取合同范本数据。

- **tranDocx.py**：使用unoconv工具将.doc或.wps格式文件批量转换为.docx格式，确保文档格式兼容性。

- **tranKeywords.py**：调用通义千问API从合同内容中提取关键词，生成代表性标签。用于合同分类和快速检索。

- **tranTemplate.py**：利用大模型将原始合同范本转换为含占位符的模板格式，自动化模板预处理过程。

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
