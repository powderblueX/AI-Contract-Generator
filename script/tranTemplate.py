# 给原始合同范本生成含占位符的合同模版
import os
import json,markdown,subprocess
from dashscope import Generation
from datetime import datetime
from docx import Document 


# 记录开始时间
start_time = datetime.now()

def format_message(user_input):
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': f'''请直接输出修改后的文本，不要添加任何解释性文字或额外说明：把待填写的空白部分(包括空格部分、冒号后部分等)变成大括号占位符，若无待填写部分则原话输出即可。占位符例子如下：
            {{联系电话}}
            以下是我给出的文本：
            {user_input}'''}]
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
    
    response_md = ""
    if hasattr(response, 'output') and hasattr(response.output, 'choices'):
        # 获取处理后的结果
        response_md = response['output']['choices'][0]['message']['content']
    else:
        print("API响应格式不正确")
    return response_md

def test(input_folder, output_folder):
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
        
        print(f"正在处理文件: {file_name} 进度:{start_file_index}/{file_num}")
        
        # 读取文件内容
        doc = Document(file_path)

        for i,paragraph in enumerate(doc.paragraphs):
            #空段落
            if not paragraph.text.strip():
                continue
            #无空格且无冒号的无需填入内容
            if ' ' not in paragraph.text and (':' not in paragraph.text and '：' not in paragraph.text):
                continue
            #逐run修改
            runs = paragraph.runs
            if not runs:
                continue

            #获得大模型输出
            response_text = model_response(paragraph.text)
            current_position = 0
            for run in runs:
                run_length = len(run.text)
                # 计算当前 run 对应的新文本部分
                new_run_text = response_text[current_position:current_position + run_length]
                # 更新 run 的文本内容
                run.text = new_run_text
                current_position += run_length
        
            # 如果新文本比原段落长，将剩余部分添加到最后一个 run
            if current_position < len(response_text):
                runs[-1].text += response_text[current_position:]
        
        output_file = os.path.join(output_folder, file_name) 
        doc.save(output_file)
        print(f"处理完成，已保存")
        start_file_index += 1


# 主函数
if __name__ == "__main__":
    test("contracts/部委","contracts/tran_template")
    # 记录结束时间
    end_time = datetime.now()
    print(f"所有文件处理完成！总耗时: {end_time - start_time}")