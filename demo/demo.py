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
from services.RecommendationWorker import RecommendationWorker
from services.GenerationWorker import GenerationWorker


class ContractGenerator(QMainWindow):
    """
    合同生成主界面
    Main Window for Contract Generation
    提供合同类型选择、模板推荐、合同生成等完整交互。
    """
    def __init__(self):
        """
        初始化主界面。
        Initialize main window.
        """
        super().__init__()
        self.contract_service = ContractService()
        self.recommendation_worker = None
        self.initUI()

    def initUI(self):
        """
        初始化UI组件。
        Initialize UI components.
        """
        # 设置窗口
        self.setWindowTitle('合同生成器')
        self.setGeometry(100, 100, 1000, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 合同类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel('合同类型:')
        self.type_combo = QComboBox()
        template_types = self.contract_service.get_template_types()
        self.type_combo.addItems(template_types.keys())
        self.type_combo.currentTextChanged.connect(self.update_templates)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # 模板选择
        template_layout = QHBoxLayout()
        template_label = QLabel('合同模板:')
        self.template_combo = QComboBox()
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.template_combo)
        layout.addLayout(template_layout)

        # 合同描述输入
        desc_label = QLabel('请输入合同商讨的会议纪要:')
        layout.addWidget(desc_label)
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_edit)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 日志显示
        log_label = QLabel('处理日志:')
        layout.addWidget(log_label)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # 结果表格
        result_label = QLabel('推荐结果:')
        layout.addWidget(result_label)
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["ID", "名称", "匹配度", "置信度"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.result_table)

        # 按钮
        button_layout = QHBoxLayout()
        self.recommend_btn = QPushButton('推荐模板')
        self.recommend_btn.clicked.connect(self.recommend_template)
        self.generate_btn = QPushButton('生成合同')
        self.generate_btn.clicked.connect(self.generate_contract)
        button_layout.addWidget(self.recommend_btn)
        button_layout.addWidget(self.generate_btn)
        layout.addLayout(button_layout)

        # 设置状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('就绪')

        # 更新模板列表
        if self.type_combo.count() > 0:
            self.update_templates(self.type_combo.currentText())

    def update_templates(self, contract_type: str):
        """更新模板列表"""
        self.template_combo.clear()
        templates = self.contract_service.get_templates_by_type(contract_type)
        self.template_combo.addItems(templates)

    def recommend_template(self):
        """推荐合同模板"""
        description = self.desc_edit.toPlainText().strip()
        if not description:
            QMessageBox.warning(self, "警告", "请输入合同需求描述")
            return
        
        # 清空之前的结果
        self.log_text.clear()
        self.result_table.setRowCount(0)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage('正在处理推荐任务...')
        # 推荐和生成按钮都禁用
        self.recommend_btn.setEnabled(False)
        self.generate_btn.setEnabled(False)
        
        # 创建后台工作线程
        self.recommendation_worker = RecommendationWorker(
            contract_service=self.contract_service,
            user_input=description,
            contract_type=self.type_combo.currentText()
        )
        
        # 连接信号
        self.recommendation_worker.progress.connect(self.update_log)
        self.recommendation_worker.update_progress.connect(self.update_progress_bar)
        self.recommendation_worker.finished.connect(self.handle_recommendation_result)
        self.recommendation_worker.finished.connect(self.recommendation_worker.deleteLater)
        
        # 启动线程
        self.recommendation_worker.start()

    def update_log(self, message):
        """更新日志显示"""
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
        QApplication.processEvents()  # 确保UI及时更新

    def update_progress_bar(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)

    def handle_recommendation_result(self, result):
        """处理推荐结果"""
        # 推荐和生成按钮恢复
        self.recommend_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if result["status"] == "failed":
            self.status_bar.showMessage('推荐失败')
            QMessageBox.critical(self, "处理失败", result["message"])
            return
        
        # 显示分析结果
        analysis = result["data"]["analysis"]
        analysis_text = (
            f"合同大类: {analysis['contract_category']}\n"
            f"具体类型: {analysis['specific_type']}\n"
            f"特别关注: {', '.join(analysis['special_concerns'])}"
        )
        self.update_log("\n分析结果:\n" + analysis_text)
        self.status_bar.showMessage('合同推荐完成')
        
        # 显示推荐结果
        recommendations = result["data"]["recommendations"]
        if not recommendations:
            self.update_log("\n未找到匹配的合同模板")
            return
        
        self.update_log(f"\n找到 {len(recommendations)} 个推荐合同:")
        
        # 更新表格显示
        self.result_table.setRowCount(len(recommendations))
        for row, rec in enumerate(recommendations):
            self.result_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))  # 动态生成ID
            self.result_table.setItem(row, 1, QTableWidgetItem(rec['name']))
            self.result_table.setItem(row, 2, QTableWidgetItem(f"{rec['score']}%"))
            self.update_log(f"{row + 1}.{rec['name']}")
            # 根据置信度设置颜色
            item = QTableWidgetItem(rec["confidence"])
            if rec["confidence"] == "高":
                item.setBackground(QColor(200, 255, 200))  # 绿色
            elif rec["confidence"] == "中":
                item.setBackground(QColor(255, 255, 200))  # 黄色
            else:
                item.setBackground(QColor(255, 200, 200))  # 红色
            self.result_table.setItem(row, 3, item)
        
        # 自动选择第一个推荐结果
        if recommendations:
            first_recommendation = recommendations[0]
            template_name = first_recommendation["name"]
            
            # 查找并选择对应的模板
            template_idx = self.template_combo.findText(template_name)
            if template_idx >= 0:
                self.template_combo.setCurrentIndex(template_idx)
                self.update_log(f"\n已自动选择推荐模板: {template_name}\n")
            
            # 启用生成按钮
            self.generate_btn.setEnabled(True)

    def generate_contract(self):
        """推荐合同模板"""
        description = self.desc_edit.toPlainText().strip()
        if not description:
            QMessageBox.warning(self, "警告", "请输入合同需求描述")
            return
        
        # 清空之前的结果
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage('正在处理合同生成任务...')
        # 推荐和生成按钮都禁用
        self.recommend_btn.setEnabled(False)
        self.generate_btn.setEnabled(False)
        
        # 创建后台工作线程
        self.generation_worker = GenerationWorker(
            contract_service=self.contract_service,
            user_input=description,
            contract_name=self.template_combo.currentText(),
            contract_type=self.type_combo.currentText()
        )
        
        # 连接信号
        self.generation_worker.progress.connect(self.update_log)
        self.generation_worker.update_progress.connect(self.update_progress_bar)
        self.generation_worker.finished.connect(self.handle_generation_result)
        self.generation_worker.finished.connect(self.generation_worker.deleteLater)
        
        # 启动线程
        self.generation_worker.start()

    def handle_generation_result(self, result):
        """处理推荐结果"""
        # 推荐和生成按钮恢复
        self.recommend_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if result["status"] == "failed":
            self.status_bar.showMessage('生成失败')
            QMessageBox.critical(self, "处理失败", result["message"])
            return
        
        self.status_bar.showMessage('合同生成完成')
        
        generation_file = result["data"]

        # 保存文件
        try:
            file_path = os.path.join(GENERATED_DIR, generation_file["file_name"])
            generation_file["filled_docx"].save(file_path)
            
            # 确保文件权限正确
            try:
                os.chmod(file_path, 0o644)  # 确保文件可读
            except Exception as e:
                print(f"警告: 设置文件权限失败: {str(e)}")
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            ereply = QMessageBox.question(
                self, 
                '失败', 
                f"保存文件失败: {str(e)}",
                QMessageBox.No
            )


        # 显示成功消息
        reply = QMessageBox.question(
            self, 
            '完成', 
            f'合同已生成到:\n{file_path}\n\n是否打开文件？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            os.startfile(file_path)
            
        
        
        

def main():
    app = QApplication(sys.argv)
    window = ContractGenerator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()