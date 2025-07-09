import sys
import os
import json
import re
import docx
import gc
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QComboBox, QPushButton, 
                           QTextEdit, QFileDialog, QMessageBox, QProgressBar,
                           QStatusBar, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from services.contract import ContractService
from core.config import *
import uuid
import traceback
import docx
from docx import Document


class GenerationWorker(QThread):
    """
    合同生成后台线程
    Contract Generation Background Thread
    负责根据用户输入和模板生成定制化合同。
    """
    finished = pyqtSignal(dict)  # 任务完成时发送结果
    progress = pyqtSignal(str)   # 进度更新信号
    update_progress = pyqtSignal(int)  # 进度条更新信号
    
    def __init__(self, contract_service: ContractService, user_input, contract_name, contract_type):
        """
        初始化生成线程。
        Initialize generation thread.
        :param contract_service: 合同服务实例
        :param user_input: 用户输入文本
        :param contract_name: 合同模板名称
        :param contract_type: 合同类型
        """
        super().__init__()
        self.contract_service = contract_service
        self.user_input = user_input
        self.contract_name = contract_name
        self.contract_type = contract_type
    
    def run(self):
        """
        线程主逻辑，执行合同生成流程。
        Main thread logic, execute contract generation process.
        """
        try:
            self.progress.emit("开始处理合同生成任务...")
            self.update_progress.emit(5)

            # 寻找合同模板目录
            contracts_dir = os.path.join(TRAN_TEMPLATE_DIR, f"{self.contract_type}模版")
            print(f"寻找合同模板目录: {contracts_dir}")

            try:
                # 列出目录内容
                if os.path.exists(contracts_dir):
                    dir_contents = os.listdir(contracts_dir)
            except Exception as e:
                print(f"列出目录内容时出错: {str(e)}")
                return

            # 检查合同名称是否有效
            if not self.contract_name:
                return
            else:
                contract_name = self.contract_name.removesuffix(".docx")

            # 定义部委模板和地方模板的占位符文件路径
            ph_path = os.path.join(TRAN_TEMPLATE_DIR, f"{self.contract_type}","占位符",f"{contract_name}.json")
            docx_path = os.path.join(TRAN_TEMPLATE_DIR, f"{self.contract_type}",f"{contract_name}.docx")
            print(f"占位符文件路径: {ph_path}")
            print(f"模板文件路径: {docx_path}")

            # 检查ph是否存在
            if os.path.exists(ph_path):
                print(f"占位符文件存在，准备提取占位符")
                try:
                    ph_json = self.contract_service.extract_ph(self.user_input, ph_path)
                    print(f"占位符提取完成: {len(ph_json) if ph_json else 0} 个键值对")
                    
                    # 确保ph_json不为None
                    if ph_json is None:
                        ph_json = {}
                        print(f"警告: 提取到的占位符为空，使用空字典代替")
                        return
                    
                except Exception as e:
                    print(f"提取占位符失败: {str(e)}")
                    return
            else:
                print(f"占位符文件不存在: {ph_path}")
                return
            
            self.update_progress.emit(80)
            
            # 检查模板是否存在
            if os.path.exists(docx_path):
                try:
                    docx = Document(docx_path)
                except Exception as e:
                    print(f"加载合同模板失败: {str(e)}")
                    return
            else:
                print(f"合同模板文件不存在: {docx_path}")
                return
            
            self.update_progress.emit(85)
            
            self.progress.emit("开始填充合同...")
            # 填充模板
            try:
                filled_docx = self.contract_service.fill_template(docx, ph_json)
            except Exception as e:
                print(f"填充模板失败: {str(e)}")
                return
            
            self.update_progress.emit(95)

            # 生成唯一文件名 - 以生成的时间戳为前缀，保持原文件名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            new_contract_name = f"generated_{timestamp}_{unique_id}_{contract_name}"
            file_name = f"{new_contract_name}.docx"

            # 创建保存目录
            os.makedirs(GENERATED_DIR, exist_ok=True)

            self.progress.emit("智能填写的合同已保存到 {GENERATED_DIR} 路径下...")
            self.update_progress.emit(100)
    
            # 返回最终结果
            self.finished.emit({
                "status": "completed",
                "message": "生成任务完成",
                "data": {
                    "file_name": file_name,
                    "filled_docx": filled_docx
                }
            })
        

        except Exception as e:
            error_details = traceback.format_exc()
            print(f"生成失败! 错误: {str(e)}")
            print(f"详细错误信息:\n{error_details}")
            self.progress.emit(f"处理失败: {str(e)}")
            self.finished.emit({
                "status": "failed",
                "message": str(e)
            })
