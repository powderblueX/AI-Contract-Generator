import os,gc,re
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# 加载所有 .txt 文件的内容
def load_txt_files(folder_path):
    """
    从指定文件夹中加载所有 .txt 文件的内容。
    返回一个包含 (文件名, 文件内容) 的列表。
    """
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:  # 忽略空文件
                    documents.append((filename, content))
    return documents

def clean_text(text):
    """
    清理文本内容：
    - 去除多余空白字符（包括换行符、制表符等）。
    - 去除顿号、逗号等分隔符。
    - 去除特殊字符（如标点符号）。
    :param text: 原始文本
    :return: 清理后的文本
    """
    # 去除多余空白字符
    text = re.sub(r"\s+", " ", text).strip()
    
    # 去除顿号、逗号等分隔符
    text = re.sub(r"[、，,]", " ", text)
    
    # 去除其他特殊字符（可选）
    text = re.sub(r"[^\w\s]", "", text)
    
    return text.strip()

# 将文本内容向量化
def generate_embeddings(documents, model):
    """
    使用 SentenceTransformer 模型将文档内容转换为向量。
    返回文件名列表和对应的向量矩阵。
    """
    filenames, contents = zip(*documents)  # 分离文件名和内容
    # 清理内容
    contents = [clean_text(content) for content in contents]

    embeddings = model.encode(contents, convert_to_tensor=False)  # 生成向量
    return list(filenames), np.array(embeddings).astype('float32')

# 构建 FAISS 索引并保存
def build_faiss_index(embeddings, dimension):
    """
    使用 FAISS 构建向量索引。
    """
    index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离
    index.add(embeddings)  # 添加向量到索引
    return index

# 加载 FAISS 索引
def load_faiss_index(index_file):
    """
    从磁盘加载 FAISS 索引。
    """
    index = faiss.read_index(index_file)
    print(f"FAISS 索引已加载，包含 {index.ntotal} 个向量")
    return index

# 查询知识库
def search_in_knowledge_base(query, model, index, filenames, top_k=5):
    """
    根据查询字符串在知识库中搜索最相似的文档。
    """
    query_vector = model.encode([query], convert_to_tensor=False).astype('float32')
    distances, indices = index.search(query_vector, top_k)
    results = [(filenames[i], distances[0][j]) for j, i in enumerate(indices[0])]
    return results

# 主程序
if __name__ == "__main__":
    # 配置路径和模型
    folder_path = "contracts/部委/关键词" 
    model_path = 'embed_model/all-MiniLM-L6-v2'
    index_file = "contracts/RAG/部委/knowledge_base.index"
    filenames_file = "contracts/RAG/部委/filenames.txt"  # 定义文件名列表文件路径

    # 加载模型
    print("加载 SentenceTransformer 模型...")
    model = SentenceTransformer(model_path)

    if not os.path.isfile(index_file):
        # 加载文档并生成向量
        print("加载 .txt 文件并生成向量...")
        documents = load_txt_files(folder_path)
        filenames, embeddings = generate_embeddings(documents, model)
        print(f"共加载 {len(filenames)} 个文档，每个向量维度为 {embeddings.shape[1]}")

        # 构建 FAISS 索引
        print("构建 FAISS 索引...")
        index = build_faiss_index(embeddings, embeddings.shape[1])

        # 保存索引
        print("保存 FAISS 索引...")
        faiss.write_index(index, index_file)

        # 保存文件名列表
        print("保存文件名列表...")
        with open(filenames_file, "w", encoding="utf-8") as f:
            for filename in filenames:
                f.write(filename + "\n")
    else:
        # 直接加载索引文件
        print("加载 FAISS 索引...")
        index = load_faiss_index(index_file)

        # 加载文件名列表
        if not os.path.isfile(filenames_file):
            raise FileNotFoundError(f"文件名列表文件 '{filenames_file}' 不存在！")
        
        print("加载文件名列表...")
        with open(filenames_file, "r", encoding="utf-8") as f:
            filenames = [line.strip() for line in f.readlines()]

    while True:
        # 示例查询
        query = input("输入您的查询关键词：")
        query = clean_text(query)
        results = search_in_knowledge_base(query, model, index, filenames, top_k=5)
        print("查询结果：")
        for rank, (filename, distance) in enumerate(results, start=1):
            filename = filename.replace('.txt', '.docx')
            print(f"排名 {rank}: 文件名: {filename}, 距离: {distance:.4f}")
        
        judge = input("继续[y/n]: ")
        if judge == 'n':
            break

    # 释放 hf_model 的内存
    del model  # 删除模型对象
    gc.collect()  # 调用垃圾回收器清理内存
    print("模型内存已释放！")
