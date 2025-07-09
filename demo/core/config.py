"""
配置模块
Config Module
定义项目路径、模型参数、API密钥等全局配置。
This module defines global configuration such as project paths, model parameters, and API keys.
"""
import os
from pathlib import Path

# 项目根目录
# Project root directory
BASE_DIR = Path(__file__).parent.parent

# 嵌入模型配置
# Embedding model configuration
MiniLM_MODEL_NAME = 'all-MiniLM-L6-v2'  # 嵌入模型名称/Embedding model name
MODEL_DIR = BASE_DIR.joinpath('embed_model').absolute()  # 嵌入模型目录/Embedding model directory

# 合同模板相关目录
# Contract template related directories
CONTRACT_DIR = os.path.join(BASE_DIR, "contracts")  # 合同主目录/Contract main directory
TEMPLATE_DIR = os.path.join(CONTRACT_DIR, "template")  # 模板目录/Template directory
GENERATED_DIR = os.path.join(CONTRACT_DIR, "generated")  # 生成合同目录/Generated contracts directory
RAG_DIR = os.path.join(CONTRACT_DIR, "RAG")  # RAG知识库目录/RAG knowledge base directory
TRAN_TEMPLATE_DIR = os.path.join(CONTRACT_DIR, "tran_template")  # 翻译模板目录/Translation template directory

# 确保目录存在
# Ensure directories exist
for dir_path in [CONTRACT_DIR, TEMPLATE_DIR, GENERATED_DIR, RAG_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# 大模型API配置
# LLM API configuration
API_KEY = "YOUR_API_KEY_OF_QWEN"  # 千问API密钥/Qwen API key
LLM_MODEL_NAME = 'qwen-turbo'  # 千问模型名称/Qwen model name