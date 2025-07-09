# Contract Generation System

[English](README.md) | [中文](README_CN.md)

## Project Overview
The Contract Generation System is an AI-powered automated contract creation platform designed to improve the efficiency and accuracy of contract drafting through template recommendation, intelligent information extraction, and automated document generation. The system features a modular design combining a front-end graphical interface, back-end business logic, and AI model services to achieve end-to-end automation from user requirements to final contract documents.

## Key Features
- **Intelligent Template Recommendation**: Automatically recommends the most suitable contract templates based on user requirements
- **Information Auto-Extraction**: Uses large language models to extract key contract information from user inputs
- **Automated Contract Generation**: Populates templates with extracted information to generate complete contract documents
- **Knowledge Base Retrieval**: Integrates vector search technology to provide contract-related knowledge support

## System Requirements
- Python 3.9.21
- Conda environment management tool
- Internet connection (for model downloads and API calls)

## Installation Steps
1. **Create and activate virtual environment**
   ```bash
   conda env create -f demo/environment.yml
   conda activate contract_generator

2. **Configure API Key**
   Edit the `demo/core/config.py` file to set your Tongyi Qianwen API key:

   ```python
   API_KEY = "your_api_key_here"
   ```

3. **Launch Application**

   ```python
   cd demo
   python demo.py
   ```

## Usage Guide

1. Enter contract requirements in the main interface
2. System automatically recommends relevant contract templates
3. Select appropriate template and supplement necessary information
4. Click "Generate Contract" button
5. Review and download the generated contract document

## Project Structure

```
contract_generation/
├── README.md                   # Project documentation
├── demo/                       # Main application directory
│   ├── __init__.py
│   ├── contracts/              # Contract templates and resources
│   │   ├── generated/          # Generated contract files
│   │   ├── template/           # Contract template files
│   │   └── tran_template/      # Translation templates
│   ├── core/                   # Core configuration module
│   │   ├── __init__.py
│   │   └── config.py           # System configuration
│   ├── demo.py                 # Application entry point
│   ├── embed_model/            # Embedding models and vector data
│   ├── environment.yml         # Environment dependencies
│   ├── run.bat                 # Configuration script (Windows)
│   └── services/               # Business service modules
│       ├── __init__.py
│       ├── contract.py         # Core contract service logic
│       ├── GenerationWorker.py # Contract generation worker thread
│       └── RecommendationWorker.py # Template recommendation worker thread
├── documentation/              # Project documentation
│   ├── Technical Documentation.md # Technical docs (English)
│   ├── User Manual.md          # User guide (English)
│   ├── 技术文档.md             # Technical docs (Chinese)
│   └── 用户手册.md             # User guide (Chinese)
└── script/                     # Utility scripts
```

## Core Technology Stack

- **Frontend Framework**: PyQt5 5.15.4
- **Backend Language**: Python 3.9.21
- **Natural Language Processing**:
  - SentenceTransformers 2.2.2 (Text embedding)
  - FAISS 1.7.2 (Vector search)
- **Document Processing**:
  - python-docx 0.8.11 (Word document operations)
  - docxtpl 0.16.7 (Word template rendering)
- **AI Model**: Tongyi Qianwen (qwen-turbo)
- **Dependency Management**: Conda