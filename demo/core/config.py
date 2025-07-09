"""
配置模块
Config Module
定义项目路径、模型参数、API密钥等全局配置。
"""
import os
from pathlib import Path

# 项目根目录
# Project root directory
BASE_DIR = Path(__file__).parent.parent

# 嵌入模型配置
# Embedding model configuration
MiniLM_MODEL_NAME = 'all-MiniLM-L6-v2'
MODEL_DIR = BASE_DIR.joinpath('embed_model').absolute()

# 合同模板相关目录
# Contract template related directories
CONTRACT_DIR = os.path.join(BASE_DIR, "contracts")
TEMPLATE_DIR = os.path.join(CONTRACT_DIR, "template")
GENERATED_DIR = os.path.join(CONTRACT_DIR, "generated")
RAG_DIR = os.path.join(CONTRACT_DIR, "RAG")
TRAN_TEMPLATE_DIR = os.path.join(CONTRACT_DIR, "tran_template")

# 确保目录存在
# Ensure directories exist
for dir_path in [CONTRACT_DIR, TEMPLATE_DIR, GENERATED_DIR, RAG_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# 大模型API配置
# LLM API configuration
API_KEY = "sk-4c0e21d21fb748bd81d918e0cdc346f3"
LLM_MODEL_NAME = 'qwen-turbo'