# 获取合同模版的占位符并存为json
import re,os
import json
from docx import Document 

def read_docx(docx_path):
    document = Document(docx_path)
    full_text = []
    
    # 遍历文档中的每个段落并添加其文本到列表中
    for paragraph in document.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

def extract_placeholders_to_json(input_folder, output_folder):
    """
    提取合同模板中的占位符并保存为 JSON 文件。
    
    :param template_text: 合同模板的文本内容
    :param output_file: 输出的 JSON 文件路径
    """
    all_files = os.listdir(input_folder)
    
    # 过滤出文件（排除子文件夹）
    file_num = sum(os.path.isfile(os.path.join(input_folder, item)) for item in all_files)
 
    #逐docx文件处理
    start_file_index = 0
    file_names = os.listdir(input_folder)[start_file_index:]

    for file_name in file_names:
        if not file_name.endswith(".docx"):
            print(f"文件有问题，不做处理: {file_name} 进度:{start_file_index}/{file_num}")
            start_file_index += 1
            continue

        file_path = os.path.join(input_folder, file_name)  # 获取完整路径
        
        print(f"正在处理文件: {file_name} 进度:{start_file_index+1}/{file_num}")
        
        # 读取文件内容
        template_text = read_docx(file_path)

        # 匹配占位符的正则表达式
        placeholder_pattern = r"\{(.*?)\}"  # 匹配 {内容}
        
        # 提取所有占位符内容
        placeholders = re.findall(placeholder_pattern, template_text)
        
        # 去重（避免重复的占位符）
        unique_placeholders = list(set(placeholders))
        
        # 构造 JSON 数据
        placeholders_data = {
            "placeholders": unique_placeholders
        }
        
        #输出文件路径
        output_file = os.path.join(output_folder,file_name.replace(".docx",".json"))
        # 将占位符保存为 JSON 文件
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(placeholders_data, json_file, ensure_ascii=False, indent=4)
        
        print(f"占位符已提取并保存到文件: {output_file}")
        start_file_index += 1

# 示例调用
if __name__ == "__main__":
    # 输出 JSON 文件路径
    input_folder = "contracts/tran_template/地方模版"
    output_folder = os.path.join(input_folder,"占位符")

    # 调用函数提取占位符并保存为 JSON 文件
    extracted_placeholders = extract_placeholders_to_json(input_folder, output_folder)

    # 打印提取结果
    print("全部完成")