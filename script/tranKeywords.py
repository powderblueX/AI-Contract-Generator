import os
import json
from dashscope import Generation
from docx import Document 

def format_message(user_input):
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': f'''请仔细分析以下合同模板内容，提取出能体现该合同独特性的关键词。请直接输出关键词，用逗号','分隔。

            要求：
            1. 要先输出合同名称作为第一个关键词
            2. 重点关注该合同特有的内容，不要提取通用条款（如违约责任、争议解决等）
            3. 区分性：生成的关键词应能清楚区分该合同与其他类型的合同，避免混淆。
            4. 代表性：关键词必须能够准确反映该合同的核心内容和主要条款。
            5. 提取合同适用的特定场景（如特定行业、特殊用途等）
            6. 提取合同中的特殊条款（如特殊的质量要求、特殊的验收标准等）
            7. 不要提取通用性条款，如：技术标准、质量要求、交付期限、违约责任、争议解决、定金条款、留置权等
            8. 不要添加任何解释性文字
            9. 数量
            合同模板内容：
            {user_input}

            示例：
            输入：[二手房交易合同内容]
            输出：二手房交易合同,学区房,按揭贷款,房屋过户,税费承担,房屋现状'''
        }]
    return messages

def model_response(input_text):
    # 格式化消息并调用大模型 API
    messages = format_message(input_text)
    # 调用API生成响应
    response = Generation.call(
        api_key="sk-4c0e21d21fb748bd81d918e0cdc346f3",
        model="qwen-turbo",
        messages=messages,
        result_format="message"
    )
    
    response_txt = ""
    if hasattr(response, 'output') and hasattr(response.output, 'choices'):
        # 获取处理后的结果
        response_txt = response['output']['choices'][0]['message']['content']
    else:
        print("API响应格式不正确")
    return response_txt

def get_docx(file_path):
    # 打开.docx文档
    document = Document(file_path)
    full_text = []
    
    # 遍历每一段落并添加到full_text列表中
    for para in document.paragraphs:
        full_text.append(para.text)
    
    # 返回合并后的全文字符串
    return '\n'.join(full_text)

def save_string_to_txt(string, file_path):
    """
    将字符串保存为 .txt 文件。

    参数：
    - string: 要保存的字符串内容。
    - file_path: 保存的目标文件路径（包括文件名）。
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:  # 使用写入模式 ("w")
            file.write(string)  # 写入字符串内容
        print(f"字符串已成功保存到 {file_path}")
    except Exception as e:
        print(f"保存失败：{e}")

if __name__ == "__main__":
    input_folder = "contracts/部委"
    output_folder = "contracts/部委/关键词"
    all_files = os.listdir(input_folder)
    
    # 过滤出文件（排除子文件夹）
    file_num = sum(os.path.isfile(os.path.join(input_folder, item)) for item in all_files)
 
    #逐docx文件处理
    start_file_index = 0
    file_names = os.listdir(input_folder)[start_file_index:]
    for file_name in file_names:
        if not file_name.endswith(".docx"):
            start_file_index += 1
            print(f"文件有问题，不做处理: {file_name} 进度:{start_file_index}/{file_num}")
            continue

        start_file_index += 1

        file_path = os.path.join(input_folder, file_name)  # 获取完整路径
        print(f"正在处理文件: {file_name} 进度:{start_file_index}/{file_num}")

        docx_content = get_docx(file_path)
        keywords = model_response(docx_content)

        # 写入txt
        txt_path = os.path.join(output_folder, file_name.replace('.docx', '.txt'))
        save_string_to_txt(keywords,txt_path)


        


        

