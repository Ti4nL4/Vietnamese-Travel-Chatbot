#!/usr/bin/env python
# coding: utf-8

# In[1]:


from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader,PyPDFLoader, DirectoryLoader
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
import os

import re
def remove_metadata(text):
    # Xóa đoạn có dạng metadata={...}
    cleaned_text = re.sub(r"metadata=\{.*?\}", "", text, flags=re.DOTALL)
    return cleaned_text.strip()

# Get the absolute path to the rag_data directory
current_dir = os.path.dirname(os.path.abspath(__file__))
rag_data_path = os.path.join(current_dir, "rag_data", "text")

loader = DirectoryLoader(
    rag_data_path,
    loader_cls=TextLoader,
    loader_kwargs={'autodetect_encoding': True},
)
documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,       # Giảm từ 1000 -> 600
    chunk_overlap=150,    # Giảm từ 200 -> 150 (25% chunk size)
    length_function=len,
    separators=[
        "\n\n",        # Ưu tiên 1: Đoạn văn
        "\n",          # Ưu tiên 2: Xuống dòng
        ".", "!", "?", # Ưu tiên 3: Kết thúc câu
        " ",           # Ưu tiên 4: Từ
        ""             # Fallback
    ]
)
# Tách văn bản thành các đoạn nhỏ
texts = text_splitter.split_documents(documents)

model = SentenceTransformer('dangvantuan/vietnamese-document-embedding', trust_remote_code=True)

# Create a custom embeddings class
class VietnameseEmbeddings(Embeddings):
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        """Embed a list of documents."""
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, text):
        """Embed a query."""
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

# Create embeddings instance
embeddings = VietnameseEmbeddings(model)

# Tạo cơ sở dữ liệu FAISS
db = FAISS.from_documents(
    texts,
    embeddings,
    distance_strategy="COSINE"  # Use cosine similarity for better performance
)
db.save_local("faiss_index")


# In[2]:


import ollama

def generate_response(prompt):
    messages = [
        {"role": "system", "content": "Dựa trên thông tin sau đây, hãy trả lời câu hỏi một cách chính xác và ngắn gọn. Nếu thông tin không đủ để trả lời, hãy nói rõ điều đó."},
        {"role": "user", "content": prompt}
    ]
    print(len(prompt))
    response = ollama.chat(
        model='gemma:7b-instruct-v1.1-q4_K_M',
        messages=messages,
    )
    return response["message"]["content"]



# In[5]:


import time
import sys
from pg_query import process_query

def rag_pipeline(query):
    start_time = time.time()
    
    # Get documents with scores
    docs_and_scores = db.similarity_search_with_score(query, k=3)
    
    # Define similarity threshold
    SIMILARITY_THRESHOLD = 0.3  # Adjust this threshold based on your needs
    
    # Filter documents by relevance
    filtered_docs = []
    max_similarity = 0
    
    for doc, score in docs_and_scores:
        # Convert score to similarity (FAISS uses distance, so lower is better)
        similarity = 1 - score
        print(similarity)   
        max_similarity = max(max_similarity, similarity)
        
        if similarity > SIMILARITY_THRESHOLD:
            doc.page_content = remove_metadata(doc.page_content)
            filtered_docs.append(doc)
    
    print(f"🔍 FAISS search mất: {time.time() - start_time:.2f} giây")
    print(f"Found {len(filtered_docs)} relevant documents")
    print(f"Max similarity score: {max_similarity:.4f}")
        
    # If no documents meet the threshold, try PostgreSQL
    if not filtered_docs:
        print("No documents meet similarity threshold, querying PostgreSQL...")
        try:
            postgres_result = process_query(query)
            if postgres_result and "Không tìm thấy kết quả" not in postgres_result:
                print("Found results in PostgreSQL")
                return postgres_result, "sql"  # Return the result and the path used
            else:
                return "⚠️ Không tìm thấy dữ liệu phù hợp để trả lời!", "sql"  # Return the result and the path used
        except Exception as e:
            print(f"Error querying PostgreSQL: {str(e)}")
            return "⚠️ Không tìm thấy dữ liệu phù hợp để trả lời!", "sql"  # Return the result and the path used
        
    
    # Create context from filtered documents
    context = "\n\n".join([doc.page_content for doc in filtered_docs])
    
    # Improved prompt template
    prompt_template = """Dựa trên thông tin sau đây, hãy trả lời câu hỏi một cách chính xác và ngắn gọn.
    Nếu thông tin không đủ để trả lời, hãy nói rõ điều đó.

    Thông tin tham khảo:
    {context}

    Câu hỏi: {query}

    Trả lời:"""
    
    prompt = prompt_template.format(context=context, query=query)
    
    print(f"Context length: {len(context)} characters")
    sys.stdout.write(prompt)
    
    start_time = time.time()
    response = generate_response(prompt)
    print(f"🤖 AI generate mất: {time.time() - start_time:.2f} giây")
    return {
        "answer": response,
        "sources": [doc.metadata.get('source', 'unknown') for doc in filtered_docs],
        "path": "rag"
    }, "rag"
    # return response, "rag"  # Return the result and the path used

# Ví dụ sử dụng
# query = "Những điểm du lịch nổi bật ở Đà Nẵng?"
# query = "Festval phở 2025 diễn ra khi nào?"
# query = "Doanh thu của Du lịch Huế trong quý I năm 2025?"
# query = "Phù điêu Kala Núi Bà là gì?"

# query = "Cho tôi biết thông tin của một số hướng dẫn viên tại điểm du lịch Hội An"
# query = "Cho tôi biết thông tin của một số hướng dẫn viên ở có nơi cấp thẻ ở Hồ Chí Minh"
# query = "Cho tôi biết thông tin của một số nơi lưu trú ở Hà Nội"


# print(rag_pipeline(query))


