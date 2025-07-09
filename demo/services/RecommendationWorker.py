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


class RecommendationWorker(QThread):
    """
    合同推荐后台线程
    Contract Recommendation Background Thread
    负责根据用户输入进行合同模板推荐。
    """
    finished = pyqtSignal(dict)  # 任务完成时发送结果
    progress = pyqtSignal(str)   # 进度更新信号
    update_progress = pyqtSignal(int)  # 进度条更新信号
    
    def __init__(self, contract_service: ContractService, user_input, contract_type):
        """
        初始化推荐线程。
        Initialize recommendation thread.
        :param contract_service: 合同服务实例
        :param user_input: 用户输入文本
        :param contract_type: 合同类型
        """
        super().__init__()
        self.contract_service = contract_service
        self.user_input = user_input
        self.contract_type = contract_type
    
    def run(self):
        """
        线程主逻辑，执行推荐流程。
        Main thread logic, execute recommendation process.
        """
        try:
            self.progress.emit("开始处理合同推荐任务...")
            self.update_progress.emit(5)
            
            # 检查用户输入是否为空或过短
            user_input_check = self.user_input.strip() if self.user_input else ""
            input_length = len(user_input_check)

            if not user_input_check:
                print("用户输入为空，无法推荐合同")
                return
            # 对极短文本特殊处理
            is_extremely_short = input_length < 10
            if is_extremely_short:
                print(f"用户输入极短({input_length}字符)，这可能导致不准确的推荐")

            # # 限制过长的用户输入
            # max_input_length = 5000  # 设置最大输入长度限制
            # if input_length > max_input_length:
            #     print(f"用户输入过长({input_length}字符)，截断至{max_input_length}字符")
            #     user_input = user_input[:max_input_length]

            # 确保模型已加载
            if self.contract_service.model is None:
                self.contract_service.load_model()
            
            # 确保索引已加载
            if self.contract_service.index is None:
                self.contract_service.load_faiss_index()

            # 确保合同空白模板已加载
            if self.contract_service.filenames is None:
                self.contract_service.load_template_types
            
            # 1. 对用户需求进行深度分析
            user_analysis = self.contract_service.analyze_user_needs(self.user_input)

            # 特殊判断：如果分析结果显示无相关合同且输入极短，直接返回空结果
            no_relevant_contract = not user_analysis["contract_category"] or user_analysis["contract_category"] == "无相关合同"
            if no_relevant_contract and is_extremely_short:
                print(f"分析结果显示无相关合同且输入极短，返回空结果")
                return
            
            self.update_progress.emit(15)
            
            # 2. 提取用户输入的关键词
            print(f"提取关键词...")
            user_input_keywords = self.contract_service.extract_keywords(self.user_input)
            # 增强关键词，添加分析出的合同类型和关注点
            enhanced_keywords = user_input_keywords
            if user_analysis["contract_category"] and user_analysis["contract_category"] != "无相关合同":
                enhanced_keywords += " " + user_analysis["contract_category"]
            if user_analysis["specific_type"] and user_analysis["specific_type"] != "N/A":
                enhanced_keywords += " " + user_analysis["specific_type"]

            query = self.contract_service.clean_text_for_legal(enhanced_keywords)
            print(f"增强后的查询关键词: {query}")

            self.update_progress.emit(35)

            # 3. 加载合同类型分类映射
            print(f"加载合同类型映射...")
            categories_map = self.contract_service.load_contract_categories(TEMPLATE_DIR, self.contract_type)

            # 4. 使用高级搜索算法进行检索
            print(f"执行向量搜索...")
            results = self.contract_service.advanced_search_in_knowledge_base(
                query, 
                self.contract_service.model, 
                self.contract_service.index[self.contract_type], 
                self.contract_service.template_types[self.contract_type], 
                categories_map, 
                self.user_input, 
                top_k=5
            )

            # 构造返回结果
            print(f"构造返回结果...")
            recommendations = []

            self.update_progress.emit(85)

            # 获取输入文本长度用于评分调整
            # 设置长度阈值和权重，短文本将获得较低的可信度
            min_input_length = 50  # 最小有效输入长度
            # 调整权重计算方式，对短文本更加严格
            length_weight = min(1.0, max(0.3, (input_length / min_input_length) ** 0.8))
            print(f"输入长度: {input_length}, 长度权重: {length_weight}")

            # 如果分析显示无相关合同，进一步降低权重
            if no_relevant_contract:
                length_weight *= 0.5
                print(f"分析结果显示无相关合同，进一步降低权重至: {length_weight}")

            for filename, score in results:
                filename = os.path.splitext(filename.strip())[0]
                try:
                    #  更精确的分数计算，考虑文本长度和更严格的距离惩罚
                    raw_score = (1 - score) * 100  # 基础分数
                    adjusted_score = raw_score * length_weight  # 按输入长度调整
                    
                    # 对分数进行缩放和拉伸，使得差异更明显
                    # 小于70的分数会被更严重地惩罚，实现门槛效应
                    if raw_score < 70:
                        scaled_score = adjusted_score * 0.7  # 更严格的惩罚
                    else:
                        scaled_score = adjusted_score
                    
                    # 对极短文本特殊处理，进一步降低分数
                    if is_extremely_short:
                        scaled_score *= 0.5  # 对极短文本再减半
                    
                    # 获得最终分数
                    final_score = max(0, min(100, scaled_score))
                    
                    # 记录匹配度计算详情
                    print(f"匹配度详情 - 文件: {filename}, 原始距离: {score}, 基础分数: {raw_score:.2f}, 长度调整后: {adjusted_score:.2f}, 最终分数: {final_score:.2f}")
                    
                    # 添加置信度评级
                    confidence_rating = "高" if final_score >= 80 else ("中" if final_score >= 60 else "低")
                    
                    recommendations.append({
                        "name": filename,
                        "score": round(final_score, 1),  # 将调整后的分数四舍五入到一位小数
                        "confidence": confidence_rating  # 添加置信度评级
                    })
                except Exception as e:
                    print(f"获取合同ID出错: {filename}, {str(e)}")
                    continue

            # 按照分数从高到低排序
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            # 移除阈值过滤，直接获取前5个结果
            filtered_recommendations = recommendations[:5]
            print(f"选取前5个匹配结果（或更少，如果结果不足5个）")
            
            # 如果无相关合同，限制返回数量为2个
            if no_relevant_contract and len(filtered_recommendations) > 2:
                filtered_recommendations = filtered_recommendations[:2]
                print(f"分析显示无相关合同，但有匹配结果，只保留前2个")
            
            # 记录结果数量
            print(f"返回的匹配结果数量: {len(filtered_recommendations)}")
            
            # 更新任务状态为已完成
            print(f"推荐任务完成，找到 {len(filtered_recommendations)} 个匹配")
            
            self.progress.emit(f"找到 {len(filtered_recommendations)} 个推荐合同")
            self.update_progress.emit(100)
            
            # 返回最终结果
            self.finished.emit({
                "status": "completed",
                "message": "推荐任务完成",
                "data": {
                    "recommendations": filtered_recommendations,
                    "analysis": user_analysis
                }
            })
        

        except Exception as e:
            error_details = traceback.format_exc()
            print(f"推荐失败! 错误: {str(e)}")
            print(f"详细错误信息:\n{error_details}")
            self.progress.emit(f"处理失败: {str(e)}")
            self.finished.emit({
                "status": "failed",
                "message": str(e)
            })
