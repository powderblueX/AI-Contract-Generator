import subprocess,os
from docx import Document

def convert_doc_to_docx(doc_path, docx_path):
    """
    使用 unoconv 将 .doc 文件转换为 .docx 文件。
    
    :param doc_path: .doc 文件路径
    :param docx_path: 转换后的 .docx 文件路径
    """
    try:
        subprocess.run(["unoconv", "-f", "docx", "-o", docx_path, doc_path], check=True)
        print(f"成功将 {doc_path} 转换为 {docx_path}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")



# 示例调用
if __name__ == "__main__":
    input_folder = "contracts/地方"
    output_folder = "contracts/地方doc2docx"
    all_files = os.listdir(input_folder)
    
    # 过滤出文件（排除子文件夹）
    file_num = sum(os.path.isfile(os.path.join(input_folder, item)) for item in all_files)
    file_count = 423
    #逐docx文件处理
    file_names = os.listdir(input_folder)[file_count:]
    for file_name in file_names:
        print(f"正在处理{file_name}")
        if (not file_name.endswith(".wps")) and (not file_name.endswith(".doc")):
            pass
        else:
            doc_file_path = os.path.join(input_folder,file_name)  # 替换为你的 .doc/.wps 文件路径
            if file_name.endswith(".doc"):
                docx_file_path = os.path.join(output_folder,file_name.replace("doc","docx"))  # 转换后的文件路径
            if file_name.endswith(".wps"):
                docx_file_path = os.path.join(output_folder,file_name.replace("wps","docx"))  # 转换后的文件路径
            # 转换 .doc 为 .docx
            convert_doc_to_docx(doc_file_path, docx_file_path)
        print(f"进度：{file_count}/{file_num}")
        file_count += 1
        
        